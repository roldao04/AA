"""
Main script to run Edge Cover experiments.
Student Number: 113920
"""

import argparse
from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    """Run experiments on Minimum Edge Cover algorithms."""

    parser = argparse.ArgumentParser(
        description='Run Minimum Edge Cover experiments'
    )
    parser.add_argument(
        '--min-vertices',
        type=int,
        default=4,
        help='Minimum number of vertices (default: 4)'
    )
    parser.add_argument(
        '--max-vertices',
        type=int,
        default=12,
        help='Maximum number of vertices (default: 12)'
    )
    parser.add_argument(
        '--timeout',
        type=float,
        default=60.0,
        help='Timeout for exhaustive search in seconds (default: 60)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results',
        help='Output directory for results (default: results)'
    )
    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip generating plots'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick test with fewer configurations'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("MINIMUM EDGE COVER - EXPERIMENTAL ANALYSIS")
    print("Student Number: 113920")
    print("=" * 70)

    # Initialize experiment runner
    runner = ExperimentRunner(
        output_dir=args.output_dir,
        timeout_seconds=args.timeout,
        seed=113920
    )

    # Define vertex counts to test
    if args.quick:
        vertex_counts = list(range(args.min_vertices, min(args.max_vertices, 8) + 1))
        edge_densities = [25.0, 75.0]  # Test only two densities
        print("\n[QUICK MODE: Testing limited configurations]\n")
    else:
        vertex_counts = list(range(args.min_vertices, args.max_vertices + 1))
        edge_densities = None  # Use default [12.5, 25.0, 50.0, 75.0]

    # Run experiments
    results = runner.run_batch_experiments(
        vertex_counts=vertex_counts,
        edge_densities=edge_densities,
        repetitions=1,
        verbose=True
    )

    # Save results
    print("\n=== Saving Results ===")
    runner.save_results_csv()
    runner.save_results_json()

    # Print summary
    runner.print_summary()

    # Generate visualizations
    if not args.no_plots and results:
        try:
            visualizer = ResultVisualizer(results, output_dir=args.output_dir)
            plots = visualizer.generate_all_plots()
            print(f"\nGenerated {len(plots)} visualization plots")
        except Exception as e:
            print(f"\nError generating plots: {e}")
            print("Install matplotlib with: pip install matplotlib")

    print("\n" + "=" * 70)
    print("EXPERIMENTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
