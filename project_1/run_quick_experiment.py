"""
Quick Experiment Runner - Fast validation and testing.

Purpose: Rapid testing, debugging, verification
Run time: 2-5 minutes
Outputs: ~50 files (data + limited visualizations)

Student Number: 113920
"""

import sys
from datetime import datetime
from pathlib import Path
from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    """Run quick experiments for testing and validation."""

    print("=" * 70)
    print("MINIMUM EDGE COVER - QUICK EXPERIMENT")
    print("Fast Testing & Validation Mode")
    print("Student Number: 113920")
    print("=" * 70)

    # Quick experiment configuration
    config = {
        'min_vertices': 4,
        'max_vertices': 8,
        'edge_densities': [25.0, 75.0],  # Only 2 densities for speed
        'timeout': 30.0,  # 30 seconds
        'save_graphs': True,
        'save_every_nth': 1,  # Save all graphs (it's only 10 total)
        'seed': 113920
    }

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results/quick_{timestamp}"

    print("\nConfiguration:")
    print(f"  Vertex range: {config['min_vertices']} to {config['max_vertices']}")
    print(f"  Edge densities: {config['edge_densities']}")
    print(f"  Timeout: {config['timeout']}s")
    print(f"  Save graphs: {config['save_graphs']}")
    print(f"  Output directory: {output_dir}")
    print(f"  Random seed: {config['seed']}")

    # Calculate total experiments
    vertex_range = range(config['min_vertices'], config['max_vertices'] + 1)
    total_experiments = len(list(vertex_range)) * len(config['edge_densities'])
    print(f"\nTotal experiments: {total_experiments}")
    print(f"Expected time: 2-5 minutes")
    print("\nThis is a quick test - perfect for validation and debugging.")
    print("For comprehensive results, use run_standard_experiment.py")
    print("For deep analysis, use run_deep_analysis_experiment.py\n")

    # Initialize experiment runner
    runner = ExperimentRunner(
        output_dir=output_dir,
        timeout_seconds=config['timeout'],
        seed=config['seed']
    )

    # Run experiments
    print("\n=== Running Experiments ===\n")
    results = runner.run_batch_experiments(
        vertex_counts=list(vertex_range),
        edge_densities=config['edge_densities'],
        repetitions=1,
        verbose=True,
        save_graphs=config['save_graphs'],
        save_every_nth=config['save_every_nth']
    )

    if not results:
        print("\nNo results generated!")
        return 1

    # Save results
    print("\n=== Saving Results ===")
    data_dir = Path(output_dir) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_path = runner.save_results_csv('data/results.csv')
    json_path = runner.save_results_json('data/results.json')
    print(f"CSV saved: {csv_path}")
    print(f"JSON saved: {json_path}")

    # Print summary
    print("\n=== Experiment Summary ===")
    runner.print_summary()

    # Generate visualizations
    print("\n=== Generating Metric Plots ===")
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
    print("QUICK EXPERIMENT COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {output_dir}")
    print("\nOutput structure:")
    print(f"  {output_dir}/")
    print("  ├── data/")
    print("  │   ├── results.csv")
    print("  │   └── results.json")
    print("  ├── graphs/")
    print("  │   ├── instances/       (graph visualizations)")
    print("  │   ├── solutions/       (algorithm solutions)")
    print("  │   └── comparisons/     (side-by-side comparisons)")
    print("  └── metrics/")
    print("      └── *.png            (performance plots)")
    print("\nNext steps:")
    print("  - Review results in CSV/JSON files")
    print("  - Examine graph visualizations")
    print("  - Check metric plots for trends")
    print("  - Run standard experiment for report-quality results")
    print("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
