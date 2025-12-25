"""
Comprehensive Algorithm Comparison Experiment Runner.

This module provides functions to load results from all algorithms (ExactCounter,
FixedProbabilityCounter, and SpaceSaving) and generate comprehensive comparison
analyses. Can be imported by notebooks or executed from command line.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from analysis.comparison import (
    load_all_results,
    create_master_comparison_table,
    compare_memory_usage,
    compare_execution_time,
    calculate_ranking_correlation
)
from utils.config import (
    RESULTS_COMPARISON_PATH,
    RESULTS_EXACT_PATH,
    RESULTS_FIXED_PROB_PATH,
    RESULTS_SPACE_SAVING_PATH
)


def run_comparison_analysis(
    load_existing: bool = True,
    exact_path: Optional[str] = None,
    fixed_prob_path: Optional[str] = None,
    space_saving_path: Optional[str] = None,
    save_results: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run comprehensive comparison analysis across all algorithms.

    Loads results from ExactCounter, FixedProbabilityCounter, and SpaceSaving
    experiments, then generates comparison tables, performance metrics analysis,
    and ranking correlation studies.

    Parameters
    ----------
    load_existing : bool, default=True
        Whether to load existing results or run experiments first
    exact_path : str, optional
        Path to exact counter results directory
    fixed_prob_path : str, optional
        Path to fixed probability results directory
    space_saving_path : str, optional
        Path to space-saving results directory
    save_results : bool, default=True
        Whether to save comparison results to files
    verbose : bool, default=True
        Whether to print progress information

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - 'all_results': Raw loaded results from all algorithms
        - 'master_comparison': Master comparison table
        - 'performance_comparison': Performance metrics comparison
        - 'ranking_correlation': Ranking correlation analysis
        - 'time_comparison': Execution time comparison
        - 'memory_comparison': Memory usage comparison

    Examples
    --------
    >>> # Use in notebook
    >>> from src.experiments.run_comparison import run_comparison_analysis
    >>> results = run_comparison_analysis(save_results=False)
    >>> print(results['master_comparison'])

    >>> # Run from command line
    >>> # python -m src.experiments.run_comparison
    """
    if verbose:
        print("=" * 70)
        print("COMPREHENSIVE ALGORITHM COMPARISON")
        print("=" * 70)
        print()

    # Check if results exist, run experiments if needed
    if not load_existing:
        if verbose:
            print("Running all experiments...")
            print()

        from src.experiments.run_exact import run_exact_experiment
        from src.experiments.run_fixed_prob import run_fixed_prob_experiment
        from src.experiments.run_space_saving import run_space_saving_experiment

        # Run all experiments
        if verbose:
            print("1/3: Running ExactCounter...")
        run_exact_experiment(verbose=verbose)

        if verbose:
            print("\n2/3: Running FixedProbabilityCounter...")
        run_fixed_prob_experiment(verbose=verbose)

        if verbose:
            print("\n3/3: Running SpaceSaving...")
        run_space_saving_experiment(verbose=verbose)

        if verbose:
            print()
            print("=" * 70)
            print()

    # Load all results
    if verbose:
        print("Loading results from all algorithms...")

    all_results = load_all_results(
        exact_path=exact_path or RESULTS_EXACT_PATH,
        fixed_prob_path=fixed_prob_path or RESULTS_FIXED_PROB_PATH,
        space_saving_path=space_saving_path or RESULTS_SPACE_SAVING_PATH
    )

    if verbose:
        print(f"  ✓ Loaded ExactCounter results")
        print(f"  ✓ Loaded FixedProbabilityCounter results")
        print(f"  ✓ Loaded SpaceSaving results for all k values")
        print()

    # Create master comparison table
    if verbose:
        print("Creating master comparison table...")

    master_comparison = create_master_comparison_table(all_results)

    if verbose:
        print()
        print("Master Comparison Table:")
        print("-" * 70)
        print(master_comparison.to_string(index=False))
        print()

    # Compare performance metrics
    if verbose:
        print("Analyzing performance metrics...")

    time_comparison = compare_execution_time(all_results)
    memory_comparison = compare_memory_usage(all_results)

    performance_comparison = {
        'time_comparison': time_comparison,
        'memory_comparison': memory_comparison
    }

    if verbose and not time_comparison.empty:
        print()
        print("Execution Time Comparison:")
        print("-" * 70)
        print(time_comparison.to_string(index=False))
        print()

    if verbose and not memory_comparison.empty:
        print("Memory Usage Comparison:")
        print("-" * 70)
        print(memory_comparison.to_string(index=False))
        print()

    # Calculate ranking correlations
    if verbose:
        print("Computing ranking correlations...")

    ranking_correlation = calculate_ranking_correlation(all_results)

    if verbose and ranking_correlation is not None and not ranking_correlation.empty:
        print()
        print("Ranking Correlation Analysis:")
        print("-" * 70)
        print(ranking_correlation.to_string(index=False))
        print()

    # Save results if requested
    if save_results:
        if verbose:
            print("Saving comparison results...")

        # Ensure output directory exists
        output_dir = Path(RESULTS_COMPARISON_PATH)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save master comparison table
        master_path = output_dir / 'master_comparison_table.csv'
        master_comparison.to_csv(master_path, index=False)
        if verbose:
            print(f"  ✓ Saved master comparison to {master_path}")

        # Save time comparison
        if not time_comparison.empty:
            time_path = output_dir / 'time_comparison.csv'
            time_comparison.to_csv(time_path, index=False)
            if verbose:
                print(f"  ✓ Saved time comparison to {time_path}")

        # Save memory comparison
        if not memory_comparison.empty:
            memory_path = output_dir / 'memory_comparison.csv'
            memory_comparison.to_csv(memory_path, index=False)
            if verbose:
                print(f"  ✓ Saved memory comparison to {memory_path}")

        # Save ranking correlation
        if ranking_correlation is not None and not ranking_correlation.empty:
            ranking_path = output_dir / 'ranking_correlation_analysis.csv'
            ranking_correlation.to_csv(ranking_path, index=False)
            if verbose:
                print(f"  ✓ Saved ranking correlation to {ranking_path}")

        # Save summary statistics
        summary = {
            'num_algorithms_compared': len(master_comparison),
            'exact_total_obs': int(all_results['exact'].get('statistics', {}).get('total_observations', 0)),
            'exact_unique_values': int(all_results['exact'].get('statistics', {}).get('unique_values', 0)),
            'fixed_prob_is_unbiased': all_results['fixed_prob'].get('error_analysis', {}).get('unbiased_test', {}).get('is_unbiased', None),
            'space_saving_k_values_tested': list(all_results['space_saving'].keys()) if 'space_saving' in all_results else []
        }

        summary_path = output_dir / 'comparison_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        if verbose:
            print(f"  ✓ Saved summary to {summary_path}")

    if verbose:
        print()
        print("=" * 70)
        print("✓ COMPARISON ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print("Key Findings:")
        if not master_comparison.empty:
            best_memory = master_comparison.loc[master_comparison['peak_memory_kb'].idxmin(), 'algorithm']
            best_time = master_comparison.loc[master_comparison['execution_time_ms'].idxmin(), 'algorithm']
            print(f"  • Most memory efficient: {best_memory}")
            print(f"  • Fastest execution: {best_time}")
            print(f"  • Exact counter: {master_comparison.loc[master_comparison['algorithm'] == 'ExactCounter', 'unique_values'].values[0] if 'ExactCounter' in master_comparison['algorithm'].values else 'N/A'} unique values")

    return {
        'all_results': all_results,
        'master_comparison': master_comparison,
        'performance_comparison': performance_comparison,
        'ranking_correlation': ranking_correlation,
        'time_comparison': time_comparison,
        'memory_comparison': memory_comparison
    }


if __name__ == "__main__":
    """
    Command-line interface for running the comparison analysis.

    Usage:
        python -m src.experiments.run_comparison
        python -m src.experiments.run_comparison --run-experiments
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Run comprehensive algorithm comparison analysis"
    )
    parser.add_argument(
        '--run-experiments',
        action='store_true',
        help='Run all experiments before comparison (if results not found)'
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

    # Run comparison
    results = run_comparison_analysis(
        load_existing=not args.run_experiments,
        save_results=not args.no_save,
        verbose=not args.quiet
    )

    # Print summary if not quiet
    if not args.quiet:
        print()
        print("Comparison completed successfully!")
        print(f"Analyzed {len(results['master_comparison'])} algorithm configurations")
