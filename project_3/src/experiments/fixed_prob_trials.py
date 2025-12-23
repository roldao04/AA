"""
Trial Manager for Fixed Probability Counter Experiments.

This module orchestrates running multiple independent trials of the Fixed
Probability Counter algorithm to build statistical distributions of estimates
and validate theoretical properties.

Author: Joao Roldao (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import random
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union
from scipy import stats

from ..algorithms.fixed_probability_counter import FixedProbabilityCounter


def run_single_trial(
    temperatures: Union[list, pd.Series, np.ndarray],
    p: float,
    seed: int
) -> Dict[int, float]:
    """
    Run a single trial of the Fixed Probability Counter.

    Processes the entire temperature stream with a fresh counter instance
    using the specified random seed for reproducibility.

    Parameters
    ----------
    temperatures : list, pd.Series, or np.ndarray
        Stream of temperature values to process
    p : float
        Probability of incrementing (0 < p <= 1)
    seed : int
        Random seed for this trial

    Returns
    -------
    Dict[int, float]
        Dictionary mapping temperatures to their estimated counts

    Examples
    --------
    >>> temps = [12, 15, 12, 18, 15, 12]
    >>> result = run_single_trial(temps, p=0.25, seed=113920)
    >>> isinstance(result, dict)
    True
    >>> all(temp in result for temp in [12, 15, 18])
    True
    """
    # Set random seed for reproducibility
    random.seed(seed)

    # Create fresh counter
    counter = FixedProbabilityCounter(p=p)

    # Process entire stream
    counter.process_stream(temperatures)

    # Return all estimates
    return counter.get_all_estimates()


def run_multiple_trials(
    temperatures: Union[list, pd.Series, np.ndarray],
    p: float = 0.25,
    num_trials: int = 100,
    base_seed: int = 113920,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Run multiple independent trials of the Fixed Probability Counter.

    Orchestrates running num_trials independent trials, each with a different
    random seed derived from base_seed. Collects all estimates into a DataFrame
    for statistical analysis.

    Parameters
    ----------
    temperatures : list, pd.Series, or np.ndarray
        Stream of temperature values to process
    p : float, default=0.25
        Probability of incrementing
    num_trials : int, default=100
        Number of independent trials to run
    base_seed : int, default=113920
        Base random seed; trial i uses seed base_seed + i
    verbose : bool, default=True
        Whether to print progress information

    Returns
    -------
    pd.DataFrame
        DataFrame with columns 'trial', 'temperature', 'estimate'
        Each row represents one temperature's estimate in one trial

    Examples
    --------
    >>> temps = [12, 15, 12, 18, 15, 12]
    >>> results = run_multiple_trials(temps, p=0.5, num_trials=10, verbose=False)
    >>> len(results)  # doctest: +SKIP
    30  # 10 trials × 3 unique temps
    >>> set(results.columns)
    {'trial', 'temperature', 'estimate'}
    """
    if verbose:
        print(f"Running {num_trials} trials with p={p}, base_seed={base_seed}")
        print(f"Processing {len(temperatures)} observations per trial...")

    results = []

    for trial_num in range(num_trials):
        # Derive unique seed for this trial
        trial_seed = base_seed + trial_num

        # Run trial
        estimates = run_single_trial(temperatures, p, trial_seed)

        # Store results
        for temp, estimate in estimates.items():
            results.append({
                'trial': trial_num,
                'temperature': temp,
                'estimate': estimate
            })

        if verbose and (trial_num + 1) % 10 == 0:
            print(f"  Completed {trial_num + 1}/{num_trials} trials...")

    if verbose:
        print(f"✓ All {num_trials} trials completed")

    return pd.DataFrame(results)


def aggregate_trial_results(
    trial_results: pd.DataFrame,
    confidence_level: float = 0.95
) -> pd.DataFrame:
    """
    Aggregate trial results to compute statistics for each temperature.

    For each unique temperature, computes:
    - Mean estimate across trials
    - Standard deviation
    - Min and max estimates
    - Confidence interval bounds

    Parameters
    ----------
    trial_results : pd.DataFrame
        Results from run_multiple_trials with columns:
        ['trial', 'temperature', 'estimate']
    confidence_level : float, default=0.95
        Confidence level for confidence intervals

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per temperature, columns:
        - temperature: Temperature value
        - num_trials: Number of trials
        - mean_estimate: Mean of estimates across trials
        - std_estimate: Standard deviation of estimates
        - min_estimate: Minimum estimate
        - max_estimate: Maximum estimate
        - ci_lower: Lower bound of confidence interval
        - ci_upper: Upper bound of confidence interval

    Examples
    --------
    >>> trial_data = pd.DataFrame({
    ...     'trial': [0, 0, 1, 1],
    ...     'temperature': [12, 15, 12, 15],
    ...     'estimate': [20.0, 16.0, 24.0, 12.0]
    ... })
    >>> agg = aggregate_trial_results(trial_data)
    >>> agg.loc[agg['temperature'] == 12, 'mean_estimate'].values[0]
    22.0
    """
    # Group by temperature
    grouped = trial_results.groupby('temperature')['estimate']

    # Calculate statistics
    aggregated = pd.DataFrame({
        'temperature': grouped.apply(lambda x: x.name),
        'num_trials': grouped.count(),
        'mean_estimate': grouped.mean(),
        'std_estimate': grouped.std(),
        'min_estimate': grouped.min(),
        'max_estimate': grouped.max()
    }).reset_index(drop=True)

    # Calculate confidence intervals using t-distribution
    alpha = 1 - confidence_level

    # Calculate CI for each temperature
    ci_lower_list = []
    ci_upper_list = []

    for temp in aggregated['temperature']:
        temp_estimates = trial_results[trial_results['temperature'] == temp]['estimate']
        n = len(temp_estimates)
        mean = temp_estimates.mean()
        std = temp_estimates.std()
        se = std / np.sqrt(n)
        t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
        margin = t_crit * se
        ci_lower_list.append(mean - margin)
        ci_upper_list.append(mean + margin)

    aggregated['ci_lower'] = ci_lower_list
    aggregated['ci_upper'] = ci_upper_list

    return aggregated


