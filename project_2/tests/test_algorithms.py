"""
Test harness for edge cover algorithms with immediate validation.

This module provides utilities to test algorithms as they are implemented:
- Load small and medium test graphs
- Verify edge cover correctness
- Check approximation bounds
- Compare algorithm performance
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import networkx as nx
import numpy as np
from typing import Callable, Dict, List, Tuple, Set
import time

# Import algorithms (will be used as they're implemented)
from src.algorithms.exact import exact_edge_cover, verify_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover


class TestGraphs:
    """Collection of test graphs for validation."""

    @staticmethod
    def get_small_graphs() -> Dict[str, nx.Graph]:
        """
        Get small graphs for quick testing.

        Returns:
            Dictionary mapping graph names to NetworkX graphs
        """
        graphs = {}

        # Very small graphs
        graphs['path_10'] = nx.path_graph(10)
        graphs['star_20'] = nx.star_graph(20)
        graphs['complete_5'] = nx.complete_graph(5)
        graphs['cycle_15'] = nx.cycle_graph(15)

        # NetworkX built-in graphs
        graphs['karate'] = nx.karate_club_graph()

        return graphs

    @staticmethod
    def get_medium_graphs() -> Dict[str, nx.Graph]:
        """
        Get medium-sized graphs for validation.

        Returns:
            Dictionary mapping graph names to NetworkX graphs
        """
        graphs = {}

        # NetworkX built-in graphs
        try:
            graphs['dolphins'] = nx.read_gml(str(Path(__file__).parent.parent / 'data' / 'dolphins.gml'))
        except:
            # Generate if not available
            graphs['dolphins'] = nx.erdos_renyi_graph(62, 0.1, seed=42)

        try:
            graphs['football'] = nx.read_gml(str(Path(__file__).parent.parent / 'data' / 'football.gml'))
        except:
            # Generate if not available
            graphs['football'] = nx.erdos_renyi_graph(115, 0.08, seed=42)

        # Synthetic graphs with known properties
        graphs['er_100'] = nx.erdos_renyi_graph(100, 0.1, seed=42)
        graphs['ba_100'] = nx.barabasi_albert_graph(100, 3, seed=42)
        graphs['ws_100'] = nx.watts_strogatz_graph(100, 6, 0.3, seed=42)

        return graphs

    @staticmethod
    def load_sw_graph(filename: str) -> nx.Graph:
        """
        Load graph from SW_ALGUNS_GRAFOS directory.

        Args:
            filename: Name of the file (e.g., 'SWtinyG.txt')

        Returns:
            NetworkX graph
        """
        filepath = Path(__file__).parent.parent / 'data' / 'SW_ALGUNS_GRAFOS' / filename

        # Read first line to get number of vertices and edges
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            parts = first_line.split()
            n_vertices = int(parts[0])
            n_edges = int(parts[1])

            G = nx.Graph()
            G.add_nodes_from(range(n_vertices))

            # Read edges
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    G.add_edge(u, v)

        return G


class Validator:
    """Validation utilities for edge cover algorithms."""

    @staticmethod
    def verify_correctness(G: nx.Graph, edge_cover: Set[Tuple[int, int]]) -> Tuple[bool, str]:
        """
        Verify that edge_cover is a valid edge cover for G.

        Args:
            G: NetworkX graph
            edge_cover: Set of edges

        Returns:
            Tuple of (is_valid, message)
        """
        if not edge_cover:
            return False, "Edge cover is empty"

        # Check all edges are in the graph
        for u, v in edge_cover:
            if not G.has_edge(u, v) and not G.has_edge(v, u):
                return False, f"Edge ({u}, {v}) not in graph"

        # Check all vertices are covered
        covered = set()
        for u, v in edge_cover:
            covered.add(u)
            covered.add(v)

        uncovered = set(G.nodes()) - covered
        if uncovered:
            return False, f"Vertices {uncovered} are not covered"

        return True, "Valid edge cover"

    @staticmethod
    def check_approximation_ratio(
        actual_size: int,
        optimal_size: int,
        expected_ratio: float,
        algorithm_name: str
    ) -> Tuple[bool, str]:
        """
        Check if approximation ratio is satisfied.

        Args:
            actual_size: Size of returned edge cover
            optimal_size: Size of optimal edge cover
            expected_ratio: Expected approximation ratio
            algorithm_name: Name of algorithm being tested

        Returns:
            Tuple of (is_satisfied, message)
        """
        if optimal_size == 0:
            return False, "Optimal size is 0"

        actual_ratio = actual_size / optimal_size

        if actual_ratio <= expected_ratio + 0.01:  # Small tolerance for floating point
            return True, f"{algorithm_name}: {actual_ratio:.3f} ≤ {expected_ratio} ✓"
        else:
            return False, f"{algorithm_name}: {actual_ratio:.3f} > {expected_ratio} ✗"


class AlgorithmTester:
    """Test runner for individual algorithms."""

    def __init__(self):
        self.results = []

    def test_algorithm(
        self,
        algo_func: Callable,
        algo_name: str,
        graphs: Dict[str, nx.Graph],
        num_trials: int = 5,
        **algo_params
    ) -> Dict:
        """
        Test an algorithm on multiple graphs.

        Args:
            algo_func: Algorithm function to test
            algo_name: Name of algorithm
            graphs: Dictionary of test graphs
            num_trials: Number of trials per graph
            **algo_params: Additional parameters for algorithm

        Returns:
            Dictionary with test results
        """
        print(f"\n{'='*70}")
        print(f"Testing: {algo_name}")
        print(f"{'='*70}")

        results = {
            'algorithm': algo_name,
            'graphs': {},
            'all_valid': True
        }

        for graph_name, G in graphs.items():
            print(f"\nGraph: {graph_name} ({G.number_of_nodes()}v, {G.number_of_edges()}e)")

            # Check for isolated vertices
            isolated = [v for v in G.nodes() if G.degree(v) == 0]
            if isolated:
                print(f"  ⚠️  Skipping: has {len(isolated)} isolated vertices")
                continue

            # Run multiple trials
            sizes = []
            runtimes = []
            all_valid = True

            for trial in range(num_trials):
                try:
                    # Set different seed for randomized algorithms
                    params = algo_params.copy()
                    if 'seed' in algo_func.__code__.co_varnames:
                        params['seed'] = trial

                    edge_cover, metrics = algo_func(G, **params)

                    # Validate correctness
                    is_valid, msg = Validator.verify_correctness(G, edge_cover)
                    if not is_valid:
                        print(f"  ✗ Trial {trial}: {msg}")
                        all_valid = False
                        results['all_valid'] = False
                        continue

                    sizes.append(len(edge_cover))
                    runtimes.append(metrics['runtime'])

                except Exception as e:
                    print(f"  ✗ Trial {trial}: Error - {str(e)}")
                    all_valid = False
                    results['all_valid'] = False

            if sizes:
                mean_size = np.mean(sizes)
                std_size = np.std(sizes)
                mean_runtime = np.mean(runtimes)

                print(f"  ✓ Valid edge covers: {len(sizes)}/{num_trials}")
                print(f"  ✓ Cover size: {mean_size:.1f} ± {std_size:.2f}")
                print(f"  ✓ Runtime: {mean_runtime*1000:.2f}ms")

                results['graphs'][graph_name] = {
                    'valid_trials': len(sizes),
                    'mean_size': mean_size,
                    'std_size': std_size,
                    'mean_runtime': mean_runtime,
                    'all_valid': all_valid
                }

        return results

    def compare_with_optimal(
        self,
        algo_func: Callable,
        algo_name: str,
        graphs: Dict[str, nx.Graph],
        optimal_sizes: Dict[str, int],
        expected_ratio: float,
        num_trials: int = 5,
        **algo_params
    ):
        """
        Test algorithm and compare with known optimal solutions.

        Args:
            algo_func: Algorithm function
            algo_name: Algorithm name
            graphs: Test graphs
            optimal_sizes: Dictionary mapping graph names to optimal cover sizes
            expected_ratio: Expected approximation ratio
            num_trials: Number of trials
            **algo_params: Algorithm parameters
        """
        print(f"\n{'='*70}")
        print(f"Approximation Ratio Test: {algo_name}")
        print(f"Expected ratio: ≤ {expected_ratio}")
        print(f"{'='*70}")

        all_satisfied = True

        for graph_name, G in graphs.items():
            if graph_name not in optimal_sizes:
                continue

            optimal_size = optimal_sizes[graph_name]

            # Run trials
            sizes = []
            for trial in range(num_trials):
                params = algo_params.copy()
                if 'seed' in algo_func.__code__.co_varnames:
                    params['seed'] = trial

                try:
                    edge_cover, _ = algo_func(G, **params)
                    sizes.append(len(edge_cover))
                except Exception as e:
                    print(f"  ✗ {graph_name}: Error - {str(e)}")
                    continue

            if sizes:
                mean_size = np.mean(sizes)
                actual_ratio = mean_size / optimal_size

                is_satisfied, msg = Validator.check_approximation_ratio(
                    mean_size, optimal_size, expected_ratio, graph_name
                )

                print(f"  {graph_name}: {mean_size:.1f} / {optimal_size} = {actual_ratio:.3f} {'✓' if is_satisfied else '✗'}")

                if not is_satisfied:
                    all_satisfied = False

        return all_satisfied


def quick_test_exact():
    """Quick test for exact algorithm."""
    print("\n" + "="*70)
    print("QUICK TEST: Exact Algorithm")
    print("="*70)

    tester = AlgorithmTester()
    graphs = TestGraphs.get_small_graphs()

    results = tester.test_algorithm(
        exact_edge_cover,
        "Exact (Matching-based)",
        graphs,
        num_trials=3
    )

    return results['all_valid']


def quick_test_nearest_neighbor():
    """Quick test for nearest neighbor algorithm."""
    print("\n" + "="*70)
    print("QUICK TEST: Nearest Neighbor")
    print("="*70)

    tester = AlgorithmTester()
    graphs = TestGraphs.get_small_graphs()

    results = tester.test_algorithm(
        nearest_neighbor_edge_cover,
        "Nearest Neighbor (2-approx)",
        graphs,
        num_trials=5
    )

    return results['all_valid']


def quick_test_israeli_itai():
    """Quick test for Israeli-Itai algorithm."""
    print("\n" + "="*70)
    print("QUICK TEST: Israeli-Itai")
    print("="*70)

    tester = AlgorithmTester()
    graphs = TestGraphs.get_small_graphs()

    results = tester.test_algorithm(
        israeli_itai_edge_cover,
        "Israeli-Itai (Randomized Matching)",
        graphs,
        num_trials=5
    )

    return results['all_valid']


def quick_test_lazy_greedy():
    """Quick test for lazy greedy algorithm."""
    print("\n" + "="*70)
    print("QUICK TEST: Lazy Greedy")
    print("="*70)

    tester = AlgorithmTester()
    graphs = TestGraphs.get_small_graphs()

    results = tester.test_algorithm(
        lazy_greedy_edge_cover,
        "Lazy Greedy (3/2-approx)",
        graphs,
        num_trials=5
    )

    return results['all_valid']


def quick_test_simulated_annealing():
    """Quick test for simulated annealing algorithm."""
    print("\n" + "="*70)
    print("QUICK TEST: Simulated Annealing")
    print("="*70)

    tester = AlgorithmTester()
    graphs = TestGraphs.get_small_graphs()

    results = tester.test_algorithm(
        simulated_annealing_edge_cover,
        "Simulated Annealing",
        graphs,
        num_trials=5,
        max_iterations=1000  # Quick test with fewer iterations
    )

    return results['all_valid']


def comprehensive_test_suite():
    """
    Run comprehensive test suite on all algorithms.

    Tests all 5 algorithms on small and medium graphs with multiple trials.
    """
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST SUITE")
    print("="*70)

    # Get all graphs
    small_graphs = TestGraphs.get_small_graphs()
    medium_graphs = TestGraphs.get_medium_graphs()
    all_graphs = {**small_graphs, **medium_graphs}

    # Compute optimal solutions using exact algorithm
    print("\nComputing optimal solutions...")
    optimal_sizes = {}
    for name, G in all_graphs.items():
        isolated = [v for v in G.nodes() if G.degree(v) == 0]
        if not isolated:
            try:
                cover, _ = exact_edge_cover(G, timeout=60)
                optimal_sizes[name] = len(cover)
                print(f"  {name}: {len(cover)}")
            except:
                print(f"  {name}: timeout or error")

    # Test each algorithm
    tester = AlgorithmTester()

    algorithms = [
        (exact_edge_cover, "Exact", {}, None),
        (nearest_neighbor_edge_cover, "Nearest Neighbor", {}, 2.0),
        (israeli_itai_edge_cover, "Israeli-Itai", {}, None),
        (lazy_greedy_edge_cover, "Lazy Greedy", {}, 1.5),
        (simulated_annealing_edge_cover, "Simulated Annealing", {'max_iterations': 1000}, None),
    ]

    all_results = []

    for algo_func, algo_name, params, approx_ratio in algorithms:
        results = tester.test_algorithm(
            algo_func,
            algo_name,
            all_graphs,
            num_trials=5,
            **params
        )
        all_results.append(results)

        # Check approximation ratio if applicable
        if approx_ratio is not None:
            tester.compare_with_optimal(
                algo_func,
                algo_name,
                all_graphs,
                optimal_sizes,
                approx_ratio,
                num_trials=5,
                **params
            )

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for result in all_results:
        status = "✓ PASS" if result['all_valid'] else "✗ FAIL"
        print(f"{result['algorithm']:30s} {status}")

    return all_results


if __name__ == "__main__":
    """Run tests based on command line arguments."""
    import sys

    if len(sys.argv) > 1:
        test_name = sys.argv[1]

        if test_name == "exact":
            quick_test_exact()
        elif test_name == "nearest":
            quick_test_nearest_neighbor()
        elif test_name == "israeli":
            quick_test_israeli_itai()
        elif test_name == "greedy":
            quick_test_lazy_greedy()
        elif test_name == "sa":
            quick_test_simulated_annealing()
        elif test_name == "all":
            comprehensive_test_suite()
        else:
            print(f"Unknown test: {test_name}")
            print("Available: exact, nearest, israeli, greedy, sa, all")
    else:
        print("Usage: python test_algorithms.py [exact|nearest|israeli|greedy|sa|all]")
