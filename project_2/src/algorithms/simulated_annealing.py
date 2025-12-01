"""
Simulated Annealing for Edge Cover Optimization

This module implements simulated annealing metaheuristic for finding
near-optimal edge covers. The algorithm explores the solution space
using probabilistic acceptance of worse solutions to escape local optima.

Time Complexity: O(iterations * |V|) where iterations is configurable
Quality: Often near-optimal with proper parameter tuning
"""

import networkx as nx
import random
import math
from typing import Set, Tuple, List, Literal
import time

# Import for initial solution generation
from .lazy_greedy import lazy_greedy_edge_cover
from .nearest_neighbor import nearest_neighbor_edge_cover


def simulated_annealing_edge_cover(
    G: nx.Graph,
    initial_temp: float = None,
    cooling_rate: float = 0.95,
    max_iterations: int = None,
    seed: int = None,
    initial_solution: Literal['all_edges', 'lazy_greedy', 'nearest_neighbor'] = 'lazy_greedy',
    timeout: int = 300
) -> Tuple[Set[Tuple[int, int]], dict]:
    """
    Compute edge cover using simulated annealing optimization.

    Algorithm:
    1. Start with initial feasible solution (e.g., all edges)
    2. Iteratively apply neighborhood operators:
       - Remove redundant edge (if cover remains valid)
       - Swap edge
       - Add edge then remove redundant
    3. Accept worse solutions with probability exp(-Δ/T)
    4. Decrease temperature according to cooling schedule
    5. Return best solution found

    Args:
        G: NetworkX graph (must have no isolated vertices)
        initial_temp: Initial temperature (default: auto-tune based on graph size)
        cooling_rate: Temperature multiplier per iteration (default: 0.95)
        max_iterations: Maximum iterations (default: 1000 * n)
        seed: Random seed for reproducibility
        initial_solution: Method to generate initial solution (default: 'lazy_greedy')
            - 'all_edges': Start with all edges (original, slow)
            - 'lazy_greedy': Start with lazy greedy solution (recommended)
            - 'nearest_neighbor': Start with nearest neighbor solution
        timeout: Maximum time allowed in seconds (default: 300)

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Best edge cover found
        - metrics_dict: Contains 'runtime', 'cover_size', 'iterations',
                       'acceptance_rate', 'convergence_history'

    Neighborhood Operators:
        1. Remove Redundant: Remove edge if remaining edges still cover all vertices
        2. Swap Edge: Replace one edge with another
        3. Add-Remove: Add edge covering uncovered area, remove redundant elsewhere
    """
    if seed is not None:
        random.seed(seed)

    start_time = time.time()

    # Check for isolated vertices
    if any(G.degree(v) == 0 for v in G.nodes()):
        raise ValueError("Graph contains isolated vertices")

    n = G.number_of_nodes()

    # Auto-tune parameters if not provided
    if initial_temp is None:
        initial_temp = 100.0 * math.log(n + 1)

    if max_iterations is None:
        # OPTIMIZED: Reduced iteration caps for better performance
        # After removing per-iteration validation, we can afford fewer iterations
        if n <= 100:
            max_iterations = min(5000, 50 * n)    # Small: 5k cap (was 1000*n)
        elif n <= 500:
            max_iterations = min(10000, 20 * n)   # Medium: 10k cap (was 100*n)
        elif n <= 2000:
            max_iterations = min(15000, 10 * n)   # Large: 15k cap (was 50*n)
        else:
            max_iterations = min(20000, 5 * n)    # Very large: 20k cap (was 20*n)

        # Overall safety cap
        max_iterations = min(max_iterations, 20000)  # Reduced from 50k

    # Step 1: Generate initial solution
    if initial_solution == 'all_edges':
        # Original approach: start with all edges
        current_cover = set()
        for u, v in G.edges():
            current_cover.add((min(u, v), max(u, v)))
    elif initial_solution == 'lazy_greedy':
        # Recommended: start with lazy greedy solution
        current_cover, _ = lazy_greedy_edge_cover(G, seed=seed, timeout=timeout)
    elif initial_solution == 'nearest_neighbor':
        # Alternative: start with nearest neighbor solution
        current_cover, _ = nearest_neighbor_edge_cover(G, seed=seed, timeout=timeout)
    else:
        raise ValueError(f"Unknown initial_solution method: {initial_solution}")

    # Verify initial solution is valid
    if not _is_valid_cover(current_cover, G):
        raise RuntimeError("Initial solution is not a valid cover")

    # Track initial size before optimization
    initial_cover_size = len(current_cover)

    # Track best solution found
    best_cover = current_cover.copy()
    best_size = len(best_cover)

    # Tracking metrics
    temperature = initial_temp
    acceptances = 0
    rejections = 0
    convergence_history = []

    # Step 2: Main SA loop
    for iteration in range(max_iterations):
        # Generate neighbor solution using one of three operators
        operator_choice = random.choice(['remove', 'swap', 'add_remove'])

        if operator_choice == 'remove':
            neighbor_cover = _remove_redundant_edge(current_cover.copy(), G)
            # Remove operator checks validity internally, safe to skip validation
            needs_validation = False
        elif operator_choice == 'swap':
            neighbor_cover = _swap_edge(current_cover.copy(), G)
            # Swap can create invalid covers, must validate
            needs_validation = True
        else:  # add_remove
            neighbor_cover = _add_remove_edge(current_cover.copy(), G)
            # Add-remove can create invalid covers, must validate
            needs_validation = True

        # OPTIMIZATION: Only validate when operator doesn't guarantee validity
        # This reduces validation calls significantly (~66% reduction)
        if needs_validation:
            if not _is_valid_cover(neighbor_cover, G):
                continue  # Skip invalid neighbors

        # Periodic safety check for current solution
        if iteration % 1000 == 0:
            if not _is_valid_cover(current_cover, G):
                raise RuntimeError(f"Invalid cover detected at iteration {iteration}")

        # Compute energy (solution size)
        current_energy = len(current_cover)
        neighbor_energy = len(neighbor_cover)
        delta_energy = neighbor_energy - current_energy

        # Metropolis acceptance criterion
        if delta_energy < 0:
            # Better solution, always accept
            current_cover = neighbor_cover
            acceptances += 1
        elif temperature > 0:
            # Worse solution, accept with probability exp(-delta/T)
            acceptance_prob = math.exp(-delta_energy / temperature)
            if random.random() < acceptance_prob:
                current_cover = neighbor_cover
                acceptances += 1
            else:
                rejections += 1
        else:
            rejections += 1

        # Update best solution
        if len(current_cover) < best_size:
            best_cover = current_cover.copy()
            best_size = len(best_cover)

        # Update temperature (exponential cooling)
        temperature *= cooling_rate

        # Record convergence (sample every 100 iterations)
        if iteration % 100 == 0:
            convergence_history.append({
                'iteration': iteration,
                'current_size': len(current_cover),
                'best_size': best_size,
                'temperature': temperature
            })

    # Calculate acceptance rate
    total_attempts = acceptances + rejections
    acceptance_rate = acceptances / total_attempts if total_attempts > 0 else 0.0

    # Final validation to ensure best solution is valid
    if not _is_valid_cover(best_cover, G):
        raise RuntimeError("Final best solution is not a valid edge cover!")

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': len(best_cover),
        'iterations': max_iterations,
        'acceptance_rate': acceptance_rate,
        'convergence_history': convergence_history,
        'final_temperature': temperature,
        'initial_solution_method': initial_solution,
        'initial_solution_size': initial_cover_size,
        'improvement': initial_cover_size - len(best_cover)
    }

    return best_cover, metrics


