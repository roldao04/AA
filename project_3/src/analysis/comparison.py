"""
Comprehensive Algorithm Comparison Analysis Module.

This module provides functions for comparing ExactCounter, FixedProbabilityCounter,
and SpaceSaving algorithms across multiple performance dimensions including
accuracy, memory usage, execution time, and statistical properties.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any
from scipy import stats


def load_all_results(
    exact_path: str = None,
    fixed_prob_path: str = None,
    space_saving_path: str = None
) -> Dict[str, Any]:
    """
    Load all algorithm results for comprehensive comparison.

    Parameters
    ----------
    exact_path : str, optional
        Path to exact counter results directory
    fixed_prob_path : str, optional
        Path to fixed probability results directory
    space_saving_path : str, optional
        Path to space-saving results directory

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - 'exact': Exact counter results
        - 'fixed_prob': Fixed probability results
        - 'space_saving': Space-Saving results for all k values
        - 'metadata': Loading metadata
    """
    from utils.config import (
        RESULTS_EXACT_PATH,
        RESULTS_FIXED_PROB_PATH,
        RESULTS_SPACE_SAVING_PATH,
        SPACE_SAVING_K_VALUES
    )

    exact_path = exact_path or RESULTS_EXACT_PATH
    fixed_prob_path = fixed_prob_path or RESULTS_FIXED_PROB_PATH
    space_saving_path = space_saving_path or RESULTS_SPACE_SAVING_PATH

    results = {
        'exact': {},
        'fixed_prob': {},
        'space_saving': {},
        'metadata': {}
    }

    # Load exact counter results
    exact_stats_file = Path(exact_path) / 'exact_statistics.json'
    exact_counts_file = Path(exact_path) / 'exact_counts_full_dataset.csv'
    exact_perf_file = Path(exact_path) / 'exact_performance.json'

    if exact_stats_file.exists():
        with open(exact_stats_file, 'r') as f:
            results['exact']['statistics'] = json.load(f)

    if exact_counts_file.exists():
        results['exact']['counts_df'] = pd.read_csv(exact_counts_file)
        results['exact']['counts_dict'] = dict(
            zip(results['exact']['counts_df']['temperature'],
                results['exact']['counts_df']['count'])
        )

    if exact_perf_file.exists():
        with open(exact_perf_file, 'r') as f:
            results['exact']['performance'] = json.load(f)

    # Load fixed probability results
    fp_trials_file = Path(fixed_prob_path) / 'trial_results_p25_n100.pkl'
    fp_summary_file = Path(fixed_prob_path) / 'summary_statistics.csv'
    fp_error_file = Path(fixed_prob_path) / 'error_analysis.json'
    fp_perf_file = Path(fixed_prob_path) / 'performance_metrics.json'

    if fp_trials_file.exists():
        with open(fp_trials_file, 'rb') as f:
            results['fixed_prob']['trial_results'] = pickle.load(f)

    if fp_summary_file.exists():
        results['fixed_prob']['summary'] = pd.read_csv(fp_summary_file)

    if fp_error_file.exists():
        with open(fp_error_file, 'r') as f:
            results['fixed_prob']['error_analysis'] = json.load(f)

    if fp_perf_file.exists():
        with open(fp_perf_file, 'r') as f:
            results['fixed_prob']['performance'] = json.load(f)

    # Load Space-Saving results for all k values
    results['space_saving']['by_k'] = {}

    for k in SPACE_SAVING_K_VALUES:
        ss_results_file = Path(space_saving_path) / f'ss_results_k{k}.json'
        if ss_results_file.exists():
            with open(ss_results_file, 'r') as f:
                results['space_saving']['by_k'][k] = json.load(f)

    # Load aggregated Space-Saving analyses
    ss_precision_recall_file = Path(space_saving_path) / 'precision_recall_analysis.csv'
    ss_comparison_file = Path(space_saving_path) / 'k_comparison.csv'
    ss_perf_file = Path(space_saving_path) / 'performance_metrics.json'

    if ss_precision_recall_file.exists():
        results['space_saving']['precision_recall'] = pd.read_csv(ss_precision_recall_file)

    if ss_comparison_file.exists():
        results['space_saving']['k_comparison'] = pd.read_csv(ss_comparison_file)

    if ss_perf_file.exists():
        with open(ss_perf_file, 'r') as f:
            results['space_saving']['performance'] = json.load(f)

    # Metadata
    results['metadata']['exact_loaded'] = bool(results['exact'])
    results['metadata']['fixed_prob_loaded'] = bool(results['fixed_prob'])
    results['metadata']['space_saving_k_loaded'] = list(results['space_saving']['by_k'].keys())

    return results


def create_master_comparison_table(results: Dict[str, Any]) -> pd.DataFrame:
    """
    Create master comparison table with all algorithms and metrics.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()

    Returns
    -------
    pd.DataFrame
        Comprehensive comparison table with columns:
        - Algorithm: Algorithm name/configuration
        - Memory_KB: Peak memory usage in kilobytes
        - Time_ms: Execution time in milliseconds
        - Mean_Rel_Error_%: Mean relative error percentage
        - Std_Rel_Error_%: Standard deviation of relative error
        - Max_Abs_Error: Maximum absolute error
        - RMSE: Root mean squared error
    """
    table_rows = []

    # Exact Counter
    if 'performance' in results['exact']:
        perf = results['exact']['performance']
        table_rows.append({
            'Algorithm': 'Exact Counter',
            'Memory_KB': perf.get('peak_memory_kb', 0),
            'Time_ms': perf.get('execution_time_ms', 0),
            'Mean_Rel_Error_%': 0.0,
            'Std_Rel_Error_%': 0.0,
            'Max_Abs_Error': 0,
            'RMSE': 0.0
        })

    # Fixed Probability Counter
    if 'summary' in results['fixed_prob']:
        summary = results['fixed_prob']['summary']
        perf = results['fixed_prob'].get('performance', {})

        table_rows.append({
            'Algorithm': 'Fixed Prob (p=0.25)',
            'Memory_KB': perf.get('peak_memory_kb', 0),
            'Time_ms': perf.get('avg_execution_time_ms', 0),
            'Mean_Rel_Error_%': summary['relative_error'].mean() * 100,
            'Std_Rel_Error_%': summary['relative_error'].std() * 100,
            'Max_Abs_Error': summary['absolute_error'].max(),
            'RMSE': summary['rmse'].mean()
        })

    # Space-Saving for each k
    if 'by_k' in results['space_saving']:
        for k, ss_data in sorted(results['space_saving']['by_k'].items()):
            # Calculate metrics from monitored items
            monitored_items = ss_data.get('monitored_items', {})
            exact_counts = results['exact']['counts_dict']

            # Calculate errors
            errors = []
            rel_errors = []
            for temp_str, item_data in monitored_items.items():
                temp = int(temp_str) if isinstance(temp_str, str) else temp_str
                count = item_data['count']
                true_count = exact_counts.get(temp, 0)
                if true_count > 0:
                    abs_error = abs(count - true_count)
                    errors.append(abs_error)
                    rel_errors.append(abs_error / true_count)

            # Get performance metrics directly from ss_data
            memory_kb = ss_data.get('peak_memory_kb', 0)
            time_sec = ss_data.get('execution_time_sec', 0)
            time_ms = time_sec * 1000  # Convert to milliseconds

            table_rows.append({
                'Algorithm': f'Space-Saving (k={k})',
                'Memory_KB': memory_kb,
                'Time_ms': time_ms,
                'Mean_Rel_Error_%': np.mean(rel_errors) * 100 if rel_errors else 0.0,
                'Std_Rel_Error_%': np.std(rel_errors) * 100 if rel_errors else 0.0,
                'Max_Abs_Error': max(errors) if errors else 0,
                'RMSE': np.sqrt(np.mean([e**2 for e in errors])) if errors else 0.0
            })

    df = pd.DataFrame(table_rows)

    # Round for readability
    df['Memory_KB'] = df['Memory_KB'].round(2)
    df['Time_ms'] = df['Time_ms'].round(3)
    df['Mean_Rel_Error_%'] = df['Mean_Rel_Error_%'].round(3)
    df['Std_Rel_Error_%'] = df['Std_Rel_Error_%'].round(3)
    df['Max_Abs_Error'] = df['Max_Abs_Error'].round(0)
    df['RMSE'] = df['RMSE'].round(2)

    return df


def calculate_cross_algorithm_errors(results: Dict[str, Any]) -> pd.DataFrame:
    """
    Calculate detailed error metrics for all algorithms on all temperatures.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - temperature: Temperature value
        - true_count: Exact count
        - fp_mean_estimate: Fixed Prob mean estimate
        - fp_abs_error: Fixed Prob absolute error
        - fp_rel_error: Fixed Prob relative error
        - ss_k{k}_estimate: Space-Saving estimate for each k
        - ss_k{k}_abs_error: Space-Saving absolute error for each k
        - ss_k{k}_rel_error: Space-Saving relative error for each k
    """
    exact_counts = results['exact']['counts_dict']
    fp_summary = results['fixed_prob'].get('summary')
    ss_by_k = results['space_saving'].get('by_k', {})

    # Start with exact counts
    df = pd.DataFrame([
        {'temperature': temp, 'true_count': count}
        for temp, count in exact_counts.items()
    ])

    # Add Fixed Probability estimates
    if fp_summary is not None:
        fp_data = fp_summary[['temperature', 'mean_estimate', 'absolute_error', 'relative_error']].copy()
        fp_data.columns = ['temperature', 'fp_mean_estimate', 'fp_abs_error', 'fp_rel_error']
        df = df.merge(fp_data, on='temperature', how='left')

    # Add Space-Saving estimates for each k
    for k, ss_data in sorted(ss_by_k.items()):
        monitored_items = ss_data.get('monitored_items', {})

        # Create k-specific columns
        k_estimates = []
        k_abs_errors = []
        k_rel_errors = []

        for _, row in df.iterrows():
            temp = int(row['temperature'])
            true_count = row['true_count']

            if str(temp) in monitored_items:
                item_data = monitored_items[str(temp)]
                ss_count = item_data['count']
                abs_error = abs(ss_count - true_count)
                rel_error = abs_error / true_count if true_count > 0 else 0
            else:
                ss_count = 0
                abs_error = true_count  # Missed item
                rel_error = 1.0 if true_count > 0 else 0

            k_estimates.append(ss_count)
            k_abs_errors.append(abs_error)
            k_rel_errors.append(rel_error)

        df[f'ss_k{k}_estimate'] = k_estimates
        df[f'ss_k{k}_abs_error'] = k_abs_errors
        df[f'ss_k{k}_rel_error'] = k_rel_errors

    # Sort by true count descending
    df = df.sort_values('true_count', ascending=False).reset_index(drop=True)

    return df


def paired_comparison_test(
    results: Dict[str, Any],
    k_value: int = 20,
    alpha: float = 0.05
) -> Dict[str, Union[float, str, bool]]:
    """
    Perform paired t-test comparing Fixed Prob vs Space-Saving.

    Compares absolute errors for temperatures monitored by both algorithms.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()
    k_value : int, default=20
        Which Space-Saving k value to compare against
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    Dict[str, Union[float, str, bool]]
        Test results including:
        - n_compared: Number of temperatures compared
        - mean_diff: Mean difference (FP - SS)
        - t_statistic: t-test statistic
        - p_value: Two-tailed p-value
        - cohen_d: Effect size
        - significant: True if p < alpha
        - conclusion: Human-readable conclusion
    """
    exact_counts = results['exact']['counts_dict']
    fp_summary = results['fixed_prob'].get('summary')
    ss_data = results['space_saving']['by_k'].get(k_value)

    if fp_summary is None or ss_data is None:
        return {'error': 'Missing data for comparison'}

    # Get errors for temperatures monitored by both
    fp_errors = []
    ss_errors = []
    compared_temps = []

    monitored_items = ss_data.get('monitored_items', {})
    monitored_temps = set(int(t) for t in monitored_items.keys())

    for temp in monitored_temps:
        if temp in exact_counts:
            # Fixed Prob error
            fp_row = fp_summary[fp_summary['temperature'] == temp]
            if not fp_row.empty:
                fp_errors.append(fp_row['absolute_error'].values[0])

                # Space-Saving error
                item_data = monitored_items[str(temp)]
                ss_count = item_data['count']
                ss_error = abs(ss_count - exact_counts[temp])
                ss_errors.append(ss_error)
                compared_temps.append(temp)

    if len(fp_errors) < 2:
        return {'error': 'Insufficient data for paired comparison'}

    # Paired t-test
    fp_errors = np.array(fp_errors)
    ss_errors = np.array(ss_errors)
    differences = fp_errors - ss_errors

    t_stat, p_value = stats.ttest_rel(fp_errors, ss_errors)

    # Cohen's d for paired samples
    mean_diff = differences.mean()
    std_diff = differences.std()
    cohen_d = mean_diff / std_diff if std_diff > 0 else 0

    significant = p_value < alpha

    if significant:
        winner = "Fixed Prob" if mean_diff < 0 else "Space-Saving"
        conclusion = (
            f"✓ Significant difference (p={p_value:.4f} < α={alpha}). "
            f"{winner} has lower error by {abs(mean_diff):.2f} on average "
            f"(Cohen's d={cohen_d:.3f})."
        )
    else:
        conclusion = (
            f"✗ No significant difference (p={p_value:.4f} >= α={alpha}). "
            f"Algorithms perform similarly (mean diff={mean_diff:.2f})."
        )

    return {
        'n_compared': len(compared_temps),
        'compared_temperatures': compared_temps,
        'mean_diff_fp_minus_ss': mean_diff,
        'std_diff': std_diff,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohen_d': cohen_d,
        'significant': significant,
        'alpha': alpha,
        'conclusion': conclusion
    }


def calculate_effect_sizes(results: Dict[str, Any]) -> pd.DataFrame:
    """
    Calculate Cohen's d effect sizes for all pairwise algorithm comparisons.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()

    Returns
    -------
    pd.DataFrame
        Effect size comparison table with columns:
        - comparison: "Algorithm1 vs Algorithm2"
        - n: Number of temperatures compared
        - cohen_d: Effect size
        - magnitude: Interpretation (small/medium/large)
    """
    cross_errors = calculate_cross_algorithm_errors(results)

    comparisons = []

    # Fixed Prob vs each Space-Saving k
    for col in cross_errors.columns:
        if col.startswith('ss_k') and col.endswith('_abs_error'):
            k_value = col.split('_')[1]  # Extract k value

            # Get errors for both algorithms
            fp_errors = cross_errors['fp_abs_error'].dropna()
            ss_errors = cross_errors[col].dropna()

            # Find common temperatures
            common_idx = cross_errors['fp_abs_error'].notna() & cross_errors[col].notna()
            fp_common = cross_errors.loc[common_idx, 'fp_abs_error'].values
            ss_common = cross_errors.loc[common_idx, col].values

            if len(fp_common) > 1:
                # Pooled standard deviation
                pooled_std = np.sqrt((fp_common.var() + ss_common.var()) / 2)
                cohen_d = (fp_common.mean() - ss_common.mean()) / pooled_std if pooled_std > 0 else 0

                # Interpret magnitude
                abs_d = abs(cohen_d)
                if abs_d < 0.2:
                    magnitude = "negligible"
                elif abs_d < 0.5:
                    magnitude = "small"
                elif abs_d < 0.8:
                    magnitude = "medium"
                else:
                    magnitude = "large"

                comparisons.append({
                    'comparison': f'Fixed Prob vs Space-Saving {k_value}',
                    'n': len(fp_common),
                    'cohen_d': cohen_d,
                    'magnitude': magnitude
                })

    return pd.DataFrame(comparisons)


def compare_memory_usage(results: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract and compare memory usage across all algorithms.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()

    Returns
    -------
    pd.DataFrame
        Memory comparison with columns:
        - algorithm: Algorithm name
        - peak_memory_kb: Peak memory in KB
        - memory_per_item_bytes: Memory per unique item
    """
    memory_data = []

    n_unique = len(results['exact']['counts_dict'])

    # Validation warnings
    warnings = []

    # Exact Counter
    if 'performance' in results['exact']:
        perf = results['exact']['performance']
        memory_kb = perf.get('peak_memory_kb', 0)
        memory_data.append({
            'algorithm': 'Exact Counter',
            'peak_memory_kb': memory_kb,
            'memory_per_item_bytes': (memory_kb * 1024) / n_unique if n_unique > 0 else 0
        })

    # Fixed Probability - divide by 100 to get per-trial average
    if 'performance' in results['fixed_prob']:
        perf = results['fixed_prob']['performance']
        memory_kb_total = perf.get('peak_memory_kb', 0)
        num_trials = perf.get('num_trials', 100)
        memory_kb = memory_kb_total / num_trials  # Per-trial average
        memory_data.append({
            'algorithm': 'Fixed Prob (p=0.25)',
            'peak_memory_kb': memory_kb,
            'memory_per_item_bytes': (memory_kb * 1024) / n_unique if n_unique > 0 else 0
        })

    # Space-Saving for each k - correctly parse metrics array structure
    if 'performance' in results['space_saving']:
        perf = results['space_saving']['performance']
        # Check if metrics is a list (new structure)
        if 'metrics' in perf and isinstance(perf['metrics'], list):
            for metric in perf['metrics']:
                k = metric.get('k')
                memory_kb = metric.get('peak_memory_kb', 0)
                memory_data.append({
                    'algorithm': f'Space-Saving (k={k})',
                    'peak_memory_kb': memory_kb,
                    'memory_per_item_bytes': (memory_kb * 1024) / k if k > 0 else 0
                })
        else:
            # Fallback to old structure
            for k in sorted(results['space_saving']['by_k'].keys()):
                k_perf = perf.get(f'k{k}', {})
                memory_kb = k_perf.get('peak_memory_kb', 0)
                memory_data.append({
                    'algorithm': f'Space-Saving (k={k})',
                    'peak_memory_kb': memory_kb,
                    'memory_per_item_bytes': (memory_kb * 1024) / k if k > 0 else 0
                })

    df = pd.DataFrame(memory_data)

    # Data validation
    zero_memory = df[df['peak_memory_kb'] == 0]
    if len(zero_memory) > 0:
        print(f"⚠ WARNING: {len(zero_memory)} algorithms show 0 KB memory usage:")
        for alg in zero_memory['algorithm'].values:
            print(f"    - {alg}")
        print("  This may indicate a data collection issue.")

    return df


