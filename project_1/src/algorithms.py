"""
Algorithms for finding Minimum Edge Cover.
Includes exhaustive search and greedy heuristic implementations.
"""

import time
from typing import Set, Optional, List, Tuple
from dataclasses import dataclass
from src.graph import Graph, Edge


@dataclass
class AlgorithmMetrics:
    """Metrics collected during algorithm execution."""
    execution_time: float  # Seconds
    basic_operations: int  # Number of basic operations (comparisons, etc.)
    solutions_explored: int  # Number of candidate solutions examined
    solution_size: int  # Size of the found edge cover
    solution: Set[Edge]  # The actual edge cover found
    is_optimal: Optional[bool] = None  # True if guaranteed optimal, False otherwise


class ExhaustiveSearch:
    """Exhaustive search algorithm for Minimum Edge Cover using backtracking."""

    def __init__(self, graph: Graph):
        """
        Initialize exhaustive search for a graph.

        Args:
            graph: The graph to find minimum edge cover for
        """
        self.graph = graph
        self.best_cover: Optional[Set[Edge]] = None
        self.best_size: int = float('inf')
        self.basic_operations = 0
        self.solutions_explored = 0

    def find_minimum_edge_cover(self) -> AlgorithmMetrics:
        """
        Find the minimum edge cover using exhaustive search with backtracking.

        Returns:
            AlgorithmMetrics with results and performance data
        """
        start_time = time.time()

        # Reset metrics
        self.best_cover = None
        self.best_size = float('inf')
        self.basic_operations = 0
        self.solutions_explored = 0

        # Handle edge case: empty graph
        if self.graph.num_vertices() == 0:
            execution_time = time.time() - start_time
            return AlgorithmMetrics(
                execution_time=execution_time,
                basic_operations=0,
                solutions_explored=0,
                solution_size=0,
                solution=set(),
                is_optimal=True
            )

        # Start backtracking
        current_cover = set()
        edge_list = list(self.graph.edges)
        self._backtrack(edge_list, 0, current_cover)

        execution_time = time.time() - start_time

        return AlgorithmMetrics(
            execution_time=execution_time,
            basic_operations=self.basic_operations,
            solutions_explored=self.solutions_explored,
            solution_size=self.best_size if self.best_cover else 0,
            solution=self.best_cover if self.best_cover else set(),
            is_optimal=True
        )

    def _backtrack(self, edge_list: List[Edge], index: int, current_cover: Set[Edge]) -> None:
        """
        Recursive backtracking to explore all possible edge subsets.

        Args:
            edge_list: List of all edges in the graph
            index: Current index in edge_list
            current_cover: Current set of edges being considered
        """
        self.basic_operations += 1

        # Pruning: if current cover size already exceeds best, abandon this branch
        if len(current_cover) >= self.best_size:
            self.basic_operations += 1
            return

        # Base case: processed all edges
        if index == len(edge_list):
            self.solutions_explored += 1
            self.basic_operations += 1

            # Check if this is a valid edge cover
            if self.graph.is_edge_cover(current_cover):
                self.basic_operations += 1
                if len(current_cover) < self.best_size:
                    self.best_size = len(current_cover)
                    self.best_cover = current_cover.copy()
                    self.basic_operations += 1
            return

        # Branch 1: Include current edge
        current_cover.add(edge_list[index])
        self._backtrack(edge_list, index + 1, current_cover)
        current_cover.remove(edge_list[index])

        # Branch 2: Exclude current edge
        self._backtrack(edge_list, index + 1, current_cover)


