"""
Edge Cover Algorithm Implementations

This module contains implementations of:
- Exact algorithm (matching-based)
- Israeli-Itai randomized matching
- Simulated annealing
- Lazy greedy (3/2-approximation)
- Nearest neighbor (2-approximation)
"""

from .exact import exact_edge_cover
from .israeli_itai import israeli_itai_edge_cover
from .simulated_annealing import simulated_annealing_edge_cover
from .lazy_greedy import lazy_greedy_edge_cover
from .nearest_neighbor import nearest_neighbor_edge_cover

__all__ = [
    'exact_edge_cover',
    'israeli_itai_edge_cover',
    'simulated_annealing_edge_cover',
    'lazy_greedy_edge_cover',
    'nearest_neighbor_edge_cover'
]
