"""
Experimental framework for systematic testing of Edge Cover algorithms.
"""

import time
import json
import csv
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

from src.graph import Graph
from src.graph_generator import GraphGenerator, DEFAULT_EDGE_DENSITIES
from src.algorithms import (
    ExhaustiveSearch,
    GreedyHeuristic,
    GreedyMatchingBased,
    AlgorithmMetrics,
    compare_solutions
)


@dataclass
class ExperimentResult:
    """Results from a single experiment run."""
    timestamp: str
    num_vertices: int
    num_edges: int
    edge_density: float

    # Exhaustive search metrics
    exhaustive_time: Optional[float]
    exhaustive_operations: Optional[int]
    exhaustive_solutions_explored: Optional[int]
    exhaustive_solution_size: Optional[int]
    exhaustive_timed_out: bool

    # Greedy metrics
    greedy_time: float
    greedy_operations: int
    greedy_solution_size: int

    # Comparison metrics
    is_optimal: Optional[bool]
    quality_ratio: Optional[float]
    size_difference: Optional[int]
    speedup: Optional[float]
    operation_reduction: Optional[float]


class ExperimentRunner:
    """Runs systematic experiments on edge cover algorithms."""

    def __init__(
        self,
        output_dir: str = "results",
        timeout_seconds: float = 300.0,  # 5 minutes default timeout
        seed: int = 113920
    ):
        """
        Initialize experiment runner.

        Args:
            output_dir: Directory to save results
            timeout_seconds: Timeout for exhaustive search (seconds)
            seed: Random seed for graph generation
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timeout_seconds = timeout_seconds
        self.generator = GraphGenerator(seed=seed)
        self.results: List[ExperimentResult] = []

    def run_single_experiment(
        self,
        num_vertices: int,
        edge_density: float,
        verbose: bool = True
    ) -> ExperimentResult:
        """
        Run both algorithms on a single graph configuration.

        Args:
            num_vertices: Number of vertices in the graph
            edge_density: Edge density percentage
            verbose: Print progress information

        Returns:
            ExperimentResult with all metrics
        """
        if verbose:
            print(f"  Testing: V={num_vertices}, density={edge_density}%", end=" ... ")

        # Generate graph
        graph = self.generator.generate_graph(num_vertices, edge_density)

        timestamp = datetime.now().isoformat()

        # Run exhaustive search with timeout
        exhaustive_metrics = None
        exhaustive_timed_out = False

        if graph.num_edges() <= 20:  # Only run exhaustive for small graphs
            try:
                exhaustive = ExhaustiveSearch(graph)
                start_time = time.time()
                exhaustive_metrics = exhaustive.find_minimum_edge_cover()

                # Check if it took too long
                if exhaustive_metrics.execution_time > self.timeout_seconds:
                    exhaustive_timed_out = True
                    if verbose:
                        print(f"[TIMEOUT: {exhaustive_metrics.execution_time:.2f}s]", end=" ")
            except Exception as e:
                if verbose:
                    print(f"[ERROR: {e}]", end=" ")
                exhaustive_timed_out = True
        else:
            exhaustive_timed_out = True
            if verbose:
                print("[SKIPPED: too many edges]", end=" ")

        # Run greedy heuristic (always fast)
        greedy = GreedyHeuristic(graph)
        greedy_metrics = greedy.find_edge_cover()

        # Compare if exhaustive completed
        comparison = None
        if exhaustive_metrics and not exhaustive_timed_out:
            comparison = compare_solutions(exhaustive_metrics, greedy_metrics)

        # Create result
        result = ExperimentResult(
            timestamp=timestamp,
            num_vertices=num_vertices,
            num_edges=graph.num_edges(),
            edge_density=edge_density,
            exhaustive_time=exhaustive_metrics.execution_time if exhaustive_metrics else None,
            exhaustive_operations=exhaustive_metrics.basic_operations if exhaustive_metrics else None,
            exhaustive_solutions_explored=exhaustive_metrics.solutions_explored if exhaustive_metrics else None,
            exhaustive_solution_size=exhaustive_metrics.solution_size if exhaustive_metrics else None,
            exhaustive_timed_out=exhaustive_timed_out,
            greedy_time=greedy_metrics.execution_time,
            greedy_operations=greedy_metrics.basic_operations,
            greedy_solution_size=greedy_metrics.solution_size,
            is_optimal=comparison['is_optimal'] if comparison else None,
            quality_ratio=comparison['quality'] if comparison else None,
            size_difference=comparison['size_difference'] if comparison else None,
            speedup=comparison['speedup'] if comparison else None,
            operation_reduction=comparison['operation_reduction'] if comparison else None
        )

        if verbose:
            if exhaustive_metrics and not exhaustive_timed_out:
                print(f"Optimal={exhaustive_metrics.solution_size}, "
                      f"Greedy={greedy_metrics.solution_size}, "
                      f"Quality={comparison['quality']:.2f}, "
                      f"Speedup={comparison['speedup']:.1f}x")
            else:
                print(f"Greedy={greedy_metrics.solution_size} "
                      f"(optimal unknown)")

        return result

    def run_batch_experiments(
        self,
        vertex_counts: List[int],
        edge_densities: List[float] = None,
        repetitions: int = 1,
        verbose: bool = True
    ) -> List[ExperimentResult]:
        """
        Run experiments on a batch of configurations.

        Args:
            vertex_counts: List of vertex counts to test
            edge_densities: List of edge densities to test (default: [12.5, 25, 50, 75])
            repetitions: Number of times to repeat each configuration
            verbose: Print progress information

        Returns:
            List of ExperimentResult objects
        """
        if edge_densities is None:
            edge_densities = DEFAULT_EDGE_DENSITIES

        if verbose:
            print(f"\n=== Starting Batch Experiments ===")
            print(f"Vertex counts: {vertex_counts}")
            print(f"Edge densities: {edge_densities}")
            print(f"Repetitions: {repetitions}")
            print(f"Timeout: {self.timeout_seconds}s\n")

        results = []

        for rep in range(repetitions):
            if repetitions > 1 and verbose:
                print(f"\n--- Repetition {rep + 1}/{repetitions} ---")

            for num_vertices in vertex_counts:
                if verbose:
                    print(f"\nVertex count: {num_vertices}")

                for density in edge_densities:
                    # Reset seed for reproducibility within each experiment
                    self.generator.reset_seed()

                    result = self.run_single_experiment(num_vertices, density, verbose)
                    results.append(result)

                    # Stop testing larger graphs if exhaustive is timing out
                    if result.exhaustive_timed_out and num_vertices >= 8:
                        if verbose:
                            print(f"  Stopping experiments - exhaustive search too slow for V>={num_vertices}")
                        break

        self.results.extend(results)
        return results

    def save_results_csv(self, filename: str = None) -> Path:
        """
        Save results to CSV file.

        Args:
            filename: Output filename (default: results_TIMESTAMP.csv)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.csv"

        output_path = self.output_dir / filename

        with open(output_path, 'w', newline='') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=asdict(self.results[0]).keys())
                writer.writeheader()
                for result in self.results:
                    writer.writerow(asdict(result))

        print(f"\nResults saved to: {output_path}")
        return output_path

    def save_results_json(self, filename: str = None) -> Path:
        """
        Save results to JSON file.

        Args:
            filename: Output filename (default: results_TIMESTAMP.json)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.json"

        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            json.dump(
                [asdict(result) for result in self.results],
                f,
                indent=2
            )

        print(f"Results saved to: {output_path}")
        return output_path

    def generate_summary_statistics(self) -> Dict[str, Any]:
        """
        Generate summary statistics from collected results.

        Returns:
            Dictionary with summary statistics
        """
        if not self.results:
            return {}

        # Filter results where we have optimal solutions
        optimal_results = [r for r in self.results if not r.exhaustive_timed_out]

        summary = {
            'total_experiments': len(self.results),
            'completed_experiments': len(optimal_results),
            'timed_out_experiments': len([r for r in self.results if r.exhaustive_timed_out]),
        }

        if optimal_results:
            # Greedy quality statistics
            qualities = [r.quality_ratio for r in optimal_results if r.quality_ratio is not None]
            if qualities:
                summary['greedy_quality'] = {
                    'min': min(qualities),
                    'max': max(qualities),
                    'avg': sum(qualities) / len(qualities),
                    'optimal_count': sum(1 for q in qualities if q == 1.0),
                    'optimal_percentage': (sum(1 for q in qualities if q == 1.0) / len(qualities)) * 100
                }

            # Speedup statistics
            speedups = [r.speedup for r in optimal_results if r.speedup is not None and r.speedup != float('inf')]
            if speedups:
                summary['speedup'] = {
                    'min': min(speedups),
                    'max': max(speedups),
                    'avg': sum(speedups) / len(speedups)
                }

            # Execution time statistics
            exhaustive_times = [r.exhaustive_time for r in optimal_results if r.exhaustive_time is not None]
            greedy_times = [r.greedy_time for r in self.results]

            if exhaustive_times:
                summary['exhaustive_time'] = {
                    'min': min(exhaustive_times),
                    'max': max(exhaustive_times),
                    'avg': sum(exhaustive_times) / len(exhaustive_times)
                }

            if greedy_times:
                summary['greedy_time'] = {
                    'min': min(greedy_times),
                    'max': max(greedy_times),
                    'avg': sum(greedy_times) / len(greedy_times)
                }

        return summary

    def print_summary(self) -> None:
        """Print summary statistics to console."""
        summary = self.generate_summary_statistics()

        print("\n" + "=" * 60)
        print("EXPERIMENT SUMMARY")
        print("=" * 60)

        print(f"\nTotal experiments: {summary.get('total_experiments', 0)}")
        print(f"Completed (optimal found): {summary.get('completed_experiments', 0)}")
        print(f"Timed out: {summary.get('timed_out_experiments', 0)}")

        if 'greedy_quality' in summary:
            gq = summary['greedy_quality']
            print(f"\nGreedy Algorithm Quality:")
            print(f"  Optimal solutions found: {gq['optimal_count']} ({gq['optimal_percentage']:.1f}%)")
            print(f"  Quality ratio: min={gq['min']:.3f}, max={gq['max']:.3f}, avg={gq['avg']:.3f}")

        if 'speedup' in summary:
            sp = summary['speedup']
            print(f"\nSpeedup (Exhaustive vs Greedy):")
            print(f"  min={sp['min']:.1f}x, max={sp['max']:.1f}x, avg={sp['avg']:.1f}x")

        if 'exhaustive_time' in summary:
            et = summary['exhaustive_time']
            print(f"\nExhaustive Search Time:")
            print(f"  min={et['min']:.4f}s, max={et['max']:.4f}s, avg={et['avg']:.4f}s")

        if 'greedy_time' in summary:
            gt = summary['greedy_time']
            print(f"\nGreedy Search Time:")
            print(f"  min={gt['min']:.6f}s, max={gt['max']:.6f}s, avg={gt['avg']:.6f}s")

        print("\n" + "=" * 60)
