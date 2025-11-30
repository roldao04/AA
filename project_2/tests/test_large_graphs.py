"""
Large Graph Testing Suite

Tests all 5 edge cover algorithms on progressively larger SW graphs:
- Tiny (13 vertices)
- Medium (250 vertices)
- Large (1000 vertices)
- Very Large (10000 vertices)
- Extreme (100MB graph - optional)
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import networkx as nx
from typing import Dict, List, Tuple
import pandas as pd

from src.utils.graph_loader import load_sw_graph
from src.algorithms.exact import exact_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover


# SW graphs to test in order of increasing size
SW_GRAPHS = [
    ('SWtinyG.txt', 'Tiny', 60),        # ~13 vertices, 60s timeout
    ('SWmediumG.txt', 'Medium', 120),    # ~250 vertices, 120s timeout
    ('SW1000EWD.txt', 'Large', 300),     # 1000 vertices, 300s timeout
    ('SW10000EWD.txt', 'Very Large', 600), # 10000 vertices, 600s timeout
]


def test_single_algorithm(
    G: nx.Graph,
    algo_name: str,
    algo_func,
    graph_name: str,
    timeout: int,
    **algo_params
) -> Dict:
    """
    Test a single algorithm on a graph with timeout protection.

    Returns:
        Dictionary with results or error information
    """
    print(f"  Testing {algo_name}...", end=' ', flush=True)

    try:
        start = time.time()

        # Run algorithm
        if 'timeout' in algo_func.__code__.co_varnames:
            edge_cover, metrics = algo_func(G, timeout=timeout, **algo_params)
        else:
            edge_cover, metrics = algo_func(G, **algo_params)

        runtime = time.time() - start

        # Check if timed out
        if runtime > timeout:
            print(f"⚠️  TIMEOUT ({runtime:.1f}s)")
            return {
                'algorithm': algo_name,
                'graph': graph_name,
                'status': 'timeout',
                'cover_size': None,
                'runtime': runtime,
                'error': None
            }

        print(f"✓ size={len(edge_cover)}, {runtime*1000:.1f}ms")

        return {
            'algorithm': algo_name,
            'graph': graph_name,
            'status': 'success',
            'cover_size': len(edge_cover),
            'runtime': runtime,
            'metrics': metrics,
            'error': None
        }

    except TimeoutError as e:
        runtime = time.time() - start
        print(f"⚠️  TIMEOUT ({runtime:.1f}s)")
        return {
            'algorithm': algo_name,
            'graph': graph_name,
            'status': 'timeout',
            'cover_size': None,
            'runtime': runtime,
            'error': str(e)
        }

    except Exception as e:
        runtime = time.time() - start
        print(f"✗ ERROR: {str(e)[:50]}")
        return {
            'algorithm': algo_name,
            'graph': graph_name,
            'status': 'error',
            'cover_size': None,
            'runtime': runtime,
            'error': str(e)
        }


def test_graph(filename: str, graph_label: str, timeout: int) -> List[Dict]:
    """
    Test all algorithms on a single SW graph.

    Returns:
        List of result dictionaries
    """
    print(f"\n{'='*70}")
    print(f"Testing: {filename} ({graph_label})")
    print(f"{'='*70}")

    # Load graph
    try:
        G = load_sw_graph(filename)
        print(f"Graph loaded: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
        print(f"Density: {nx.density(G):.4f}")
        print(f"Timeout: {timeout}s\n")
    except Exception as e:
        print(f"✗ Failed to load graph: {e}")
        return []

    results = []

    # Test 1: Exact (may timeout on large graphs)
    result = test_single_algorithm(
        G, 'Exact', exact_edge_cover, graph_label, timeout
    )
    results.append(result)

    # Store optimal size for comparison
    optimal_size = result['cover_size'] if result['status'] == 'success' else None

    # Test 2: Nearest Neighbor (always fast)
    result = test_single_algorithm(
        G, 'Nearest Neighbor', nearest_neighbor_edge_cover, graph_label, timeout, seed=42
    )
    results.append(result)

    # Test 3: Israeli-Itai (fast randomized)
    result = test_single_algorithm(
        G, 'Israeli-Itai', israeli_itai_edge_cover, graph_label, timeout, seed=42
    )
    results.append(result)

    # Test 4: Lazy Greedy (best approximation)
    result = test_single_algorithm(
        G, 'Lazy Greedy', lazy_greedy_edge_cover, graph_label, timeout, seed=42
    )
    results.append(result)

    # Test 5: Simulated Annealing (with improved initial solution)
    # Use fewer iterations for very large graphs
    if G.number_of_nodes() > 5000:
        max_iter = 100 * G.number_of_nodes()
    elif G.number_of_nodes() > 1000:
        max_iter = 500 * G.number_of_nodes()
    else:
        max_iter = 1000 * G.number_of_nodes()

    result = test_single_algorithm(
        G, 'Simulated Annealing', simulated_annealing_edge_cover, graph_label, timeout,
        seed=42, max_iterations=max_iter, initial_solution='lazy_greedy'
    )
    results.append(result)

    # Print summary
    print(f"\n{'-'*70}")
    print("Summary:")
    if optimal_size:
        print(f"Optimal: {optimal_size} edges")

    for result in results:
        if result['status'] == 'success' and result['cover_size']:
            ratio = result['cover_size'] / optimal_size if optimal_size else None
            ratio_str = f" ({ratio:.3f}x)" if ratio else ""
            print(f"  {result['algorithm']:20s}: {result['cover_size']:4d} edges{ratio_str}, {result['runtime']*1000:7.1f}ms")
        else:
            print(f"  {result['algorithm']:20s}: {result['status'].upper()}")

    return results


def run_all_tests():
    """
    Run complete test suite on all SW graphs.
    """
    print("\n" + "="*70)
    print("LARGE GRAPH TEST SUITE")
    print("Testing all 5 algorithms on progressively larger SW graphs")
    print("="*70)

    all_results = []

    for filename, label, timeout in SW_GRAPHS:
        results = test_graph(filename, label, timeout)
        all_results.extend(results)

    # Create summary DataFrame
    print("\n" + "="*70)
    print("OVERALL SUMMARY")
    print("="*70)

    df = pd.DataFrame(all_results)

    print("\nSuccess Rates by Algorithm:")
    success_counts = df.groupby('algorithm')['status'].apply(
        lambda x: f"{(x == 'success').sum()}/{len(x)}"
    )
    print(success_counts)

    print("\nAverage Cover Size (successful runs only):")
    successful = df[df['status'] == 'success']
    if not successful.empty:
        avg_sizes = successful.groupby('algorithm')['cover_size'].mean()
        print(avg_sizes.sort_values())

    print("\nAverage Runtime (successful runs only):")
    if not successful.empty:
        avg_runtimes = successful.groupby('algorithm')['runtime'].mean()
        print(avg_runtimes.sort_values())

    # Save results
    results_path = Path(__file__).parent.parent / 'results' / 'large_graph_results.csv'
    df.to_csv(results_path, index=False)
    print(f"\nResults saved to: {results_path}")

    return df


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Test specific graph
        graph_name = sys.argv[1]

        # Find matching graph
        matching = [g for g in SW_GRAPHS if graph_name.lower() in g[1].lower()]

        if matching:
            filename, label, timeout = matching[0]
            test_graph(filename, label, timeout)
        else:
            print(f"Unknown graph: {graph_name}")
            print(f"Available: {', '.join([g[1] for g in SW_GRAPHS])}")
    else:
        # Run all tests
        run_all_tests()
