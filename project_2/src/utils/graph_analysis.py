"""
Graph Analysis Utilities

Functions for characterizing graph properties to enable scenario-based algorithm testing.
Computes structural metrics like density, clustering, degree distribution, etc.

Created: December 1, 2025
"""

import networkx as nx
import numpy as np
from typing import Dict, Optional, Tuple


def characterize_graph(G: nx.Graph) -> Dict[str, any]:
    """
    Compute comprehensive structural characteristics of a graph.

    Args:
        G: NetworkX graph

    Returns:
        Dictionary with graph characteristics:
        - Basic: vertices, edges, density
        - Degree: avg_degree, max_degree, min_degree, degree_std
        - Structure: clustering_coeff, diameter (if computable)
        - Type: graph_type classification
        - Scenario: scenario_category for algorithm selection

    Examples:
        >>> G = nx.karate_club_graph()
        >>> props = characterize_graph(G)
        >>> props['avg_degree']
        4.588...
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()

    if n == 0:
        raise ValueError("Graph has no vertices")

    if n == 1:
        return {
            'vertices': 1,
            'edges': 0,
            'density': 0.0,
            'avg_degree': 0.0,
            'max_degree': 0,
            'min_degree': 0,
            'degree_std': 0.0,
            'clustering_coeff': 0.0,
            'diameter': 0,
            'graph_type': 'singleton',
            'scenario_category': 'trivial'
        }

    # Basic metrics
    density = 2 * m / (n * (n - 1)) if n > 1 else 0.0

    # Degree metrics
    degrees = dict(G.degree())
    degree_values = list(degrees.values())
    avg_degree = np.mean(degree_values)
    max_degree = np.max(degree_values)
    min_degree = np.min(degree_values)
    degree_std = np.std(degree_values)

    # Clustering coefficient
    try:
        clustering_coeff = nx.average_clustering(G)
    except:
        clustering_coeff = 0.0

    # Diameter (only for small connected graphs)
    diameter = None
    if n <= 1000 and nx.is_connected(G):
        try:
            diameter = nx.diameter(G)
        except:
            diameter = None

    # Graph type classification
    graph_type = classify_graph_type(G, density, clustering_coeff, degree_std, avg_degree)

    # Scenario category for algorithm selection
    scenario_category = classify_scenario(n, m, density, avg_degree)

    return {
        # Basic
        'vertices': n,
        'edges': m,
        'density': density,

        # Degree statistics
        'avg_degree': avg_degree,
        'max_degree': max_degree,
        'min_degree': min_degree,
        'degree_std': degree_std,

        # Structure
        'clustering_coeff': clustering_coeff,
        'diameter': diameter,

        # Classification
        'graph_type': graph_type,
        'scenario_category': scenario_category
    }


def classify_graph_type(G: nx.Graph, density: float, clustering: float,
                       degree_std: float, avg_degree: float) -> str:
    """
    Classify graph into structural type based on properties.

    Types:
    - tree/forest: very sparse, low clustering
    - social_network: moderate density, high clustering
    - random: moderate density, low clustering
    - dense: high density
    - scale_free: high degree variance (power-law)
    - regular: low degree variance

    Args:
        G: NetworkX graph
        density: Graph density
        clustering: Average clustering coefficient
        degree_std: Standard deviation of degrees
        avg_degree: Average degree

    Returns:
        Graph type string
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()

    # Tree or forest (very sparse, acyclic structure)
    if m <= n and density < 0.001:
        if nx.is_forest(G):
            return 'tree' if nx.is_connected(G) else 'forest'
        return 'very_sparse'

    # Dense graphs
    if density > 0.5:
        return 'ultra_dense'
    if density > 0.2:
        return 'dense'

    # Regular or near-regular (low degree variance)
    if degree_std < 2 and avg_degree > 3:
        return 'regular'

    # Scale-free (power-law degree distribution - high variance)
    if degree_std > avg_degree:
        return 'scale_free'

    # Social network (moderate density, high clustering)
    if 0.001 < density < 0.1 and clustering > 0.3:
        return 'social_network'

    # Random graph (moderate density, low clustering)
    if 0.01 < density < 0.2 and clustering < 0.2:
        return 'random'

    # Sparse
    if density < 0.01:
        return 'sparse'

    # Default
    return 'mixed'


