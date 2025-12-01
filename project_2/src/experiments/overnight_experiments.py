"""
Overnight Experiment Suite - Enhanced Version with Density Spectrum Analysis

Comprehensive experiments with 2-tier structure:
- CORE TIER: 38 graphs (22 real + 16 synthetic) with 40 repetitions for statistical rigor
- STRETCH TIER: 4 massive graphs (3 DIMACS/SW + YouTube) with 10 repetitions

Key Features (December 1, 2025 Update):
✅ Synthetic graphs covering full density spectrum (trees to dense)
✅ Graph characterization (clustering, avg degree, diameter, type classification)
✅ Scenario-based algorithm recommendation
✅ Enhanced metrics collection (quality, speed, tradeoffs)
✅ Statistical analysis across graph types

Synthetic Graphs Added:
- Trees: Minimal density baseline
- Scale-free (Barabási-Albert): Power-law degree distribution
- Random (Erdős-Rényi): Various densities (p=0.005 to p=0.5)
- Small-world (Watts-Strogatz): High clustering like social networks

Tier 3 MEGA Dataset (in stretch tier):
- YouTube: 1.1M vertices, 3M edges
(LiveJournal, Orkut, Friendster tested separately in tier3_mega_scale_test.py)

Updated: December 1, 2025 (Density spectrum + characterization upgrade)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple
import pandas as pd
import numpy as np
from tqdm import tqdm
import gc
import psutil
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.algorithms.exact import exact_edge_cover
from src.algorithms.lazy_greedy import lazy_greedy_edge_cover
from src.algorithms.nearest_neighbor import nearest_neighbor_edge_cover
from src.algorithms.israeli_itai import israeli_itai_edge_cover
from src.algorithms.simulated_annealing import simulated_annealing_edge_cover
from src.utils.graph_loader import (
    load_sw_graph,
    load_snap_graph,
    load_snap_graph_memory_efficient,
    load_facebook_ego,
    load_dimacs_graph
)
from src.utils.graph_analysis import (
    characterize_graph,
    identify_best_algorithm,
    compute_degree_distribution_stats
)
from src.experiments.experiment_runner import ExperimentRunner
import networkx as nx


# ============================================================================
# SYNTHETIC GRAPH GENERATORS (for density spectrum coverage)
# ============================================================================

def generate_erdos_renyi(n: int, p: float, seed: int = 42) -> nx.Graph:
    """Generate Erdős-Rényi random graph."""
    G = nx.erdos_renyi_graph(n, p, seed=seed)
    # Remove isolated vertices
    G.remove_nodes_from(list(nx.isolates(G)))
    return G


def generate_barabasi_albert(n: int, m: int, seed: int = 42) -> nx.Graph:
    """Generate Barabási-Albert scale-free network."""
    return nx.barabasi_albert_graph(n, m, seed=seed)


def generate_watts_strogatz(n: int, k: int, p: float, seed: int = 42) -> nx.Graph:
    """Generate Watts-Strogatz small-world network."""
    return nx.watts_strogatz_graph(n, k, p, seed=seed)


def generate_random_tree(n: int, seed: int = 42) -> nx.Graph:
    """Generate random tree (minimum density baseline)."""
    return nx.random_tree(n, seed=seed)


# ============================================================================
# MEMORY MANAGEMENT UTILITIES
# ============================================================================

def get_memory_usage_gb() -> float:
    """Get current process memory usage in GB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 3)


def get_available_memory_gb() -> float:
    """Get available system memory in GB"""
    return psutil.virtual_memory().available / (1024 ** 3)


def force_memory_cleanup():
    """Force aggressive garbage collection"""
    gc.collect()
    gc.collect()  # Run twice for thoroughness
    gc.collect()


# ============================================================================
# SA INCLUSION DECISION
# ============================================================================
# Set this based on Tier 2 SA validation test results
# True = SA completed C2000.9 in <5 minutes
# False = SA exceeded 5 minutes or failed on C2000.9
SA_INCLUDE = False  # ← UPDATE AFTER TIER 2 SA VALIDATION TEST