class GreedyHeuristic:
    """Greedy heuristic algorithm for Edge Cover."""

    def __init__(self, graph: Graph):
        """
        Initialize greedy heuristic for a graph.

        Args:
            graph: The graph to find edge cover for
        """
        self.graph = graph
        self.basic_operations = 0

    def find_edge_cover(self) -> AlgorithmMetrics:
        """
        Find an edge cover using a greedy heuristic.
        Strategy: Repeatedly select edges that cover the most uncovered vertices.

        Returns:
            AlgorithmMetrics with results and performance data
        """
        start_time = time.time()

        # Reset metrics
        self.basic_operations = 0
        solutions_explored = 1  # Greedy explores only one solution path

        edge_cover = set()
        uncovered_vertices = {v.id for v in self.graph.vertices}

        # Greedy selection: pick edges covering most uncovered vertices
        while uncovered_vertices:
            self.basic_operations += 1

            best_edge = None
            best_coverage = 0

            # Find edge that covers the most uncovered vertices
            for edge in self.graph.edges:
                self.basic_operations += 1

                coverage = 0
                if edge.v1.id in uncovered_vertices:
                    coverage += 1
                    self.basic_operations += 1
                if edge.v2.id in uncovered_vertices:
                    coverage += 1
                    self.basic_operations += 1

                if coverage > best_coverage:
                    best_coverage = coverage
                    best_edge = edge
                    self.basic_operations += 1

            # If no edge covers any uncovered vertex, pick any edge with an uncovered vertex
            if best_edge is None:
                break

            # Add best edge to cover
            edge_cover.add(best_edge)
            uncovered_vertices.discard(best_edge.v1.id)
            uncovered_vertices.discard(best_edge.v2.id)
            self.basic_operations += 2

        execution_time = time.time() - start_time

        return AlgorithmMetrics(
            execution_time=execution_time,
            basic_operations=self.basic_operations,
            solutions_explored=solutions_explored,
            solution_size=len(edge_cover),
            solution=edge_cover,
            is_optimal=False  # Greedy doesn't guarantee optimal solution
        )


class GreedyMatchingBased:
    """
    Alternative greedy heuristic based on maximum matching.
    Theory: minimum edge cover size = n - |maximum matching|
    This approach finds a maximal matching and adds edges for uncovered vertices.
    """

    def __init__(self, graph: Graph):
        """
        Initialize matching-based greedy heuristic.

        Args:
            graph: The graph to find edge cover for
        """
        self.graph = graph
        self.basic_operations = 0

    def find_edge_cover(self) -> AlgorithmMetrics:
        """
        Find an edge cover using a matching-based greedy approach.

        Returns:
            AlgorithmMetrics with results and performance data
        """
        start_time = time.time()

        # Reset metrics
        self.basic_operations = 0

        # Find a maximal matching (greedy)
        matching = set()
        matched_vertices = set()

        for edge in self.graph.edges:
            self.basic_operations += 1

            # If neither vertex is matched, add edge to matching
            if edge.v1.id not in matched_vertices and edge.v2.id not in matched_vertices:
                matching.add(edge)
                matched_vertices.add(edge.v1.id)
                matched_vertices.add(edge.v2.id)
                self.basic_operations += 2

        # Edge cover starts with the matching
        edge_cover = matching.copy()

        # Find unmatched vertices
        all_vertex_ids = {v.id for v in self.graph.vertices}
        unmatched_vertices = all_vertex_ids - matched_vertices

        # For each unmatched vertex, add an arbitrary incident edge
        for vertex_id in unmatched_vertices:
            self.basic_operations += 1

            # Find any edge incident to this vertex
            for edge in self.graph.edges:
                self.basic_operations += 1

                if edge.contains_vertex(self.graph.get_vertex(vertex_id)):
                    edge_cover.add(edge)
                    self.basic_operations += 1
                    break

        execution_time = time.time() - start_time

        return AlgorithmMetrics(
            execution_time=execution_time,
            basic_operations=self.basic_operations,
            solutions_explored=1,
            solution_size=len(edge_cover),
            solution=edge_cover,
            is_optimal=False
        )


def compare_solutions(optimal_metrics: AlgorithmMetrics,
                      heuristic_metrics: AlgorithmMetrics) -> dict:
    """
    Compare optimal and heuristic solutions.

    Args:
        optimal_metrics: Metrics from exhaustive search
        heuristic_metrics: Metrics from greedy heuristic

    Returns:
        Dictionary with comparison statistics
    """
    if optimal_metrics.solution_size == 0:
        quality = 1.0
    else:
        quality = optimal_metrics.solution_size / heuristic_metrics.solution_size

    return {
        'optimal_size': optimal_metrics.solution_size,
        'heuristic_size': heuristic_metrics.solution_size,
        'quality': quality,  # 1.0 = optimal, < 1.0 = suboptimal
        'is_optimal': heuristic_metrics.solution_size == optimal_metrics.solution_size,
        'size_difference': heuristic_metrics.solution_size - optimal_metrics.solution_size,
        'speedup': optimal_metrics.execution_time / heuristic_metrics.execution_time if heuristic_metrics.execution_time > 0 else float('inf'),
        'operation_reduction': 1.0 - (heuristic_metrics.basic_operations / optimal_metrics.basic_operations) if optimal_metrics.basic_operations > 0 else 0
    }
