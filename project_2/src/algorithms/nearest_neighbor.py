"""
Nearest Neighbor Algorithm for Edge Cover (2-approximation)

This module implements a simple nearest neighbor heuristic for edge cover.
For each vertex, select the minimum weight (or arbitrary) incident edge.

Time Complexity: O(|V| + |E|)
Approximation Ratio: 2 (trivial, since each vertex needs at least one edge)
"""

import networkx as nx
import random
from typing import Set, Tuple
import time


def nearest_neighbor_edge_cover(G: nx.Graph, seed: int = None) -> Tuple[Set[Tuple[int, int]], dict]:
    """
    Compute edge cover using simple nearest neighbor heuristic.

    Algorithm:
    1. For each vertex v in arbitrary order:
       - If v is not yet covered
       - Select an arbitrary (or min-weight) incident edge
       - Add edge to cover
    2. Return edge cover

    Args:
        G: NetworkX graph (must have no isolated vertices)
        seed: Random seed for vertex ordering

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Edge cover (not necessarily optimal)
        - metrics_dict: Contains 'runtime', 'cover_size'

    Approximation Guarantee:
        |returned cover| ≤ 2 * |optimal cover|

        Proof: Each vertex needs at least one incident edge. In worst case,
        we select n edges for n vertices. Optimal is at least n/2 (matching lower bound).

    Notes:
        - Very fast baseline algorithm
        - Often performs better than 2-approximation in practice
        - Trivially parallelizable
    """
    if seed is not None:
        random.seed(seed)

    start_time = time.time()

    # Check for isolated vertices
    if any(G.degree(v) == 0 for v in G.nodes()):
        raise ValueError("Graph contains isolated vertices")

    # TODO: Implement nearest neighbor algorithm
    # 1. Initialize covered vertices set
    # 2. Iterate through vertices (random or fixed order)
    # 3. For each uncovered vertex, select incident edge
    # 4. Mark both endpoints as covered
    # 5. Return edge cover with metrics

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': 0
    }

    return set(), metrics