# ============================================================================
# TIER 1: CORE GRAPHS (40 reps, statistical rigor)
# ============================================================================
CORE_GRAPHS = [
    # Format: (name, loader_func, size_category)

    # Baseline validation (4 graphs)
    ('SWtinyG', lambda: load_sw_graph('SWtinyG.txt'), 'tiny'),
    ('karate', lambda: nx.karate_club_graph(), 'tiny'),
    ('SWmediumG', lambda: load_sw_graph('SWmediumG.txt'), 'medium'),
    ('SWmediumEWD', lambda: load_sw_graph('SWmediumEWD.txt'), 'medium'),

    # Ego networks - dense structure (9 graphs)
    ('ego-698', lambda: load_facebook_ego('698'), 'tiny'),
    ('ego-348', lambda: load_facebook_ego('348'), 'small'),
    ('ego-686', lambda: load_facebook_ego('686'), 'small'),
    ('ego-414', lambda: load_facebook_ego('414'), 'small'),
    ('ego-0', lambda: load_facebook_ego('0'), 'medium'),
    ('ego-3437', lambda: load_facebook_ego('3437'), 'medium'),
    ('ego-1684', lambda: load_facebook_ego('1684'), 'medium'),
    ('ego-1912', lambda: load_facebook_ego('1912'), 'medium'),
    ('ego-107', lambda: load_facebook_ego('107'), 'large'),

    # SNAP social networks (3 graphs)
    ('email-Eu-core', lambda: load_snap_graph('email_eu_core/email-Eu-core.txt'), 'large'),
    ('facebook_combined', lambda: load_snap_graph('facebook/facebook_combined.txt'), 'large'),
    ('Wiki-Vote', lambda: load_snap_graph('wiki_vote/Wiki-Vote.txt'), 'xlarge'),

    # SW large graphs (2 graphs)
    ('SW1000EWD', lambda: load_sw_graph('SW1000EWD.txt'), 'large'),
    ('SW10000EWD', lambda: load_sw_graph('SW10000EWD.txt'), 'xlarge'),

    # SNAP collaboration (2 graphs)
    ('CA-GrQc', lambda: load_snap_graph('ca-grqc/CA-GrQc.txt'), 'xlarge'),
    ('CA-HepPh', lambda: load_snap_graph('ca-hepph/CA-HepPh.txt'), 'xlarge'),

    # DIMACS ultra-dense (1 graph)
    ('C1000.9', lambda: load_dimacs_graph('C1000.9/c1000.txt'), 'dense'),

    # SYNTHETIC GRAPHS - Density Spectrum Coverage (16 graphs)
    # Trees - minimal density baseline
    ('tree-100', lambda: generate_random_tree(100), 'tree'),
    ('tree-500', lambda: generate_random_tree(500), 'tree'),

    # Sparse: Barabási-Albert scale-free (power-law degree distribution)
    ('BA-500-2', lambda: generate_barabasi_albert(500, 2), 'sparse_scalefree'),
    ('BA-1000-3', lambda: generate_barabasi_albert(1000, 3), 'sparse_scalefree'),

    # Very sparse: Erdős-Rényi p=0.005 (social network density)
    ('ER-500-0.005', lambda: generate_erdos_renyi(500, 0.005), 'very_sparse'),
    ('ER-1000-0.003', lambda: generate_erdos_renyi(1000, 0.003), 'very_sparse'),

    # Sparse: Erdős-Rényi p=0.01
    ('ER-500-0.01', lambda: generate_erdos_renyi(500, 0.01), 'sparse'),
    ('ER-1000-0.01', lambda: generate_erdos_renyi(1000, 0.01), 'sparse'),

    # Medium sparse: Erdős-Rényi p=0.05
    ('ER-500-0.05', lambda: generate_erdos_renyi(500, 0.05), 'medium_sparse'),
    ('ER-1000-0.05', lambda: generate_erdos_renyi(1000, 0.05), 'medium_sparse'),

    # Medium: Erdős-Rényi p=0.1
    ('ER-300-0.1', lambda: generate_erdos_renyi(300, 0.1), 'medium'),
    ('ER-500-0.1', lambda: generate_erdos_renyi(500, 0.1), 'medium'),

    # Medium-dense: Erdős-Rényi p=0.2
    ('ER-200-0.2', lambda: generate_erdos_renyi(200, 0.2), 'medium_dense'),

    # Small-world: Watts-Strogatz (high clustering like social networks)
    ('WS-500-10-0.1', lambda: generate_watts_strogatz(500, 10, 0.1), 'small_world'),
    ('WS-1000-6-0.05', lambda: generate_watts_strogatz(1000, 6, 0.05), 'small_world'),

    # Dense: Erdős-Rényi p=0.5
    ('ER-100-0.5', lambda: generate_erdos_renyi(100, 0.5), 'dense'),
]
# Total: 38 core graphs (22 real + 16 synthetic)


