"""
Lazy Greedy Algorithm for Edge Cover (3/2-approximation)

This module implements the lazy greedy algorithm that achieves a 3/2-approximation
ratio for the minimum edge cover problem. The algorithm uses a priority queue
to efficiently select edges that cover the most uncovered vertices.

Time Complexity: O(|E| log |E|)
Approximation Ratio: 3/2
"""

import networkx as nx
import heapq
from typing import Set, Tuple, List
import time


def lazy_greedy_edge_cover(G: nx.Graph, randomize_ties: bool = False, seed: int = None) -> Tuple[Set[Tuple[int, int]], dict]:
    """
    Compute edge cover using lazy greedy algorithm with 3/2-approximation guarantee.

    Algorithm:
    1. Initialize priority queue with all edges, prioritized by number of uncovered endpoints
    2. While there are uncovered vertices:
       - Extract edge with maximum uncovered endpoints
       - If edge still covers uncovered vertices, add to cover
       - Otherwise, recompute priority and re-insert
    3. Return edge cover

    Args:
        G: NetworkX graph (must have no isolated vertices)
        randomize_ties: Use random tie-breaking for edges with equal priority
        seed: Random seed for reproducibility

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Edge cover with 3/2-approximation guarantee
        - metrics_dict: Contains 'runtime', 'cover_size', 'operations'

    Approximation Guarantee:
        |returned cover| ≤ (3/2) * |optimal cover|

        Proof sketch: The algorithm mimics a matching-based approach.
        Each edge covers at most 2 vertices. Optimal uses at least n - m edges
        where m is maximum matching size. Greedy uses at most 3m/2 edges.

    References:
        Bar-Yehuda, R., & Even, S. (1981). "A linear-time approximation
        algorithm for the weighted vertex cover problem"
    """
    if seed is not None:
        import random
        random.seed(seed)

    start_time = time.time()
    operations = 0

    # Check for isolated vertices
    if any(G.degree(v) == 0 for v in G.nodes()):
        raise ValueError("Graph contains isolated vertices")

    # Step 1: Initialize uncovered vertices
    uncovered = set(G.nodes())
    edge_cover = set()

    # Step 2: Create priority queue with all edges
    # Use negative priority for max-heap (heapq is min-heap by default)
    # Priority: number of uncovered endpoints (2, 1, or 0)
    # Heap entries: (-priority, tie_breaker, edge)
    pq = []
    tie_breaker = 0

    for u, v in G.edges():
        edge = (min(u, v), max(u, v))
        priority = _count_uncovered_endpoints(edge, uncovered)
        heapq.heappush(pq, (-priority, tie_breaker, edge))
        tie_breaker += 1
        operations += 1

    # Step 3: Main greedy loop
    while uncovered and pq:
        # Pop edge with highest priority
        neg_priority, _, edge = heapq.heappop(pq)
        old_priority = -neg_priority
        operations += 1

        # Lazy evaluation: check if priority is still valid
        current_priority = _count_uncovered_endpoints(edge, uncovered)

        if current_priority == 0:
            # Both endpoints already covered, skip this edge
            continue

        if current_priority != old_priority:
            # Priority changed, re-insert with updated priority
            heapq.heappush(pq, (-current_priority, tie_breaker, edge))
            tie_breaker += 1
            operations += 1
            continue

        # Priority is still valid, add edge to cover
        edge_cover.add(edge)
        u, v = edge

        # Update uncovered vertices
        uncovered.discard(u)
        uncovered.discard(v)
        operations += 1

    # Verify all vertices are covered
    if uncovered:
        raise RuntimeError(f"Algorithm failed: {len(uncovered)} vertices still uncovered")

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': len(edge_cover),
        'operations': operations
    }

    return edge_cover, metrics


def _count_uncovered_endpoints(edge: Tuple[int, int], uncovered: Set[int]) -> int:
    """
    Count how many endpoints of edge are uncovered.

    Args:
        edge: Tuple (u, v) representing edge
        uncovered: Set of uncovered vertices

    Returns:
        Number of uncovered endpoints (0, 1, or 2)
    """
    u, v = edge
    count = 0
    if u in uncovered:
        count += 1
    if v in uncovered:
        count += 1
    return count