def classify_scenario(n: int, m: int, density: float, avg_degree: float) -> str:
    """
    Classify graph into scenario category for algorithm recommendation.

    Scenarios:
    - ultra_dense: p > 0.5 (exact/SA struggle, NN excels)
    - dense: 0.2 < p <= 0.5 (lazy greedy good balance)
    - medium: 0.01 < p <= 0.2 (israeli-itai shines)
    - sparse: p <= 0.01 (all approximations similar, NN fastest)
    - ultra_large: n > 100k (only NN practical)
    - mega: n > 1M (scalability limits)

    Args:
        n: Number of vertices
        m: Number of edges
        density: Graph density
        avg_degree: Average degree

    Returns:
        Scenario category string
    """
    # Size-based first (overrides density)
    if n > 1_000_000:
        return 'mega'
    if n > 100_000:
        return 'ultra_large'

    # Density-based for smaller graphs
    if density > 0.5:
        return 'ultra_dense'
    if density > 0.2:
        return 'dense'
    if density > 0.01:
        return 'medium'

    # Sparse
    if n > 10_000:
        return 'sparse_large'
    return 'sparse'


def compute_degree_distribution_stats(G: nx.Graph) -> Dict[str, float]:
    """
    Compute detailed degree distribution statistics.

    Args:
        G: NetworkX graph

    Returns:
        Dictionary with percentiles, skewness, kurtosis
    """
    degrees = list(dict(G.degree()).values())

    return {
        'degree_p25': np.percentile(degrees, 25),
        'degree_p50': np.median(degrees),
        'degree_p75': np.percentile(degrees, 75),
        'degree_p95': np.percentile(degrees, 95),
        'degree_skewness': float(np.mean((degrees - np.mean(degrees))**3) / (np.std(degrees)**3 + 1e-10)),
        'degree_gini': compute_gini_coefficient(degrees)
    }


def compute_gini_coefficient(values: list) -> float:
    """
    Compute Gini coefficient (inequality measure) for degree distribution.

    0 = perfect equality (all degrees same)
    1 = perfect inequality (one vertex has all edges)

    Args:
        values: List of degree values

    Returns:
        Gini coefficient in [0, 1]
    """
    if len(values) == 0:
        return 0.0

    sorted_values = np.sort(values)
    n = len(sorted_values)
    cumsum = np.cumsum(sorted_values)
    total = cumsum[-1]

    if total == 0:
        return 0.0

    # Gini formula
    return (2 * np.sum((np.arange(1, n + 1)) * sorted_values)) / (n * total) - (n + 1) / n


def identify_best_algorithm(graph_props: Dict[str, any]) -> Tuple[str, str]:
    """
    Recommend best algorithm based on graph properties.

    Args:
        graph_props: Graph characteristics from characterize_graph()

    Returns:
        Tuple of (recommended_algorithm, reason)

    Examples:
        >>> props = {'density': 0.9, 'vertices': 1000}
        >>> identify_best_algorithm(props)
        ('nearest_neighbor', 'Ultra-dense graph: NN fastest for p>0.5')
    """
    scenario = graph_props['scenario_category']
    n = graph_props['vertices']
    density = graph_props['density']

    # Ultra-dense: NN is best
    if scenario == 'ultra_dense':
        return ('nearest_neighbor', 'Ultra-dense graph: NN fastest for p>0.5')

    # Mega/ultra-large: Only NN practical
    if scenario in ['mega', 'ultra_large']:
        return ('nearest_neighbor', f'Large scale ({n} vertices): Only NN scales well')

    # Dense: Lazy Greedy good balance
    if scenario == 'dense':
        return ('lazy_greedy', 'Dense graph: Lazy Greedy offers best quality/speed tradeoff')

    # Medium density: Israeli-Itai best quality
    if scenario == 'medium':
        return ('israeli_itai', 'Medium density: Israeli-Itai achieves best quality')

    # Sparse: NN fastest, quality similar
    if scenario in ['sparse', 'sparse_large']:
        return ('nearest_neighbor', 'Sparse graph: All algorithms similar quality, NN fastest')

    # Default: Israeli-Itai for quality
    return ('israeli_itai', 'Default: Israeli-Itai typically best quality')


def generate_graph_summary(G: nx.Graph) -> str:
    """
    Generate human-readable summary of graph characteristics.

    Args:
        G: NetworkX graph

    Returns:
        Multi-line string summary

    Examples:
        >>> G = nx.karate_club_graph()
        >>> print(generate_graph_summary(G))
        Graph Summary:
          Vertices: 34
          Edges: 78
          Density: 0.1390
          ...
    """
    props = characterize_graph(G)
    best_algo, reason = identify_best_algorithm(props)

    summary = f"""Graph Summary:
  Vertices: {props['vertices']:,}
  Edges: {props['edges']:,}
  Density: {props['density']:.4f}
  Avg Degree: {props['avg_degree']:.2f}
  Clustering: {props['clustering_coeff']:.4f}
  Type: {props['graph_type']}
  Scenario: {props['scenario_category']}

  Recommended Algorithm: {best_algo}
  Reason: {reason}
"""

    return summary
