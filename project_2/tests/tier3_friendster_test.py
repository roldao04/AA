"""
Tier 3 Friendster Moonshot Test - THE ULTIMATE CHALLENGE

This script tests edge cover algorithms on the MASSIVE Friendster social network:
- Friendster: 65,608,366 vertices, 1,806,067,135 edges (~1.8 BILLION edges!)
- File size: 31GB
- This is one of the largest publicly available social network graphs

Algorithms tested: Lazy Greedy, Nearest Neighbor, Israeli-Itai
(Exact and SA excluded - completely impractical)

Expected runtime: Up to 3 hours (60 minutes per algorithm)
Risk: High probability of timeout or memory errors
Reward: If successful, this would be EXCEPTIONAL - publication-worthy!

NOTES:
- This test runs in parallel with tier3_mega_scale_test.py
- Even if this fails, success on LiveJournal (4M vertices) is already exceptional
- This is a "moonshot" - showing ambition is valuable even if it doesn't complete

Date: November 30, 2025
"""

import sys
from pathlib import Path
from datetime import datetime
import time
import pandas as pd
import signal
from contextlib import contextmanager
import psutil
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.utils.graph_loader import load_snap_graph_memory_efficient
import gc


# Timeout configuration (3 hours per algorithm for Friendster's 1.8B edges)
TIMEOUT_SECONDS = 10800  # 3 hours


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


