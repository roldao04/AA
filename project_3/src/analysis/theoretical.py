"""
Theoretical Validation Module.

This module provides functions for validating theoretical predictions against
empirical results for Fixed Probability Counter and Space-Saving algorithms.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union
from scipy import stats


def validate_fixed_prob_variance(
    trial_results: pd.DataFrame,
    exact_counts: Dict[int, int],
    p: float = 0.25
) -> pd.DataFrame:
    """
    Validate Fixed Probability Counter variance against theoretical predictions.

    Theoretical variance: Var[estimate] = (1-p)/p * n = 3n for p=0.25

    Parameters
    ----------
    trial_results : pd.DataFrame
        Trial results with columns: trial, temperature, estimate
    exact_counts : Dict[int, int]
        Ground truth exact counts
    p : float, default=0.25
        Probability parameter

    Returns
    -------
    pd.DataFrame
        Validation results with columns:
        - temperature: Temperature value
        - true_count: Exact count
        - empirical_variance: Variance across trials
        - theoretical_variance: Predicted variance
        - variance_ratio: empirical / theoretical
        - agrees: True if ratio is close to 1
    """
    validation_data = []

    for temp in trial_results['temperature'].unique():
        temp_data = trial_results[trial_results['temperature'] == temp]
        estimates = temp_data['estimate'].values

        true_count = exact_counts.get(temp, 0)

        # Empirical variance
        empirical_var = np.var(estimates, ddof=1)  # Sample variance

        # Theoretical variance: (1-p)/p * n
        theoretical_var = ((1 - p) / p) * true_count

        # Ratio (should be close to 1)
        ratio = empirical_var / theoretical_var if theoretical_var > 0 else np.nan

        # Consider "agrees" if ratio is within reasonable bounds (0.7 to 1.3)
        agrees = 0.7 <= ratio <= 1.3 if not np.isnan(ratio) else False

        validation_data.append({
            'temperature': temp,
            'true_count': true_count,
            'empirical_variance': empirical_var,
            'theoretical_variance': theoretical_var,
            'variance_ratio': ratio,
            'agrees': agrees
        })

    df = pd.DataFrame(validation_data)
    df = df.sort_values('true_count', ascending=False).reset_index(drop=True)

    return df


def validate_space_saving_guarantees(
    monitored: Dict[int, Tuple[int, int]],
    exact_counts: Dict[int, int],
    stream_length: int,
    k: int
) -> Dict[str, Union[bool, float, List]]:
    """
    Validate Space-Saving theoretical guarantees.

    Guarantees:
    1. All items with frequency > N/k are captured
    2. No item has error > N/k
    3. Per-item error bounds are valid (true_error <= recorded_error)

    Parameters
    ----------
    monitored : Dict[int, Tuple[int, int]]
        Space-Saving monitored items: {temp: (count, error)}
    exact_counts : Dict[int, int]
        Ground truth counts
    stream_length : int
        Total stream length
    k : int
        Space budget parameter

    Returns
    -------
    Dict[str, Union[bool, float, List]]
        Validation results including:
        - threshold_N_k: N/k threshold
        - frequent_items: Items with count > N/k
        - all_frequent_captured: True if all frequent items captured
        - max_error_theoretical: N/k
        - max_error_actual: Actual maximum error
        - max_error_guarantee_holds: True if max_error <= N/k
        - per_item_bounds_hold: True if all per-item bounds valid
        - violations: List of any bound violations
    """
    threshold = stream_length / k
    max_error_theoretical = threshold

    # Find frequent items (count > N/k)
    frequent_items = {temp: count for temp, count in exact_counts.items()
                      if count > threshold}

    # Check if all frequent items are captured
    monitored_temps = set(int(t) if isinstance(t, str) else t for t in monitored.keys())
    all_frequent_captured = all(temp in monitored_temps for temp in frequent_items.keys())

    # Check maximum error
    max_error_actual = 0
    per_item_violations = []

    for temp_key, (ss_count, ss_error) in monitored.items():
        temp = int(temp_key) if isinstance(temp_key, str) else temp_key
        true_count = exact_counts.get(temp, 0)
        actual_error = ss_count - true_count

        # Update max error
        if actual_error > max_error_actual:
            max_error_actual = actual_error

        # Check per-item bound
        if actual_error > ss_error:
            per_item_violations.append({
                'temperature': temp,
                'true_count': true_count,
                'ss_count': ss_count,
                'ss_error_bound': ss_error,
                'actual_error': actual_error,
                'violation_amount': actual_error - ss_error
            })

    max_error_guarantee_holds = max_error_actual <= max_error_theoretical
    per_item_bounds_hold = len(per_item_violations) == 0

    return {
        'threshold_N_k': threshold,
        'frequent_items': list(frequent_items.keys()),
        'num_frequent': len(frequent_items),
        'all_frequent_captured': all_frequent_captured,
        'max_error_theoretical': max_error_theoretical,
        'max_error_actual': max_error_actual,
        'max_error_guarantee_holds': max_error_guarantee_holds,
        'per_item_bounds_hold': per_item_bounds_hold,
        'num_violations': len(per_item_violations),
        'violations': per_item_violations,
        'all_guarantees_hold': (all_frequent_captured and
                                max_error_guarantee_holds and
                                per_item_bounds_hold)
    }


def calculate_theoretical_error_bounds(
    true_count: int,
    p: float = 0.25,
    confidence_level: float = 0.95
) -> Dict[str, float]:
    """
    Calculate theoretical error bounds for Fixed Probability Counter.

    Uses binomial distribution properties and Chernoff bounds.

    Parameters
    ----------
    true_count : int
        True frequency of an item
    p : float, default=0.25
        Probability parameter
    confidence_level : float, default=0.95
        Confidence level for intervals

    Returns
    -------
    Dict[str, float]
        Theoretical bounds including:
        - expected_estimate: E[estimate] = true_count
        - variance: Var[estimate]
        - std: Standard deviation
        - relative_std: Std / true_count
        - ci_lower: Lower confidence bound (normal approximation)
        - ci_upper: Upper confidence bound
        - chernoff_tail_bound: Tail probability bound for 20% deviation
    """
    # Expected value (unbiased)
    expected_estimate = true_count

    # Variance: (1-p)/p * n
    variance = ((1 - p) / p) * true_count

    # Standard deviation
    std = np.sqrt(variance)

    # Relative standard deviation
    relative_std = std / true_count if true_count > 0 else 0

    # Confidence interval (normal approximation for large n)
    alpha = 1 - confidence_level
    z_crit = stats.norm.ppf(1 - alpha/2)
    ci_lower = expected_estimate - z_crit * std
    ci_upper = expected_estimate + z_crit * std

    # Chernoff bound for tail probability
    # P(|estimate - true| > ε*true) ≤ 2*exp(-ε²*true / (3*(1-p)/p))
    # For ε = 0.2 (20% deviation)
    epsilon = 0.2
    chernoff_exponent = -(epsilon**2 * true_count) / (3 * ((1 - p) / p))
    chernoff_tail_bound = 2 * np.exp(chernoff_exponent)

    return {
        'expected_estimate': expected_estimate,
        'variance': variance,
        'std': std,
        'relative_std': relative_std,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'chernoff_tail_bound_20pct': chernoff_tail_bound,
        'epsilon': epsilon
    }


def test_concentration_inequalities(
    estimates: np.ndarray,
    true_value: float,
    epsilons: List[float] = [0.1, 0.2, 0.3]
) -> pd.DataFrame:
    """
    Test Chernoff concentration inequality empirically.

    For each epsilon, compares theoretical tail bound with empirical frequency.

    Parameters
    ----------
    estimates : np.ndarray
        Estimates from multiple trials
    true_value : float
        True value being estimated
    epsilons : List[float], default=[0.1, 0.2, 0.3]
        Relative deviation thresholds to test

    Returns
    -------
    pd.DataFrame
        Results with columns:
        - epsilon: Deviation threshold
        - empirical_tail_prob: Observed frequency
        - theoretical_bound: Chernoff bound
        - bound_holds: True if empirical <= theoretical
        - bound_tightness: empirical / theoretical
    """
    results = []

    for eps in epsilons:
        # Empirical tail probability
        deviations = np.abs(estimates - true_value)
        relative_deviations = deviations / true_value if true_value > 0 else deviations
        empirical_prob = np.mean(relative_deviations > eps)

        # Theoretical Chernoff bound
        # P(|X - μ| > ε*μ) ≤ 2*exp(-ε²*μ/3) for certain conditions
        # This is a simplified bound; exact form depends on distribution
        theoretical_bound = 2 * np.exp(-(eps**2 * true_value) / 3)

        bound_holds = empirical_prob <= theoretical_bound
        tightness = empirical_prob / theoretical_bound if theoretical_bound > 0 else np.inf

        results.append({
            'epsilon': eps,
            'empirical_tail_prob': empirical_prob,
            'theoretical_bound': theoretical_bound,
            'bound_holds': bound_holds,
            'bound_tightness': tightness,
            'n_violations': int(np.sum(relative_deviations > eps)),
            'n_total': len(estimates)
        })

    return pd.DataFrame(results)


def correlation_theoretical_empirical(
    theoretical_values: np.ndarray,
    empirical_values: np.ndarray
) -> Dict[str, float]:
    """
    Calculate correlation and agreement between theoretical and empirical values.

    Parameters
    ----------
    theoretical_values : np.ndarray
        Theoretical predictions
    empirical_values : np.ndarray
        Empirical observations

    Returns
    -------
    Dict[str, float]
        Correlation metrics including:
        - pearson_r: Pearson correlation coefficient
        - pearson_p: P-value for correlation
        - spearman_rho: Spearman rank correlation
        - rmse: Root mean squared error
        - mae: Mean absolute error
        - mape: Mean absolute percentage error
    """
    # Remove NaN pairs
    mask = ~(np.isnan(theoretical_values) | np.isnan(empirical_values))
    theo_clean = theoretical_values[mask]
    emp_clean = empirical_values[mask]

    if len(theo_clean) < 2:
        return {'error': 'Insufficient data for correlation'}

    # Pearson correlation
    pearson_r, pearson_p = stats.pearsonr(theo_clean, emp_clean)

    # Spearman correlation
    spearman_rho, spearman_p = stats.spearmanr(theo_clean, emp_clean)

    # Error metrics
    errors = emp_clean - theo_clean
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))

    # Mean absolute percentage error
    with np.errstate(divide='ignore', invalid='ignore'):
        percentage_errors = np.abs(errors / theo_clean) * 100
        percentage_errors = percentage_errors[np.isfinite(percentage_errors)]
        mape = np.mean(percentage_errors) if len(percentage_errors) > 0 else np.nan

    return {
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_rho': spearman_rho,
        'spearman_p': spearman_p,
        'rmse': rmse,
        'mae': mae,
        'mape': mape,
        'n_points': len(theo_clean)
    }


def scaling_relationship_validation(
    frequencies: np.ndarray,
    errors: np.ndarray,
    expected_scaling: str = 'sqrt'
) -> Dict[str, Union[float, bool]]:
    """
    Validate error scaling relationship with frequency.

    For Fixed Prob: relative error ∝ 1/√n
    For Space-Saving: error bounded by constant

    Parameters
    ----------
    frequencies : np.ndarray
        True frequencies
    errors : np.ndarray
        Observed errors (absolute or relative)
    expected_scaling : str, default='sqrt'
        Expected scaling: 'sqrt' for 1/√n, 'constant' for bounded

    Returns
    -------
    Dict[str, Union[float, bool]]
        Validation results including fit quality
    """
    # Remove invalid points
    mask = (frequencies > 0) & (errors > 0) & np.isfinite(frequencies) & np.isfinite(errors)
    freq_clean = frequencies[mask]
    err_clean = errors[mask]

    if len(freq_clean) < 3:
        return {'error': 'Insufficient data for scaling validation'}

    if expected_scaling == 'sqrt':
        # Test if error ∝ 1/√n
        # Log-log regression: log(error) = a + b*log(freq)
        # Expected: b ≈ -0.5 for 1/√n relationship

        log_freq = np.log(freq_clean)
        log_err = np.log(err_clean)

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_freq, log_err)

        # Goodness of fit
        expected_slope = -0.5
        slope_close_to_expected = abs(slope - expected_slope) < 0.2

        return {
            'scaling_type': 'sqrt',
            'expected_slope': expected_slope,
            'observed_slope': slope,
            'slope_difference': slope - expected_slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'slope_std_error': std_err,
            'validates_scaling': slope_close_to_expected and r_value**2 > 0.5
        }

    elif expected_scaling == 'constant':
        # Test if errors are bounded by constant
        # Calculate coefficient of variation
        mean_error = np.mean(err_clean)
        std_error = np.std(err_clean)
        cv = std_error / mean_error if mean_error > 0 else np.inf

        # Check if errors are relatively constant (low CV)
        constant_bound = cv < 0.5  # Arbitrary threshold

        return {
            'scaling_type': 'constant',
            'mean_error': mean_error,
            'std_error': std_error,
            'coefficient_of_variation': cv,
            'validates_constant_bound': constant_bound
        }

    else:
        return {'error': f'Unknown scaling type: {expected_scaling}'}
