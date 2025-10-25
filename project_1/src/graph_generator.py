"""
Random graph generator for Minimum Edge Cover experiments.
Uses student number 113920 as random seed for reproducibility.
"""

import random
from typing import List, Set, Tuple
from src.graph import Graph, Vertex, Edge


class GraphGenerator:
    """Generates random graphs with specified properties."""

    # Student number as seed for reproducibility
    SEED = 113920

    # Coordinate range for 2D vertices
    MIN_COORD = 1
    MAX_COORD = 500

    # Minimum distance between vertices to avoid clustering
    MIN_DISTANCE = 10.0

    def __init__(self, seed: int = SEED):
        """
        Initialize the graph generator with a random seed.

        Args:
            seed: Random seed for reproducibility (default: 113920)
        """
        self.seed = seed
        random.seed(seed)

    def generate_vertices(self, num_vertices: int) -> List[Vertex]:
        """
        Generate vertices with random 2D coordinates [1, 500].
        Ensures vertices are not too close to each other.

        Args:
            num_vertices: Number of vertices to generate

        Returns:
            List of Vertex objects
        """
        vertices = []
        attempts = 0
        max_attempts = num_vertices * 1000  # Prevent infinite loops

        while len(vertices) < num_vertices and attempts < max_attempts:
            x = random.randint(self.MIN_COORD, self.MAX_COORD)
            y = random.randint(self.MIN_COORD, self.MAX_COORD)
            new_vertex = Vertex(len(vertices), x, y)

            # Check if new vertex is far enough from existing vertices
            too_close = False
            for existing_vertex in vertices:
                if new_vertex.distance_to(existing_vertex) < self.MIN_DISTANCE:
                    too_close = True
                    break

            if not too_close:
                vertices.append(new_vertex)

            attempts += 1

        if len(vertices) < num_vertices:
            # If we couldn't generate enough spaced vertices, relax the constraint
            while len(vertices) < num_vertices:
                x = random.randint(self.MIN_COORD, self.MAX_COORD)
                y = random.randint(self.MIN_COORD, self.MAX_COORD)
                vertices.append(Vertex(len(vertices), x, y))

        return vertices

    def generate_edges(self, vertices: List[Vertex], target_edge_count: int) -> List[Edge]:
        """
        Generate random edges between vertices.

        Args:
            vertices: List of vertices to connect
            target_edge_count: Number of edges to generate

        Returns:
            List of Edge objects
        """
        n = len(vertices)
        max_edges = n * (n - 1) // 2

        if target_edge_count > max_edges:
            target_edge_count = max_edges

        # Generate all possible edges
        all_possible_edges = []
        for i in range(n):
            for j in range(i + 1, n):
                all_possible_edges.append(Edge(vertices[i], vertices[j]))

        # Randomly select edges
        selected_edges = random.sample(all_possible_edges, target_edge_count)

        return selected_edges

    def ensure_no_isolated_vertices(self, vertices: List[Vertex], edges: List[Edge]) -> List[Edge]:
        """
        Ensure all vertices have at least degree 1 (no isolated vertices).
        Edge cover requires all vertices to be incident to at least one edge.

        Args:
            vertices: List of vertices
            edges: Current list of edges

        Returns:
            Updated list of edges with no isolated vertices
        """
        # Find covered vertices
        covered_vertex_ids = set()
        for edge in edges:
            covered_vertex_ids.add(edge.v1.id)
            covered_vertex_ids.add(edge.v2.id)

        # Find isolated vertices
        isolated_vertices = [v for v in vertices if v.id not in covered_vertex_ids]

        # Connect isolated vertices
        edges = list(edges)  # Make a copy
        for isolated in isolated_vertices:
            # Connect to a random other vertex (prefer already connected ones)
            if covered_vertex_ids:
                # Pick a random covered vertex
                target_id = random.choice(list(covered_vertex_ids))
                target_vertex = next(v for v in vertices if v.id == target_id)
            else:
                # Pick any other vertex
                target_vertex = random.choice([v for v in vertices if v.id != isolated.id])

            new_edge = Edge(isolated, target_vertex)
            edges.append(new_edge)
            covered_vertex_ids.add(isolated.id)
            covered_vertex_ids.add(target_vertex.id)

        return edges

    def generate_graph(self, num_vertices: int, edge_density: float) -> Graph:
        """
        Generate a random graph with specified number of vertices and edge density.

        Args:
            num_vertices: Number of vertices in the graph
            edge_density: Edge density as percentage of maximum possible edges
                         (e.g., 12.5, 25.0, 50.0, 75.0)

        Returns:
            Generated Graph object
        """
        if num_vertices < 2:
            raise ValueError("Graph must have at least 2 vertices")

        if not (0 <= edge_density <= 100):
            raise ValueError("Edge density must be between 0 and 100")

        # Generate vertices
        vertices = self.generate_vertices(num_vertices)

        # Calculate target number of edges
        max_edges = num_vertices * (num_vertices - 1) // 2
        target_edge_count = int(max_edges * edge_density / 100)

        # Ensure at least one edge per vertex (minimum for edge cover)
        min_edges = (num_vertices + 1) // 2  # Minimum edges for edge cover
        target_edge_count = max(target_edge_count, min_edges)

        # Generate edges
        edges = self.generate_edges(vertices, target_edge_count)

        # Ensure no isolated vertices
        edges = self.ensure_no_isolated_vertices(vertices, edges)

        # Build graph
        graph = Graph()
        for vertex in vertices:
            graph.add_vertex(vertex)
        for edge in edges:
            graph.add_edge(edge)

        return graph

    def generate_graphs_batch(
        self,
        num_vertices_range: List[int],
        edge_densities: List[float]
    ) -> List[Tuple[int, float, Graph]]:
        """
        Generate a batch of graphs for experimentation.

        Args:
            num_vertices_range: List of vertex counts to test
            edge_densities: List of edge densities to test

        Returns:
            List of tuples (num_vertices, edge_density, graph)
        """
        graphs = []

        for num_vertices in num_vertices_range:
            for density in edge_densities:
                graph = self.generate_graph(num_vertices, density)
                graphs.append((num_vertices, density, graph))

        return graphs

    def reset_seed(self, seed: int = None):
        """Reset the random seed."""
        if seed is None:
            seed = self.seed
        random.seed(seed)


# Default edge densities as specified in requirements
DEFAULT_EDGE_DENSITIES = [12.5, 25.0, 50.0, 75.0]
