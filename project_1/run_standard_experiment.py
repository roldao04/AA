"""
Standard Experiment Runner - Report-quality comprehensive analysis.

Purpose: Generate figures and data for final report
Run time: 30-60 minutes
Outputs: ~400 files (complete dataset + all visualizations)

Student Number: 113920
"""

import sys
from datetime import datetime
from pathlib import Path
from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    """Run standard experiments for report-quality results."""

    print("=" * 70)
    print("MINIMUM EDGE COVER - STANDARD EXPERIMENT")
    print("Report-Quality Comprehensive Analysis")
    print("Student Number: 113920")
    print("=" * 70)

    # Standard experiment configuration
    config = {
        'min_vertices': 4,
        'max_vertices': 15,
        'edge_densities': [12.5, 25.0, 50.0, 75.0],  # All 4 densities
        'timeout': 300.0,  # 5 minutes
        'save_graphs': True,
        'save_every_nth': 1,  # Save all graphs
        'seed': 113920
    }

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results/standard_{timestamp}"

    print("\nConfiguration:")
    print(f"  Vertex range: {config['min_vertices']} to {config['max_vertices']}")
    print(f"  Edge densities: {config['edge_densities']}")
    print(f"  Timeout: {config['timeout']}s ({config['timeout']/60:.1f} minutes)")
    print(f"  Save graphs: {config['save_graphs']}")
    print(f"  Output directory: {output_dir}")
    print(f"  Random seed: {config['seed']}")

    # Calculate total experiments
    vertex_range = range(config['min_vertices'], config['max_vertices'] + 1)
    total_experiments = len(list(vertex_range)) * len(config['edge_densities'])
    print(f"\nTotal experiments: {total_experiments}")
    print(f"Expected time: 30-60 minutes")
    print(f"Expected outputs: ~400 files")
    print("\nThis will generate:")
    print(f"  - {total_experiments} graph instance visualizations")
    print(f"  - {total_experiments * 5} solution visualizations (~{total_experiments * 5} images)")
    print(f"  - {total_experiments} comparison visualizations")
    print("  - Complete metric plots")
    print("  - Complexity validation reports")
    print("  - CSV/JSON datasets")
    print("\nNote: This will take 30-60 minutes and generate ~400 files.")
    print("For quick testing, use run_quick_experiment.py")
    print("For deep analysis, use run_deep_analysis_experiment.py\n")

    # Confirm before proceeding
    try:
        response = input("Proceed with standard experiment? (y/n): ")
        if response.lower() != 'y':
            print("\nCancelled.")
            return 0
    except (EOFError, KeyboardInterrupt):
        print("\n\nCancelled.")
        return 0

    # Initialize experiment runner
    runner = ExperimentRunner(
        output_dir=output_dir,
        timeout_seconds=config['timeout'],
        seed=config['seed']
    )

    # Run experiments
    print("\n=== Running Experiments ===\n")
    try:
        results = runner.run_batch_experiments(
            vertex_counts=list(vertex_range),
            edge_densities=config['edge_densities'],
            repetitions=1,
            verbose=True,
            save_graphs=config['save_graphs'],
            save_every_nth=config['save_every_nth']
        )
    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user!")
        print("Partial results may be saved.\n")
        return 1

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

    # Run complexity analysis
    print("\n=== Running Complexity Analysis ===")
    print("For complexity validation, run:")
    print(f"  python3 analyze_complexity.py --results-file {output_dir}/data/results.json")
    print("\nFor algorithm limits analysis, run:")
    print(f"  python3 find_limits.py")

    # Print completion
    print("\n" + "=" * 70)
    print("STANDARD EXPERIMENT COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {output_dir}")
    print("\nOutput structure:")
    print(f"  {output_dir}/")
    print("  ├── data/")
    print("  │   ├── results.csv           (tabular data)")
    print("  │   ├── results.json          (structured data)")
    print("  │   └── summary.txt           (statistics)")
    print("  ├── graphs/")
    print("  │   ├── instances/            (graph visualizations)")
    print("  │   ├── solutions/            (algorithm solutions by type)")
    print("  │   │   ├── exhaustive_search/")
    print("  │   │   ├── branch_&_bound/")
    print("  │   │   ├── optimal_matching/")
    print("  │   │   ├── greedy_coverage/")
    print("  │   │   └── greedy_matching/")
    print("  │   └── comparisons/          (side-by-side comparisons)")
    print("  └── metrics/")
    print("      ├── time_vs_vertices.png")
    print("      ├── operations_vs_vertices.png")
    print("      ├── all_algorithms_comparison.png")
    print("      └── ... (more metric plots)")
    print("\nKey files for report:")
    print("  - graphs/instances/*.png        → Example graph instances")
    print("  - graphs/comparisons/*.png      → Algorithm comparisons")
    print("  - metrics/*.png                 → Performance plots")
    print("  - data/results.csv              → Raw data for analysis")
    print("\nNext steps:")
    print("  1. Review graph visualizations in graphs/")
    print("  2. Examine metric plots in metrics/")
    print("  3. Run complexity analysis (analyze_complexity.py)")
    print("  4. Select best figures for report")
    print("  5. For deeper analysis, run overnight experiment")
    print("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
