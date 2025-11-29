"""
Overnight Experiment Suite

This module configures and runs comprehensive experiments overnight
for statistical validation and graph property correlation analysis.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.algorithms import (
    exact_edge_cover,
    israeli_itai_edge_cover,
    simulated_annealing_edge_cover,
    lazy_greedy_edge_cover,
    nearest_neighbor_edge_cover
)
from src.utils import load_graph, get_builtin_graphs, compute_graph_properties, generate_synthetic_graphs
from src.experiments import ExperimentRunner
from datetime import datetime
from typing import List, Tuple, Dict
import networkx as nx


# Configuration
ALGORITHMS = {
    'exact': exact_edge_cover,
    'israeli_itai': israeli_itai_edge_cover,
    'simulated_annealing': simulated_annealing_edge_cover,
    'lazy_greedy': lazy_greedy_edge_cover,
    'nearest_neighbor': nearest_neighbor_edge_cover
}

REAL_WORLD_GRAPHS = [
    'karate',
    'florentine',
    'davis',
    # Add SNAP datasets when downloaded
    # 'ego-Facebook',
    # 'email-Eu-core',
    # 'wiki-Vote',
    # 'ca-GrQc',
    # 'ca-HepTh',
]

REPETITIONS = 40
TIMEOUT = 300  # 5 minutes


def run_overnight_suite(
    algorithms: List[str] = None,
    real_graphs: List[str] = None,
    use_synthetic: bool = True,
    repetitions: int = REPETITIONS
) -> None:
    """
    Run comprehensive overnight experiment suite.

    Args:
        algorithms: List of algorithm names to run (None = all)
        real_graphs: List of real-world graphs to use (None = default)
        use_synthetic: Whether to include synthetic graphs
        repetitions: Number of trials per algorithm-graph pair
    """
    if algorithms is None:
        algorithms = list(ALGORITHMS.keys())

    if real_graphs is None:
        real_graphs = REAL_WORLD_GRAPHS

    runner = ExperimentRunner(results_dir='overnight')

    # Collect all graph instances
    graph_instances = []

    # Load real-world graphs
    print("Loading real-world graphs...")
    for graph_name in real_graphs:
        try:
            G = load_graph(graph_name)
            props = compute_graph_properties(G)
            graph_instances.append((graph_name, G, props))
            print(f"  Loaded {graph_name}: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
        except Exception as e:
            print(f"  Failed to load {graph_name}: {e}")

    # Generate synthetic graphs
    if use_synthetic:
        print("\nGenerating synthetic graphs...")
        synthetic = generate_synthetic_graphs(n_graphs=30, base_size=500)
        graph_instances.extend(synthetic)

    print(f"\nTotal graphs: {len(graph_instances)}")
    print(f"Algorithms: {len(algorithms)}")
    print(f"Repetitions per pair: {repetitions}")
    print(f"Estimated total runs: {len(graph_instances) * len(algorithms) * repetitions}")

    # Run experiments
    total_experiments = len(graph_instances) * len(algorithms)
    experiment_num = 0

    start_time = datetime.now()
    print(f"\nStarting experiments at {start_time}")

    for graph_name, G, props in graph_instances:
        for algo_name in algorithms:
            experiment_num += 1
            print(f"\n[{experiment_num}/{total_experiments}] {algo_name} on {graph_name}")

            algo_func = ALGORITHMS[algo_name]

            # Run multiple trials
            trial_results = runner.run_multi_trial(
                graph=G,
                algorithm_func=algo_func,
                algorithm_name=algo_name,
                graph_name=graph_name,
                graph_properties=props,
                repetitions=repetitions
            )

            # Compute and print statistics
            stats = runner.compute_statistics(trial_results)
            print(f"  Success rate: {stats['success_rate']:.2%}")
            if stats['n_successful'] > 0:
                print(f"  Cover size: {stats['cover_size_mean']:.2f} ± {stats['cover_size_std']:.2f}")
                print(f"  Runtime: {stats['runtime_mean']:.4f}s ± {stats['runtime_std']:.4f}s")

            # Checkpoint every 50 runs
            if len(runner.results) % 50 == 0:
                runner.save_checkpoint()

    # Final save
    print("\nSaving final results...")
    runner.save_results(filename='overnight_final_results.json')
    runner.save_checkpoint(checkpoint_file='overnight_final_checkpoint.pkl')

    # Export to CSV for analysis
    df = runner.export_to_dataframe()
    df.to_csv('overnight/overnight_results.csv', index=False)

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\nExperiments completed at {end_time}")
    print(f"Total duration: {duration}")
    print(f"Total runs: {len(runner.results)}")


if __name__ == '__main__':
    run_overnight_suite()
