"""
Exact Counter Experiment Runner.

This module provides functions to run the ExactCounter algorithm on the
Porto weather dataset, measuring performance metrics and saving results.
Can be imported by notebooks or executed from command line.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
import time
import tracemalloc
from pathlib import Path
from typing import Dict, Any, Optional

from algorithms.exact_counter import ExactCounter
from utils.data_loader import load_porto_temperatures
from utils.config import RESULTS_EXACT_PATH


def run_exact_experiment(
    data_path: Optional[str] = None,
    save_results: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run ExactCounter experiment on Porto temperature data.

    Processes the complete temperature stream using ExactCounter,
    measuring execution time and memory usage. Optionally saves
    results to the results/exact/ directory.

    Parameters
    ----------
    data_path : str, optional
        Path to porto.csv file. If None, uses default from config.
    save_results : bool, default=True
        Whether to save results to files
    verbose : bool, default=True
        Whether to print progress information

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - 'counter': ExactCounter instance with final state
        - 'counts_dict': Dictionary of temperature -> count
        - 'statistics': Summary statistics dictionary
        - 'performance': Performance metrics (time, memory)
        - 'top_10': List of top 10 temperatures with counts

    Examples
    --------
    >>> # Use in notebook
    >>> from src.experiments.run_exact import run_exact_experiment
    >>> results = run_exact_experiment(save_results=False)
    >>> print(f"Unique temps: {results['statistics']['unique_values']}")

    >>> # Run from command line
    >>> # python -m src.experiments.run_exact
    """
    if verbose:
        print("=" * 70)
        print("EXACT COUNTER EXPERIMENT")
        print("=" * 70)
        print()

    # Load temperature data
    if verbose:
        print("Loading temperature data...")

    temperatures = load_porto_temperatures(verbose=verbose)

    if verbose:
        print()
        print("Running ExactCounter algorithm...")
        print("-" * 70)

    # Initialize counter
    counter = ExactCounter()

    # Start performance measurement
    tracemalloc.start()
    start_time = time.perf_counter()

    # Process stream
    counter.process_stream(temperatures)

    # End performance measurement
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calculate metrics
    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak_mem / 1024

    if verbose:
        print(f"✓ Processing complete")
        print()
        print("Performance Metrics:")
        print(f"  • Execution time: {execution_time_ms:.2f} ms")
        print(f"  • Peak memory: {peak_memory_kb:.2f} KB")
        print()

    # Get results
    counts_dict = counter.get_all_counts()
    top_10 = counter.get_top_k(10)

    # Build statistics dictionary
    total_obs = sum(counts_dict.values())
    unique_values = len(counts_dict)

    statistics = {
        'total_observations': total_obs,
        'unique_values': unique_values,
        'min_count': min(counts_dict.values()) if counts_dict else 0,
        'max_count': max(counts_dict.values()) if counts_dict else 0,
        'top_10': [
            {'temperature': temp, 'count': count}
            for temp, count in top_10
        ],
        'cumulative_coverage': {}
    }

    # Calculate cumulative coverage
    for n in [5, 10, 15, 20]:
        top_n = counter.get_top_k(n)
        top_n_sum = sum(count for _, count in top_n)
        coverage_pct = (top_n_sum / total_obs * 100) if total_obs > 0 else 0
        statistics['cumulative_coverage'][f'top_{n}'] = round(coverage_pct, 2)

    # Performance metrics
    performance = {
        'execution_time_ms': round(execution_time_ms, 4),
        'peak_memory_kb': round(peak_memory_kb, 2),
        'total_observations': total_obs,
        'unique_values': unique_values
    }

    if verbose:
        print("Results Summary:")
        print(f"  • Total observations: {total_obs}")
        print(f"  • Unique temperatures: {unique_values}")
        print(f"  • Most frequent: {top_10[0][0]}°C ({top_10[0][1]} occurrences)")
        print()

    # Save results if requested
    if save_results:
        if verbose:
            print("Saving results...")

        # Ensure output directory exists
        output_dir = Path(RESULTS_EXACT_PATH)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save full counts to CSV
        csv_path = output_dir / 'exact_counts_full_dataset.csv'
        counter.save_to_csv(str(csv_path))
        if verbose:
            print(f"  ✓ Saved counts to {csv_path}")

        # Save statistics to JSON
        stats_path = output_dir / 'exact_statistics.json'
        with open(stats_path, 'w') as f:
            json.dump(statistics, f, indent=2)
        if verbose:
            print(f"  ✓ Saved statistics to {stats_path}")

        # Save performance metrics
        perf_path = output_dir / 'exact_performance.json'
        with open(perf_path, 'w') as f:
            json.dump(performance, f, indent=2)
        if verbose:
            print(f"  ✓ Saved performance to {perf_path}")

    if verbose:
        print()
        print("=" * 70)
        print("✓ EXACT COUNTER EXPERIMENT COMPLETE")
        print("=" * 70)

    # Return all results
    return {
        'counter': counter,
        'counts_dict': counts_dict,
        'statistics': statistics,
        'performance': performance,
        'top_10': top_10
    }


if __name__ == "__main__":
    """
    Command-line interface for running the exact counter experiment.

    Usage:
        python -m src.experiments.run_exact
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Run ExactCounter experiment on Porto weather data"
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save results to files'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output messages'
    )

    args = parser.parse_args()

    # Run experiment
    results = run_exact_experiment(
        save_results=not args.no_save,
        verbose=not args.quiet
    )

    # Print summary if not quiet
    if not args.quiet:
        print()
        print("Experiment completed successfully!")
        print(f"Processed {results['statistics']['total_observations']} observations")
        print(f"Found {results['statistics']['unique_values']} unique temperatures")
