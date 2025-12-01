"""
Israeli-Itai Randomized Matching Algorithm for Edge Cover

This module implements the randomized parallel matching algorithm by Israeli & Itai (1986).
The algorithm runs in expected O(log n) parallel rounds.

Key Idea:
- Each round, vertices randomly propose to neighbors
- Conflicts are resolved randomly
- Accepted proposals form matching edges
- Continue until all vertices are matched or covered

Expected Parallel Depth: O(log n) rounds
Sequential Work: O(|E| log n)
"""

import networkx as nx
import random
from typing import Set, Tuple, List
import time


def israeli_itai_edge_cover(G: nx.Graph, max_rounds: int = None, seed: int = None, verbose: bool = False, smart_proposals: bool = True, timeout: int = 300) -> Tuple[Set[Tuple[int, int]], dict]:
    """
    Compute edge cover using Israeli-Itai randomized matching with greedy extension.

    Algorithm:
    1. Phase 1 - Randomized Matching:
       - Each round: unmatched vertices propose to random neighbor
       - Receiving vertex randomly accepts one proposal
       - Accepted proposals become matching edges
       - Repeat until no more matches possible

    2. Phase 2 - Greedy Extension:
       - For remaining unmatched vertices, add incident edge

    Args:
        G: NetworkX graph (must have no isolated vertices)
        max_rounds: Maximum matching rounds (default: 10 * ceil(log2(n)))
        seed: Random seed for reproducibility
        verbose: If True, print detailed diagnostics
        smart_proposals: If True, use improved proposal strategy (default: True)
        timeout: Maximum time allowed in seconds (default: 300)

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Set of edges forming the edge cover
        - metrics_dict: Contains runtime, cover_size, rounds, matching_size,
                       convergence_history, proposal_conflict_stats

    References:
        Israeli, A., & Itai, A. (1986). "A fast and simple randomized parallel
        algorithm for maximal matching". Information Processing Letters.
    """
    if seed is not None:
        random.seed(seed)

    start_time = time.time()

    # Check for isolated vertices
    if any(G.degree(v) == 0 for v in G.nodes()):
        raise ValueError("Graph contains isolated vertices")

    n = G.number_of_nodes()
    if max_rounds is None:
        max_rounds = 10 * (n.bit_length())  # 10 * log2(n)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Israeli-Itai Algorithm Diagnostics")
        print(f"{'='*60}")
        print(f"Graph: {n} vertices, {G.number_of_edges()} edges")
        print(f"Max rounds: {max_rounds} (10 * log2({n}) = 10 * {n.bit_length()})")

    # Step 1: Initialize
    matching_edges = set()
    matched_vertices = set()
    unmatched_vertices = set(G.nodes())

    # Tracking metrics
    convergence_history = []
    total_proposal_conflicts = 0
    rounds_with_conflicts = 0

    # Phase 1: Randomized matching rounds
    rounds_completed = 0
    for round_num in range(max_rounds):
        if not unmatched_vertices:
            break  # All vertices matched

        # Execute one propose-accept round
        new_edges, conflicts = _propose_accept_round_instrumented(G, unmatched_vertices, smart_proposals=smart_proposals)

        # Track conflicts
        if conflicts > 0:
            total_proposal_conflicts += conflicts
            rounds_with_conflicts += 1

        if not new_edges:
            if verbose:
                print(f"\nRound {round_num + 1}: No new matches, stopping early")
            break  # No new matches possible

        # Add new edges to matching
        matched_this_round = 0
        for edge in new_edges:
            matching_edges.add(edge)
            u, v = edge
            matched_vertices.add(u)
            matched_vertices.add(v)
            unmatched_vertices.discard(u)
            unmatched_vertices.discard(v)
            matched_this_round += 2

        rounds_completed += 1

        # Record convergence
        convergence_history.append({
            'round': round_num + 1,
            'matched_this_round': matched_this_round,
            'total_matched': len(matched_vertices),
            'unmatched_remaining': len(unmatched_vertices),
            'matching_size': len(matching_edges),
            'proposal_conflicts': conflicts
        })

        if verbose and (round_num < 5 or round_num % 10 == 0 or not unmatched_vertices):
            print(f"Round {round_num + 1:3d}: +{matched_this_round:3d} matched | "
                  f"Total: {len(matched_vertices):4d}/{n:4d} | "
                  f"Unmatched: {len(unmatched_vertices):4d} | "
                  f"Conflicts: {conflicts:3d}")

    if verbose:
        print(f"\n{'─'*60}")
        print(f"Phase 1 Complete: {rounds_completed} rounds")
        print(f"Matching size: {len(matching_edges)} edges")
        print(f"Matched vertices: {len(matched_vertices)}/{n}")
        print(f"Unmatched vertices: {len(unmatched_vertices)}")
        print(f"Avg conflicts per round: {total_proposal_conflicts / max(rounds_completed, 1):.2f}")

    # Phase 2: Greedy extension for remaining unmatched vertices
    edge_cover = matching_edges.copy()
    extension_edges_added = 0

    for v in unmatched_vertices:
        # Add arbitrary incident edge (could be improved!)
        neighbors = list(G.neighbors(v))
        if not neighbors:
            raise ValueError(f"Vertex {v} has no neighbors (isolated)")

        # Choose first neighbor (TODO: could use min-degree neighbor)
        neighbor = neighbors[0]
        edge = (min(v, neighbor), max(v, neighbor))
        if edge not in edge_cover:
            edge_cover.add(edge)
            extension_edges_added += 1

    if verbose:
        print(f"\nPhase 2 Complete: Greedy Extension")
        print(f"Extension edges added: {extension_edges_added}")
        print(f"Final cover size: {len(edge_cover)} edges")
        print(f"{'='*60}\n")

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': len(edge_cover),
        'rounds': rounds_completed,
        'max_rounds': max_rounds,
        'matching_size': len(matching_edges),
        'unmatched_after_matching': len(unmatched_vertices),
        'extension_edges': extension_edges_added,
        'convergence_history': convergence_history,
        'total_proposal_conflicts': total_proposal_conflicts,
        'avg_conflicts_per_round': total_proposal_conflicts / max(rounds_completed, 1) if rounds_completed > 0 else 0,
        'rounds_with_conflicts': rounds_with_conflicts
    }

    return edge_cover, metrics


