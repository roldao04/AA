"""
Performance Profiling and Complexity Analysis Utilities

This module provides functions for:
- Asymptotic complexity validation
- Performance profiling
- Computational bottleneck identification

Author: João Roldão (113920)
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Callable
import time
import cProfile
import pstats
import io
from pathlib import Path


def validate_time_complexity(sizes: List[int], times: List[float],
                             expected_complexity: str = 'linear') -> Dict:
    """
    Validate empirical time complexity against theoretical expectations.

    Uses log-log regression to determine actual complexity.

    Parameters:
    -----------
    sizes : list
        Input sizes (e.g., stream sizes)
    times : list
        Execution times (in any consistent unit)
    expected_complexity : str
        Expected complexity: 'constant', 'linear', 'log', 'nlogn', 'quadratic'

    Returns:
    --------
    dict : Validation results including fitted slope, R², and comparison
    """
    sizes = np.array(sizes)
    times = np.array(times)

    # Remove any zeros or negative values
    mask = (sizes > 0) & (times > 0)
    sizes = sizes[mask]
    times = times[mask]

    # Log-log regression
    log_sizes = np.log(sizes)
    log_times = np.log(times)

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_sizes, log_times)

    # Expected slopes
    expected_slopes = {
        'constant': 0.0,
        'log': 0.0,  # O(log n) becomes linear in log-log but with small coefficient
        'linear': 1.0,
        'nlogn': 1.0,  # Approximate to linear in log-log
        'quadratic': 2.0
    }

    expected_slope = expected_slopes.get(expected_complexity, 1.0)

    # Determine if slope matches expectation (within tolerance)
    tolerance = 0.3  # Allow 30% deviation
    matches_expected = abs(slope - expected_slope) < tolerance

    # Interpret actual complexity from slope
    if slope < 0.3:
        actual_complexity = 'constant or logarithmic'
    elif slope < 1.3:
        actual_complexity = 'linear'
    elif slope < 2.3:
        actual_complexity = 'quadratic'
    else:
        actual_complexity = f'polynomial (O(n^{slope:.1f}))'

    return {
        'expected_complexity': expected_complexity,
        'expected_slope': expected_slope,
        'actual_slope': slope,
        'slope_std_error': std_err,
        'r_squared': r_value ** 2,
        'p_value': p_value,
        'matches_expected': matches_expected,
        'actual_complexity': actual_complexity,
        'sample_size': len(sizes)
    }


def validate_space_complexity(sizes: List[int], memory: List[float],
                              expected_complexity: str = 'linear') -> Dict:
    """
    Validate empirical space complexity against theoretical expectations.

    Parameters:
    -----------
    sizes : list
        Problem sizes (e.g., number of unique items)
    memory : list
        Memory usage (in any consistent unit)
    expected_complexity : str
        Expected complexity: 'constant', 'linear', 'quadratic'

    Returns:
    --------
    dict : Validation results
    """
    # Similar to time complexity validation
    return validate_time_complexity(sizes, memory, expected_complexity)


def theoretical_complexity_table() -> pd.DataFrame:
    """
    Generate table of theoretical time and space complexities.

    Returns:
    --------
    DataFrame : Complexity table for all algorithms
    """
    data = [
        {
            'Algorithm': 'Exact Counter',
            'Insert_Time': 'O(1)',
            'Query_Time': 'O(1)',
            'Space': 'O(d)',
            'Space_Note': 'd = unique items',
            'Insert_Details': 'Hash table insert (amortized)',
            'Query_Details': 'Hash table lookup'
        },
        {
            'Algorithm': 'Fixed Probability',
            'Insert_Time': 'O(1)',
            'Query_Time': 'O(1)',
            'Space': 'O(1)',
            'Space_Note': 'Per counter instance',
            'Insert_Details': 'Random number generation + conditional increment',
            'Query_Details': 'Multiplication (counter * 1/p)'
        },
        {
            'Algorithm': 'Space-Saving',
            'Insert_Time': 'O(log k)',
            'Query_Time': 'O(1)',
            'Space': 'O(k)',
            'Space_Note': 'k = budget parameter',
            'Insert_Details': 'Min-heap operations for eviction',
            'Query_Details': 'Hash table lookup'
        }
    ]

    return pd.DataFrame(data)


def operation_breakdown_table() -> pd.DataFrame:
    """
    Generate detailed operation cost breakdown.

    Returns:
    --------
    DataFrame : Operation costs for each algorithm
    """
    data = [
        {
            'Algorithm': 'Exact Counter',
            'Operation': 'Insert (new item)',
            'Cost': 'O(1)',
            'Description': 'Hash table insert'
        },
        {
            'Algorithm': 'Exact Counter',
            'Operation': 'Insert (existing item)',
            'Cost': 'O(1)',
            'Description': 'Hash table lookup + increment'
        },
        {
            'Algorithm': 'Exact Counter',
            'Operation': 'Query count',
            'Cost': 'O(1)',
            'Description': 'Hash table lookup'
        },
        {
            'Algorithm': 'Exact Counter',
            'Operation': 'Get top-k',
            'Cost': 'O(d log d)',
            'Description': 'Sort all d items'
        },
        {
            'Algorithm': 'Fixed Probability',
            'Operation': 'Insert',
            'Cost': 'O(1)',
            'Description': 'RNG + conditional increment'
        },
        {
            'Algorithm': 'Fixed Probability',
            'Operation': 'Query count',
            'Cost': 'O(1)',
            'Description': 'Return counter * 1/p'
        },
        {
            'Algorithm': 'Space-Saving',
            'Operation': 'Insert (monitored item)',
            'Cost': 'O(log k)',
            'Description': 'Hash lookup + heap update'
        },
        {
            'Algorithm': 'Space-Saving',
            'Operation': 'Insert (new item, space available)',
            'Cost': 'O(log k)',
            'Description': 'Hash insert + heap insert'
        },
        {
            'Algorithm': 'Space-Saving',
            'Operation': 'Insert (new item, eviction)',
            'Cost': 'O(log k)',
            'Description': 'Heap extract-min + heap insert'
        },
        {
            'Algorithm': 'Space-Saving',
            'Operation': 'Query count',
            'Cost': 'O(1)',
            'Description': 'Hash table lookup'
        },
        {
            'Algorithm': 'Space-Saving',
            'Operation': 'Get top-n (n≤k)',
            'Cost': 'O(k log k)',
            'Description': 'Sort monitored items'
        }
    ]

    return pd.DataFrame(data)


def profile_function(func: Callable, *args, **kwargs) -> Tuple[any, Dict]:
    """
    Profile a function and return results with statistics.

    Parameters:
    -----------
    func : callable
        Function to profile
    *args, **kwargs
        Arguments to pass to function

    Returns:
    --------
    tuple : (function_result, profiling_stats_dict)
    """
    profiler = cProfile.Profile()

    # Run with profiling
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()

    # Get statistics
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(20)  # Top 20 functions

    # Parse into structured format
    profile_text = s.getvalue()

    stats_dict = {
        'profile_text': profile_text,
        'total_calls': ps.total_calls,
        'primitive_calls': ps.prim_calls,
        'total_time': ps.total_tt
    }

    return result, stats_dict


def extract_hotspots(profile_stats: Dict, top_n: int = 10) -> pd.DataFrame:
    """
    Extract computational hotspots from profiling results.

    Parameters:
    -----------
    profile_stats : dict
        Profiling statistics from profile_function
    top_n : int
        Number of top functions to extract

    Returns:
    --------
    DataFrame : Top hotspots by cumulative time
    """
    # Parse profile text (simplified version)
    # In practice, you'd want more robust parsing
    lines = profile_stats['profile_text'].split('\n')

    # Find header line
    header_idx = -1
    for i, line in enumerate(lines):
        if 'ncalls' in line.lower() and 'tottime' in line.lower():
            header_idx = i
            break

    if header_idx == -1:
        return pd.DataFrame()

    # Parse data lines
    data = []
    for line in lines[header_idx+1:header_idx+1+top_n]:
        line = line.strip()
        if not line:
            continue

        parts = line.split(None, 5)
        if len(parts) >= 6:
            data.append({
                'ncalls': parts[0],
                'tottime': parts[1],
                'percall_tot': parts[2],
                'cumtime': parts[3],
                'percall_cum': parts[4],
                'function': parts[5]
            })

    return pd.DataFrame(data)


def compare_complexity_predictions(empirical_results: pd.DataFrame,
                                  algorithm: str,
                                  size_column: str = 'stream_size',
                                  time_column: str = 'execution_time_ms') -> Dict:
    """
    Compare empirical results against theoretical complexity predictions.

    Parameters:
    -----------
    empirical_results : DataFrame
        Results from scalability tests
    algorithm : str
        Algorithm name
    size_column : str
        Column name containing size values
    time_column : str
        Column name containing time values

    Returns:
    --------
    dict : Comparison results
    """
    # Filter for specific algorithm
    data = empirical_results[empirical_results['algorithm'] == algorithm].copy()

    if len(data) == 0:
        return {'error': f'No data found for algorithm: {algorithm}'}

    sizes = data[size_column].values
    times = data[time_column].values

    # Determine expected complexity
    if 'Space-Saving' in algorithm:
        expected = 'linear'  # O(n) for stream processing
    elif 'Fixed Prob' in algorithm:
        expected = 'linear'  # O(n) for stream processing
    elif 'Exact' in algorithm:
        expected = 'linear'  # O(n) for stream processing
    else:
        expected = 'linear'

    validation = validate_time_complexity(sizes, times, expected)

    return {
        'algorithm': algorithm,
        'validation': validation,
        'empirical_slope': validation['actual_slope'],
        'matches_theory': validation['matches_expected'],
        'r_squared': validation['r_squared']
    }


def generate_complexity_summary(scalability_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Generate comprehensive complexity validation summary.

    Parameters:
    -----------
    scalability_results : dict
        Dictionary of scalability test results

    Returns:
    --------
    DataFrame : Summary of complexity validation
    """
    summaries = []

    # Process each result set
    for test_name, df in scalability_results.items():
        if 'algorithm' not in df.columns:
            continue

        algorithms = df['algorithm'].unique()

        for algo in algorithms:
            algo_data = df[df['algorithm'] == algo]

            # Time complexity (if we have multiple sizes)
            if 'stream_size' in df.columns and len(algo_data) > 3:
                time_val = validate_time_complexity(
                    algo_data['stream_size'].values,
                    algo_data['execution_time_ms'].values,
                    expected_complexity='linear'
                )

                summaries.append({
                    'test': test_name,
                    'algorithm': algo,
                    'complexity_type': 'Time (stream size)',
                    'expected': 'O(n)',
                    'empirical_slope': time_val['actual_slope'],
                    'r_squared': time_val['r_squared'],
                    'matches': time_val['matches_expected']
                })

            # Space complexity (if we have cardinality data)
            if 'cardinality' in df.columns and len(algo_data) > 3:
                space_val = validate_space_complexity(
                    algo_data['cardinality'].values,
                    algo_data['peak_memory_kb'].values,
                    expected_complexity='linear' if 'Exact' in algo else 'constant'
                )

                expected_space = 'O(d)' if 'Exact' in algo else 'O(k)' if 'Space-Saving' in algo else 'O(1)'

                summaries.append({
                    'test': test_name,
                    'algorithm': algo,
                    'complexity_type': 'Space (cardinality)',
                    'expected': expected_space,
                    'empirical_slope': space_val['actual_slope'],
                    'r_squared': space_val['r_squared'],
                    'matches': space_val['matches_expected']
                })

    return pd.DataFrame(summaries)