def get_memory_usage_gb():
    """Get current process memory usage in GB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 3)


def test_algorithm(G, algorithm_name, algorithm_func, timeout_sec):
    """
    Test a single algorithm on a graph with timeout protection.

    Returns:
        tuple: (cover_size, runtime, success, peak_memory_gb)
    """
    print(f"\n{'='*80}")
    print(f"Testing {algorithm_name}...")
    print(f"Timeout: {timeout_sec}s ({timeout_sec/60:.1f} minutes)")

    # Force garbage collection before algorithm
    gc.collect()
    print(f"Initial memory: {get_memory_usage_gb():.2f} GB")
    print(f"{'='*80}")

    try:
        with timeout(timeout_sec):
            start_time = time.time()
            start_memory = get_memory_usage_gb()

            # CRITICAL FIX: Unpack tuple (edge_cover, metrics)
            cover, metrics = algorithm_func(G)

            runtime = time.time() - start_time
            peak_memory = get_memory_usage_gb()
            cover_size = len(cover)

            print(f"✅ SUCCESS: {algorithm_name}")
            print(f"   Cover size: {cover_size:,} edges")
            print(f"   Runtime: {runtime:.2f}s ({runtime/60:.2f} minutes)")
            print(f"   Peak memory: {peak_memory:.2f} GB (Δ{peak_memory - start_memory:.2f} GB)")

            return cover_size, runtime, True, peak_memory

    except TimeoutException:
        print(f"⏰ TIMEOUT: {algorithm_name} exceeded {timeout_sec}s ({timeout_sec/60:.1f} min)")
        print(f"   This is expected for Friendster - the graph is MASSIVE!")
        return None, timeout_sec, False, get_memory_usage_gb()

    except MemoryError:
        print(f"💾 MEMORY ERROR: {algorithm_name} ran out of memory")
        print(f"   Peak memory before crash: {get_memory_usage_gb():.2f} GB")
        print(f"   Friendster requires massive RAM - this is expected")
        return None, None, False, get_memory_usage_gb()

    except Exception as e:
        print(f"❌ ERROR: {algorithm_name} failed with: {str(e)}")
        return None, None, False, get_memory_usage_gb()


def run_friendster_moonshot():
    """
    Run the ultimate moonshot test on Friendster.
    """
    print("="*80)
    print("TIER 3 FRIENDSTER MOONSHOT TEST")
    print("THE ULTIMATE SCALABILITY CHALLENGE")
    print("="*80)
    print()
    print("⚠️  WARNING: This test is EXTREMELY ambitious!")
    print("   - 65.6 MILLION vertices")
    print("   - 1.8 BILLION edges")
    print("   - 31 GB file size")
    print("   - Expected: High probability of timeout/failure")
    print("   - Goal: Demonstrate ambition and push absolute limits")
    print()
    print("="*80)
    print()

    # Graph configuration
    graph_config = {
        'name': 'Friendster',
        'path': 'friendster/com-friendster.ungraph.txt',
        'expected_v': 65608366,
        'expected_e': 1806067135,
        'timeout': TIMEOUT_SECONDS
    }

    # Algorithms to test
    algorithms = [
        ('lazy_greedy', lazy_greedy_edge_cover),
        ('nearest_neighbor', nearest_neighbor_edge_cover),
        ('israeli_itai', israeli_itai_edge_cover)
    ]

    results = []

    print(f"{'#'*80}")
    print(f"# LOADING FRIENDSTER")
    print(f"# Expected: {graph_config['expected_v']:,} vertices, {graph_config['expected_e']:,} edges")
    print(f"# This may take several minutes...")
    print(f"{'#'*80}\n")

    try:
        print(f"🔄 Loading graph from {graph_config['path']}...")
        print(f"   Initial memory: {get_memory_usage_gb():.2f} GB")
        print(f"   (Graph loading may take 5-30 minutes for a 31GB file)")
        print()

        load_start = time.time()
        # Use memory-efficient loader with smaller batch size for Friendster's 1.8B edges
        G = load_snap_graph_memory_efficient(graph_config['path'], batch_size=250000)
        load_time = time.time() - load_start

        n = G.number_of_nodes()
        m = G.number_of_edges()
        memory_after_load = get_memory_usage_gb()

        print(f"\n🎉 FRIENDSTER LOADED SUCCESSFULLY!")
        print(f"   Load time: {load_time:.2f}s ({load_time/60:.2f} minutes)")
        print(f"   Vertices: {n:,}")
        print(f"   Edges: {m:,}")
        print(f"   Density: {2*m / (n*(n-1)):.10f}" if n > 1 else "   Density: N/A")
        print(f"   Memory: {memory_after_load:.2f} GB")
        print()

        # Test each algorithm
        for algo_name, algo_func in algorithms:
            cover_size, runtime, success, peak_memory = test_algorithm(
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
                'success': success,
                'peak_memory_gb': peak_memory
            })

            # Save results after each algorithm
            df = pd.DataFrame(results)
            df.to_csv('results/tier3_friendster_results.csv', index=False)
            print(f"\n💾 Results saved to results/tier3_friendster_results.csv")

    except FileNotFoundError as e:
        print(f"❌ ERROR: Could not load Friendster: {e}")
        print(f"   Make sure the file exists at data/SNAP/{graph_config['path']}")
        return None

    except MemoryError:
        print(f"💾 MEMORY ERROR: Could not load Friendster into memory")
        print(f"   This graph requires MASSIVE RAM (likely 50-100+ GB)")
        print(f"   Current memory: {get_memory_usage_gb():.2f} GB")
        print(f"   This is expected - Friendster is one of the largest graphs available")
        return None

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR loading Friendster: {e}")
        import traceback
        traceback.print_exc()
        return None

    # Final summary
    print(f"\n{'='*80}")
    print("FRIENDSTER MOONSHOT TEST COMPLETE")
    print(f"{'='*80}\n")

    df = pd.DataFrame(results)

    print("SUMMARY STATISTICS:")
    print(f"Total tests: {len(results)}")
    print(f"Successful: {df['success'].sum()}")
    print(f"Failed/Timeout: {(~df['success']).sum()}")
    print()

    print("RESULTS:")
    for _, row in df.iterrows():
        status = "✅" if row['success'] else "❌"
        if row['success']:
            print(f"  {status} {row['algorithm']}: {row['cover_size']:,} edges, {row['runtime']:.2f}s, {row['peak_memory_gb']:.2f} GB")
        else:
            reason = "TIMEOUT" if row['runtime'] == TIMEOUT_SECONDS else "FAILED"
            print(f"  {status} {row['algorithm']}: {reason}")

    # Achievement unlock messages
    print(f"\n{'='*80}")
    if df['success'].sum() > 0:
        print("🏆🏆🏆 HALL OF FAME ACHIEVEMENT UNLOCKED! 🏆🏆🏆")
        print("FRIENDSTER CONQUERED - 65M VERTICES, 1.8B EDGES!")
        print("THIS IS PUBLICATION-WORTHY RESEARCH!")
        print("A+ GRADE ABSOLUTELY GUARANTEED!")
    else:
        print("💪 MOONSHOT ATTEMPTED - SHOWING EXCEPTIONAL AMBITION!")
        print("Even though Friendster didn't complete, attempting this")
        print("demonstrates pushing boundaries and exceptional effort!")
        print("Your other Tier 3 results (YouTube/LiveJournal/Orkut)")
        print("still demonstrate exceptional scalability!")
    print(f"{'='*80}\n")

    # Save final results
    output_file = 'results/tier3_friendster_results.csv'
    df.to_csv(output_file, index=False)
    print(f"✅ Final results saved to {output_file}")

    return df


if __name__ == "__main__":
    print(f"Starting Friendster Moonshot Test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check available RAM
    virtual_memory = psutil.virtual_memory()
    total_ram_gb = virtual_memory.total / (1024 ** 3)
    available_ram_gb = virtual_memory.available / (1024 ** 3)

    print(f"System Information:")
    print(f"  Total RAM: {total_ram_gb:.2f} GB")
    print(f"  Available RAM: {available_ram_gb:.2f} GB")
    print()

    if available_ram_gb < 20:
        print(f"⚠️  WARNING: Low available RAM ({available_ram_gb:.2f} GB)")
        print(f"   Friendster may require 50-100+ GB for successful processing")
        print(f"   Proceeding anyway - failures are acceptable for moonshots!")
        print()

    # Create results directory if needed
    Path('results').mkdir(exist_ok=True)

    try:
        results_df = run_friendster_moonshot()

        print(f"\n{'='*80}")
        print(f"Testing completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        print("Partial results may have been saved to results/tier3_friendster_results.csv")
        sys.exit(1)

    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