# ============================================================================
# TIER 2: STRETCH GRAPHS (10 reps, scalability showcase)
# ============================================================================
STRETCH_GRAPHS = [
    # Original DIMACS and SW stretch goals
    ('C2000.9', lambda: load_dimacs_graph('C2000.9/c2000.txt'), 'ultra_dense'),
    ('C4000.5', lambda: load_dimacs_graph('C4000.5/c4000.txt'), 'xlarge_dense'),
    ('SWlargeG', lambda: load_sw_graph('SWlargeG.txt'), 'ultra_large'),  # 1M vertices!

    # TIER 3 MEGA DATASETS - Exceptional scalability showcase
    # NOTE: YouTube uses regular loader (fast enough)
    ('YouTube', lambda: load_snap_graph('youtube/com-youtube.ungraph.txt'), 'mega_1M'),      # 1.1M v, 3M e

    # LiveJournal: ADDED BACK with memory-efficient loader (5 reps, adds ~5 hours)
    ('LiveJournal', lambda: load_snap_graph_memory_efficient('live_journal/com-lj.ungraph.txt'), 'mega_4M'),  # 4M v, 34.7M e
]
# NOTE: Orkut, Friendster excluded from overnight experiments due to:
# - Orkut: OOM issues at ~21GB RAM, 117M edges (tested separately)
# - Friendster: Impractical (1.8B edges, 10+ days to load)
# These remain in tier3_mega_scale_test.py

# Total: 5 stretch graphs (3 DIMACS/SW + 2 mega datasets: YouTube + LiveJournal)


# ============================================================================
# SIZE CATEGORY DEFINITIONS
# ============================================================================
SIZE_CATEGORIES = {
    'tiny': {'vertices': '<100', 'description': 'Validation graphs'},
    'small': {'vertices': '100-500', 'description': 'Small real-world'},
    'medium': {'vertices': '500-1k', 'description': 'Medium networks'},
    'large': {'vertices': '1k-5k', 'description': 'Large networks'},
    'xlarge': {'vertices': '5k-15k', 'description': 'Very large networks'},
    'dense': {'vertices': 'any', 'description': 'Ultra-dense (p>0.5)'},
    'ultra_dense': {'vertices': 'any', 'description': 'Extreme density (p≈0.9)'},
    'xlarge_dense': {'vertices': 'any', 'description': 'Large + dense'},
    'ultra_large': {'vertices': '>100k', 'description': 'Extreme scale'},
    # Tier 3 mega dataset categories
    'mega_1M': {'vertices': '~1M', 'description': 'Mega-scale 1M vertices'},
    'mega_4M': {'vertices': '~4M', 'description': 'Mega-scale 4M vertices'},
    'mega_dense': {'vertices': '~3M', 'description': 'Mega-scale ultra-dense (117M edges)'},
    'mega_extreme': {'vertices': '65M', 'description': 'Extreme mega-scale (1.8B edges)'},
    # Synthetic graph categories (density spectrum)
    'tree': {'vertices': 'any', 'description': 'Trees (minimal density)'},
    'very_sparse': {'vertices': 'any', 'description': 'Very sparse (p≤0.005)'},
    'sparse': {'vertices': 'any', 'description': 'Sparse (p≈0.01)'},
    'sparse_scalefree': {'vertices': 'any', 'description': 'Scale-free network (power-law)'},
    'medium_sparse': {'vertices': 'any', 'description': 'Medium-sparse (p≈0.05)'},
    'medium_dense': {'vertices': 'any', 'description': 'Medium-dense (p≈0.2)'},
    'small_world': {'vertices': 'any', 'description': 'Small-world network (high clustering)'},
}


