"""
TIER 1 COMPREHENSIVE TEST
Tests all 12 critical graphs with all algorithms
Goal: Prove SCALE (10k-12k vertices) and DENSITY (p=0.9)
"""
import sys
sys.path.insert(0, '/home/roldao/Desktop/MEI/AA/project_2')

from src.utils.graph_loader import load_sw_graph, load_snap_graph, load_facebook_ego, load_dimacs_graph
from src.algorithms.exact import exact_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover
import networkx as nx
import pandas as pd
import time

def test_graph(name, G, run_exact=True, exact_timeout=600, run_sa=True):
    """
    Test all algorithms on a graph

    Args:
        name: Graph name
        G: NetworkX graph
        run_exact: Whether to run exact algorithm
        exact_timeout: Timeout for exact in seconds
        run_sa: Whether to run SA (skip for very large graphs)
    """
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")

    n = G.number_of_nodes()
    m = G.number_of_edges()
    density = 2 * m / (n * (n - 1)) if n > 1 else 0

    print(f"Graph: {n} vertices, {m} edges, density={density:.4f}")

    results = {
        'graph_name': name,
        'vertices': n,
        'edges': m,
        'density': density
    }

    optimal = None

    # Algorithm 1: Exact (with timeout)
    if run_exact:
        print(f"\n[1/5] Running EXACT (timeout: {exact_timeout}s)...", end=" ", flush=True)
        try:
            start = time.time()
            exact_cover, exact_metrics = exact_edge_cover(G)
            elapsed = time.time() - start

            if elapsed > exact_timeout:
                print(f"TIMEOUT ({elapsed:.2f}s)")
                results['exact_size'] = None
                results['exact_runtime'] = None
                results['exact_status'] = 'timeout'
            else:
                optimal = exact_metrics['cover_size']
                results['exact_size'] = optimal
                results['exact_runtime'] = exact_metrics['runtime']
                results['exact_status'] = 'success'
                print(f"✅ {optimal} edges ({exact_metrics['runtime']:.4f}s)")
        except Exception as e:
            print(f"ERROR: {str(e)[:50]}")
            results['exact_size'] = None
            results['exact_runtime'] = None
            results['exact_status'] = 'error'
    else:
        print(f"\n[1/5] EXACT skipped (graph too large)")
        results['exact_size'] = None
        results['exact_runtime'] = None
        results['exact_status'] = 'skipped'

    # Algorithm 2: Lazy Greedy
    print(f"[2/5] Running LAZY GREEDY...", end=" ", flush=True)
    lg_cover, lg_metrics = lazy_greedy_edge_cover(G)
    results['lg_size'] = lg_metrics['cover_size']
    results['lg_runtime'] = lg_metrics['runtime']
    results['lg_ratio'] = lg_metrics['cover_size'] / optimal if optimal else None
    print(f"✅ {lg_metrics['cover_size']} edges ({lg_metrics['runtime']:.4f}s)", end="")
    if optimal:
        print(f" = {results['lg_ratio']:.4f}x")
    else:
        print()

    # Algorithm 3: Nearest Neighbor
    print(f"[3/5] Running NEAREST NEIGHBOR...", end=" ", flush=True)
    nn_cover, nn_metrics = nearest_neighbor_edge_cover(G)
    results['nn_size'] = nn_metrics['cover_size']
    results['nn_runtime'] = nn_metrics['runtime']
    results['nn_ratio'] = nn_metrics['cover_size'] / optimal if optimal else None
    print(f"✅ {nn_metrics['cover_size']} edges ({nn_metrics['runtime']:.4f}s)", end="")
    if optimal:
        print(f" = {results['nn_ratio']:.4f}x")
    else:
        print()

    # Algorithm 4: Israeli-Itai (IMPROVED)
    print(f"[4/5] Running ISRAELI-ITAI (improved)...", end=" ", flush=True)
    ii_cover, ii_metrics = israeli_itai_edge_cover(G, smart_proposals=True)
    results['ii_size'] = ii_metrics['cover_size']
    results['ii_runtime'] = ii_metrics['runtime']
    results['ii_ratio'] = ii_metrics['cover_size'] / optimal if optimal else None
    print(f"✅ {ii_metrics['cover_size']} edges ({ii_metrics['runtime']:.4f}s)", end="")
    if optimal:
        print(f" = {results['ii_ratio']:.4f}x")
    else:
        print()

    # Algorithm 5: Simulated Annealing (OPTIMIZED)
    if run_sa:
        print(f"[5/5] Running SA (optimized)...", end=" ", flush=True)
        try:
            sa_cover, sa_metrics = simulated_annealing_edge_cover(G, initial_solution='lazy_greedy')
            results['sa_size'] = sa_metrics['cover_size']
            results['sa_runtime'] = sa_metrics['runtime']
            results['sa_ratio'] = sa_metrics['cover_size'] / optimal if optimal else None
            print(f"✅ {sa_metrics['cover_size']} edges ({sa_metrics['runtime']:.4f}s)", end="")
            if optimal:
                print(f" = {results['sa_ratio']:.4f}x")
            else:
                print()
        except Exception as e:
            print(f"ERROR: {str(e)[:50]}")
            results['sa_size'] = None
            results['sa_runtime'] = None
            results['sa_ratio'] = None
    else:
        print(f"[5/5] SA skipped (graph too large)")
        results['sa_size'] = None
        results['sa_runtime'] = None
        results['sa_ratio'] = None

    # Summary
    if optimal:
        print(f"\nQuality Summary (vs optimal {optimal}):")
        print(f"  Lazy Greedy: {results['lg_ratio']:.4f}x | Israeli-Itai: {results['ii_ratio']:.4f}x | NN: {results['nn_ratio']:.4f}x")

    return results


