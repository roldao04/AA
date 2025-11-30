"""
Exact Edge Cover Algorithm using Maximum Matching

This module implements the exact edge cover algorithm based on Gallai's theorem:
For a graph G with no isolated vertices:
    |minimum edge cover| + |maximum matching| = |V|

Time Complexity: O(n²√n) via Blossom algorithm for maximum matching
"""

import networkx as nx
from typing import Set, Tuple
import time


def exact_edge_cover(G: nx.Graph, timeout: int = 300) -> Tuple[Set[Tuple[int, int]], dict]:
    """
    Compute the minimum edge cover using maximum matching.

    Algorithm:
    1. Find maximum matching M using Blossom algorithm
    2. For each unmatched vertex v, add an arbitrary incident edge
    3. Return M ∪ {incident edges of unmatched vertices}

    Args:
        G: NetworkX graph (must have no isolated vertices)
        timeout: Maximum time allowed in seconds (default: 300)

    Returns:
        Tuple of (edge_cover_set, metrics_dict)
        - edge_cover_set: Set of edges forming the minimum edge cover
        - metrics_dict: Contains 'runtime', 'cover_size', 'operations'

    Raises:
        TimeoutError: If computation exceeds timeout
        ValueError: If graph has isolated vertices

    References:
        Gallai, T. (1959). "Über extreme Punkt-und Kantenmengen"
    """
    start_time = time.time()
    operations = 0

    # Check for isolated vertices
    if any(G.degree(v) == 0 for v in G.nodes()):
        raise ValueError("Graph contains isolated vertices")

    # Step 1: Compute maximum matching using NetworkX
    # For unweighted graphs, max_weight_matching with maxcardinality=True gives max matching
    try:
        matching_dict = nx.max_weight_matching(G, maxcardinality=True)
        operations += 1

        # Convert matching dict to set of edges
        matching_edges = set()
        matched_vertices = set()

        for u, v in matching_dict:
            # Normalize edge representation (smaller vertex first)
            edge = (min(u, v), max(u, v))
            matching_edges.add(edge)
            matched_vertices.add(u)
            matched_vertices.add(v)
            operations += 1
    except Exception as e:
        # If timeout or other error during matching
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Matching computation exceeded timeout of {timeout}s")
        raise e

    # Step 2: Find unmatched vertices
    all_vertices = set(G.nodes())
    unmatched_vertices = all_vertices - matched_vertices
    operations += 1

    # Step 3: For each unmatched vertex, add an arbitrary incident edge
    edge_cover = matching_edges.copy()

    for v in unmatched_vertices:
        # Get any neighbor of v
        neighbors = list(G.neighbors(v))
        if not neighbors:
            raise ValueError(f"Vertex {v} has no neighbors (isolated)")

        # Add edge to first neighbor (arbitrary choice)
        neighbor = neighbors[0]
        edge = (min(v, neighbor), max(v, neighbor))
        edge_cover.add(edge)
        operations += 1

    # Check timeout
    if time.time() - start_time > timeout:
        raise TimeoutError(f"Edge cover computation exceeded timeout of {timeout}s")

    # Verify result is valid (optional, but good for debugging)
    assert verify_edge_cover(G, edge_cover), "Generated edge cover is invalid"

    metrics = {
        'runtime': time.time() - start_time,
        'cover_size': len(edge_cover),
        'operations': operations,
        'matching_size': len(matching_edges),
        'unmatched_vertices': len(unmatched_vertices)
    }

    return edge_cover, metrics


def verify_edge_cover(G: nx.Graph, edge_cover: Set[Tuple[int, int]]) -> bool:
    """
    Verify that a set of edges forms a valid edge cover.

    Args:
        G: NetworkX graph
        edge_cover: Set of edges to verify

    Returns:
        True if edge_cover covers all vertices, False otherwise
    """
    covered_vertices = set()
    for u, v in edge_cover:
        covered_vertices.add(u)
        covered_vertices.add(v)

    return covered_vertices == set(G.nodes())
