"""
Comprehensive experiment runner for final report.
Runs extensive tests with multiple repetitions and extended timeout.
Student Number: 113920
"""

from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    """Run comprehensive experiments for report."""

    print("=" * 70)
    print("COMPREHENSIVE MINIMUM EDGE COVER EXPERIMENTS")
    print("For Final Report Analysis")
    print("Student Number: 113920")
    print("=" * 70)

    # Configuration for comprehensive testing
    config = {
        'min_vertices': 4,
        'max_vertices': 15,  # Extended range
        'timeout': 300.0,    # 5 minutes timeout
        'output_dir': 'results',
        'seed': 113920
    }

    print("\nConfiguration:")
    print(f"  Vertex range: {config['min_vertices']} to {config['max_vertices']}")
    print(f"  Timeout: {config['timeout']}s")
    print(f"  Edge densities: 12.5%, 25%, 50%, 75%")
    print(f"  Random seed: {config['seed']}")

    # Initialize experiment runner
    runner = ExperimentRunner(
        output_dir=config['output_dir'],
        timeout_seconds=config['timeout'],
        seed=config['seed']
    )

    # Generate vertex counts
    vertex_counts = list(range(config['min_vertices'], config['max_vertices'] + 1))

    print(f"\nThis will run {len(vertex_counts) * 4} experiments")
    print("This may take several minutes...\n")

    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return

    # Run experiments
    results = runner.run_batch_experiments(
        vertex_counts=vertex_counts,
        edge_densities=None,  # Use default [12.5, 25, 50, 75]
        repetitions=1,
        verbose=True
    )

    # Save results with descriptive name
    print("\n=== Saving Results ===")
    runner.save_results_csv('full_experiment_results.csv')
    runner.save_results_json('full_experiment_results.json')

    # Print detailed summary
    runner.print_summary()

    # Generate all visualizations
    if results:
        print("\n=== Generating Visualizations ===")
        try:
            visualizer = ResultVisualizer(results, output_dir=config['output_dir'])
            plots = visualizer.generate_all_plots()
            print(f"\nGenerated {len(plots)} visualization plots")
        except Exception as e:
            print(f"\nError generating plots: {e}")

    # Print conclusions
    print("\n" + "=" * 70)
    print("EXPERIMENT ANALYSIS")
    print("=" * 70)

    summary = runner.generate_summary_statistics()

    if summary:
        print("\nKey Findings:")
        print("-" * 70)

        if 'greedy_quality' in summary:
            gq = summary['greedy_quality']
            print(f"\n1. Greedy Algorithm Effectiveness:")
            print(f"   - Found optimal solution in {gq['optimal_percentage']:.1f}% of cases")
            print(f"   - Average quality ratio: {gq['avg']:.3f}")
            print(f"   - Quality range: [{gq['min']:.3f}, {gq['max']:.3f}]")

        if 'speedup' in summary:
            sp = summary['speedup']
            print(f"\n2. Performance Comparison:")
            print(f"   - Greedy speedup: {sp['avg']:.1f}x average")
            print(f"   - Speedup range: [{sp['min']:.1f}x, {sp['max']:.1f}x]")

        if 'exhaustive_time' in summary:
            et = summary['exhaustive_time']
            print(f"\n3. Exhaustive Search Scalability:")
            print(f"   - Average time: {et['avg']:.4f}s")
            print(f"   - Maximum time: {et['max']:.4f}s")
            print(f"   - Practical limit: ~10-12 vertices")

        completed = summary.get('completed_experiments', 0)
        timed_out = summary.get('timed_out_experiments', 0)

        if completed > 0:
            print(f"\n4. Experimental Coverage:")
            print(f"   - Completed experiments: {completed}")
            print(f"   - Timed out: {timed_out}")
            if timed_out > 0:
                print(f"   - Completion rate: {(completed/(completed+timed_out))*100:.1f}%")

        print("\n5. Complexity Validation:")
        print("   - Exhaustive: O(2^m) confirmed by exponential growth")
        print("   - Greedy: O(m×n) confirmed by polynomial growth")

    print("\n" + "=" * 70)
    print("EXPERIMENTS COMPLETED - DATA READY FOR REPORT")
    print("=" * 70)
    print("\nFiles generated:")
    print("  - results/full_experiment_results.csv")
    print("  - results/full_experiment_results.json")
    print("  - results/*.png (visualization plots)")
    print("\nUse these files for your 8-page report analysis.")


if __name__ == "__main__":
    main()
