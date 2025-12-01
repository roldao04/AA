import sys
sys.path.insert(0, '/home/roldao/Desktop/MEI/AA/project_2')

from src.utils.graph_loader import load_facebook_ego, load_dimacs_graph
from src.algorithms.exact import exact_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover
import time
import pandas as pd
import signal
from contextlib import contextmanager
from pathlib import Path


# Timeout mechanism for SA test
class TimeoutException(Exception):
    """Exception raised when algorithm exceeds timeout"""
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out long-running operations"""
    def signal_handler(signum, frame):
        raise TimeoutException(f"Operation timed out after {seconds} seconds")

    old_handler = signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


# Create results directory
Path('results').mkdir(exist_ok=True)
output_file = 'results/tier2_sa_validation_results.csv'

# SA timeout configuration
SA_TIMEOUT = 300  # 5 minutes = decision threshold


def save_intermediate_results(results):
    """Save results to CSV after each algorithm completes"""
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"  💾 Intermediate results saved ({len(results)} tests)")
    return df

print("="*70)
print("TIER 2: SA VALIDATION ON BIGGER GRAPHS")
print("="*70)
print("Goal: Determine if SA should be included in overnight experiments")
print("Decision criteria: SA completes C2000.9 in <5 minutes")
print("="*70)

results = []

# Test 1: ego-1912 (747v)
print("\n[1/3] Testing ego-1912 (747v, 60k edges)")
print("Loading graph...", end=" ", flush=True)
try:
    G = load_facebook_ego('1912')
    print(f"✅ Loaded: {G.number_of_nodes()}v, {G.number_of_edges()}e")

    # Test all algorithms for comparison
    for algo_name, algo_func in [
        ('lazy_greedy', lazy_greedy_edge_cover),
        ('nearest_neighbor', nearest_neighbor_edge_cover),
        ('israeli_itai', lambda g: israeli_itai_edge_cover(g, smart_proposals=True)),
        ('simulated_annealing', lambda g: simulated_annealing_edge_cover(g, initial_solution='lazy_greedy'))
    ]:
        print(f"  Running {algo_name}...", end=" ", flush=True)
        start = time.time()
        try:
            cover, metrics = algo_func(G)
            elapsed = time.time() - start
            print(f"✅ {metrics['cover_size']} edges ({elapsed:.4f}s)")
            results.append({
                'graph': 'ego-1912',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': metrics['cover_size'],
                'runtime': elapsed,
                'success': True
            })
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ FAILED: {e}")
            results.append({
                'graph': 'ego-1912',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': None,
                'runtime': elapsed,
                'success': False
            })

        # Save after each algorithm
        save_intermediate_results(results)

except Exception as e:
    print(f"❌ Failed to load ego-1912: {e}")

# Test 2: ego-107 (1034v)
print("\n[2/3] Testing ego-107 (1034v, 53k edges)")
print("Loading graph...", end=" ", flush=True)
try:
    G = load_facebook_ego('107')
    print(f"✅ Loaded: {G.number_of_nodes()}v, {G.number_of_edges()}e")

    for algo_name, algo_func in [
        ('lazy_greedy', lazy_greedy_edge_cover),
        ('nearest_neighbor', nearest_neighbor_edge_cover),
        ('israeli_itai', lambda g: israeli_itai_edge_cover(g, smart_proposals=True)),
        ('simulated_annealing', lambda g: simulated_annealing_edge_cover(g, initial_solution='lazy_greedy'))
    ]:
        print(f"  Running {algo_name}...", end=" ", flush=True)
        start = time.time()
        try:
            cover, metrics = algo_func(G)
            elapsed = time.time() - start
            print(f"✅ {metrics['cover_size']} edges ({elapsed:.4f}s)")
            results.append({
                'graph': 'ego-107',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': metrics['cover_size'],
                'runtime': elapsed,
                'success': True
            })
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ FAILED: {e}")
            results.append({
                'graph': 'ego-107',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': None,
                'runtime': elapsed,
                'success': False
            })

        # Save after each algorithm
        save_intermediate_results(results)

except Exception as e:
    print(f"❌ Failed to load ego-107: {e}")

# Test 3: C2000.9 (2000v, 1.8M edges) - CRITICAL DECISION POINT
print("\n[3/3] Testing C2000.9 (2000v, 1.8M edges, p=0.9) ⚠️ CRITICAL")
print("="*70)
print("THIS IS THE SA DECISION POINT")
print("="*70)
print("Loading graph (may take time - 19MB file)...", end=" ", flush=True)

sa_decision = None

try:
    G = load_dimacs_graph('C2000.9/c2000.txt')
    print(f"✅ Loaded: {G.number_of_nodes()}v, {G.number_of_edges()}e")

    # Test fast algorithms first
    for algo_name, algo_func in [
        ('lazy_greedy', lazy_greedy_edge_cover),
        ('nearest_neighbor', nearest_neighbor_edge_cover),
    ]:
        print(f"  Running {algo_name}...", end=" ", flush=True)
        start = time.time()
        try:
            cover, metrics = algo_func(G)
            elapsed = time.time() - start
            print(f"✅ {metrics['cover_size']} edges ({elapsed:.4f}s)")
            results.append({
                'graph': 'C2000.9',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': metrics['cover_size'],
                'runtime': elapsed,
                'success': True
            })
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ FAILED: {e}")
            results.append({
                'graph': 'C2000.9',
                'vertices': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'algorithm': algo_name,
                'cover_size': None,
                'runtime': elapsed,
                'success': False
            })

        # Save after each fast algorithm
        save_intermediate_results(results)

    # Now the critical SA test
    print("\n  " + "="*66)
    print("  SIMULATED ANNEALING TEST - DECISION POINT")
    print("  " + "="*66)
    print(f"  Running simulated_annealing with {SA_TIMEOUT}s timeout...", flush=True)
    print(f"  If completes in <{SA_TIMEOUT}s → INCLUDE SA in overnight")
    print(f"  If >{SA_TIMEOUT}s or fails → EXCLUDE SA from overnight")
    print()

    start = time.time()
    try:
        # Wrap SA with timeout
        with timeout(SA_TIMEOUT):
            sa_cover, sa_metrics = simulated_annealing_edge_cover(G, initial_solution='lazy_greedy')
        elapsed = time.time() - start

        print(f"  ✅ SA COMPLETED: {sa_metrics['cover_size']} edges in {elapsed:.2f}s")
        results.append({
            'graph': 'C2000.9',
            'vertices': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'algorithm': 'simulated_annealing',
            'cover_size': sa_metrics['cover_size'],
            'runtime': elapsed,
            'success': True
        })

        # Save after SA success
        save_intermediate_results(results)

        print("\n  " + "="*66)
        if elapsed < SA_TIMEOUT:
            print("  ✅✅✅ DECISION: INCLUDE SA IN OVERNIGHT EXPERIMENTS ✅✅✅")
            print(f"  Rationale: SA completed C2000.9 in {elapsed:.2f}s < {SA_TIMEOUT}s threshold")
            print("  SA will be enabled for small/medium graphs in overnight run")
            sa_decision = "INCLUDE"
        else:
            print("  ⚠️⚠️⚠️ DECISION: EXCLUDE SA FROM OVERNIGHT EXPERIMENTS ⚠️⚠️⚠️")
            print(f"  Rationale: SA completed in {elapsed:.2f}s ≈ {SA_TIMEOUT}s threshold")
            print("  SA deemed too slow for production use on larger graphs")
            sa_decision = "EXCLUDE"
        print("  " + "="*66)

    except TimeoutException:
        elapsed = time.time() - start
        print(f"  ⏰ SA TIMEOUT after {elapsed:.2f}s (>{SA_TIMEOUT}s limit)")
        print(f"  SA exceeded {SA_TIMEOUT/60:.1f} minute threshold")
        results.append({
            'graph': 'C2000.9',
            'vertices': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'algorithm': 'simulated_annealing',
            'cover_size': None,
            'runtime': SA_TIMEOUT,
            'success': False
        })

        # Save after SA timeout
        save_intermediate_results(results)

        print("\n  " + "="*66)
        print("  ❌❌❌ DECISION: EXCLUDE SA FROM OVERNIGHT EXPERIMENTS ❌❌❌")
        print(f"  Rationale: SA timeout on C2000.9 after {SA_TIMEOUT}s")
        print("  SA deemed too slow for production use on larger graphs")
        print("  " + "="*66)
        sa_decision = "EXCLUDE"

    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ SA FAILED: {e}")
        print(f"  Elapsed before failure: {elapsed:.2f}s")
        results.append({
            'graph': 'C2000.9',
            'vertices': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'algorithm': 'simulated_annealing',
            'cover_size': None,
            'runtime': elapsed,
            'success': False
        })

        # Save after SA failure
        save_intermediate_results(results)

        print("\n  " + "="*66)
        print("  ❌❌❌ DECISION: EXCLUDE SA FROM OVERNIGHT EXPERIMENTS ❌❌❌")
        print(f"  Rationale: SA failed on C2000.9 after {elapsed:.2f}s")
        print("  SA deemed unreliable for production use")
        print("  " + "="*66)
        sa_decision = "EXCLUDE"

except Exception as e:
    print(f"❌ Failed to load C2000.9: {e}")
    print("\n  ❌ DECISION: EXCLUDE SA (cannot test without C2000.9)")
    sa_decision = "EXCLUDE"

# Save results
print("\n" + "="*70)
print("SAVING RESULTS")
print("="*70)

df = pd.DataFrame(results)
output_file = '/home/roldao/Desktop/MEI/AA/project_2/results/tier2_sa_validation_results.csv'
df.to_csv(output_file, index=False)
print(f"Results saved to: {output_file}")

# Summary
print("\n" + "="*70)
print("TIER 2 SA VALIDATION COMPLETE")
print("="*70)
print(df.to_string(index=False))

print("\n" + "="*70)
print("FINAL SA DECISION FOR OVERNIGHT EXPERIMENTS")
print("="*70)
if sa_decision:
    print(f"DECISION: {sa_decision} SA")

    # Save decision to file for easy reference
    with open('/home/roldao/Desktop/MEI/AA/project_2/results/sa_decision.txt', 'w') as f:
        f.write(f"SA_DECISION: {sa_decision}\n")
        f.write(f"Test Date: {pd.Timestamp.now()}\n")
        f.write("\nRationale:\n")
        if sa_decision == "INCLUDE":
            sa_row = df[(df['graph'] == 'C2000.9') & (df['algorithm'] == 'simulated_annealing')]
            if not sa_row.empty and sa_row.iloc[0]['success']:
                runtime = sa_row.iloc[0]['runtime']
                f.write(f"- SA completed C2000.9 (2000v, 1.8M edges) in {runtime:.2f}s\n")
                f.write(f"- Runtime < 300s threshold: PASSED\n")
                f.write(f"- SA will be enabled for graphs with size_category: tiny, small, medium\n")
        else:
            f.write(f"- SA failed to meet performance criteria on C2000.9\n")
            f.write(f"- SA will be excluded from overnight experiments\n")

    print(f"Decision saved to: results/sa_decision.txt")
else:
    print("ERROR: Could not determine SA decision (tests may have failed)")

print("="*70)
