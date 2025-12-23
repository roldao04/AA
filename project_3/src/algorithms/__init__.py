"""
Counting Algorithms for AA Project 3.

This package contains implementations of exact and approximate counting algorithms:
- ExactCounter: Baseline exact counting using dictionaries
- FixedProbabilityCounter: Probabilistic counting with fixed p
- SpaceSaving: Frequent items algorithm

Author: Joao Roldao (113920)
"""

from .exact_counter import ExactCounter

__all__ = ['ExactCounter']
