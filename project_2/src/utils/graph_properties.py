"""
Graph Property Extraction and Synthetic Graph Generation

This module provides functions to:
- Compute structural properties of graphs
- Generate synthetic graphs with controlled properties
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Tuple


def compute_graph_properties(G: nx.Graph) -> Dict[str, float]:
    """
    Compute structural properties of a graph.

    Args:
        G: NetworkX graph

    Returns:
        Dictionary containing:
        - vertices: Number of vertices
        - edges: Number of edges
        - density: Edge density
        - avg_degree: Average vertex degree
        - degree_std: Standard deviation of degrees
        - max_degree: Maximum degree
        - avg_clustering: Average clustering coefficient
        - connected_components: Number of connected components
        - diameter: Graph diameter (if connected and small enough)
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()

    properties = {
        'vertices': n,
        'edges': m,
        'density': nx.density(G),
        'avg_degree': 2 * m / n if n > 0 else 0,
    }

    # Degree statistics
    degrees = [d for _, d in G.degree()]
    properties['degree_std'] = np.std(degrees) if degrees else 0
    properties['max_degree'] = max(degrees) if degrees else 0

    # Clustering coefficient (can be slow for large graphs)
    try:
        properties['avg_clustering'] = nx.average_clustering(G)
    except:
        properties['avg_clustering'] = 0.0

    # Connected components
    properties['connected_components'] = nx.number_connected_components(G)

    # Diameter (only for small connected graphs)
    if nx.is_connected(G) and n < 1000:
        try:
            properties['diameter'] = nx.diameter(G)
        except:
            properties['diameter'] = -1
    else:
        properties['diameter'] = -1

    return properties


def generate_synthetic_graphs(
    n_graphs: int = 30,
    base_size: int = 500
) -> List[Tuple[str, nx.Graph, Dict[str, float]]]:
    """
    Generate synthetic graphs with controlled properties for empirical study.

    Generates three categories:
    1. Erdős-Rényi: Varying density
    2. Watts-Strogatz: Varying clustering
    3. Barabási-Albert: Varying degree distribution

    Args:
        n_graphs: Total number of graphs to generate
        base_size: Base number of vertices

    Returns:
        List of tuples (name, graph, properties_dict)
    """
    graphs = []

    # Category 1: Erdős-Rényi with varying density
    print("Generating Erdős-Rényi graphs (density variation)...")
    densities = np.linspace(0.1, 0.9, 9)
    for i, p in enumerate(densities):
        G = nx.erdos_renyi_graph(n=base_size, p=p, seed=42 + i)

        # Remove isolated vertices
        isolated = list(nx.isolates(G))
        G.remove_nodes_from(isolated)

        if G.number_of_nodes() > 0:
            name = f"ER_n{base_size}_p{p:.2f}"
            props = compute_graph_properties(G)
            graphs.append((name, G, props))

    # Category 2: Watts-Strogatz with varying clustering
    print("Generating Watts-Strogatz graphs (clustering variation)...")
    k_values = [4, 6, 8, 10, 12]
    p_values = [0.01, 0.1, 0.3]
    for i, k in enumerate(k_values):
        for j, p in enumerate(p_values):
            G = nx.watts_strogatz_graph(n=base_size, k=k, p=p, seed=100 + i * 10 + j)

            if G.number_of_nodes() > 0:
                name = f"WS_n{base_size}_k{k}_p{p:.2f}"
                props = compute_graph_properties(G)
                graphs.append((name, G, props))

    # Category 3: Barabási-Albert with varying degree distribution
    print("Generating Barabási-Albert graphs (degree distribution variation)...")
    sizes = [200, 500, 1000]
    m_values = [2, 5, 10]
    for i, n in enumerate(sizes):
        for j, m in enumerate(m_values):
            G = nx.barabasi_albert_graph(n=n, m=m, seed=200 + i * 10 + j)

            if G.number_of_nodes() > 0:
                name = f"BA_n{n}_m{m}"
                props = compute_graph_properties(G)
                graphs.append((name, G, props))

    print(f"Generated {len(graphs)} synthetic graphs")
    return graphs


def print_graph_summary(G: nx.Graph, name: str = "Graph") -> None:
    """
    Print a formatted summary of graph properties.

    Args:
        G: NetworkX graph
        name: Graph name for display
    """
    props = compute_graph_properties(G)

    print(f"\n{name} Properties:")
    print(f"  Vertices: {props['vertices']}")
    print(f"  Edges: {props['edges']}")
    print(f"  Density: {props['density']:.4f}")
    print(f"  Avg Degree: {props['avg_degree']:.2f} ± {props['degree_std']:.2f}")
    print(f"  Max Degree: {props['max_degree']}")
    print(f"  Avg Clustering: {props['avg_clustering']:.4f}")
    print(f"  Connected Components: {props['connected_components']}")
    if props['diameter'] > 0:
        print(f"  Diameter: {props['diameter']}")