# ============================================================================
# MAIN TEST SUITE
# ============================================================================

print("="*70)
print("TIER 1 COMPREHENSIVE TEST SUITE")
print("="*70)
print("Goal: Prove SCALE (10k-12k vertices) and DENSITY (p=0.9)")
print("Testing 12 critical graphs with all 5 algorithms")
print("="*70)

all_results = []

# Graph 1: SWtinyG (baseline validation)
print("\n" + "🔹"*35)
print("GRAPH 1/12: SWtinyG (13v) - Baseline Validation")
print("🔹"*35)
G = load_sw_graph('SWtinyG.txt')
all_results.append(test_graph("SWtinyG", G, run_exact=True, run_sa=True))

# Graph 2: Karate (NetworkX validation)
print("\n" + "🔹"*35)
print("GRAPH 2/12: Karate Club (34v) - NetworkX Validation")
print("🔹"*35)
G = nx.karate_club_graph()
G.remove_edges_from(nx.selfloop_edges(G))
all_results.append(test_graph("karate", G, run_exact=True, run_sa=True))

# Graph 3: SWmediumG (medium baseline)
print("\n" + "🔹"*35)
print("GRAPH 3/12: SWmediumG (250v) - Medium Baseline")
print("🔹"*35)
G = load_sw_graph('SWmediumG.txt')
all_results.append(test_graph("SWmediumG", G, run_exact=True, run_sa=True))

# Graph 4: SW1000EWD (1k sparse baseline)
print("\n" + "🔹"*35)
print("GRAPH 4/12: SW1000EWD (1000v, sparse) - 1k Sparse Baseline ⭐")
print("🔹"*35)
G = load_sw_graph('SW1000EWD.txt')
all_results.append(test_graph("SW1000EWD", G, run_exact=True, exact_timeout=600, run_sa=True))

# Graph 5: C1000.9 (1k ultra-dense) ⭐⭐⭐ CRITICAL FOR DENSITY STUDY
print("\n" + "🔹"*35)
print("GRAPH 5/12: C1000.9 (1000v, 450k edges, p=0.9) - DENSITY PROOF ⭐⭐⭐")
print("🔹"*35)
G = load_dimacs_graph('C1000.9/c1000.txt')
all_results.append(test_graph("C1000.9", G, run_exact=True, exact_timeout=1800, run_sa=False))

# Graph 6: ego-698 (tiny dense)
print("\n" + "🔹"*35)
print("GRAPH 6/12: ego-698 (62v, dense) - Tiny Dense Ego Network")
print("🔹"*35)
G = load_facebook_ego('698')
all_results.append(test_graph("ego-698", G, run_exact=True, run_sa=True))

# Graph 7: ego-414 (small very dense)
print("\n" + "🔹"*35)
print("GRAPH 7/12: ego-414 (150v, very dense) - Small Dense Network")
print("🔹"*35)
try:
    G = load_facebook_ego('414')
    all_results.append(test_graph("ego-414", G, run_exact=True, run_sa=True))
except Exception as e:
    print(f"⚠️  Failed to load ego-414: {e}")

