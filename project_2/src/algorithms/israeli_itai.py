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


def israeli_itai_edge_cover(G: nx.Graph, max_rounds: int = None, seed: int = None) -> Tuple[Set[Tuple[int, int]], dict]:
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

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Set of edges forming the edge cover
        - metrics_dict: Contains 'runtime', 'cover_size', 'rounds', 'matching_size'

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

    # Step 1: Initialize
    matching_edges = set()
    matched_vertices = set()
    unmatched_vertices = set(G.nodes())

    # Phase 1: Randomized matching rounds
    rounds_completed = 0
    for round_num in range(max_rounds):
        if not unmatched_vertices:
            break  # All vertices matched

        # Execute one propose-accept round
        new_edges = _propose_accept_round(G, unmatched_vertices)

        if not new_edges:
            break  # No new matches possible

        # Add new edges to matching
        for edge in new_edges:
            matching_edges.add(edge)
            u, v = edge
            matched_vertices.add(u)
            matched_vertices.add(v)
            unmatched_vertices.discard(u)
            unmatched_vertices.discard(v)

        rounds_completed += 1

    # Phase 2: Greedy extension for remaining unmatched vertices
    edge_cover = matching_edges.copy()

    for v in unmatched_vertices:
        # Add arbitrary incident edge
        neighbors = list(G.neighbors(v))
        if not neighbors:
            raise ValueError(f"Vertex {v} has no neighbors (isolated)")

        # Choose first neighbor
        neighbor = neighbors[0]
        edge = (min(v, neighbor), max(v, neighbor))
        edge_cover.add(edge)

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': len(edge_cover),
        'rounds': rounds_completed,
        'matching_size': len(matching_edges),
        'unmatched_after_matching': len(unmatched_vertices)
    }

    return edge_cover, metrics


def _propose_accept_round(G: nx.Graph, unmatched: Set[int]) -> Set[Tuple[int, int]]:
    """
    Execute one round of propose-accept mechanism.

    Args:
        G: NetworkX graph
        unmatched: Set of currently unmatched vertices

    Returns:
        Set of newly matched edges in this round
    """
    # Step 1: Each unmatched vertex proposes to a random neighbor
    proposals = {}  # proposer -> proposed_neighbor
    proposals_received = {}  # receiver -> list of proposers

    for v in unmatched:
        # Get neighbors of v
        neighbors = list(G.neighbors(v))
        if not neighbors:
            continue

        # Randomly select a neighbor to propose to
        proposed_neighbor = random.choice(neighbors)

        # Record proposal
        proposals[v] = proposed_neighbor

        # Track who received this proposal
        if proposed_neighbor not in proposals_received:
            proposals_received[proposed_neighbor] = []
        proposals_received[proposed_neighbor].append(v)

    # Step 2: Each vertex that received proposals randomly accepts one
    matched_edges = set()

    for receiver, proposers in proposals_received.items():
        # Randomly accept one proposal
        accepted_proposer = random.choice(proposers)

        # Create edge (normalize representation)
        edge = (min(receiver, accepted_proposer), max(receiver, accepted_proposer))
        matched_edges.add(edge)

    return matched_edges