def calculate_error_metrics(
    aggregated_results: pd.DataFrame,
    exact_counts: Dict[int, int]
) -> pd.DataFrame:
    """
    Calculate error metrics by comparing estimates against exact counts.

    Parameters
    ----------
    aggregated_results : pd.DataFrame
        Aggregated trial results from aggregate_trial_results
    exact_counts : Dict[int, int]
        Ground truth counts from ExactCounter

    Returns
    -------
    pd.DataFrame
        DataFrame with additional columns:
        - true_count: Exact count from ground truth
        - absolute_error: |mean_estimate - true_count|
        - relative_error: absolute_error / true_count
        - bias: mean_estimate - true_count
        - rmse: Root mean squared error across trials

    Examples
    --------
    >>> agg = pd.DataFrame({
    ...     'temperature': [12, 15],
    ...     'mean_estimate': [100.0, 50.0],
    ...     'std_estimate': [10.0, 5.0]
    ... })
    >>> exact = {12: 100, 15: 48}
    >>> metrics = calculate_error_metrics(agg, exact)
    >>> metrics.loc[metrics['temperature'] == 12, 'bias'].values[0]
    0.0
    """
    # Make a copy to avoid modifying input
    results = aggregated_results.copy()

    # Add true counts
    results['true_count'] = results['temperature'].map(exact_counts)

    # Calculate errors
    results['bias'] = results['mean_estimate'] - results['true_count']
    results['absolute_error'] = results['bias'].abs()
    results['relative_error'] = results['absolute_error'] / results['true_count']

    # RMSE is std of estimates (since estimator is unbiased in theory)
    # But we calculate it properly as RMSE from true value
    results['rmse'] = np.sqrt(
        results['std_estimate']**2 + results['bias']**2
    )

    return results


def calculate_theoretical_variance(
    exact_counts: Dict[int, int],
    p: float
) -> pd.DataFrame:
    """
    Calculate theoretical variance for each temperature.

    Theoretical variance: Var = (1-p)/p * n

    Parameters
    ----------
    exact_counts : Dict[int, int]
        Ground truth counts
    p : float
        Probability parameter used in trials

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - temperature: Temperature value
        - true_count: Exact count
        - theoretical_variance: (1-p)/p * true_count
        - theoretical_std: sqrt(theoretical_variance)

    Examples
    --------
    >>> exact = {12: 100, 15: 50}
    >>> theoretical = calculate_theoretical_variance(exact, p=0.25)
    >>> theoretical.loc[theoretical['temperature'] == 100, 'theoretical_variance'].values[0]
    300.0
    """
    data = []
    for temp, count in exact_counts.items():
        variance = ((1 - p) / p) * count
        std = np.sqrt(variance)
        data.append({
            'temperature': temp,
            'true_count': count,
            'theoretical_variance': variance,
            'theoretical_std': std
        })

    return pd.DataFrame(data)


def test_unbiased_estimator(
    error_metrics: pd.DataFrame,
    alpha: float = 0.05
) -> Dict[str, Union[float, bool, str]]:
    """
    Test whether the estimator is unbiased using a t-test.

    Tests null hypothesis H₀: mean(bias) = 0 across all temperatures.

    Parameters
    ----------
    error_metrics : pd.DataFrame
        Error metrics from calculate_error_metrics
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    Dict[str, Union[float, bool, str]]
        Dictionary containing:
        - mean_bias: Mean bias across all temperatures
        - t_statistic: t-test statistic
        - p_value: p-value from t-test
        - is_unbiased: True if we fail to reject H₀
        - conclusion: Human-readable conclusion

    Examples
    --------
    >>> metrics = pd.DataFrame({'bias': [0.5, -0.3, 0.2, -0.1]})
    >>> result = test_unbiased_estimator(metrics)
    >>> 'p_value' in result
    True
    """
    biases = error_metrics['bias'].values
    mean_bias = biases.mean()
    std_bias = biases.std()
    n = len(biases)

    # One-sample t-test against mean = 0
    t_stat, p_value = stats.ttest_1samp(biases, 0.0)

    is_unbiased = p_value > alpha

    conclusion = (
        f"{'✓ Fail to reject' if is_unbiased else '✗ Reject'} H₀ "
        f"at α={alpha:.3f} (p={p_value:.4f}). "
        f"Estimator is {'unbiased' if is_unbiased else 'biased'} "
        f"(mean bias={mean_bias:.4f})."
    )

    return {
        'mean_bias': mean_bias,
        'std_bias': std_bias,
        't_statistic': t_stat,
        'p_value': p_value,
        'is_unbiased': is_unbiased,
        'conclusion': conclusion
    }