def analyze_efficiency_ratios(comparison_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate efficiency ratios between algorithms.

    Parameters:
    -----------
    comparison_df : DataFrame
        Comparison table with multiple algorithms

    Returns:
    --------
    DataFrame : Efficiency ratio analysis
    """
    if 'algorithm' not in comparison_df.columns:
        return pd.DataFrame()

    # Use Exact Counter as baseline
    baseline = comparison_df[comparison_df['algorithm'].str.contains('Exact', case=False)]

    if len(baseline) == 0:
        return pd.DataFrame()

    baseline = baseline.iloc[0]

    ratios = []

    for _, row in comparison_df.iterrows():
        if row['algorithm'] == baseline['algorithm']:
            continue

        ratios.append({
            'algorithm': row['algorithm'],
            'memory_ratio': row.get('peak_memory_kb', 0) / baseline.get('peak_memory_kb', 1),
            'time_ratio': row.get('execution_time_ms', 0) / baseline.get('execution_time_ms', 1),
            'error_vs_memory_tradeoff': row.get('Mean_Rel_Error_%', 0) / (row.get('peak_memory_kb', 1) / baseline.get('peak_memory_kb', 1))
        })

    return pd.DataFrame(ratios)


def limitations_analysis() -> pd.DataFrame:
    """
    Generate comprehensive limitations table for all algorithms.

    Returns:
    --------
    DataFrame : Limitations analysis
    """
    data = [
        {
            'Algorithm': 'Exact Counter',
            'Primary_Limitation': 'Memory scales with cardinality',
            'Failure_Mode': 'Memory exhaustion with high-cardinality streams',
            'Breaking_Point': 'd > 10⁶ items (millions of unique values)',
            'Not_Suitable_For': 'High-cardinality unbounded streams (IP addresses, user IDs)',
            'Theoretical_Guarantee': 'Perfect accuracy (no error)',
            'Practical_Constraint': 'Requires knowing/bounding cardinality in advance'
        },
        {
            'Algorithm': 'Fixed Probability Counter',
            'Primary_Limitation': 'Requires multiple trials for confidence intervals',
            'Failure_Mode': 'High variance for low-frequency items',
            'Breaking_Point': 'Items with count < 10 (rel. error > 30%)',
            'Not_Suitable_For': 'Single-pass requirements, need for deterministic bounds',
            'Theoretical_Guarantee': 'Unbiased estimate, Var = (1-p)/p * n',
            'Practical_Constraint': 'Must run 100+ trials for robust statistics'
        },
        {
            'Algorithm': 'Space-Saving',
            'Primary_Limitation': 'Requires k ≥ unique items for perfect accuracy',
            'Failure_Mode': 'Severe overestimation when k << d',
            'Breaking_Point': 'k < 0.5*d (>100% errors common)',
            'Not_Suitable_For': 'Unknown cardinality, need for counts of rare items',
            'Theoretical_Guarantee': 'Error ≤ N/k (overestimation only)',
            'Practical_Constraint': 'Must choose k based on expected cardinality'
        }
    ]

    return pd.DataFrame(data)


def generate_decision_tree_data() -> Dict:
    """
    Generate data for algorithm selection decision tree.

    Returns:
    --------
    dict : Decision tree structure
    """
    return {
        'root': {
            'question': 'Memory constrained?',
            'yes': {
                'question': 'Cardinality known?',
                'yes': {
                    'question': 'Can set k ≥ cardinality?',
                    'yes': 'Space-Saving (deterministic bounds)',
                    'no': 'Fixed Probability (probabilistic)'
                },
                'no': 'Fixed Probability (adaptive)'
            },
            'no': {
                'question': 'Need perfect accuracy?',
                'yes': 'Exact Counter',
                'no': {
                    'question': 'Need deterministic bounds?',
                    'yes': 'Space-Saving',
                    'no': 'Fixed Probability'
                }
            }
        }
    }


if __name__ == '__main__':
    # Generate reference tables
    print("Theoretical Complexity Table:")
    print(theoretical_complexity_table())

    print("\n\nOperation Breakdown:")
    print(operation_breakdown_table())

    print("\n\nLimitations Analysis:")
    print(limitations_analysis())