# ============================================================================
# TIMEOUT CONFIGURATION
# ============================================================================
TIMEOUT_CONFIG = {
    # Format: {'exact': seconds, 'approx': seconds}
    'tiny': {'exact': 300, 'approx': 60},           # <100v
    'small': {'exact': 600, 'approx': 120},         # 100-500v
    'medium': {'exact': 900, 'approx': 180},        # 500-1kv
    'large': {'exact': 1800, 'approx': 300},        # 1k-5kv
    'xlarge': {'exact': None, 'approx': 600},       # >5kv (skip exact)
    'dense': {'exact': 1800, 'approx': 600},        # Ultra-dense (p>0.5)
    'ultra_dense': {'exact': None, 'approx': 900},  # Extreme density
    'xlarge_dense': {'exact': None, 'approx': 1200}, # Large + dense
    'ultra_large': {'exact': None, 'approx': 1800}, # 1M vertices
    # Tier 3 mega dataset timeouts (very generous)
    'mega_1M': {'exact': None, 'approx': 1800},     # YouTube: 1M vertices
    'mega_4M': {'exact': None, 'approx': 2400},     # LiveJournal: 4M vertices (40 min)
    'mega_dense': {'exact': None, 'approx': 3000},  # Orkut: 117M edges (50 min)
    'mega_extreme': {'exact': None, 'approx': 3600}, # Friendster: 1.8B edges (60 min)
    # Synthetic graph timeouts
    'tree': {'exact': 600, 'approx': 120},          # Trees are fast
    'very_sparse': {'exact': 600, 'approx': 120},   # Very sparse
    'sparse': {'exact': 600, 'approx': 120},        # Sparse
    'sparse_scalefree': {'exact': 600, 'approx': 120}, # Scale-free
    'medium_sparse': {'exact': 900, 'approx': 180}, # Medium sparse
    'medium_dense': {'exact': 900, 'approx': 300},  # Medium dense
    'small_world': {'exact': 900, 'approx': 180},   # Small world
}


# ============================================================================
# ALGORITHM CONFIGURATION
# ============================================================================
ALGORITHMS_CONFIG = {
    'exact': {
        'func': exact_edge_cover,
        'skip_on': ['xlarge', 'ultra_large', 'dense', 'ultra_dense', 'xlarge_dense'],
        'description': 'Exact via maximum matching (Gallai)'
    },
    'lazy_greedy': {
        'func': lazy_greedy_edge_cover,
        'skip_on': [],  # ALWAYS RUN
        'description': 'Lazy greedy 3/2-approximation'
    },
    'nearest_neighbor': {
        'func': nearest_neighbor_edge_cover,
        'skip_on': [],  # ALWAYS RUN
        'description': 'Nearest neighbor 2-approximation'
    },
    'israeli_itai': {
        'func': lambda G, **kwargs: israeli_itai_edge_cover(G, smart_proposals=True, **kwargs),
        'skip_on': [],  # RUN ON ALL GRAPHS - produces best quality results
        'description': 'Israeli-Itai improved (smart proposals)'
    },
}

# Add SA conditionally based on validation test results
if SA_INCLUDE:
    ALGORITHMS_CONFIG['simulated_annealing'] = {
        'func': lambda G, **kwargs: simulated_annealing_edge_cover(G, initial_solution='lazy_greedy', **kwargs),
        'skip_on': ['large', 'xlarge', 'ultra_large', 'dense', 'ultra_dense', 'xlarge_dense'],
        'description': 'Simulated annealing (optimized, small/medium graphs only)'
    }


