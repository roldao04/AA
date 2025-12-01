"""
Tier 3 Mega-Scale Testing - YouTube, LiveJournal, Orkut

This script tests the edge cover algorithms on MASSIVE social network graphs:
- YouTube: 1.1M vertices, 3M edges
- LiveJournal: 4M vertices, 34.7M edges
- Orkut: 3M vertices, 117M edges (ultra-dense!)

Algorithms tested: Lazy Greedy, Nearest Neighbor, Israeli-Itai
(Exact and SA excluded - impractical for graphs this large)

Expected runtime: 30-90 minutes total
Goal: Demonstrate exceptional scalability beyond 1M vertices

Date: November 30, 2025
"""

import sys
from pathlib import Path
from datetime import datetime
import time
import pandas as pd
import signal
from contextlib import contextmanager
import gc
import psutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.utils.graph_loader import load_snap_graph, load_snap_graph_memory_efficient


# Timeout configuration
TIMEOUT_SECONDS = 7200  # 2 hours per algorithm (extended for large graphs)


def get_memory_usage_gb():
    """Get current process memory usage in GB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 3)


class TimeoutException(Exception):
    """Exception raised when algorithm exceeds timeout"""
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out long-running operations"""
    def signal_handler(signum, frame):
        raise TimeoutException(f"Operation timed out after {seconds} seconds")

    # Set the signal handler
    old_handler = signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        # Restore the old handler and cancel the alarm
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def test_algorithm(G, algorithm_name, algorithm_func, timeout_sec):
    """
    Test a single algorithm on a graph with timeout protection.

    Returns:
        tuple: (cover_size, runtime, success)
    """
    print(f"\n{'='*80}")
    print(f"Testing {algorithm_name}...")
    print(f"Timeout: {timeout_sec}s ({timeout_sec/60:.1f} minutes)")

    # Force garbage collection before algorithm
    gc.collect()
    print(f"Memory before: {get_memory_usage_gb():.2f} GB")
    print(f"{'='*80}")

    try:
        with timeout(timeout_sec):
            start_time = time.time()
            start_memory = get_memory_usage_gb()

            # CRITICAL FIX: Unpack tuple (edge_cover, metrics)
            cover, metrics = algorithm_func(G)

            runtime = time.time() - start_time
            end_memory = get_memory_usage_gb()
            cover_size = len(cover)

            print(f"✅ SUCCESS: {algorithm_name}")
            print(f"   Cover size: {cover_size:,} edges")
            print(f"   Runtime: {runtime:.2f}s ({runtime/60:.2f} minutes)")
            print(f"   Memory after: {end_memory:.2f} GB (Δ{end_memory - start_memory:+.2f} GB)")

            # Cleanup after algorithm
            del cover
            gc.collect()
            print(f"   Memory after cleanup: {get_memory_usage_gb():.2f} GB")

            return cover_size, runtime, True

    except TimeoutException:
        print(f"⏰ TIMEOUT: {algorithm_name} exceeded {timeout_sec}s")
        gc.collect()
        return None, timeout_sec, False

    except MemoryError:
        print(f"💾 MEMORY ERROR: {algorithm_name} ran out of memory")
        gc.collect()
        return None, None, False

    except Exception as e:
        print(f"❌ ERROR: {algorithm_name} failed with: {str(e)}")
        gc.collect()
        return None, None, False