def _remove_redundant_edge(cover: Set[Tuple[int, int]], G: nx.Graph) -> Set[Tuple[int, int]]:
    """
    Try to remove a redundant edge from cover.

    An edge is redundant if removing it still leaves all vertices covered.
    """
    if not cover:
        return cover

    # Randomly select an edge to try removing
    edge_to_remove = random.choice(list(cover))
    test_cover = cover - {edge_to_remove}

    # Check if remaining cover is still valid
    if _is_valid_cover(test_cover, G):
        return test_cover
    else:
        return cover  # Cannot remove, return original


def _swap_edge(cover: Set[Tuple[int, int]], G: nx.Graph) -> Set[Tuple[int, int]]:
    """
    Swap one edge in the cover for another edge not in the cover.
    """
    if not cover:
        return cover

    # Get edges not in cover
    all_edges = set()
    for u, v in G.edges():
        all_edges.add((min(u, v), max(u, v)))

    edges_not_in_cover = all_edges - cover

    if not edges_not_in_cover:
        return cover  # No edges to swap in

    # Randomly select edge to remove and edge to add
    edge_to_remove = random.choice(list(cover))
    edge_to_add = random.choice(list(edges_not_in_cover))

    # Create new cover
    new_cover = (cover - {edge_to_remove}) | {edge_to_add}

    return new_cover


def _add_remove_edge(cover: Set[Tuple[int, int]], G: nx.Graph) -> Set[Tuple[int, int]]:
    """
    Add a random edge and try to remove a redundant edge.

    This can help explore the solution space more broadly.
    """
    # Get edges not in cover
    all_edges = set()
    for u, v in G.edges():
        all_edges.add((min(u, v), max(u, v)))

    edges_not_in_cover = all_edges - cover

    if not edges_not_in_cover:
        # All edges already in cover, just try to remove one
        return _remove_redundant_edge(cover, G)

    # Add a random edge
    edge_to_add = random.choice(list(edges_not_in_cover))
    new_cover = cover | {edge_to_add}

    # Try to remove a redundant edge
    new_cover = _remove_redundant_edge(new_cover, G)

    return new_cover


def _is_valid_cover(cover: Set[Tuple[int, int]], G: nx.Graph) -> bool:
    """Check if cover is valid (all vertices covered)."""
    covered = set()
    for u, v in cover:
        covered.add(u)
        covered.add(v)
    return covered == set(G.nodes())
