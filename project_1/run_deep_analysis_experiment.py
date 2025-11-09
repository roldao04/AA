"""
Deep Analysis Experiment Runner - True 8-hour intensive experiment.

Purpose: Maximum statistical significance and fine-grained analysis
Run time: 8-12 hours (actual overnight!)
Outputs: ~3000+ experiments with complete data

This experiment focuses on the "productive range" (V=4-14) where all algorithms
complete successfully, providing statistically robust data for analysis.

Student Number: 113920
"""

import sys
from datetime import datetime
from pathlib import Path
from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    """Run deep analysis experiment for publication-quality results."""

    print("=" * 70)
    print("MINIMUM EDGE COVER - DEEP ANALYSIS EXPERIMENT")
    print("True 8-Hour Intensive Experiment")
    print("Student Number: 113920")
    print("=" * 70)

    # Deep analysis experiment configuration
    config = {
        'min_vertices': 4,
        'max_vertices': 14,  # Productive range (all algorithms complete)
        'edge_densities': [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0,
                          50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0],  # 17 densities
        'timeout': 900.0,  # 15 minutes (reasonable for V≤14)
        'repetitions': 15,  # Statistical robustness (15-20 runs per config)
        'save_graphs': True,
        'save_every_nth': 10,  # Save every 10th graph (reduces storage)
        'seed': 113920
    }

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results/deep_analysis_{timestamp}"

    print("\nConfiguration:")
    print(f"  Vertex range: {config['min_vertices']} to {config['max_vertices']} (PRODUCTIVE RANGE)")
    print(f"  Edge densities: {len(config['edge_densities'])} densities (10% to 90% in 5% steps)")
    print(f"  Densities: {config['edge_densities'][:3]}...{config['edge_densities'][-3:]}")
    print(f"  Timeout: {config['timeout']}s ({config['timeout']/60:.0f} minutes)")
    print(f"  Repetitions: {config['repetitions']} (for statistical significance)")
    print(f"  Save graphs: Every {config['save_every_nth']}th graph")
    print(f"  Output directory: {output_dir}")
    print(f"  Random seed: {config['seed']}")

    # Calculate total experiments
    vertex_range = range(config['min_vertices'], config['max_vertices'] + 1)
    experiments_per_rep = len(list(vertex_range)) * len(config['edge_densities'])
    total_experiments = experiments_per_rep * config['repetitions']
    saved_graphs = total_experiments // config['save_every_nth']

    print(f"\nExperiment Scale:")
    print(f"  Vertex sizes: {len(list(vertex_range))}")
    print(f"  Densities: {len(config['edge_densities'])}")
    print(f"  Repetitions: {config['repetitions']}")
    print(f"  Total experiments: {total_experiments} ({experiments_per_rep} × {config['repetitions']} reps)")
    print(f"  Graphs to save: ~{saved_graphs}")
    print(f"  Expected time: 8-12 hours")
    print(f"  Expected complete data: ~{int(total_experiments * 0.95)}+ experiments (95%+ completion rate)")

    print("\n" + "=" * 70)
    print("DEEP ANALYSIS EXPERIMENT - 8-HOUR RUN")
    print("=" * 70)

    print("\nExperiment provides:")
    print(f"  - {config['repetitions']} repetitions per configuration (statistical significance)")
    print(f"  - {len(config['edge_densities'])} density levels (fine-grained analysis)")
    print(f"  - ~{int(total_experiments * 0.95)}+ complete experiments expected")
    print("  - Focused on V=4-14 (productive range with high completion rate)")

    print("\n" + "=" * 70)
    print("IMPORTANT: LONG-RUNNING EXPERIMENT")
    print("=" * 70)
    print("\nExperiment details:")
    print("  - Runtime: 8-12 hours")
    print(f"  - Total experiments: {total_experiments}")
    print(f"  - Graph visualizations: ~{saved_graphs}")
    print("  - Disk space: ~500-800 MB")
    print("\nRequirements:")
    print("  - Sufficient disk space (~1 GB free)")
    print("  - Uninterrupted power/computer access")
    print("  - Do not close terminal or interrupt process")

    print("\nAlternative experiment runners:")
    print("  - run_quick_experiment.py (5 min)")
    print("  - run_standard_experiment.py (1 hr)")
    print("\n")

    # Confirm before proceeding
    try:
        response = input(f"This will take 8-12 hours and run {total_experiments} experiments. Proceed? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("\nCancelled.")
            return 0
    except (EOFError, KeyboardInterrupt):
        print("\n\nCancelled.")
        return 0

    print("\n" + "=" * 70)
    print("Starting Deep Analysis Experiment...")
    print("=" * 70)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Expected completion: ~{datetime.now().hour + 10}:00 (approximately)")
    print("\nYou can safely leave your computer.")
    print("Results will be saved continuously to preserve data if interrupted.")
    print("To monitor progress, check the output directory periodically.")
    print()

    # Initialize experiment runner
    runner = ExperimentRunner(
        output_dir=output_dir,
        timeout_seconds=config['timeout'],
        seed=config['seed']
    )

    # Run experiments
    print("=== Running Experiments ===\n")
    start_time = datetime.now()

    experiment_count = 0
    checkpoint_interval = 50  # Save checkpoint every 50 experiments

    try:
        results = runner.run_batch_experiments(
            vertex_counts=list(vertex_range),
            edge_densities=config['edge_densities'],
            repetitions=config['repetitions'],
            verbose=True,
            save_graphs=config['save_graphs'],
            save_every_nth=config['save_every_nth']
        )
    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user!")
        print("Partial results have been saved.")
        end_time = datetime.now()
        elapsed = end_time - start_time
        print(f"Ran for: {elapsed}")
        print(f"Completed: {len(runner.results)}/{total_experiments} experiments")
        print(f"Completion rate: {100*len(runner.results)/total_experiments:.1f}%")
        return 1

    end_time = datetime.now()
    elapsed = end_time - start_time

    if not results:
        print("\nNo results generated!")
        return 1

    # Save results
    print("\n" + "=" * 70)
    print("=== Saving Results ===")
    print("=" * 70)
    data_dir = Path(output_dir) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_path = runner.save_results_csv('data/deep_analysis_results.csv')
    json_path = runner.save_results_json('data/deep_analysis_results.json')
    print(f"CSV saved: {csv_path}")
    print(f"JSON saved: {json_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("=== Experiment Summary ===")
    print("=" * 70)
    print(f"Total runtime: {elapsed}")
    print(f"Experiments completed: {len(results)}/{total_experiments} ({100*len(results)/total_experiments:.1f}%)")
    runner.print_summary()

    # Generate visualizations
    print("\n" + "=" * 70)
    print("=== Generating Metric Plots ===")
    print("=" * 70)
    try:
        visualizer = ResultVisualizer(results, output_dir=f"{output_dir}/metrics")
        plots = visualizer.generate_all_plots()
        print(f"\nGenerated {len(plots)} metric visualization plots")
    except Exception as e:
        print(f"\nError generating plots: {e}")
        import traceback
        traceback.print_exc()

    # Print completion
    print("\n" + "=" * 70)
    print("DEEP ANALYSIS EXPERIMENT COMPLETE")
    print("=" * 70)
    print(f"\nTotal runtime: {elapsed}")
    print(f"Average time per experiment: {elapsed.total_seconds()/len(results):.2f} seconds")
    print(f"Results saved to: {output_dir}")

    print("\nOutput structure:")
    print(f"  {output_dir}/")
    print("  ├── data/")
    print("  │   ├── deep_analysis_results.csv  (MASSIVE DATASET)")
    print("  │   ├── deep_analysis_results.json (structured data)")
    print("  │   └── summary.txt")
    print("  ├── graphs/")
    print("  │   ├── instances/             (every 10th graph)")
    print("  │   ├── solutions/             (algorithm solutions)")
    print("  │   └── comparisons/           (selected comparisons)")
    print("  └── metrics/")
    print("      └── *.png                  (all performance plots)")

    print("\n" + "=" * 70)
    print("Next Steps: Statistical Analysis")
    print("=" * 70)
    print("\n1. Run complexity analysis:")
    print(f"   python3 analyze_complexity.py --results-file {output_dir}/data/deep_analysis_results.json")

    print("\n2. Statistical analysis (Python/R/Excel):")
    print("   - Group by (num_vertices, edge_density)")
    print("   - Calculate: mean, std dev, min, max, median")
    print("   - Generate: confidence interval plots")
    print("   - Identify: outliers and interesting cases")

    print("\n3. Create publication-quality figures:")
    print("   - Performance curves with error bars (mean ± std dev)")
    print("   - Density vs. execution time heatmaps")
    print("   - Algorithm comparison with statistical significance")
    print("   - Scaling analysis with confidence bands")

    print("\n4. Write report sections:")
    print("   - Experimental setup (with full configuration)")
    print("   - Results with statistical validation")
    print("   - Discussion of variance and edge cases")
    print("   - Conclusions with confidence intervals")


    return 0


if __name__ == "__main__":
    sys.exit(main())
