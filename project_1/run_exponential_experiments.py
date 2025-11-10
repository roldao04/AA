#!/usr/bin/env python3
"""
Targeted Experiments for Exponential Algorithms (Exhaustive Search & Branch-Bound)

This script runs experiments specifically designed to achieve good R² values for
exponential complexity algorithms by controlling variance.

Strategy:
- Small vertex range (4-12) where algorithms can complete
- Multiple densities tested separately
- High repetition count for statistical significance
- Focused on getting clean O(2^m) fit

Student Number: 113920
"""

import sys
from datetime import datetime
from pathlib import Path

from src.experiment import ExperimentRunner
from src.visualization import ResultVisualizer


def main():
    print("=" * 80)
    print("EXPONENTIAL ALGORITHMS TARGETED EXPERIMENT")
    print("Optimized for R² > 0.85 on Exhaustive Search & Branch-Bound")
    print("=" * 80)

    # Configuration for clean exponential fit
    config = {
        'vertices': list(range(4, 13)),  # 4-12 vertices
        'densities': [12.5, 25.0, 50.0, 75.0],  # PDF-required densities
        'repetitions': 20,  # High for statistical significance
        'timeout': 300.0,  # 5 minutes per experiment
        'seed': 113920,
    }

    print(f"\nConfiguration:")
    print(f"  Vertices: {config['vertices'][0]}-{config['vertices'][-1]} ({len(config['vertices'])} values)")
    print(f"  Densities: {config['densities']}")
    print(f"  Repetitions: {config['repetitions']}")
    print(f"  Timeout: {config['timeout']}s")

    total_experiments = len(config['vertices']) * len(config['densities']) * config['repetitions']
    print(f"\n  Total experiments: {total_experiments}")
    print(f"  Estimated time: {total_experiments * 0.5 / 60:.1f} minutes (assuming 0.5s avg)")
    print("=" * 80)

    response = input('\nProceed? (yes/no): ')
    if response.strip().lower() not in ('y', 'yes'):
        print('Cancelled.')
        return 0

    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"results/exponential_targeted_{timestamp}"

    # Initialize runner
    runner = ExperimentRunner(
        output_dir=output_dir,
        timeout_seconds=config['timeout'],
        seed=config['seed']
    )

    # Run experiments
    print("\nRunning experiments...")
    start_time = datetime.now()

    try:
        results = runner.run_batch_experiments(
            vertex_counts=config['vertices'],
            edge_densities=config['densities'],
            repetitions=config['repetitions'],
            verbose=True,
            save_graphs=True,
            save_every_nth=20  # Save fewer graphs to speed up
        )
    except KeyboardInterrupt:
        print('\n\nInterrupted by user!')
        results = runner.results

    end_time = datetime.now()
    elapsed = end_time - start_time

    if not results:
        print('No results generated!')
        return 1

    # Save results
    data_dir = Path(output_dir) / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_path = runner.save_results_csv('exponential_results.csv')
    json_path = runner.save_results_json('exponential_results.json')

    print(f'\n{"=" * 80}')
    print('Experiment Complete')
    print("=" * 80)
    print(f'Runtime: {elapsed}')
    print(f'Experiments completed: {len(results)}/{total_experiments} ({100*len(results)/total_experiments:.1f}%)')
    print(f'CSV: {csv_path}')
    print(f'JSON: {json_path}')

    runner.print_summary()

    # Generate visualizations
    print('\nGenerating plots...')
    try:
        visualizer = ResultVisualizer(results, output_dir=f"{output_dir}/plots")
        plots = visualizer.generate_all_plots()
        print(f'Generated {len(plots)} plots')
    except Exception as e:
        print(f'Error generating plots: {e}')

    print(f'\nResults saved to: {output_dir}')
    print('\nNext step: Run analyze_complexity.py on the results to verify R² values')

    return 0


if __name__ == '__main__':
    sys.exit(main())
