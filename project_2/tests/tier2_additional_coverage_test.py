import sys
sys.path.insert(0, '/home/roldao/Desktop/MEI/AA/project_2')

from src.utils.graph_loader import load_facebook_ego, load_sw_graph
from src.algorithms.exact import exact_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover
import time
import pandas as pd

print("="*70)
print("TIER 2: ADDITIONAL COVERAGE TESTS")
print("="*70)
print("Goal: Test remaining ego networks and SW variants for diversity")
print("="*70)

results = []

# Define graphs to test
graphs_to_test = [
    ('ego-1684', lambda: load_facebook_ego('1684'), 'ego'),
    ('ego-3437', lambda: load_facebook_ego('3437'), 'ego'),
    ('ego-348', lambda: load_facebook_ego('348'), 'ego'),
    ('ego-686', lambda: load_facebook_ego('686'), 'ego'),
    ('SWmediumEWD', lambda: load_sw_graph('SWmediumEWD.txt'), 'sw'),
]

# Define algorithms to test (all 5)
algorithms = [
    ('exact', exact_edge_cover),
    ('lazy_greedy', lazy_greedy_edge_cover),
    ('nearest_neighbor', nearest_neighbor_edge_cover),
    ('israeli_itai', lambda g: israeli_itai_edge_cover(g, smart_proposals=True)),
    ('simulated_annealing', lambda g: simulated_annealing_edge_cover(g, initial_solution='lazy_greedy')),
]

print(f"\nTesting {len(graphs_to_test)} graphs with {len(algorithms)} algorithms")
print(f"Total tests: {len(graphs_to_test) * len(algorithms)}")
print("="*70)

for idx, (graph_name, graph_loader, graph_type) in enumerate(graphs_to_test, 1):
    print(f"\n[{idx}/{len(graphs_to_test)}] Testing {graph_name}")
    print("-"*70)

    try:
        G = graph_loader()
        n = G.number_of_nodes()
        m = G.number_of_edges()
        density = 2 * m / (n * (n - 1)) if n > 1 else 0

        print(f"Loaded: {n}v, {m}e, density={density:.4f}")

        # Test all algorithms
        for algo_name, algo_func in algorithms:
            print(f"  {algo_name}...", end=" ", flush=True)
            start = time.time()

            try:
                # Set timeout for exact algorithm (30 minutes)
                if algo_name == 'exact' and n > 500:
                    print("SKIPPED (too large for exact)")
                    continue

                cover, metrics = algo_func(G)
                elapsed = time.time() - start

                print(f"✅ {metrics['cover_size']} edges ({elapsed:.4f}s)")

                results.append({
                    'graph': graph_name,
                    'graph_type': graph_type,
                    'vertices': n,
                    'edges': m,
                    'density': density,
                    'algorithm': algo_name,
                    'cover_size': metrics['cover_size'],
                    'runtime': elapsed,
                    'success': True
                })

            except Exception as e:
                elapsed = time.time() - start
                print(f"❌ FAILED: {str(e)[:50]}")

                results.append({
                    'graph': graph_name,
                    'graph_type': graph_type,
                    'vertices': n,
                    'edges': m,
                    'density': density,
                    'algorithm': algo_name,
                    'cover_size': None,
                    'runtime': elapsed,
                    'success': False
                })

    except Exception as e:
        print(f"❌ Failed to load {graph_name}: {e}")
        continue

# Save results
print("\n" + "="*70)
print("SAVING RESULTS")
print("="*70)

df = pd.DataFrame(results)
output_file = '/home/roldao/Desktop/MEI/AA/project_2/results/tier2_additional_results.csv'
df.to_csv(output_file, index=False)
print(f"Results saved to: {output_file}")

# Summary statistics
print("\n" + "="*70)
print("TIER 2 ADDITIONAL COVERAGE COMPLETE")
print("="*70)
print(f"\nTotal tests run: {len(results)}")
print(f"Successful tests: {sum(1 for r in results if r['success'])}")
print(f"Failed tests: {sum(1 for r in results if not r['success'])}")
print(f"Success rate: {sum(1 for r in results if r['success']) / len(results) * 100:.1f}%")

print("\n" + "="*70)
print("RESULTS BY ALGORITHM")
print("="*70)
algo_summary = df.groupby('algorithm').agg({
    'success': ['count', 'sum'],
    'runtime': 'mean',
    'cover_size': 'mean'
})
print(algo_summary)

print("\n" + "="*70)
print("RESULTS BY GRAPH")
print("="*70)
graph_summary = df.groupby('graph').agg({
    'success': ['count', 'sum'],
    'vertices': 'first',
    'edges': 'first'
})
print(graph_summary)

print("\n" + "="*70)
print("DETAILED RESULTS")
print("="*70)
print(df.to_string(index=False))

print(f"\nResults saved to: {output_file}")
print("="*70)
