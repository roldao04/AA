"""
Space-Saving Analysis Functions.

This module provides specialized analysis functions for evaluating Space-Saving
algorithm performance including precision/recall calculation, error bound
validation, and guarantee verification.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Set


def calculate_precision_recall(
    ss_top_n: List[Tuple[int, Tuple[int, int]]],
    exact_counts: Dict[int, int],
    n: int
) -> Dict[str, float]:
    """
    Calculate precision and recall for top-n query results.

    Precision: What fraction of reported items are truly in top-n?
    Recall: What fraction of true top-n items did we capture?

    Parameters
    ----------
    ss_top_n : List[Tuple[int, Tuple[int, int]]]
        Space-Saving top-n results: [(temp, (count, error)), ...]
    exact_counts : Dict[int, int]
        Ground truth exact counts
    n : int
        Number of top items

    Returns
    -------
    Dict[str, float]
        Dictionary with keys:
        - precision: TP / (TP + FP)
        - recall: TP / (TP + FN)
        - f1_score: Harmonic mean of precision and recall
        - intersection_size: Number of items in both sets

    Examples
    --------
    >>> ss_results = [(12, (100, 0)), (15, (80, 1)), (18, (60, 2))]
    >>> exact = {12: 100, 15: 78, 18: 60, 20: 50}
    >>> metrics = calculate_precision_recall(ss_results, exact, n=3)
    >>> metrics['precision']
    1.0
    """
    # Extract temperatures from Space-Saving results
    ss_temps = {temp for temp, _ in ss_top_n}

    # Get true top-n from exact counts
    true_top_n = set(
        sorted(exact_counts.keys(), key=lambda t: exact_counts[t], reverse=True)[:n]
    )

    # Calculate intersection (true positives)
    intersection = ss_temps & true_top_n
    tp = len(intersection)

    # Calculate metrics
    precision = tp / n if n > 0 else 0.0
    recall = tp / n if n > 0 else 0.0  # n is the same for both
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'intersection_size': tp,
        'ss_set': ss_temps,
        'true_set': true_top_n
    }


def validate_error_bounds(
    monitored: Dict[int, Tuple[int, int]],
    exact_counts: Dict[int, int],
    stream_length: int,
    k: int
) -> pd.DataFrame:
    """
    Validate Space-Saving error bounds against exact counts.

    Checks:
    1. True error ≤ recorded error for each item
    2. Maximum error ≤ N/k (theoretical bound)

    Parameters
    ----------
    monitored : Dict[int, Tuple[int, int]]
        Space-Saving monitored items: {temp: (count, error)}
    exact_counts : Dict[int, int]
        Ground truth exact counts
    stream_length : int
        Total number of items processed
    k : int
        Space budget parameter

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - temperature: Temperature value
        - ss_count: Space-Saving estimated count
        - ss_error: Space-Saving error bound
        - true_count: Exact count
        - true_error: Actual overestimation
        - bound_holds: True if true_error ≤ ss_error
        - max_error_theoretical: N/k

    Examples
    --------
    >>> monitored = {12: (105, 5), 15: (82, 2)}
    >>> exact = {12: 100, 15: 80}
    >>> df = validate_error_bounds(monitored, exact, 1000, 10)
    >>> df['bound_holds'].all()
    True
    """
    max_error_theoretical = stream_length / k

    data = []
    for temp, (ss_count, ss_error) in monitored.items():
        true_count = exact_counts.get(temp, 0)
        true_error = ss_count - true_count

        data.append({
            'temperature': temp,
            'ss_count': ss_count,
            'ss_error': ss_error,
            'true_count': true_count,
            'true_error': true_error,
            'bound_holds': true_error <= ss_error,
            'max_error_theoretical': max_error_theoretical
        })

    df = pd.DataFrame(data)
    df = df.sort_values('true_count', ascending=False).reset_index(drop=True)

    return df


def calculate_coverage(
    monitored: Dict[int, Tuple[int, int]],
    exact_counts: Dict[int, int]
) -> Dict[str, float]:
    """
    Calculate what percentage of the stream is covered by monitored items.

    Parameters
    ----------
    monitored : Dict[int, Tuple[int, int]]
        Space-Saving monitored items: {temp: (count, error)}
    exact_counts : Dict[int, int]
        Ground truth exact counts

    Returns
    -------
    Dict[str, float]
        Dictionary with coverage statistics:
        - coverage_percentage: % of observations from monitored items
        - monitored_items: Number of unique items monitored
        - total_unique_items: Total unique items in dataset
        - coverage_ratio: monitored_items / total_unique_items

    Examples
    --------
    >>> monitored = {12: (100, 0), 15: (80, 0)}
    >>> exact = {12: 100, 15: 80, 18: 20, 20: 10}
    >>> cov = calculate_coverage(monitored, exact)
    >>> cov['coverage_percentage']
    85.71...
    """
    total_observations = sum(exact_counts.values())
    monitored_temps = set(monitored.keys())

    # Sum observations from monitored items
    covered_observations = sum(
        exact_counts.get(temp, 0) for temp in monitored_temps
    )

    coverage_pct = 100 * covered_observations / total_observations if total_observations > 0 else 0.0
    coverage_ratio = len(monitored_temps) / len(exact_counts) if len(exact_counts) > 0 else 0.0

    return {
        'coverage_percentage': coverage_pct,
        'monitored_items': len(monitored_temps),
        'total_unique_items': len(exact_counts),
        'coverage_ratio': coverage_ratio,
        'covered_observations': covered_observations,
        'total_observations': total_observations
    }


def analyze_bound_tightness(
    monitored: Dict[int, Tuple[int, int]],
    exact_counts: Dict[int, int]
) -> pd.DataFrame:
    """
    Analyze how tight the error bounds are compared to actual errors.

    A tight bound means recorded_error ≈ true_error.
    A loose bound means recorded_error >> true_error.

    Parameters
    ----------
    monitored : Dict[int, Tuple[int, int]]
        Space-Saving monitored items: {temp: (count, error)}
    exact_counts : Dict[int, int]
        Ground truth exact counts

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - temperature: Temperature value
        - ss_count: Space-Saving count
        - ss_error: Space-Saving error bound
        - true_count: Exact count
        - true_error: Actual overestimation
        - slack: ss_error - true_error (how much room in the bound)
        - tightness_ratio: true_error / ss_error (1.0 = perfect, 0.0 = very loose)

    Examples
    --------
    >>> monitored = {12: (105, 5), 15: (82, 10)}
    >>> exact = {12: 100, 15: 80}
    >>> df = analyze_bound_tightness(monitored, exact)
    >>> 'tightness_ratio' in df.columns
    True
    """
    data = []
    for temp, (ss_count, ss_error) in monitored.items():
        true_count = exact_counts.get(temp, 0)
        true_error = ss_count - true_count
        slack = ss_error - true_error
        tightness = true_error / ss_error if ss_error > 0 else 1.0

        data.append({
            'temperature': temp,
            'ss_count': ss_count,
            'ss_error': ss_error,
            'true_count': true_count,
            'true_error': true_error,
            'slack': slack,
            'tightness_ratio': tightness
        })

    df = pd.DataFrame(data)
    df = df.sort_values('true_count', ascending=False).reset_index(drop=True)

    return df


def compare_k_values(
    results_dict: Dict[int, Dict]
) -> pd.DataFrame:
    """
    Compare Space-Saving performance across different k values.

    Parameters
    ----------
    results_dict : Dict[int, Dict]
        Dictionary mapping k -> results dict with keys:
        - monitored: Dict[int, Tuple[int, int]]
        - stream_length: int
        - exact_counts: Dict[int, int]

    Returns
    -------
    pd.DataFrame
        DataFrame comparing all k values with columns:
        - k: Space budget
        - num_monitored: Number of items monitored
        - max_error_theoretical: N/k
        - max_error_actual: Actual maximum error bound
        - coverage_pct: Percentage of stream covered
        - mean_true_error: Mean actual overestimation
        - mean_relative_error: Mean relative error

    Examples
    --------
    >>> results = {
    ...     10: {'monitored': {12: (100, 5)}, 'stream_length': 1000,
    ...          'exact_counts': {12: 95}},
    ...     20: {'monitored': {12: (98, 2)}, 'stream_length': 1000,
    ...          'exact_counts': {12: 95}}
    ... }
    >>> df = compare_k_values(results)
    >>> 'k' in df.columns
    True
    """
    comparison_data = []

    for k, results in sorted(results_dict.items()):
        monitored = results['monitored']
        stream_length = results['stream_length']
        exact_counts = results['exact_counts']

        # Calculate metrics
        max_error_theoretical = stream_length / k
        max_error_actual = max((error for _, error in monitored.values()), default=0)

        coverage = calculate_coverage(monitored, exact_counts)

        # Calculate mean errors
        true_errors = []
        relative_errors = []
        for temp, (ss_count, _) in monitored.items():
            true_count = exact_counts.get(temp, 0)
            if true_count > 0:
                true_error = ss_count - true_count
                true_errors.append(true_error)
                relative_errors.append(abs(true_error) / true_count)

        mean_true_error = np.mean(true_errors) if true_errors else 0.0
        mean_relative_error = np.mean(relative_errors) if relative_errors else 0.0

        comparison_data.append({
            'k': k,
            'num_monitored': len(monitored),
            'max_error_theoretical': max_error_theoretical,
            'max_error_actual': max_error_actual,
            'coverage_pct': coverage['coverage_percentage'],
            'mean_true_error': mean_true_error,
            'mean_relative_error': mean_relative_error
        })

    return pd.DataFrame(comparison_data)


def check_capture_guarantee(
    monitored: Dict[int, Tuple[int, int]],
    exact_counts: Dict[int, int],
    stream_length: int,
    k: int
) -> Dict[str, any]:
    """
    Check Space-Saving guarantee: all items with freq > N/k are captured.

    Parameters
    ----------
    monitored : Dict[int, Tuple[int, int]]
        Space-Saving monitored items
    exact_counts : Dict[int, int]
        Ground truth exact counts
    stream_length : int
        Total stream length
    k : int
        Space budget

    Returns
    -------
    Dict[str, any]
        Results of guarantee check:
        - threshold: N/k
        - frequent_items: Set of items with freq > N/k
        - captured_items: Set of frequent items that were captured
        - missed_items: Set of frequent items that were missed
        - guarantee_holds: True if all frequent items captured
        - num_frequent: Count of frequent items
        - num_captured: Count captured
        - num_missed: Count missed

    Examples
    --------
    >>> monitored = {12: (100, 0), 15: (80, 0)}
    >>> exact = {12: 100, 15: 80, 18: 10}
    >>> result = check_capture_guarantee(monitored, exact, 200, 10)
    >>> result['guarantee_holds']
    True
    """
    threshold = stream_length / k

    # Find items exceeding threshold
    frequent_items = {
        temp for temp, count in exact_counts.items()
        if count > threshold
    }

    # Check which were captured
    monitored_temps = set(monitored.keys())
    captured_items = frequent_items & monitored_temps
    missed_items = frequent_items - monitored_temps

    guarantee_holds = len(missed_items) == 0

    return {
        'threshold': threshold,
        'frequent_items': frequent_items,
        'captured_items': captured_items,
        'missed_items': missed_items,
        'guarantee_holds': guarantee_holds,
        'num_frequent': len(frequent_items),
        'num_captured': len(captured_items),
        'num_missed': len(missed_items)
    }
