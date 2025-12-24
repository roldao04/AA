"""
Advanced Statistical Testing Module for Master's-Level Analysis.

This module provides sophisticated statistical methods including bootstrap
resampling, permutation tests, advanced confidence intervals, and power
analysis for rigorous algorithm comparison.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Union, Callable
from scipy import stats
import warnings


def bootstrap_confidence_intervals(
    data: np.ndarray,
    statistic: Callable = np.mean,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = None
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Calculate bootstrap confidence intervals for a statistic.

    Implements percentile bootstrap method with resampling.

    Parameters
    ----------
    data : np.ndarray
        Data to resample from
    statistic : Callable, default=np.mean
        Function to apply to each bootstrap sample
    n_bootstrap : int, default=1000
        Number of bootstrap iterations
    confidence_level : float, default=0.95
        Confidence level for interval
    random_seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    Dict[str, Union[float, np.ndarray]]
        Dictionary containing:
        - observed_statistic: Statistic on original data
        - bootstrap_distribution: Array of bootstrap statistics
        - ci_lower: Lower confidence bound
        - ci_upper: Upper confidence bound
        - std_error: Bootstrap standard error
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    n = len(data)
    observed_stat = statistic(data)

    # Bootstrap resampling
    bootstrap_stats = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        # Resample with replacement
        resample = np.random.choice(data, size=n, replace=True)
        bootstrap_stats[i] = statistic(resample)

    # Percentile method confidence interval
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_stats, alpha/2 * 100)
    ci_upper = np.percentile(bootstrap_stats, (1 - alpha/2) * 100)

    # Bootstrap standard error
    std_error = np.std(bootstrap_stats)

    return {
        'observed_statistic': observed_stat,
        'bootstrap_distribution': bootstrap_stats,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'std_error': std_error,
        'n_bootstrap': n_bootstrap,
        'confidence_level': confidence_level
    }


def bootstrap_comparison(
    data1: np.ndarray,
    data2: np.ndarray,
    statistic: Callable = np.mean,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = None
) -> Dict[str, Union[float, np.ndarray, bool]]:
    """
    Bootstrap comparison of two samples.

    Tests whether statistic(data1) - statistic(data2) is significantly
    different from zero using bootstrap.

    Parameters
    ----------
    data1 : np.ndarray
        First sample
    data2 : np.ndarray
        Second sample
    statistic : Callable, default=np.mean
        Statistic to compare
    n_bootstrap : int, default=1000
        Number of bootstrap iterations
    confidence_level : float, default=0.95
        Confidence level
    random_seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    Dict[str, Union[float, np.ndarray, bool]]
        Comparison results including difference CI and significance
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    observed_diff = statistic(data1) - statistic(data2)

    # Bootstrap both samples
    n1, n2 = len(data1), len(data2)
    bootstrap_diffs = np.zeros(n_bootstrap)

    for i in range(n_bootstrap):
        resample1 = np.random.choice(data1, size=n1, replace=True)
        resample2 = np.random.choice(data2, size=n2, replace=True)
        bootstrap_diffs[i] = statistic(resample1) - statistic(resample2)

    # Confidence interval for difference
    alpha = 1 - confidence_level
    ci_lower = np.percentile(bootstrap_diffs, alpha/2 * 100)
    ci_upper = np.percentile(bootstrap_diffs, (1 - alpha/2) * 100)

    # Significant if CI doesn't contain 0
    significant = not (ci_lower <= 0 <= ci_upper)

    return {
        'observed_difference': observed_diff,
        'bootstrap_differences': bootstrap_diffs,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'significant': significant,
        'n_bootstrap': n_bootstrap
    }


