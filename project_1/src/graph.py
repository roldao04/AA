"""
Graph data structures for Minimum Edge Cover problem.
Includes Vertex (2D points), Edge, and Graph classes.
"""

from typing import List, Set, Tuple, Optional
import math


class Vertex:
    """Represents a 2D point vertex with integer coordinates [1, 500]."""

    def __init__(self, vertex_id: int, x: int, y: int):
        """
        Initialize a vertex with ID and 2D coordinates.

        Args:
            vertex_id: Unique identifier for the vertex
            x: X-coordinate (should be in range [1, 500])
            y: Y-coordinate (should be in range [1, 500])
        """
        self.id = vertex_id
        self.x = x
        self.y = y

    def distance_to(self, other: 'Vertex') -> float:
        """Calculate Euclidean distance to another vertex."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"V{self.id}({self.x},{self.y})"

    def __str__(self):
        return f"Vertex {self.id} at ({self.x}, {self.y})"


class Edge:
    """Represents an undirected edge between two vertices."""

    def __init__(self, v1: Vertex, v2: Vertex):
        """
        Initialize an edge between two vertices.

        Args:
            v1: First vertex
            v2: Second vertex
        """
        # Store vertices in consistent order for equality comparison
        if v1.id < v2.id:
            self.v1 = v1
            self.v2 = v2
        else:
            self.v1 = v2
            self.v2 = v1

    def contains_vertex(self, vertex: Vertex) -> bool:
        """Check if this edge contains the given vertex."""
        return vertex.id == self.v1.id or vertex.id == self.v2.id

    def get_other_vertex(self, vertex: Vertex) -> Optional[Vertex]:
        """Get the other vertex of this edge."""
        if vertex.id == self.v1.id:
            return self.v2
        elif vertex.id == self.v2.id:
            return self.v1
        return None

    def length(self) -> float:
        """Calculate the Euclidean length of this edge."""
        return self.v1.distance_to(self.v2)

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.v1.id == other.v1.id and self.v2.id == other.v2.id

    def __hash__(self):
        return hash((self.v1.id, self.v2.id))

    def __repr__(self):
        return f"E({self.v1.id},{self.v2.id})"

    def __str__(self):
        return f"Edge ({self.v1.id} - {self.v2.id})"


class Graph:
    """Undirected graph represented using adjacency lists."""

    def __init__(self):
        """Initialize an empty graph."""
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
        self.adjacency: dict[int, Set[int]] = {}  # vertex_id -> set of adjacent vertex_ids
        self._vertex_map: dict[int, Vertex] = {}  # vertex_id -> Vertex object

    def add_vertex(self, vertex: Vertex) -> None:
        """Add a vertex to the graph."""
        if vertex.id not in self._vertex_map:
            self.vertices.append(vertex)
            self._vertex_map[vertex.id] = vertex
            self.adjacency[vertex.id] = set()

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        # Ensure vertices exist
        self.add_vertex(edge.v1)
        self.add_vertex(edge.v2)

        # Add edge if not already present
        if edge not in self.edges:
            self.edges.append(edge)
            self.adjacency[edge.v1.id].add(edge.v2.id)
            self.adjacency[edge.v2.id].add(edge.v1.id)

    def get_vertex(self, vertex_id: int) -> Optional[Vertex]:
        """Get vertex by ID."""
        return self._vertex_map.get(vertex_id)

    def get_neighbors(self, vertex_id: int) -> Set[int]:
        """Get the set of vertex IDs adjacent to the given vertex."""
        return self.adjacency.get(vertex_id, set())

    def degree(self, vertex_id: int) -> int:
        """Get the degree of a vertex."""
        return len(self.adjacency.get(vertex_id, set()))

    def num_vertices(self) -> int:
        """Get the number of vertices in the graph."""
        return len(self.vertices)

    def num_edges(self) -> int:
        """Get the number of edges in the graph."""
        return len(self.edges)

    def has_isolated_vertices(self) -> bool:
        """Check if the graph has any isolated vertices (degree 0)."""
        return any(self.degree(v.id) == 0 for v in self.vertices)

    def max_possible_edges(self) -> int:
        """Calculate maximum possible edges for a complete graph with n vertices."""
        n = self.num_vertices()
        return n * (n - 1) // 2

    def edge_density(self) -> float:
        """Calculate the edge density as a percentage of maximum possible edges."""
        max_edges = self.max_possible_edges()
        if max_edges == 0:
            return 0.0
        return (self.num_edges() / max_edges) * 100

    def is_edge_cover(self, edge_subset: Set[Edge]) -> bool:
        """
        Check if a given subset of edges forms a valid edge cover.
        An edge cover must have every vertex incident to at least one edge.

        Args:
            edge_subset: Set of edges to check

        Returns:
            True if edge_subset covers all vertices, False otherwise
        """
        covered_vertices = set()

        for edge in edge_subset:
            covered_vertices.add(edge.v1.id)
            covered_vertices.add(edge.v2.id)

        all_vertex_ids = {v.id for v in self.vertices}
        return covered_vertices == all_vertex_ids

    def get_uncovered_vertices(self, edge_subset: Set[Edge]) -> Set[int]:
        """
        Get the set of vertex IDs not covered by the given edge subset.

        Args:
            edge_subset: Set of edges

        Returns:
            Set of uncovered vertex IDs
        """
        covered_vertices = set()

        for edge in edge_subset:
            covered_vertices.add(edge.v1.id)
            covered_vertices.add(edge.v2.id)

        all_vertex_ids = {v.id for v in self.vertices}
        return all_vertex_ids - covered_vertices

    def __repr__(self):
        return f"Graph(V={self.num_vertices()}, E={self.num_edges()})"

    def __str__(self):
        return f"Graph with {self.num_vertices()} vertices and {self.num_edges()} edges (density: {self.edge_density():.1f}%)"
