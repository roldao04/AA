"""
Space-Saving Algorithm Experiment Runner.

This module provides functions to run the Space-Saving algorithm on the
Porto weather dataset with multiple k values, computing precision, recall,
and error metrics. Can be imported by notebooks or executed from command line.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
import time
import tracemalloc
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd

from scipy import stats

from algorithms.space_saving import SpaceSaving
from analysis.space_saving_metrics import (
    calculate_precision_recall,
    validate_error_bounds
)
from utils.data_loader import load_porto_temperatures
from utils.config import (
    RESULTS_SPACE_SAVING_PATH,
    RESULTS_EXACT_PATH,
    SPACE_SAVING_K_VALUES,
    TOP_N_VALUES
)


def run_space_saving_experiment(
    data_path: Optional[str] = None,
    k_values: Optional[List[int]] = None,
    save_results: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run Space-Saving algorithm experiment with multiple k values.

    For each k value, runs Space-Saving on the full temperature stream,
    computes precision/recall for different top-n queries, validates
    theoretical error guarantees, and measures performance.

    Parameters
    ----------
    data_path : str, optional
        Path to porto.csv file. If None, uses default from config.
    k_values : List[int], optional
        List of k values to test. If None, uses SPACE_SAVING_K_VALUES from config.
    save_results : bool, default=True
        Whether to save results to files
    verbose : bool, default=True
        Whether to print progress information

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - 'results_by_k': Dict mapping k -> results for that k value
        - 'k_comparison': DataFrame comparing all k values
        - 'precision_recall': DataFrame with precision/recall for all k and n
        - 'error_validation': Dict with theoretical guarantee validation
        - 'performance': Performance metrics for all k values

    Examples
    --------
    >>> # Use in notebook
    >>> from src.experiments.run_space_saving import run_space_saving_experiment
    >>> results = run_space_saving_experiment(k_values=[10, 20], save_results=False)
    >>> print(results['k_comparison'])

    >>> # Run from command line
    >>> # python -m src.experiments.run_space_saving --k 10 20 30
    """
    if k_values is None:
        k_values = SPACE_SAVING_K_VALUES

    if verbose:
        print("=" * 70)
        print("SPACE-SAVING ALGORITHM EXPERIMENT")
        print("=" * 70)
        print()
        print(f"Testing k values: {k_values}")
        print(f"Top-n queries: {TOP_N_VALUES}")
        print()

    # Load temperature data
    if verbose:
        print("Loading temperature data...")

    temperatures = load_porto_temperatures(verbose=verbose)

    # Load exact counts for comparison
    exact_counts_path = Path(RESULTS_EXACT_PATH) / 'exact_counts_full_dataset.csv'

    if not exact_counts_path.exists():
        if verbose:
            print()
            print("WARNING: Exact counts not found. Running exact counter first...")
        from src.experiments.run_exact import run_exact_experiment
        exact_results = run_exact_experiment(verbose=False, save_results=True)
        exact_counts = exact_results['counts_dict']
    else:
        exact_df = pd.read_csv(exact_counts_path)
        exact_counts = dict(zip(exact_df['temperature'], exact_df['count']))

    # Get exact top-k for comparison
    exact_sorted = sorted(exact_counts.items(), key=lambda x: (-x[1], x[0]))

    if verbose:
        print()
        print("Running Space-Saving for each k value...")
        print("-" * 70)

    results_by_k = {}
    k_comparison_data = []
    precision_recall_data = []
    performance_data = []

    for k in k_values:
        if verbose:
            print(f"\nTesting k={k}...")

        # Create Space-Saving instance
        ss = SpaceSaving(k=k)

        # Measure performance
        tracemalloc.start()
        start_time = time.perf_counter()

        # Process stream
        ss.process_stream(temperatures)

        # End measurement
        end_time = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time_ms = (end_time - start_time) * 1000
        peak_memory_kb = peak_mem / 1024

        # Get all monitored items
        monitored_items = ss.get_monitored_items()

        # Calculate error validation
        error_validation_df = validate_error_bounds(
            monitored=monitored_items,
            exact_counts=exact_counts,
            stream_length=ss.stream_length,
            k=k
        )

        # Extract summary stats from validation
        max_error = error_validation_df['true_error'].max()
        theoretical_max_error = error_validation_df['max_error_theoretical'].iloc[0] if len(error_validation_df) > 0 else ss.stream_length / k
        all_guarantees_hold = error_validation_df['bound_holds'].all()

        error_validation = {
            'max_error': int(max_error) if pd.notna(max_error) else 0,
            'theoretical_max_error': int(theoretical_max_error),
            'all_guarantees_hold': bool(all_guarantees_hold)
        }

        # Calculate precision/recall for different n values
        pr_results = []
        for n in TOP_N_VALUES:
            if n <= k:  # Only query for n <= k
                pr = calculate_precision_recall(
                    ss_top_n=ss.get_top_n(n),
                    exact_counts=exact_counts,
                    n=n
                )
                pr['k'] = k
                pr['n'] = n
                # Remove sets from results for clean storage
                pr_clean = {key: val for key, val in pr.items() if key not in ['ss_set', 'true_set']}
                pr_results.append(pr_clean)
                precision_recall_data.append(pr_clean)

        # Calculate ranking correlation with exact top-k
        ss_top_k = ss.get_top_n(min(k, len(monitored_items)))
        exact_top_k = exact_sorted[:min(k, len(exact_sorted))]

        # Build ranking lists for correlation
        if len(ss_top_k) > 1 and len(exact_top_k) > 1:
            # Get common items
            ss_temps = [temp for temp, _ in ss_top_k]
            exact_temps = [temp for temp, _ in exact_top_k]
            common_temps = set(ss_temps) & set(exact_temps)

            if len(common_temps) > 1:
                # Create rank mappings
                ss_ranks = {temp: rank for rank, (temp, _) in enumerate(ss_top_k)}
                exact_ranks = {temp: rank for rank, (temp, _) in enumerate(exact_top_k)}

                # Extract ranks for common items
                common_temps_list = sorted(common_temps)
                ss_rank_list = [ss_ranks[temp] for temp in common_temps_list]
                exact_rank_list = [exact_ranks[temp] for temp in common_temps_list]

                # Calculate correlations
                kendall_tau, kendall_p = stats.kendalltau(exact_rank_list, ss_rank_list)
                spearman_rho, spearman_p = stats.spearmanr(exact_rank_list, ss_rank_list)

                ranking_metrics = {
                    'kendall_tau': float(kendall_tau),
                    'kendall_p': float(kendall_p),
                    'spearman_rho': float(spearman_rho),
                    'spearman_p': float(spearman_p),
                    'num_common_items': len(common_temps)
                }
            else:
                ranking_metrics = {'error': 'Not enough common items for correlation'}
        else:
            ranking_metrics = {'error': 'Not enough items for correlation'}

        # Store results for this k
        results_by_k[k] = {
            'algorithm': ss,
            'monitored_items': monitored_items,
            'num_monitored': len(monitored_items),
            'stream_length': ss.stream_length,
            'execution_time_ms': execution_time_ms,
            'peak_memory_kb': peak_memory_kb,
            'error_validation': error_validation,
            'precision_recall': pr_results,
            'ranking_metrics': ranking_metrics
        }

        # Add to comparison data
        k_comparison_data.append({
            'k': k,
            'num_monitored': len(monitored_items),
            'execution_time_ms': round(execution_time_ms, 4),
            'peak_memory_kb': round(peak_memory_kb, 2),
            'max_error_observed': error_validation['max_error'],
            'max_error_bound': error_validation['theoretical_max_error'],
            'all_guarantees_hold': error_validation['all_guarantees_hold'],
            'kendall_tau': ranking_metrics.get('kendall_tau', None),
            'spearman_rho': ranking_metrics.get('spearman_rho', None)
        })

        performance_data.append({
            'k': k,
            'execution_time_ms': execution_time_ms,
            'peak_memory_kb': peak_memory_kb
        })

        if verbose:
            print(f"  ✓ Monitored {len(monitored_items)} items")
            print(f"  ✓ Execution: {execution_time_ms:.2f} ms")
            print(f"  ✓ Memory: {peak_memory_kb:.2f} KB")
            print(f"  ✓ Max error: {error_validation['max_error']} (bound: {error_validation['theoretical_max_error']})")
            print(f"  ✓ Guarantees hold: {error_validation['all_guarantees_hold']}")

    # Create comparison DataFrames
    k_comparison_df = pd.DataFrame(k_comparison_data)
    precision_recall_df = pd.DataFrame(precision_recall_data)

    if verbose:
        print()
        print("=" * 70)
        print("Summary:")
        print("-" * 70)
        print(k_comparison_df.to_string(index=False))
        print()

    # Save results if requested
    if save_results:
        if verbose:
            print("Saving results...")

        # Ensure output directory exists
        output_dir = Path(RESULTS_SPACE_SAVING_PATH)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save individual k results
        for k, results in results_by_k.items():
            k_result_data = {
                'k': k,
                'num_monitored': results['num_monitored'],
                'stream_length': results['stream_length'],
                'monitored_items': [
                    {
                        'temperature': int(temp),
                        'count': int(count),
                        'error': int(error)
                    }
                    for temp, (count, error) in results['monitored_items'].items()
                ],
                'error_validation': {
                    'max_error': int(results['error_validation']['max_error']),
                    'theoretical_max_error': int(results['error_validation']['theoretical_max_error']),
                    'all_guarantees_hold': bool(results['error_validation']['all_guarantees_hold'])
                },
                'performance': {
                    'execution_time_ms': float(results['execution_time_ms']),
                    'peak_memory_kb': float(results['peak_memory_kb'])
                }
            }

            k_path = output_dir / f'ss_results_k{k}.json'
            with open(k_path, 'w') as f:
                json.dump(k_result_data, f, indent=2)

        if verbose:
            print(f"  ✓ Saved individual k results")

        # Save k comparison
        k_comp_path = output_dir / 'k_comparison.csv'
        k_comparison_df.to_csv(k_comp_path, index=False)
        if verbose:
            print(f"  ✓ Saved k comparison to {k_comp_path}")

        # Save precision/recall
        pr_path = output_dir / 'precision_recall_analysis.csv'
        precision_recall_df.to_csv(pr_path, index=False)
        if verbose:
            print(f"  ✓ Saved precision/recall to {pr_path}")

        # Save error validation summary
        error_val_summary = {
            'all_k_guarantees_hold': all(
                results['error_validation']['all_guarantees_hold']
                for results in results_by_k.values()
            ),
            'by_k': {
                k: {
                    'max_error': int(results['error_validation']['max_error']),
                    'theoretical_bound': int(results['error_validation']['theoretical_max_error']),
                    'guarantees_hold': bool(results['error_validation']['all_guarantees_hold'])
                }
                for k, results in results_by_k.items()
            }
        }

        error_val_path = output_dir / 'error_validation.json'
        with open(error_val_path, 'w') as f:
            json.dump(error_val_summary, f, indent=2)
        if verbose:
            print(f"  ✓ Saved error validation to {error_val_path}")

        # Save performance metrics
        perf_summary = {
            'by_k': {
                k: {
                    'execution_time_ms': float(results['execution_time_ms']),
                    'peak_memory_kb': float(results['peak_memory_kb'])
                }
                for k, results in results_by_k.items()
            }
        }

        perf_path = output_dir / 'performance_metrics.json'
        with open(perf_path, 'w') as f:
            json.dump(perf_summary, f, indent=2)
        if verbose:
            print(f"  ✓ Saved performance to {perf_path}")

    if verbose:
        print()
        print("=" * 70)
        print("✓ SPACE-SAVING EXPERIMENT COMPLETE")
        print("=" * 70)

    return {
        'results_by_k': results_by_k,
        'k_comparison': k_comparison_df,
        'precision_recall': precision_recall_df,
        'error_validation': error_val_summary if save_results else None,
        'performance': performance_data
    }


if __name__ == "__main__":
    """
    Command-line interface for running the Space-Saving experiment.

    Usage:
        python -m src.experiments.run_space_saving
        python -m src.experiments.run_space_saving --k 10 20 30
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Space-Saving algorithm experiment with multiple k values"
    )
    parser.add_argument(
        '--k',
        nargs='+',
        type=int,
        default=None,
        help=f'Space budget values to test (default: {SPACE_SAVING_K_VALUES})'
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
    results = run_space_saving_experiment(
        k_values=args.k,
        save_results=not args.no_save,
        verbose=not args.quiet
    )

    # Print summary if not quiet
    if not args.quiet:
        print()
        print("Experiment completed successfully!")
        print(f"Tested k values: {list(results['results_by_k'].keys())}")