def permutation_test(
    data1: np.ndarray,
    data2: np.ndarray,
    statistic: Callable = None,
    n_permutations: int = 10000,
    random_seed: int = None,
    alternative: str = 'two-sided'
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Permutation test for comparing two samples (distribution-free).

    Tests H₀: data1 and data2 come from the same distribution.

    Parameters
    ----------
    data1 : np.ndarray
        First sample
    data2 : np.ndarray
        Second sample
    statistic : Callable, optional
        Test statistic function. If None, uses difference of means.
    n_permutations : int, default=10000
        Number of permutations
    random_seed : int, optional
        Random seed
    alternative : str, default='two-sided'
        Alternative hypothesis: 'two-sided', 'less', or 'greater'

    Returns
    -------
    Dict[str, Union[float, np.ndarray]]
        Test results including p-value and permutation distribution
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    if statistic is None:
        # Default: difference of means
        statistic = lambda d1, d2: np.mean(d1) - np.mean(d2)

    # Observed test statistic
    observed_stat = statistic(data1, data2)

    # Combined data
    combined = np.concatenate([data1, data2])
    n1, n2 = len(data1), len(data2)

    # Permutation distribution
    perm_stats = np.zeros(n_permutations)
    for i in range(n_permutations):
        # Randomly shuffle and split
        permuted = np.random.permutation(combined)
        perm_data1 = permuted[:n1]
        perm_data2 = permuted[n1:]
        perm_stats[i] = statistic(perm_data1, perm_data2)

    # Calculate p-value based on alternative hypothesis
    if alternative == 'two-sided':
        p_value = np.mean(np.abs(perm_stats) >= np.abs(observed_stat))
    elif alternative == 'greater':
        p_value = np.mean(perm_stats >= observed_stat)
    elif alternative == 'less':
        p_value = np.mean(perm_stats <= observed_stat)
    else:
        raise ValueError(f"Invalid alternative: {alternative}")

    return {
        'observed_statistic': observed_stat,
        'permutation_distribution': perm_stats,
        'p_value': p_value,
        'n_permutations': n_permutations,
        'alternative': alternative,
        'significant_005': p_value < 0.05,
        'significant_001': p_value < 0.01
    }


def wilson_score_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate Wilson score confidence interval for binomial proportion.

    Recommended over normal approximation for better coverage.
    Reference: Brown, Cai, DasGupta (2001), Statistical Science.

    Parameters
    ----------
    successes : int
        Number of successes
    trials : int
        Number of trials
    confidence_level : float, default=0.95
        Confidence level

    Returns
    -------
    Tuple[float, float]
        (lower_bound, upper_bound) for proportion
    """
    if trials == 0:
        return (0.0, 1.0)

    p_hat = successes / trials
    alpha = 1 - confidence_level
    z = stats.norm.ppf(1 - alpha/2)

    denominator = 1 + (z**2 / trials)
    center = (p_hat + (z**2 / (2 * trials))) / denominator
    margin = (z / denominator) * np.sqrt((p_hat * (1 - p_hat) / trials) + (z**2 / (4 * trials**2)))

    lower = center - margin
    upper = center + margin

    return (max(0.0, lower), min(1.0, upper))


def clopper_pearson_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate Clopper-Pearson exact confidence interval for binomial proportion.

    Provides conservative (guaranteed) coverage at the nominal level.

    Parameters
    ----------
    successes : int
        Number of successes
    trials : int
        Number of trials
    confidence_level : float, default=0.95
        Confidence level

    Returns
    -------
    Tuple[float, float]
        (lower_bound, upper_bound) for proportion
    """
    if trials == 0:
        return (0.0, 1.0)

    alpha = 1 - confidence_level

    # Lower bound: F distribution
    if successes == 0:
        lower = 0.0
    else:
        lower = stats.beta.ppf(alpha/2, successes, trials - successes + 1)

    # Upper bound: F distribution
    if successes == trials:
        upper = 1.0
    else:
        upper = stats.beta.ppf(1 - alpha/2, successes + 1, trials - successes)

    return (lower, upper)


def agresti_coull_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate Agresti-Coull adjusted confidence interval.

    Simple adjustment to Wald interval that improves coverage.
    Reference: Agresti & Coull (1998), The American Statistician.

    Parameters
    ----------
    successes : int
        Number of successes
    trials : int
        Number of trials
    confidence_level : float, default=0.95
        Confidence level

    Returns
    -------
    Tuple[float, float]
        (lower_bound, upper_bound) for proportion
    """
    if trials == 0:
        return (0.0, 1.0)

    alpha = 1 - confidence_level
    z = stats.norm.ppf(1 - alpha/2)

    # Adjust counts
    n_tilde = trials + z**2
    p_tilde = (successes + (z**2 / 2)) / n_tilde

    # Standard error
    se = np.sqrt(p_tilde * (1 - p_tilde) / n_tilde)

    # Interval
    margin = z * se
    lower = max(0.0, p_tilde - margin)
    upper = min(1.0, p_tilde + margin)

    return (lower, upper)


def power_analysis_ttest(
    effect_size: float,
    n: int,
    alpha: float = 0.05,
    alternative: str = 'two-sided'
) -> float:
    """
    Calculate statistical power for t-test given effect size and sample size.

    Parameters
    ----------
    effect_size : float
        Cohen's d effect size
    n : int
        Sample size (per group for two-sample, total for one-sample)
    alpha : float, default=0.05
        Significance level
    alternative : str, default='two-sided'
        Type of test

    Returns
    -------
    float
        Statistical power (0-1)
    """
    from scipy.stats import nct

    if alternative == 'two-sided':
        critical_t = stats.t.ppf(1 - alpha/2, n - 1)
    elif alternative == 'greater':
        critical_t = stats.t.ppf(1 - alpha, n - 1)
    else:  # 'less'
        critical_t = stats.t.ppf(alpha, n - 1)

    # Non-centrality parameter
    ncp = effect_size * np.sqrt(n)

    # Power calculation using non-central t-distribution
    if alternative == 'two-sided':
        power = 1 - nct.cdf(critical_t, n - 1, ncp) + nct.cdf(-critical_t, n - 1, ncp)
    elif alternative == 'greater':
        power = 1 - nct.cdf(critical_t, n - 1, ncp)
    else:  # 'less'
        power = nct.cdf(critical_t, n - 1, ncp)

    return power


def sample_size_for_power(
    effect_size: float,
    power: float = 0.80,
    alpha: float = 0.05,
    alternative: str = 'two-sided'
) -> int:
    """
    Calculate required sample size to achieve desired power.

    Parameters
    ----------
    effect_size : float
        Cohen's d effect size to detect
    power : float, default=0.80
        Desired statistical power
    alpha : float, default=0.05
        Significance level
    alternative : str, default='two-sided'
        Type of test

    Returns
    -------
    int
        Required sample size
    """
    # Binary search for required n
    n_low, n_high = 2, 10000

    while n_low < n_high:
        n_mid = (n_low + n_high) // 2
        achieved_power = power_analysis_ttest(effect_size, n_mid, alpha, alternative)

        if achieved_power < power:
            n_low = n_mid + 1
        else:
            n_high = n_mid

    return n_low


def validate_binomial_distribution(
    observed_counts: np.ndarray,
    n_trials: int,
    p: float,
    alpha: float = 0.05
) -> Dict[str, Union[float, bool, str]]:
    """
    Test whether observed counts follow binomial distribution using chi-squared test.

    Parameters
    ----------
    observed_counts : np.ndarray
        Observed count values from trials
    n_trials : int
        Number of trials per observation
    p : float
        Binomial probability parameter
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    Dict[str, Union[float, bool, str]]
        Test results including chi-squared statistic and p-value
    """
    # Bin the observed counts
    min_count = int(observed_counts.min())
    max_count = int(observed_counts.max())

    # Create bins (combine tail bins for chi-squared validity)
    bins = np.arange(min_count, max_count + 2)
    observed_hist, _ = np.histogram(observed_counts, bins=bins)

    # Expected frequencies under binomial
    expected_probs = stats.binom.pmf(bins[:-1], n_trials, p)
    expected_hist = expected_probs * len(observed_counts)

    # Combine bins with expected < 5 (chi-squared requirement)
    combined_observed = []
    combined_expected = []
    current_obs = 0
    current_exp = 0

    for obs, exp in zip(observed_hist, expected_hist):
        current_obs += obs
        current_exp += exp
        if current_exp >= 5:
            combined_observed.append(current_obs)
            combined_expected.append(current_exp)
            current_obs = 0
            current_exp = 0

    # Add remaining if any
    if current_obs > 0 or current_exp > 0:
        if len(combined_observed) > 0:
            combined_observed[-1] += current_obs
            combined_expected[-1] += current_exp
        else:
            combined_observed.append(current_obs)
            combined_expected.append(current_exp)

    combined_observed = np.array(combined_observed)
    combined_expected = np.array(combined_expected)

    # Chi-squared test
    if len(combined_observed) > 1:
        chi_squared_stat, p_value = stats.chisquare(combined_observed, combined_expected)
        fits_binomial = p_value > alpha

        conclusion = (
            f"{'✓ Consistent' if fits_binomial else '✗ Inconsistent'} with binomial "
            f"(χ²={chi_squared_stat:.3f}, p={p_value:.4f}, α={alpha})"
        )
    else:
        chi_squared_stat, p_value = np.nan, np.nan
        fits_binomial = None
        conclusion = "Insufficient bins for chi-squared test"

    return {
        'chi_squared_statistic': chi_squared_stat,
        'p_value': p_value,
        'df': len(combined_observed) - 1 if len(combined_observed) > 1 else 0,
        'fits_binomial': fits_binomial,
        'alpha': alpha,
        'conclusion': conclusion
    }


def concentration_inequality_validation(
    estimates: np.ndarray,
    true_value: float,
    epsilon: float = 0.2
) -> Dict[str, Union[float, int]]:
    """
    Validate concentration inequalities (Chernoff, Hoeffding) empirically.

    Compares theoretical tail probability bounds with empirical frequencies.

    Parameters
    ----------
    estimates : np.ndarray
        Array of estimates from multiple trials
    true_value : float
        True value being estimated
    epsilon : float, default=0.2
        Relative deviation threshold

    Returns
    -------
    Dict[str, Union[float, int]]
        Validation results including theoretical vs empirical tail probabilities
    """
    n_trials = len(estimates)
    deviations = np.abs(estimates - true_value)
    relative_deviations = deviations / true_value if true_value > 0 else deviations

    # Empirical tail probability
    empirical_tail_prob = np.mean(relative_deviations > epsilon)

    # Theoretical Chernoff bound (for binomial-based estimates)
    # P(|X - μ| > ε*μ) ≤ 2*exp(-ε²*μ/3) for binomial
    # This is a simplified bound; exact form depends on algorithm
    theoretical_bound = 2 * np.exp(-(epsilon**2 * true_value) / 3)

    return {
        'epsilon': epsilon,
        'empirical_tail_probability': empirical_tail_prob,
        'theoretical_bound': theoretical_bound,
        'bound_holds': empirical_tail_prob <= theoretical_bound,
        'bound_tightness': empirical_tail_prob / theoretical_bound if theoretical_bound > 0 else np.inf,
        'n_trials': n_trials,
        'n_violations': int(np.sum(relative_deviations > epsilon))
    }


def qq_plot_normality_test(
    data: np.ndarray,
    alpha: float = 0.05
) -> Dict[str, Union[float, bool, np.ndarray]]:
    """
    Test normality using Q-Q plot and Shapiro-Wilk test.

    Parameters
    ----------
    data : np.ndarray
        Data to test for normality
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    Dict[str, Union[float, bool, np.ndarray]]
        Normality test results including:
        - theoretical_quantiles: Expected quantiles under normality
        - sample_quantiles: Observed quantiles
        - shapiro_statistic: Shapiro-Wilk test statistic
        - shapiro_pvalue: Shapiro-Wilk p-value
        - is_normal: True if p > alpha
    """
    # Standardize data
    standardized = (data - np.mean(data)) / np.std(data)

    # Theoretical quantiles
    n = len(data)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, n))

    # Sample quantiles
    sample_quantiles = np.sort(standardized)

    # Shapiro-Wilk test
    if n >= 3:
        shapiro_stat, shapiro_p = stats.shapiro(data)
        is_normal = shapiro_p > alpha
    else:
        shapiro_stat, shapiro_p = np.nan, np.nan
        is_normal = None

    return {
        'theoretical_quantiles': theoretical_quantiles,
        'sample_quantiles': sample_quantiles,
        'shapiro_statistic': shapiro_stat,
        'shapiro_pvalue': shapiro_p,
        'is_normal': is_normal,
        'alpha': alpha
    }