# ============================================================================
# RESUME CAPABILITY
# ============================================================================

def load_resume_state(tier: str) -> Tuple[Set[Tuple[str, str]], List[Dict]]:
    """
    Load existing progress and determine what to skip.

    Args:
        tier: Experiment tier ('core', 'stretch', 'both', 'test')

    Returns:
        Tuple of (completed_work, previous_results)
        - completed_work: Set of (graph_name, algorithm) tuples already done
        - previous_results: List of previous result dictionaries
    """
    progress_file = Path(f'results/overnight/{tier}_progress.csv')

    if not progress_file.exists():
        return set(), []  # No resume needed

    print(f"\n{'='*70}")
    print(f"📂 FOUND EXISTING PROGRESS FILE")
    print(f"{'='*70}")

    df = pd.read_csv(progress_file)
    completed = set(zip(df['graph_name'], df['algorithm']))

    print(f"✅ Completed: {len(completed)} trials from previous run")
    print(f"   Unique graphs: {df['graph_name'].nunique()}")
    print(f"   Unique algorithms: {df['algorithm'].nunique()}")
    if 'timestamp' in df.columns:
        print(f"   Latest timestamp: {df['timestamp'].iloc[-1]}")

    response = input("\nResume from this checkpoint? [y/N]: ").strip().lower()
    if response == 'y':
        print("✅ Resuming from checkpoint...")
        return completed, df.to_dict('records')
    else:
        print("⚠️  Starting fresh (previous data will be overwritten)...")
        return set(), []