def run_tier3_mega_tests():
    """
    Run Tier 3 mega-scale tests on YouTube, LiveJournal, and Orkut.
    """
    print("="*80)
    print("TIER 3 MEGA-SCALE TESTING")
    print("Testing on graphs with 1M-4M vertices, up to 117M edges")
    print("="*80)
    print()

    # Test configurations
    test_graphs = [
        {
            'name': 'YouTube',
            'path': 'youtube/com-youtube.ungraph.txt',
            'expected_v': 1134890,
            'expected_e': 2987624,
            'timeout': TIMEOUT_SECONDS
        },
        {
            'name': 'LiveJournal',
            'path': 'live_journal/com-lj.ungraph.txt',
            'expected_v': 3997962,
            'expected_e': 34681189,
            'timeout': TIMEOUT_SECONDS
        },
        {
            'name': 'Orkut',
            'path': 'orkut/com-orkut.ungraph.txt',
            'expected_v': 3072441,
            'expected_e': 117185083,
            'timeout': TIMEOUT_SECONDS
        }
    ]

    # Algorithms to test (no Exact or SA - too slow for mega graphs)
    algorithms = [
        ('lazy_greedy', lazy_greedy_edge_cover),
        ('nearest_neighbor', nearest_neighbor_edge_cover),
        ('israeli_itai', israeli_itai_edge_cover)
    ]

    results = []

    # Test each graph
    for graph_config in test_graphs:
        print(f"\n{'#'*80}")
        print(f"# LOADING: {graph_config['name']}")
        print(f"# Expected: {graph_config['expected_v']:,} vertices, {graph_config['expected_e']:,} edges")
        print(f"{'#'*80}\n")

        try:
            print(f"Initial memory: {get_memory_usage_gb():.2f} GB")

            load_start = time.time()

            # Use memory-efficient loader for LiveJournal and Orkut (massive graphs)
            # Use regular loader for YouTube (smaller, already works fine)
            if graph_config['name'] in ['LiveJournal', 'Orkut']:
                print(f"Using memory-efficient loader for {graph_config['name']}...")
                G = load_snap_graph_memory_efficient(graph_config['path'])
            else:
                G = load_snap_graph(graph_config['path'])

            load_time = time.time() - load_start

            n = G.number_of_nodes()
            m = G.number_of_edges()
            memory_after_load = get_memory_usage_gb()

            print(f"\n✅ Graph loaded successfully in {load_time:.2f}s ({load_time/60:.2f} minutes)")
            print(f"   Vertices: {n:,}")
            print(f"   Edges: {m:,}")
            print(f"   Density: {2*m / (n*(n-1)):.6f}" if n > 1 else "   Density: N/A")
            print(f"   Memory after load: {memory_after_load:.2f} GB")

            # Test each algorithm
            for algo_name, algo_func in algorithms:
                cover_size, runtime, success = test_algorithm(
                    G,
                    algo_name,
                    algo_func,
                    graph_config['timeout']
                )

                results.append({
                    'graph': graph_config['name'],
                    'vertices': n,
                    'edges': m,
                    'algorithm': algo_name,
                    'cover_size': cover_size,
                    'runtime': runtime,
                    'success': success
                })

                # Save intermediate results after each algorithm
                df = pd.DataFrame(results)
                df.to_csv('results/tier3_mega_scale_results.csv', index=False)
                print(f"💾 Intermediate results saved to results/tier3_mega_scale_results.csv")

            # Cleanup graph from memory before moving to next graph
            print(f"\nCleaning up {graph_config['name']} from memory...")
            print(f"   Memory before cleanup: {get_memory_usage_gb():.2f} GB")
            del G
            gc.collect()
            print(f"   Memory after cleanup: {get_memory_usage_gb():.2f} GB")

        except FileNotFoundError as e:
            print(f"❌ ERROR: Could not load {graph_config['name']}: {e}")
            continue

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR loading {graph_config['name']}: {e}")
            continue

    # Final summary
    print(f"\n{'='*80}")
    print("TIER 3 MEGA-SCALE TESTING COMPLETE")
    print(f"{'='*80}\n")

    df = pd.DataFrame(results)

    print("SUMMARY STATISTICS:")
    print(f"Total tests: {len(results)}")
    print(f"Successful: {df['success'].sum()}")
    print(f"Failed/Timeout: {(~df['success']).sum()}")
    print()

    print("RESULTS BY GRAPH:")
    for graph_name in df['graph'].unique():
        graph_df = df[df['graph'] == graph_name]
        success_count = graph_df['success'].sum()
        total_count = len(graph_df)
        print(f"\n{graph_name}: {success_count}/{total_count} algorithms succeeded")

        for _, row in graph_df.iterrows():
            status = "✅" if row['success'] else "❌"
            if row['success']:
                print(f"  {status} {row['algorithm']}: {row['cover_size']:,} edges, {row['runtime']:.2f}s")
            else:
                print(f"  {status} {row['algorithm']}: FAILED")

    # Save final results
    output_file = 'results/tier3_mega_scale_results.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Final results saved to {output_file}")

    # Achievement unlock messages
    print(f"\n{'='*80}")
    print("ACHIEVEMENTS UNLOCKED:")
    print(f"{'='*80}")

    successful_graphs = df[df['success']].groupby('graph')['vertices'].first()

    if 'YouTube' in successful_graphs:
        print("🏆 YOUTUBE CONQUERED - 1.1M vertices tested!")

    if 'LiveJournal' in successful_graphs:
        print("🏆🏆 LIVEJOURNAL CONQUERED - 4M vertices! EXCEPTIONAL SCALABILITY!")

    if 'Orkut' in successful_graphs:
        print("🏆🏆🏆 ORKUT CONQUERED - 117M EDGES! HALL OF FAME ACHIEVEMENT!")

    print(f"{'='*80}\n")

    return df


if __name__ == "__main__":
    print(f"Starting Tier 3 Mega-Scale Testing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Create results directory if needed
    Path('results').mkdir(exist_ok=True)

    try:
        results_df = run_tier3_mega_tests()

        print(f"\n{'='*80}")
        print(f"Testing completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        print("Partial results may have been saved to results/tier3_mega_scale_results.csv")
        sys.exit(1)

    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
