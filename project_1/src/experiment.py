"""
Experimental framework for systematic testing of Edge Cover algorithms.
"""

import time
import json
import csv
import multiprocessing
from typing import List, Dict, Optional, Any, Callable
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
from src.exceptions import AlgorithmTimeoutException
from src.logger import setup_logger

# Set up module logger
logger = setup_logger(__name__)


def _run_with_timeout(func: Callable, timeout: float, *args, **kwargs) -> Optional[Any]:
    """
    Run a function with a timeout using multiprocessing.

    Args:
        func: Function to run
        timeout: Maximum execution time in seconds
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Result from func if completed within timeout, None otherwise

    Raises:
        AlgorithmTimeoutException: If function exceeds timeout
    """
    def worker(queue, func, args, kwargs):
        """Worker function that runs in separate process."""
        try:
            result = func(*args, **kwargs)
            queue.put(('success', result))
        except Exception as e:
            queue.put(('error', e))

    # Create queue for inter-process communication
    queue = multiprocessing.Queue()

    # Create and start process
    process = multiprocessing.Process(
        target=worker,
        args=(queue, func, args, kwargs)
    )
    process.start()

    # Wait for process to complete or timeout
    process.join(timeout=timeout)

    # Check if process completed
    if process.is_alive():
        # Process is still running - kill it
        process.terminate()
        process.join(timeout=1.0)  # Give it 1 second to terminate gracefully
        if process.is_alive():
            process.kill()  # Force kill if still alive
            process.join()
        raise AlgorithmTimeoutException(f"Function exceeded timeout of {timeout} seconds")

    # Process completed - get result
    if not queue.empty():
        status, result = queue.get()
        if status == 'success':
            return result
        else:
            raise result  # Re-raise the exception from worker
    else:
        # Process ended but no result (shouldn't happen)
        raise RuntimeError("Process ended without result")


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

    # Greedy coverage-based metrics
    greedy_time: float
    greedy_operations: int
    greedy_solution_size: int

    # Greedy matching-based metrics
    greedy_matching_time: float
    greedy_matching_operations: int
    greedy_matching_solution_size: int

    # Comparison metrics (greedy coverage vs optimal)
    is_optimal: Optional[bool]
    quality_ratio: Optional[float]
    size_difference: Optional[int]
    speedup: Optional[float]
    operation_reduction: Optional[float]

    # Comparison metrics (greedy matching vs optimal)
    matching_is_optimal: Optional[bool]
    matching_quality_ratio: Optional[float]
    matching_size_difference: Optional[int]


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
        self.output_dir.mkdir(parents=True, exist_ok=True)
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

        # Run exhaustive search with timeout enforcement
        exhaustive_metrics = None
        exhaustive_timed_out = False

        # Only run exhaustive for small graphs (beyond 25 edges, it's impractical)
        if graph.num_edges() <= 25:
            try:
                # Create a wrapper function for timeout enforcement
                def run_exhaustive():
                    exhaustive = ExhaustiveSearch(graph)
                    return exhaustive.find_minimum_edge_cover()

                # Run with actual timeout (kills process if exceeded)
                exhaustive_metrics = _run_with_timeout(
                    run_exhaustive,
                    timeout=self.timeout_seconds
                )

                logger.info(f"Exhaustive search completed: V={num_vertices}, "
                          f"E={graph.num_edges()}, time={exhaustive_metrics.execution_time:.4f}s")

            except AlgorithmTimeoutException as e:
                # Timeout occurred - process was killed
                exhaustive_timed_out = True
                logger.warning(f"Exhaustive search timed out: V={num_vertices}, "
                             f"E={graph.num_edges()}, timeout={self.timeout_seconds}s")
                if verbose:
                    print(f"[TIMEOUT: >{self.timeout_seconds}s]", end=" ")

            except Exception as e:
                # Other error occurred
                exhaustive_timed_out = True
                logger.error(f"Exhaustive search error: {e}")
                if verbose:
                    print(f"[ERROR: {e}]", end=" ")
        else:
            # Too many edges - skip exhaustive search entirely
            exhaustive_timed_out = True
            logger.info(f"Skipping exhaustive search: V={num_vertices}, "
                       f"E={graph.num_edges()} (> 25 edges)")
            if verbose:
                print("[SKIPPED: too many edges]", end=" ")

        # Run both greedy heuristics (both are fast)
        greedy = GreedyHeuristic(graph)
        greedy_metrics = greedy.find_edge_cover()

        greedy_matching = GreedyMatchingBased(graph)
        greedy_matching_metrics = greedy_matching.find_edge_cover()

        # Compare both greedy algorithms against optimal (if available)
        comparison = None
        matching_comparison = None
        if exhaustive_metrics and not exhaustive_timed_out:
            comparison = compare_solutions(exhaustive_metrics, greedy_metrics)
            matching_comparison = compare_solutions(exhaustive_metrics, greedy_matching_metrics)

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
            greedy_matching_time=greedy_matching_metrics.execution_time,
            greedy_matching_operations=greedy_matching_metrics.basic_operations,
            greedy_matching_solution_size=greedy_matching_metrics.solution_size,
            is_optimal=comparison['is_optimal'] if comparison else None,
            quality_ratio=comparison['quality'] if comparison else None,
            size_difference=comparison['size_difference'] if comparison else None,
            speedup=comparison['speedup'] if comparison else None,
            operation_reduction=comparison['operation_reduction'] if comparison else None,
            matching_is_optimal=matching_comparison['is_optimal'] if matching_comparison else None,
            matching_quality_ratio=matching_comparison['quality'] if matching_comparison else None,
            matching_size_difference=matching_comparison['size_difference'] if matching_comparison else None
        )

        if verbose:
            if exhaustive_metrics and not exhaustive_timed_out:
                print(f"Optimal={exhaustive_metrics.solution_size}, "
                      f"GreedyCov={greedy_metrics.solution_size}, "
                      f"GreedyMatch={greedy_matching_metrics.solution_size}, "
                      f"QualityCov={comparison['quality']:.2f}, "
                      f"QualityMatch={matching_comparison['quality']:.2f}")
            else:
                print(f"GreedyCov={greedy_metrics.solution_size}, "
                      f"GreedyMatch={greedy_matching_metrics.solution_size} "
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
                    # Note: We do NOT reset the seed here. The seed was set once at initialization
                    # (using student number 113920), and we let the random state advance naturally.
                    # This ensures each graph instance has different vertex positions while
                    # maintaining reproducibility (same sequence of graphs on every run).
                    # This aligns with PDF requirement: "generate graph instances" (plural).

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
