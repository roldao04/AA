"""
Fixed Probability Counter Experiment Runner.

This module provides functions to run multiple trials of the Fixed Probability
Counter algorithm on the Porto weather dataset, computing statistical distributions
and error metrics. Can be imported by notebooks or executed from command line.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
import pickle
import time
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from experiments.fixed_prob_trials import (
    run_multiple_trials,
    aggregate_trial_results,
    calculate_error_metrics,
    calculate_theoretical_variance,
    test_unbiased_estimator
)
from utils.data_loader import load_porto_temperatures
from utils.config import (
    RESULTS_FIXED_PROB_PATH,
    RESULTS_EXACT_PATH,
    FIXED_PROB_P,
    NUM_TRIALS,
    RANDOM_SEED,
    CONFIDENCE_LEVEL
)


def run_fixed_prob_experiment(
    data_path: Optional[str] = None,
    p: float = FIXED_PROB_P,
    num_trials: int = NUM_TRIALS,
    base_seed: int = RANDOM_SEED,
    save_results: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run Fixed Probability Counter experiment with multiple trials.

    Runs num_trials independent trials of the Fixed Probability Counter,
    aggregates results, calculates error metrics, and performs statistical
    validation of theoretical properties.

    Parameters
    ----------
    data_path : str, optional
        Path to porto.csv file. If None, uses default from config.
    p : float, default=0.25
        Probability of incrementing
    num_trials : int, default=100
        Number of independent trials to run
    base_seed : int, default=113920
        Base random seed for reproducibility
    save_results : bool, default=True
        Whether to save results to files
    verbose : bool, default=True
        Whether to print progress information

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
        - 'trial_results': DataFrame with all trial results
        - 'aggregated': DataFrame with aggregated statistics per temperature
        - 'error_metrics': DataFrame with error analysis
        - 'theoretical': DataFrame with theoretical variance
        - 'unbiased_test': Dictionary with unbiasedness test results
        - 'performance': Performance metrics
        - 'parameters': Experiment parameters

    Examples
    --------
    >>> # Use in notebook
    >>> from src.experiments.run_fixed_prob import run_fixed_prob_experiment
    >>> results = run_fixed_prob_experiment(num_trials=50, save_results=False)
    >>> print(results['unbiased_test']['conclusion'])

    >>> # Run from command line
    >>> # python -m src.experiments.run_fixed_prob --trials 100
    """
    if verbose:
        print("=" * 70)
        print("FIXED PROBABILITY COUNTER EXPERIMENT")
        print("=" * 70)
        print()
        print(f"Parameters:")
        print(f"  • Probability p = {p}")
        print(f"  • Number of trials = {num_trials}")
        print(f"  • Base seed = {base_seed}")
        print(f"  • Confidence level = {CONFIDENCE_LEVEL}")
        print()

    # Load temperature data
    if verbose:
        print("Loading temperature data...")

    temperatures = load_porto_temperatures(verbose=verbose)

    # Load exact counts for error calculation
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

    if verbose:
        print()
        print("Running multiple trials...")
        print("-" * 70)

    # Track execution time
    start_time = time.perf_counter()

    # Run multiple trials using the trial manager
    trial_results = run_multiple_trials(
        temperatures=temperatures,
        p=p,
        num_trials=num_trials,
        base_seed=base_seed,
        verbose=verbose
    )

    end_time = time.perf_counter()
    total_time_s = end_time - start_time

    if verbose:
        print()
        print("Aggregating results...")

    # Aggregate trial results
    aggregated = aggregate_trial_results(
        trial_results,
        confidence_level=CONFIDENCE_LEVEL
    )

    # Calculate error metrics
    error_metrics = calculate_error_metrics(aggregated, exact_counts)

    # Calculate theoretical variance
    theoretical = calculate_theoretical_variance(exact_counts, p)

    # Test unbiasedness
    unbiased_test = test_unbiased_estimator(error_metrics)

    if verbose:
        print()
        print("Statistical Validation:")
        print("-" * 70)
        print(f"  {unbiased_test['conclusion']}")
        print()
        print("Error Summary:")
        print(f"  • Mean absolute error: {error_metrics['absolute_error'].mean():.2f}")
        print(f"  • Mean relative error: {error_metrics['relative_error'].mean():.4f}")
        print(f"  • RMSE: {error_metrics['rmse'].mean():.2f}")
        print()

    # Performance metrics
    performance = {
        'total_execution_time_s': round(total_time_s, 4),
        'time_per_trial_ms': round((total_time_s / num_trials) * 1000, 4),
        'num_trials': num_trials,
        'p': p,
        'base_seed': base_seed
    }

    if verbose:
        print("Performance:")
        print(f"  • Total execution time: {total_time_s:.2f} s")
        print(f"  • Time per trial: {performance['time_per_trial_ms']:.2f} ms")
        print()

    # Save results if requested
    if save_results:
        if verbose:
            print("Saving results...")

        # Ensure output directory exists
        output_dir = Path(RESULTS_FIXED_PROB_PATH)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save trial results (pickle for full data)
        trial_pkl_path = output_dir / f'trial_results_p{int(p*100)}_n{num_trials}.pkl'
        with open(trial_pkl_path, 'wb') as f:
            pickle.dump(trial_results, f)
        if verbose:
            print(f"  ✓ Saved trial results to {trial_pkl_path}")

        # Save summary statistics (CSV for easy inspection)
        summary_path = output_dir / 'summary_statistics.csv'
        error_metrics.to_csv(summary_path, index=False)
        if verbose:
            print(f"  ✓ Saved summary statistics to {summary_path}")

        # Save error analysis (JSON)
        error_analysis = {
            'unbiased_test': {
                'mean_bias': float(unbiased_test['mean_bias']),
                'std_bias': float(unbiased_test['std_bias']),
                't_statistic': float(unbiased_test['t_statistic']),
                'p_value': float(unbiased_test['p_value']),
                'is_unbiased': bool(unbiased_test['is_unbiased']),
                'conclusion': unbiased_test['conclusion']
            },
            'error_summary': {
                'mean_absolute_error': float(error_metrics['absolute_error'].mean()),
                'mean_relative_error': float(error_metrics['relative_error'].mean()),
                'mean_rmse': float(error_metrics['rmse'].mean()),
                'max_absolute_error': float(error_metrics['absolute_error'].max()),
                'max_relative_error': float(error_metrics['relative_error'].max())
            }
        }

        error_path = output_dir / 'error_analysis.json'
        with open(error_path, 'w') as f:
            json.dump(error_analysis, f, indent=2)
        if verbose:
            print(f"  ✓ Saved error analysis to {error_path}")

        # Save performance metrics
        perf_path = output_dir / 'performance_metrics.json'
        with open(perf_path, 'w') as f:
            json.dump(performance, f, indent=2)
        if verbose:
            print(f"  ✓ Saved performance to {perf_path}")

    if verbose:
        print()
        print("=" * 70)
        print("✓ FIXED PROBABILITY COUNTER EXPERIMENT COMPLETE")
        print("=" * 70)

    # Return all results
    return {
        'trial_results': trial_results,
        'aggregated': aggregated,
        'error_metrics': error_metrics,
        'theoretical': theoretical,
        'unbiased_test': unbiased_test,
        'performance': performance,
        'parameters': {
            'p': p,
            'num_trials': num_trials,
            'base_seed': base_seed,
            'confidence_level': CONFIDENCE_LEVEL
        }
    }


if __name__ == "__main__":
    """
    Command-line interface for running the fixed probability counter experiment.

    Usage:
        python -m src.experiments.run_fixed_prob
        python -m src.experiments.run_fixed_prob --trials 50 --p 0.5
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Fixed Probability Counter experiment with multiple trials"
    )
    parser.add_argument(
        '--trials',
        type=int,
        default=NUM_TRIALS,
        help=f'Number of trials to run (default: {NUM_TRIALS})'
    )
    parser.add_argument(
        '--p',
        type=float,
        default=FIXED_PROB_P,
        help=f'Probability of incrementing (default: {FIXED_PROB_P})'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=RANDOM_SEED,
        help=f'Base random seed (default: {RANDOM_SEED})'
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
    results = run_fixed_prob_experiment(
        p=args.p,
        num_trials=args.trials,
        base_seed=args.seed,
        save_results=not args.no_save,
        verbose=not args.quiet
    )

    # Print summary if not quiet
    if not args.quiet:
        print()
        print("Experiment completed successfully!")
        print(f"Ran {args.trials} trials with p={args.p}")
        print(f"Estimator is {'unbiased' if results['unbiased_test']['is_unbiased'] else 'biased'}")
