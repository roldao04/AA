"""
Overnight Experiment Suite - Tier 2 Version

Comprehensive experiments with 2-tier structure:
- CORE TIER: 20+ graphs with 40 repetitions for statistical rigor
- STRETCH TIER: 3 massive graphs with 10 repetitions for scalability showcase

Updated: November 30, 2025
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import pandas as pd
import numpy as np
from tqdm import tqdm

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
    load_facebook_ego,
    load_dimacs_graph
)
from src.experiments.experiment_runner import ExperimentRunner
import networkx as nx


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
]
# Total: 22 core graphs


# ============================================================================
# TIER 2: STRETCH GRAPHS (10 reps, scalability showcase)
# ============================================================================
STRETCH_GRAPHS = [
    # Only include if Tier 2 manual testing successful
    ('C2000.9', lambda: load_dimacs_graph('C2000.9/c2000.txt'), 'ultra_dense'),
    ('C4000.5', lambda: load_dimacs_graph('C4000.5/c4000.txt'), 'xlarge_dense'),
    ('SWlargeG', lambda: load_sw_graph('SWlargeG.txt'), 'ultra_large'),  # 1M vertices!
]


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
        'func': lambda G: israeli_itai_edge_cover(G, smart_proposals=True),
        'skip_on': ['ultra_large'],  # Too slow on 1M vertices
        'description': 'Israeli-Itai improved (smart proposals)'
    },
}

# Add SA conditionally based on validation test results
if SA_INCLUDE:
    ALGORITHMS_CONFIG['simulated_annealing'] = {
        'func': lambda G: simulated_annealing_edge_cover(G, initial_solution='lazy_greedy'),
        'skip_on': ['large', 'xlarge', 'ultra_large', 'dense', 'ultra_dense', 'xlarge_dense'],
        'description': 'Simulated annealing (optimized, small/medium graphs only)'
    }


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
    if tier == 'core':
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
    print(f"Repetitions: {reps} (core) / 10 (stretch)")

    # Count expected trials
    expected_trials = 0
    for _, _, size_cat in graphs:
        for algo_name, algo_config in ALGORITHMS_CONFIG.items():
            if size_cat not in algo_config['skip_on']:
                expected_trials += reps if tier != 'both' else (reps if size_cat != 'ultra_large' else 10)

    print(f"Estimated trials: {expected_trials}")
    print("="*70)

    total_experiments = len(graphs) * len(ALGORITHMS_CONFIG)
    experiment_num = 0

    start_time = datetime.now()
    all_results = []

    # Main loop
    for graph_name, graph_loader, size_category in graphs:
        print(f"\n{'='*70}")
        print(f"Loading graph: {graph_name} (category: {size_category})")
        print(f"{'='*70}")

        try:
            G = graph_loader()
            n = G.number_of_nodes()
            m = G.number_of_edges()
            density = 2 * m / (n * (n - 1)) if n > 1 else 0

            print(f"Loaded: {n:,} vertices, {m:,} edges, density={density:.4f}")

            graph_props = {
                'vertices': n,
                'edges': m,
                'density': density,
                'size_category': size_category
            }

        except Exception as e:
            print(f"❌ Failed to load {graph_name}: {e}")
            continue

        # Determine repetitions for this graph
        if tier == 'both' and size_category in ['ultra_large', 'ultra_dense', 'xlarge_dense']:
            current_reps = 10
        else:
            current_reps = reps

        # Test each algorithm
        for algo_name, algo_config in ALGORITHMS_CONFIG.items():
            experiment_num += 1

            # Check if should skip
            if size_category in algo_config['skip_on']:
                print(f"\n[{experiment_num}/{total_experiments}] SKIPPING {algo_name} on {graph_name} ({size_category})")
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

            # Checkpoint every 50 trials
            if len(all_results) % 50 == 0:
                runner.save_checkpoint(checkpoint_file=f'overnight/checkpoint_{len(all_results)}.pkl')

                # Save progressive CSV
                df = pd.DataFrame(all_results)
                df.to_csv('results/overnight/progress.csv', index=False)
                print(f"\n  💾 Checkpoint saved: {len(all_results)} trials")

    # Final save
    print(f"\n{'='*70}")
    print("SAVING FINAL RESULTS")
    print(f"{'='*70}")

    df = pd.DataFrame(all_results)
    df.to_csv(f'results/overnight/{tier}_final_results.csv', index=False)

    runner.save_results(filename=f'overnight/{tier}_final_results.json')
    runner.save_checkpoint(checkpoint_file=f'overnight/{tier}_final_checkpoint.pkl')

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\nExperiments completed!")
    print(f"Total duration: {duration}")
    print(f"Total trials: {len(all_results)}")
    print(f"Successful trials: {len([r for r in all_results if r.get('success', False)])}")
    print(f"Success rate: {len([r for r in all_results if r.get('success', False)]) / len(all_results) * 100:.1f}%")
    print(f"\nResults saved to: results/overnight/{tier}_final_results.csv")
    print("="*70)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run overnight experiments')
    parser.add_argument('--tier', choices=['core', 'stretch', 'both'], default='core',
                       help='Which tier to run')
    parser.add_argument('--reps', type=int, default=40,
                       help='Repetitions per algorithm-graph pair (core tier)')
    parser.add_argument('--sa-include', action='store_true', default=False,
                       help='Override SA inclusion (for testing)')

    args = parser.parse_args()

    # Update SA configuration if override specified
    if args.sa_include and not SA_INCLUDE:
        print("WARNING: Overriding SA exclusion - adding SA to algorithms")
        ALGORITHMS_CONFIG['simulated_annealing'] = {
            'func': lambda G: simulated_annealing_edge_cover(G, initial_solution='lazy_greedy'),
            'skip_on': ['large', 'xlarge', 'ultra_large', 'dense', 'ultra_dense', 'xlarge_dense'],
            'description': 'Simulated annealing (optimized, small/medium graphs only)'
        }

    run_overnight_experiments(tier=args.tier, repetitions=args.reps)