# ============================================================================
# MAIN EXPERIMENT RUNNER
# ============================================================================
def run_overnight_experiments(tier='core', repetitions=40):
    """
    Run overnight experiments with 2-tier structure

    Args:
        tier: 'core' or 'stretch' or 'both'
        repetitions: Number of trials per algorithm-graph pair (for core tier)
    """

    runner = ExperimentRunner(results_dir='results/overnight')

    # Select graphs and repetitions based on tier
    if tier == 'core' or tier == 'test':
        graphs = CORE_GRAPHS
        reps = repetitions
    elif tier == 'stretch':
        graphs = STRETCH_GRAPHS
        reps = 10  # Lower reps for massive graphs
    elif tier == 'both':
        graphs = CORE_GRAPHS + STRETCH_GRAPHS
        reps = repetitions  # Will adjust per-graph
    else:
        raise ValueError(f"Unknown tier: {tier}")

    print("="*70)
    print(f"OVERNIGHT EXPERIMENTS - TIER: {tier.upper()}")
    print("="*70)
    print(f"Graphs: {len(graphs)}")
    print(f"Algorithms: {len(ALGORITHMS_CONFIG)}")
    print(f"SA Included: {SA_INCLUDE}")
    print(f"Repetitions: {reps} (core) / 10 (stretch) / 5 (LiveJournal)")

    # System info
    print(f"\nSystem Memory:")
    print(f"  Total: {psutil.virtual_memory().total / (1024**3):.2f} GB")
    print(f"  Available: {get_available_memory_gb():.2f} GB")
    print(f"  Current usage: {get_memory_usage_gb():.2f} GB")

    # Load resume state
    completed_work, previous_results = load_resume_state(tier)
    all_results = previous_results if previous_results else []

    # Count expected trials
    expected_trials = 0
    for _, _, size_cat in graphs:
        for algo_name, algo_config in ALGORITHMS_CONFIG.items():
            if size_cat not in algo_config['skip_on']:
                expected_trials += reps if tier != 'both' else (reps if size_cat != 'ultra_large' else 10)

    print(f"\nEstimated trials: {expected_trials}")
    if completed_work:
        print(f"Already completed: {len([r for r in all_results if r.get('success', False)])} trials")
        print(f"Remaining: ~{expected_trials - len(all_results)}")
    print("="*70)

    total_experiments = len(graphs) * len(ALGORITHMS_CONFIG)
    experiment_num = 0

    start_time = datetime.now()
    completed_graphs = set([r['graph_name'] for r in all_results]) if all_results else set()

    # Main loop
    for graph_name, graph_loader, size_category in graphs:
        print(f"\n{'='*70}")
        print(f"Loading graph: {graph_name} (category: {size_category})")
        print(f"{'='*70}")

        # Memory check before loading
        available_mem = get_available_memory_gb()
        if available_mem < 8:
            print(f"⚠️  Low memory ({available_mem:.2f} GB available), forcing cleanup...")
            force_memory_cleanup()
            available_mem = get_available_memory_gb()
            print(f"   After cleanup: {available_mem:.2f} GB available")

        try:
            # Special handling for LiveJournal
            if graph_name == 'LiveJournal':
                print(f"\n⚠️  LIVEJOURNAL: Large graph - expect 3+ min load, ~5 hour total")
                print(f"   Using memory-efficient loader with batching...")

            G = graph_loader()
            n = G.number_of_nodes()
            m = G.number_of_edges()

            # ENHANCED: Full graph characterization
            graph_props = characterize_graph(G)
            graph_props['size_category'] = size_category  # Keep manual category
            graph_props['graph_name'] = graph_name

            # Print summary
            print(f"Loaded: {n:,} vertices, {m:,} edges, density={graph_props['density']:.4f}")
            print(f"  Type: {graph_props['graph_type']}, Scenario: {graph_props['scenario_category']}")
            print(f"  Avg degree: {graph_props['avg_degree']:.2f}, Clustering: {graph_props['clustering_coeff']:.4f}")
            print(f"  Memory after load: {get_memory_usage_gb():.2f} GB")

            # Identify best algorithm for this graph
            best_algo, reason = identify_best_algorithm(graph_props)
            print(f"  💡 Recommended: {best_algo} ({reason})")

        except Exception as e:
            print(f"❌ Failed to load {graph_name}: {e}")
            import traceback
            traceback.print_exc()
            continue

        # Determine repetitions for this graph (AUTO-REDUCE for large graphs)
        if tier == 'both' and size_category in ['ultra_large', 'ultra_dense', 'xlarge_dense']:
            current_reps = 10
        else:
            current_reps = reps

        # Auto-reduce reps based on graph size
        if graph_name == 'LiveJournal':
            current_reps = 5  # Fixed at 5 for LiveJournal
            print(f"  📊 LiveJournal: Using 5 reps (optimized for large graph)")
        elif n > 100_000:
            current_reps = min(current_reps, 5)
            print(f"  ⚠️  Large graph ({n:,} vertices): Reduced reps to {current_reps}")
        elif n > 10_000:
            current_reps = min(current_reps, 10)
            print(f"  ℹ️  Medium-large graph: Reduced reps to {current_reps}")

        # Track results for this graph
        graph_trial_results = []

        # Test each algorithm
        for algo_name, algo_config in ALGORITHMS_CONFIG.items():
            experiment_num += 1

            # Check if should skip (category-based)
            if size_category in algo_config['skip_on']:
                print(f"\n[{experiment_num}/{total_experiments}] SKIPPING {algo_name} on {graph_name} ({size_category})")
                continue

            # Check if already completed (resume capability)
            if (graph_name, algo_name) in completed_work:
                print(f"\n[{experiment_num}/{total_experiments}] ⏭️  SKIPPING {algo_name} on {graph_name} (already completed)")
                continue

            print(f"\n[{experiment_num}/{total_experiments}] Running {algo_name} on {graph_name}")
            print(f"  {algo_config['description']}")

            # Get timeout
            timeout_key = 'exact' if algo_name == 'exact' else 'approx'
            timeout = TIMEOUT_CONFIG[size_category][timeout_key]

            if timeout is None:
                print(f"  ⚠️  No timeout configured (algorithm not suitable for {size_category})")
                continue

            print(f"  Timeout: {timeout}s, Repetitions: {current_reps}")

            # Run multiple trials with progress bar
            trial_results = []

            for trial_num in tqdm(range(current_reps), desc=f"  {algo_name}", leave=False):
                try:
                    result = runner.run_single_trial(
                        graph=G,
                        algorithm_func=algo_config['func'],
                        algorithm_name=algo_name,
                        graph_name=graph_name,
                        graph_properties=graph_props,
                        timeout=timeout
                    )
                    trial_results.append(result)
                    all_results.append(result)
                    graph_trial_results.append(result)
                except Exception as e:
                    print(f"\n  ⚠️  Trial {trial_num+1} failed: {e}")

            # Compute stats
            successful = [r for r in trial_results if r.get('success', False)]
            if successful:
                cover_sizes = [r['cover_size'] for r in successful]
                runtimes = [r['runtime'] for r in successful]
                print(f"\n  ✅ Success: {len(successful)}/{current_reps} trials")
                print(f"     Cover size: {np.mean(cover_sizes):.2f} ± {np.std(cover_sizes):.2f}")
                print(f"     Runtime: {np.mean(runtimes):.4f}s ± {np.std(runtimes):.4f}s")
            else:
                print(f"\n  ❌ All trials failed")

            # Memory cleanup after each algorithm
            force_memory_cleanup()
            print(f"     Memory: {get_memory_usage_gb():.2f} GB")

        # ===== AFTER ALL ALGORITHMS FOR THIS GRAPH =====
        # Per-graph checkpointing and batch CSV writing
        print(f"\n💾 Saving checkpoint after {graph_name}...")

        # Write batch results to CSV (append mode)
        if graph_trial_results:
            df_batch = pd.DataFrame(graph_trial_results)
            progress_file = Path(f'results/overnight/{tier}_progress.csv')

            if not progress_file.exists():
                df_batch.to_csv(progress_file, index=False, mode='w')
                print(f"   Created progress file: {progress_file}")
            else:
                df_batch.to_csv(progress_file, index=False, mode='a', header=False)
                print(f"   Appended {len(graph_trial_results)} results to progress file")

        # Save checkpoint
        completed_graphs.add(graph_name)
        checkpoint_data = {
            'completed_graphs': list(completed_graphs),
            'last_graph': graph_name,
            'total_trials': len(all_results),
            'timestamp': datetime.now().isoformat()
        }
        runner.save_checkpoint(
            checkpoint_file=f'{tier}_checkpoint_after_{graph_name.replace("/", "_")}.pkl',
            data=checkpoint_data
        )

        # Progress update
        elapsed = datetime.now() - start_time
        graphs_done = len(completed_graphs)
        graphs_total = len(graphs)
        graphs_remaining = graphs_total - graphs_done

        if graphs_done > 0:
            avg_time_per_graph = elapsed.total_seconds() / graphs_done
            est_remaining = timedelta(seconds=avg_time_per_graph * graphs_remaining)

            print(f"\n📊 PROGRESS UPDATE")
            print(f"   Graphs: {graphs_done}/{graphs_total}")
            print(f"   Trials so far: {len(all_results)}")
            print(f"   Elapsed: {elapsed}")
            print(f"   Est. remaining: {est_remaining}")
            print(f"   Est. completion: {datetime.now() + est_remaining}")
            print(f"   Memory: {get_memory_usage_gb():.2f} GB / {get_available_memory_gb():.2f} GB available")

        # Cleanup graph from memory
        print(f"\n🗑️  Cleaning up {graph_name} from memory...")
        print(f"   Memory before: {get_memory_usage_gb():.2f} GB")
        del G
        force_memory_cleanup()
        print(f"   Memory after: {get_memory_usage_gb():.2f} GB")

        # Keep only recent results in memory (last 200 trials)
        if len(all_results) > 200:
            all_results = all_results[-200:]
            print(f"   Trimmed results list to last 200 entries (memory optimization)")

    # Final save
    print(f"\n{'='*70}")
    print("SAVING FINAL RESULTS")
    print(f"{'='*70}")

    # Load all results from progress CSV (since we trimmed all_results for memory)
    progress_file = Path(f'results/overnight/{tier}_progress.csv')
    if progress_file.exists():
        df = pd.read_csv(progress_file)
        print(f"Loaded {len(df)} total trials from progress file")
    else:
        df = pd.DataFrame(all_results)
        print(f"Using {len(df)} trials from memory")

    # Save as final results
    final_file = f'results/overnight/{tier}_final_results.csv'
    df.to_csv(final_file, index=False)
    print(f"✅ Saved final results: {final_file}")

    # Also save JSON
    runner.save_results(filename=f'{tier}_final_results.json')
    runner.save_checkpoint(checkpoint_file=f'{tier}_final_checkpoint.pkl')

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'='*70}")
    print("EXPERIMENTS COMPLETED!")
    print(f"{'='*70}")
    print(f"Total duration: {duration}")
    print(f"Total trials: {len(df)}")
    print(f"Successful trials: {len(df[df['success'] == True]) if 'success' in df.columns else 'N/A'}")
    if 'success' in df.columns and len(df) > 0:
        success_count = len(df[df['success'] == True])
        print(f"Success rate: {success_count / len(df) * 100:.1f}%")
    print(f"\nResults saved to: {final_file}")
    print(f"Progress file: {progress_file}")
    print(f"Final memory usage: {get_memory_usage_gb():.2f} GB")
    print("="*70)