# Graph 8: ego-0 (medium ego)
print("\n" + "🔹"*35)
print("GRAPH 8/12: ego-0 (333v) - Medium Ego Network")
print("🔹"*35)
G = load_facebook_ego('0')
all_results.append(test_graph("ego-0", G, run_exact=True, run_sa=True))

# Graph 9: email-Eu-core (1k SNAP baseline)
print("\n" + "🔹"*35)
print("GRAPH 9/12: email-Eu-core (1005v) - SNAP Baseline")
print("🔹"*35)
try:
    G = load_snap_graph('email_eu_core/email-Eu-core.txt')
    all_results.append(test_graph("email-Eu-core", G, run_exact=True, run_sa=True))
except Exception as e:
    print(f"⚠️  Failed to load email-Eu-core: {e}")

# Graph 10: CA-GrQc (5k sparse)
print("\n" + "🔹"*35)
print("GRAPH 10/12: CA-GrQc (5242v) - Large Sparse Collaboration")
print("🔹"*35)
G = load_snap_graph('ca-grqc/CA-GrQc.txt')
all_results.append(test_graph("CA-GrQc", G, run_exact=False, run_sa=False))

# Graph 11: SW10000EWD (10k vertices) ⭐⭐⭐ CRITICAL FOR SCALE PROOF
print("\n" + "🔹"*35)
print("GRAPH 11/12: SW10000EWD (10000v) - SCALE PROOF ⭐⭐⭐")
print("🔹"*35)
try:
    G = load_sw_graph('SW10000EWD.txt')
    all_results.append(test_graph("SW10000EWD", G, run_exact=False, run_sa=False))
except Exception as e:
    print(f"⚠️  Failed to load SW10000EWD: {e}")

# Graph 12: CA-HepPh (12k vertices) ⭐⭐⭐ CRITICAL FOR MAXIMUM SCALE
print("\n" + "🔹"*35)
print("GRAPH 12/12: CA-HepPh (12008v) - MAXIMUM SCALE PROOF ⭐⭐⭐")
print("🔹"*35)
try:
    G = load_snap_graph('ca-hepph/CA-HepPh.txt')
    all_results.append(test_graph("CA-HepPh", G, run_exact=False, run_sa=False))
except Exception as e:
    print(f"⚠️  Failed to load CA-HepPh: {e}")

# ============================================================================
# SUMMARY & EXPORT
# ============================================================================

print("\n" + "="*70)
print("TIER 1 COMPREHENSIVE TEST COMPLETE!")
print("="*70)

# Create DataFrame
df = pd.DataFrame(all_results)

# Save to CSV
output_file = 'results/tier1_comprehensive_results.csv'
df.to_csv(output_file, index=False)
print(f"\n✅ Results saved to: {output_file}")

# Print summary table
print(f"\n{'='*70}")
print("SUMMARY TABLE")
print(f"{'='*70}")
print(df[['graph_name', 'vertices', 'edges', 'density', 'exact_size', 'lg_size', 'nn_size', 'ii_size']].to_string(index=False))

# Print key achievements
print(f"\n{'='*70}")
print("KEY ACHIEVEMENTS")
print(f"{'='*70}")

# Scale achievements
max_vertices = df['vertices'].max()
print(f"✅ Maximum scale tested: {max_vertices} vertices")
if max_vertices >= 10000:
    print(f"   ⭐ SCALE PROOF: Tested graphs with 10k+ vertices!")

# Density achievements
max_density = df['density'].max()
print(f"✅ Maximum density tested: {max_density:.4f}")
if max_density >= 0.9:
    print(f"   ⭐ DENSITY PROOF: Tested ultra-dense graphs (p≈0.9)!")

# Algorithm performance
print(f"\n✅ Algorithm quality (average where optimal known):")
if 'lg_ratio' in df.columns:
    lg_avg = df['lg_ratio'].dropna().mean()
    nn_avg = df['nn_ratio'].dropna().mean()
    ii_avg = df['ii_ratio'].dropna().mean()
    print(f"   Lazy Greedy: {lg_avg:.4f}x optimal")
    print(f"   Israeli-Itai: {ii_avg:.4f}x optimal")
    print(f"   Nearest Neighbor: {nn_avg:.4f}x optimal")

print(f"\n{'='*70}")
print("PHASE 2 COMPLETE! Ready for implementation_3.md documentation.")
print(f"{'='*70}")
