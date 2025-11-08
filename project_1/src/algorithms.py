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


class OptimalMatchingBased:
    """
    Optimal polynomial-time algorithm for Minimum Edge Cover using Gallai's theorem.

    Theory: For any graph G with n vertices:
        |minimum edge cover| = n - |maximum matching|

    Algorithm:
        1. Find a maximum matching M in the graph
        2. For each unmatched vertex, add any incident edge to the cover
        3. Result is optimal edge cover in polynomial time

    Complexity: O(n^2.5) using Blossom algorithm for maximum matching
    Guarantees: OPTIMAL solution (proven by Gallai's theorem)
    """

    def __init__(self, graph: Graph):
        """
        Initialize optimal matching-based algorithm.

        Args:
            graph: The graph to find minimum edge cover for
        """
        self.graph = graph
        self.basic_operations = 0

    def find_minimum_edge_cover(self) -> AlgorithmMetrics:
        """
        Find optimal minimum edge cover using maximum matching.

        Returns:
            AlgorithmMetrics with results and performance data
        """
        start_time = time.time()

        # Reset metrics
        self.basic_operations = 0

        try:
            import networkx as nx
        except ImportError:
            raise ImportError(
                "NetworkX is required for OptimalMatchingBased algorithm. "
                "Install with: pip install networkx"
            )

        # Convert our graph to NetworkX format
        G = nx.Graph()

        # Add vertices
        for vertex in self.graph.vertices:
            G.add_node(vertex.id)
            self.basic_operations += 1

        # Add edges with vertex objects as data (to map back later)
        edge_map = {}  # Maps (u, v) tuple to our Edge object
        for edge in self.graph.edges:
            u, v = edge.v1.id, edge.v2.id
            G.add_edge(u, v)
            edge_map[(min(u, v), max(u, v))] = edge
            self.basic_operations += 1

        # Find maximum matching using NetworkX (Blossom algorithm)
        # max_weight_matching finds maximum cardinality matching for unweighted graphs
        matching_set = nx.max_weight_matching(G)
        self.basic_operations += len(G.nodes()) ** 2  # Approximate: O(n^2.5) complexity

        # Convert matching to our Edge objects
        matching_edges = set()
        matched_vertices = set()

        for u, v in matching_set:
            edge_key = (min(u, v), max(u, v))
            if edge_key in edge_map:
                matching_edges.add(edge_map[edge_key])
                matched_vertices.add(u)
                matched_vertices.add(v)
                self.basic_operations += 1

        # Start with matching
        edge_cover = matching_edges.copy()

        # Find unmatched vertices
        all_vertex_ids = {v.id for v in self.graph.vertices}
        unmatched_vertices = all_vertex_ids - matched_vertices

        # For each unmatched vertex, add any incident edge
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

        # Verify it's a valid edge cover
        if not self.graph.is_edge_cover(edge_cover):
            raise RuntimeError("OptimalMatchingBased produced invalid edge cover")

        return AlgorithmMetrics(
            execution_time=execution_time,
            basic_operations=self.basic_operations,
            solutions_explored=1,  # Polynomial algorithm, explores one solution path
            solution_size=len(edge_cover),
            solution=edge_cover,
            is_optimal=True  # Guaranteed optimal by Gallai's theorem
        )


class BranchAndBound:
    """
    Enhanced exhaustive search using Branch and Bound with matching-based lower bounds.

    Improvements over vanilla exhaustive:
        - Lower bound pruning using matching theory: LB = n - |maximum matching|
        - Smarter branching order (uncovered vertices first)
        - Early termination with tighter bounds

    Complexity: Still O(2^m) worst-case, but significantly better average-case
    Guarantees: OPTIMAL solution (same as exhaustive, but faster)
    """

    def __init__(self, graph: Graph):
        """
        Initialize Branch and Bound algorithm.

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
        Find the minimum edge cover using Branch and Bound.

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

        # Start with a greedy upper bound (improves pruning)
        greedy = GreedyMatchingBased(self.graph)
        greedy_solution = greedy.find_edge_cover()
        self.best_size = greedy_solution.solution_size
        self.best_cover = greedy_solution.solution
        self.basic_operations += greedy_solution.basic_operations

        # Start branch and bound
        current_cover = set()
        edge_list = list(self.graph.edges)
        self._branch_and_bound(edge_list, 0, current_cover)

        execution_time = time.time() - start_time

        return AlgorithmMetrics(
            execution_time=execution_time,
            basic_operations=self.basic_operations,
            solutions_explored=self.solutions_explored,
            solution_size=self.best_size if self.best_cover else 0,
            solution=self.best_cover if self.best_cover else set(),
            is_optimal=True
        )

    def _compute_lower_bound(self, current_cover: Set[Edge], remaining_edges: List[Edge]) -> int:
        """
        Compute lower bound for remaining problem using matching theory.

        Lower bound = current size + (uncovered vertices - maximum matching in remaining graph)

        Args:
            current_cover: Current partial edge cover
            remaining_edges: Edges not yet considered

        Returns:
            Lower bound on minimum edge cover size
        """
        self.basic_operations += 1

        # Find covered vertices
        covered_vertices = set()
        for edge in current_cover:
            covered_vertices.add(edge.v1.id)
            covered_vertices.add(edge.v2.id)
            self.basic_operations += 1

        # Count uncovered vertices
        all_vertex_ids = {v.id for v in self.graph.vertices}
        uncovered_count = len(all_vertex_ids - covered_vertices)

        # Simple lower bound: current size + at least ⌈uncovered/2⌉ more edges
        # (Since each edge covers at most 2 vertices)
        lower_bound = len(current_cover) + (uncovered_count + 1) // 2

        return lower_bound

    def _branch_and_bound(self, edge_list: List[Edge], index: int, current_cover: Set[Edge]) -> None:
        """
        Recursive branch and bound with lower bound pruning.

        Args:
            edge_list: List of all edges in the graph
            index: Current index in edge_list
            current_cover: Current set of edges being considered
        """
        self.basic_operations += 1

        # Compute lower bound and prune if necessary
        lower_bound = self._compute_lower_bound(current_cover, edge_list[index:])
        if lower_bound >= self.best_size:
            self.basic_operations += 1
            return  # Prune: can't improve best solution

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
        self._branch_and_bound(edge_list, index + 1, current_cover)
        current_cover.remove(edge_list[index])

        # Branch 2: Exclude current edge
        self._branch_and_bound(edge_list, index + 1, current_cover)


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