# ============================================================================
# QUICK TEST MODE
# ============================================================================

def run_quick_test():
    """
    Quick 3-graph test to verify everything works before full run.
    Tests: 1 tiny, 1 medium, 1 synthetic with 2 reps each.
    Expected runtime: 3-5 minutes
    """
    print("="*70)
    print("QUICK TEST MODE - 3 Graphs × 4 Algorithms × 2 Reps")
    print("Expected runtime: 3-5 minutes")
    print("="*70)

    # Temporarily override CORE_GRAPHS for testing
    global CORE_GRAPHS
    original_core = CORE_GRAPHS

    test_graphs = [
        ('SWtinyG', lambda: load_sw_graph('SWtinyG.txt'), 'tiny'),
        ('ER-500-0.05', lambda: generate_erdos_renyi(500, 0.05), 'medium_sparse'),
        ('ego-107', lambda: load_facebook_ego('107'), 'large'),
    ]

    CORE_GRAPHS = test_graphs

    try:
        result = run_overnight_experiments(tier='test', repetitions=2)
    finally:
        CORE_GRAPHS = original_core

    print("\n✅ QUICK TEST COMPLETED!")
    print("If you see results above with no errors, you're ready for full run.")
    print("\nTo run full experiments:")
    print("  python src/experiments/overnight_experiments.py --tier core --reps 40")

    return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run overnight experiments with comprehensive optimization')
    parser.add_argument('--tier', choices=['core', 'stretch', 'both', 'test'], default='core',
                       help='Which tier to run (test = quick 3-graph validation)')
    parser.add_argument('--reps', type=int, default=40,
                       help='Repetitions per algorithm-graph pair (core tier)')
    parser.add_argument('--sa-include', action='store_true', default=False,
                       help='Override SA inclusion (for testing)')
    parser.add_argument('--test', action='store_true', default=False,
                       help='Run quick 3-graph test before deciding on full run')

    args = parser.parse_args()

    # Update SA configuration if override specified
    if args.sa_include and not SA_INCLUDE:
        print("WARNING: Overriding SA exclusion - adding SA to algorithms")
        ALGORITHMS_CONFIG['simulated_annealing'] = {
            'func': lambda G: simulated_annealing_edge_cover(G, initial_solution='lazy_greedy'),
            'skip_on': ['large', 'xlarge', 'ultra_large', 'dense', 'ultra_dense', 'xlarge_dense'],
            'description': 'Simulated annealing (optimized, small/medium graphs only)'
        }

    # Run test mode if requested
    if args.test or args.tier == 'test':
        run_quick_test()
    else:
        run_overnight_experiments(tier=args.tier, repetitions=args.reps)