def compare_execution_time(results: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract and compare execution times across all algorithms.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()

    Returns
    -------
    pd.DataFrame
        Time comparison with columns:
        - algorithm: Algorithm name
        - execution_time_ms: Execution time in milliseconds
        - time_per_element_us: Microseconds per stream element
    """
    time_data = []

    n_total = results['exact']['statistics']['total_observations']

    # Exact Counter
    if 'performance' in results['exact']:
        perf = results['exact']['performance']
        time_ms = perf.get('execution_time_ms', 0)
        time_data.append({
            'algorithm': 'Exact Counter',
            'execution_time_ms': time_ms,
            'time_per_element_us': (time_ms * 1000) / n_total if n_total > 0 else 0
        })

    # Fixed Probability - divide by 100 to get per-trial average
    if 'performance' in results['fixed_prob']:
        perf = results['fixed_prob']['performance']
        # Convert from total seconds to per-trial milliseconds
        total_time_sec = perf.get('total_execution_time_sec', 0)
        num_trials = perf.get('num_trials', 100)
        time_ms = (total_time_sec / num_trials) * 1000 if num_trials > 0 else 0
        time_data.append({
            'algorithm': 'Fixed Prob (p=0.25)',
            'execution_time_ms': time_ms,
            'time_per_element_us': (time_ms * 1000) / n_total if n_total > 0 else 0
        })

    # Space-Saving for each k - correctly parse metrics array structure
    if 'performance' in results['space_saving']:
        perf = results['space_saving']['performance']
        # Check if metrics is a list (new structure)
        if 'metrics' in perf and isinstance(perf['metrics'], list):
            for metric in perf['metrics']:
                k = metric.get('k')
                time_sec = metric.get('execution_time_sec', 0)
                time_ms = time_sec * 1000  # Convert to milliseconds
                time_data.append({
                    'algorithm': f'Space-Saving (k={k})',
                    'execution_time_ms': time_ms,
                    'time_per_element_us': (time_ms * 1000) / n_total if n_total > 0 else 0
                })
        else:
            # Fallback to old structure
            for k in sorted(results['space_saving']['by_k'].keys()):
                k_perf = perf.get(f'k{k}', {})
                time_ms = k_perf.get('execution_time_ms', 0)
                time_data.append({
                    'algorithm': f'Space-Saving (k={k})',
                    'execution_time_ms': time_ms,
                    'time_per_element_us': (time_ms * 1000) / n_total if n_total > 0 else 0
                })

    df = pd.DataFrame(time_data)

    # Data validation
    zero_time = df[df['execution_time_ms'] == 0]
    if len(zero_time) > 0:
        print(f"⚠ WARNING: {len(zero_time)} algorithms show 0 ms execution time:")
        for alg in zero_time['algorithm'].values:
            print(f"    - {alg}")
        print("  This may indicate a data collection issue.")

    return df


def identify_pareto_frontier(
    memory: np.ndarray,
    error: np.ndarray
) -> np.ndarray:
    """
    Identify Pareto frontier points (minimize both memory and error).

    A point is on the Pareto frontier if no other point has both
    lower memory AND lower error.

    Parameters
    ----------
    memory : np.ndarray
        Memory values
    error : np.ndarray
        Error values

    Returns
    -------
    np.ndarray
        Boolean array indicating Pareto frontier points
    """
    is_pareto = np.ones(len(memory), dtype=bool)

    for i in range(len(memory)):
        for j in range(len(memory)):
            if i != j:
                # j dominates i if it has lower/equal memory AND lower error
                if memory[j] <= memory[i] and error[j] < error[i]:
                    is_pareto[i] = False
                    break
                # or lower memory AND lower/equal error
                if memory[j] < memory[i] and error[j] <= error[i]:
                    is_pareto[i] = False
                    break

    return is_pareto


def calculate_ranking_correlation(
    results: Dict[str, Any],
    n: int = 20
) -> pd.DataFrame:
    """
    Calculate ranking correlation metrics (Kendall's tau, Spearman's rho)
    to verify if algorithms identify items in the same relative order.

    This addresses the PDF requirement: "verify whether the same most frequent /
    less frequent items are identified, and in the same relative order"

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()
    n : int, default=20
        Number of top items to compare

    Returns
    -------
    pd.DataFrame
        Ranking correlation results with columns:
        - comparison: "Algorithm1 vs Algorithm2"
        - n_items: Number of items compared
        - kendall_tau: Kendall's tau correlation coefficient
        - kendall_p: p-value for Kendall's tau
        - spearman_rho: Spearman's rank correlation coefficient
        - spearman_p: p-value for Spearman's rho
        - perfect_match: True if rankings are identical
    """
    exact_counts = results['exact']['counts_dict']
    fp_summary = results['fixed_prob'].get('summary')
    ss_by_k = results['space_saving'].get('by_k', {})

    # Get exact ranking (ground truth)
    exact_ranking = sorted(exact_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    exact_temps = [temp for temp, _ in exact_ranking]

    correlation_results = []

    # Fixed Probability vs Exact
    if fp_summary is not None:
        fp_ranking = fp_summary.nlargest(n, 'mean_estimate')[['temperature', 'mean_estimate']]
        fp_temps = fp_ranking['temperature'].tolist()

        # Find common temperatures
        common_temps = [t for t in exact_temps if t in fp_temps]

        if len(common_temps) >= 2:  # Need at least 2 items for correlation
            # Get ranks for common temperatures
            exact_ranks = [exact_temps.index(t) for t in common_temps]
            fp_ranks = [fp_temps.index(t) for t in common_temps]

            # Calculate correlations
            kendall_tau, kendall_p = stats.kendalltau(exact_ranks, fp_ranks)
            spearman_rho, spearman_p = stats.spearmanr(exact_ranks, fp_ranks)

            correlation_results.append({
                'comparison': 'Exact vs Fixed Prob',
                'n_items': len(common_temps),
                'kendall_tau': kendall_tau,
                'kendall_p': kendall_p,
                'spearman_rho': spearman_rho,
                'spearman_p': spearman_p,
                'perfect_match': (exact_ranks == fp_ranks)
            })

    # Space-Saving vs Exact for each k
    for k, ss_data in sorted(ss_by_k.items()):
        monitored_items = ss_data.get('monitored_items', {})

        # Create ranking from Space-Saving
        ss_ranking = sorted(
            [(int(temp), item['count']) for temp, item in monitored_items.items()],
            key=lambda x: x[1],
            reverse=True
        )[:n]
        ss_temps = [temp for temp, _ in ss_ranking]

        # Find common temperatures
        common_temps = [t for t in exact_temps if t in ss_temps]

        if len(common_temps) >= 2:
            # Get ranks
            exact_ranks = [exact_temps.index(t) for t in common_temps]
            ss_ranks = [ss_temps.index(t) for t in common_temps]

            # Calculate correlations
            kendall_tau, kendall_p = stats.kendalltau(exact_ranks, ss_ranks)
            spearman_rho, spearman_p = stats.spearmanr(exact_ranks, ss_ranks)

            correlation_results.append({
                'comparison': f'Exact vs Space-Saving k={k}',
                'n_items': len(common_temps),
                'kendall_tau': kendall_tau,
                'kendall_p': kendall_p,
                'spearman_rho': spearman_rho,
                'spearman_p': spearman_p,
                'perfect_match': (exact_ranks == ss_ranks)
            })

    # Fixed Prob vs Space-Saving comparisons
    if fp_summary is not None:
        fp_ranking = fp_summary.nlargest(n, 'mean_estimate')[['temperature', 'mean_estimate']]
        fp_temps = fp_ranking['temperature'].tolist()

        for k, ss_data in sorted(ss_by_k.items()):
            monitored_items = ss_data.get('monitored_items', {})
            ss_ranking = sorted(
                [(int(temp), item['count']) for temp, item in monitored_items.items()],
                key=lambda x: x[1],
                reverse=True
            )[:n]
            ss_temps = [temp for temp, _ in ss_ranking]

            common_temps = [t for t in fp_temps if t in ss_temps]

            if len(common_temps) >= 2:
                fp_ranks = [fp_temps.index(t) for t in common_temps]
                ss_ranks = [ss_temps.index(t) for t in common_temps]

                kendall_tau, kendall_p = stats.kendalltau(fp_ranks, ss_ranks)
                spearman_rho, spearman_p = stats.spearmanr(fp_ranks, ss_ranks)

                correlation_results.append({
                    'comparison': f'Fixed Prob vs Space-Saving k={k}',
                    'n_items': len(common_temps),
                    'kendall_tau': kendall_tau,
                    'kendall_p': kendall_p,
                    'spearman_rho': spearman_rho,
                    'spearman_p': spearman_p,
                    'perfect_match': (fp_ranks == ss_ranks)
                })

    df = pd.DataFrame(correlation_results)

    # Round for readability
    if len(df) > 0:
        df['kendall_tau'] = df['kendall_tau'].round(4)
        df['kendall_p'] = df['kendall_p'].round(6)
        df['spearman_rho'] = df['spearman_rho'].round(4)
        df['spearman_p'] = df['spearman_p'].round(6)

    return df


def compare_top_and_bottom_n(
    results: Dict[str, Any],
    n_values: List[int] = [5, 10, 15, 20]
) -> Dict[str, pd.DataFrame]:
    """
    Compare top-N most frequent AND bottom-N least frequent items
    across all algorithms.

    Addresses PDF requirement for analyzing both most and least frequent items.

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()
    n_values : List[int], default=[5, 10, 15, 20]
        List of n values to test

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with keys:
        - 'top_n_correlations': Ranking correlations for most frequent
        - 'bottom_n_correlations': Ranking correlations for least frequent
        - 'top_n_overlap': Set overlap metrics for top-N
        - 'bottom_n_overlap': Set overlap metrics for bottom-N
    """
    all_results = {
        'top_n_correlations': [],
        'bottom_n_correlations': [],
        'top_n_overlap': [],
        'bottom_n_overlap': []
    }

    for n in n_values:
        # Top-N (most frequent)
        top_corr = calculate_ranking_correlation(results, n=n)
        top_corr['n'] = n
        top_corr['type'] = 'top_n'
        all_results['top_n_correlations'].append(top_corr)

        # Bottom-N (least frequent)
        bottom_corr = calculate_ranking_correlation_bottom_n(results, n=n)
        bottom_corr['n'] = n
        bottom_corr['type'] = 'bottom_n'
        all_results['bottom_n_correlations'].append(bottom_corr)

    # Concatenate results
    all_results['top_n_correlations'] = pd.concat(
        all_results['top_n_correlations'], ignore_index=True
    )
    all_results['bottom_n_correlations'] = pd.concat(
        all_results['bottom_n_correlations'], ignore_index=True
    )

    return all_results


def calculate_ranking_correlation_bottom_n(
    results: Dict[str, Any],
    n: int = 20
) -> pd.DataFrame:
    """
    Calculate ranking correlation for LEAST frequent items (bottom-N).

    Parameters
    ----------
    results : Dict[str, Any]
        Results from load_all_results()
    n : int, default=20
        Number of bottom items to compare

    Returns
    -------
    pd.DataFrame
        Ranking correlation results for least frequent items
    """
    exact_counts = results['exact']['counts_dict']
    fp_summary = results['fixed_prob'].get('summary')
    ss_by_k = results['space_saving'].get('by_k', {})

    # Get exact ranking (ground truth) - ASCENDING for bottom-N
    exact_ranking = sorted(exact_counts.items(), key=lambda x: x[1])[:n]
    exact_temps = [temp for temp, _ in exact_ranking]

    correlation_results = []

    # Fixed Probability vs Exact
    if fp_summary is not None:
        fp_ranking = fp_summary.nsmallest(n, 'mean_estimate')[['temperature', 'mean_estimate']]
        fp_temps = fp_ranking['temperature'].tolist()

        common_temps = [t for t in exact_temps if t in fp_temps]

        if len(common_temps) >= 2:
            exact_ranks = [exact_temps.index(t) for t in common_temps]
            fp_ranks = [fp_temps.index(t) for t in common_temps]

            kendall_tau, kendall_p = stats.kendalltau(exact_ranks, fp_ranks)
            spearman_rho, spearman_p = stats.spearmanr(exact_ranks, fp_ranks)

            correlation_results.append({
                'comparison': 'Exact vs Fixed Prob',
                'n_items': len(common_temps),
                'kendall_tau': kendall_tau,
                'kendall_p': kendall_p,
                'spearman_rho': spearman_rho,
                'spearman_p': spearman_p,
                'perfect_match': (exact_ranks == fp_ranks)
            })

    # Space-Saving vs Exact (bottom-N may not be monitored!)
    for k, ss_data in sorted(ss_by_k.items()):
        monitored_items = ss_data.get('monitored_items', {})

        # For bottom-N, Space-Saving may not have these items
        # Only compare if items are monitored
        ss_ranking = sorted(
            [(int(temp), item['count']) for temp, item in monitored_items.items()],
            key=lambda x: x[1]
        )[:n]
        ss_temps = [temp for temp, _ in ss_ranking]

        common_temps = [t for t in exact_temps if t in ss_temps]

        if len(common_temps) >= 2:
            exact_ranks = [exact_temps.index(t) for t in common_temps]
            ss_ranks = [ss_temps.index(t) for t in common_temps]

            kendall_tau, kendall_p = stats.kendalltau(exact_ranks, ss_ranks)
            spearman_rho, spearman_p = stats.spearmanr(exact_ranks, ss_ranks)

            correlation_results.append({
                'comparison': f'Exact vs Space-Saving k={k}',
                'n_items': len(common_temps),
                'kendall_tau': kendall_tau,
                'kendall_p': kendall_p,
                'spearman_rho': spearman_rho,
                'spearman_p': spearman_p,
                'perfect_match': (exact_ranks == ss_ranks)
            })

    df = pd.DataFrame(correlation_results)

    if len(df) > 0:
        df['kendall_tau'] = df['kendall_tau'].round(4)
        df['kendall_p'] = df['kendall_p'].round(6)
        df['spearman_rho'] = df['spearman_rho'].round(4)
        df['spearman_p'] = df['spearman_p'].round(6)

    return df