def _propose_accept_round_instrumented(G: nx.Graph, unmatched: Set[int], smart_proposals: bool = True) -> Tuple[Set[Tuple[int, int]], int]:
    """
    Execute one round of propose-accept mechanism with conflict tracking.

    Args:
        G: NetworkX graph
        unmatched: Set of currently unmatched vertices
        smart_proposals: If True, propose to lowest-degree unmatched neighbor to reduce conflicts

    Returns:
        Tuple of (matched_edges, num_conflicts)
        - matched_edges: Set of newly matched edges in this round
        - num_conflicts: Number of proposal conflicts (vertices receiving multiple proposals)
    """
    # Step 1: Each unmatched vertex proposes to a neighbor
    proposals = {}  # proposer -> proposed_neighbor
    proposals_received = {}  # receiver -> list of proposers

    for v in unmatched:
        # Get neighbors of v
        neighbors = list(G.neighbors(v))
        if not neighbors:
            continue

        # Select neighbor to propose to
        if smart_proposals:
            # Strategy 1: Prefer unmatched neighbors (reduces conflicts)
            unmatched_neighbors = [n for n in neighbors if n in unmatched]

            if unmatched_neighbors:
                # Among unmatched neighbors, choose lowest degree (less popular → fewer conflicts)
                proposed_neighbor = min(unmatched_neighbors, key=lambda n: G.degree(n))
            else:
                # All neighbors are matched, choose any (random or min-degree)
                proposed_neighbor = min(neighbors, key=lambda n: G.degree(n))
        else:
            # Original strategy: random neighbor
            proposed_neighbor = random.choice(neighbors)

        # Record proposal
        proposals[v] = proposed_neighbor

        # Track who received this proposal
        if proposed_neighbor not in proposals_received:
            proposals_received[proposed_neighbor] = []
        proposals_received[proposed_neighbor].append(v)

    # Count conflicts (vertices receiving >1 proposal)
    num_conflicts = sum(1 for proposers in proposals_received.values() if len(proposers) > 1)

    # Step 2: Each vertex that received proposals randomly accepts one
    matched_edges = set()

    for receiver, proposers in proposals_received.items():
        # If multiple proposers (conflict), accept the one with lowest degree
        # (more likely to need matching, fewer alternatives)
        if len(proposers) > 1 and smart_proposals:
            accepted_proposer = min(proposers, key=lambda p: G.degree(p))
        else:
            # Single proposer or random selection
            accepted_proposer = random.choice(proposers) if len(proposers) > 1 else proposers[0]

        # Create edge (normalize representation)
        edge = (min(receiver, accepted_proposer), max(receiver, accepted_proposer))
        matched_edges.add(edge)

    return matched_edges, num_conflicts


def _propose_accept_round(G: nx.Graph, unmatched: Set[int]) -> Set[Tuple[int, int]]:
    """
    Execute one round of propose-accept mechanism (non-instrumented version).

    Args:
        G: NetworkX graph
        unmatched: Set of currently unmatched vertices

    Returns:
        Set of newly matched edges in this round
    """
    edges, _ = _propose_accept_round_instrumented(G, unmatched)
    return edges
