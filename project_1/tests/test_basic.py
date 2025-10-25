"""
Basic tests for Edge Cover implementation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graph import Graph, Vertex, Edge
from src.graph_generator import GraphGenerator
from src.algorithms import ExhaustiveSearch, GreedyHeuristic


def test_simple_graph():
    """Test with a simple manually constructed graph."""
    print("\n=== Test 1: Simple Graph ===")

    # Create a simple graph: 4 vertices in a square
    graph = Graph()

    v0 = Vertex(0, 10, 10)
    v1 = Vertex(1, 100, 10)
    v2 = Vertex(2, 100, 100)
    v3 = Vertex(3, 10, 100)

    graph.add_vertex(v0)
    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)

    # Add edges to form a square
    e01 = Edge(v0, v1)
    e12 = Edge(v1, v2)
    e23 = Edge(v2, v3)
    e30 = Edge(v3, v0)

    graph.add_edge(e01)
    graph.add_edge(e12)
    graph.add_edge(e23)
    graph.add_edge(e30)

    print(f"Graph: {graph}")
    print(f"Vertices: {[v.id for v in graph.vertices]}")
    print(f"Edges: {[(e.v1.id, e.v2.id) for e in graph.edges]}")

    # Test exhaustive search
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_metrics = exhaustive.find_minimum_edge_cover()

    print(f"\nExhaustive Search:")
    print(f"  Solution size: {exhaustive_metrics.solution_size}")
    print(f"  Solution: {[(e.v1.id, e.v2.id) for e in exhaustive_metrics.solution]}")
    print(f"  Solutions explored: {exhaustive_metrics.solutions_explored}")
    print(f"  Basic operations: {exhaustive_metrics.basic_operations}")
    print(f"  Time: {exhaustive_metrics.execution_time:.6f}s")

    # Verify solution is valid
    assert graph.is_edge_cover(exhaustive_metrics.solution), "Solution is not a valid edge cover!"
    print("  ✓ Solution is valid edge cover")

    # For a square, minimum edge cover should be 2 (opposite edges)
    assert exhaustive_metrics.solution_size == 2, f"Expected size 2, got {exhaustive_metrics.solution_size}"
    print("  ✓ Solution is optimal (size 2)")

    # Test greedy heuristic
    greedy = GreedyHeuristic(graph)
    greedy_metrics = greedy.find_edge_cover()

    print(f"\nGreedy Heuristic:")
    print(f"  Solution size: {greedy_metrics.solution_size}")
    print(f"  Solution: {[(e.v1.id, e.v2.id) for e in greedy_metrics.solution]}")
    print(f"  Basic operations: {greedy_metrics.basic_operations}")
    print(f"  Time: {greedy_metrics.execution_time:.6f}s")

    # Verify solution is valid
    assert graph.is_edge_cover(greedy_metrics.solution), "Greedy solution is not a valid edge cover!"
    print("  ✓ Solution is valid edge cover")

    print("\n✓ Test 1 PASSED\n")


def test_generated_graph():
    """Test with a randomly generated graph."""
    print("\n=== Test 2: Generated Graph ===")

    generator = GraphGenerator(seed=113920)

    # Generate a small graph
    graph = generator.generate_graph(num_vertices=5, edge_density=50.0)

    print(f"Graph: {graph}")
    print(f"Vertices: {len(graph.vertices)}")
    print(f"Edges: {len(graph.edges)}")
    print(f"Edge density: {graph.edge_density():.1f}%")

    # Check no isolated vertices
    assert not graph.has_isolated_vertices(), "Graph has isolated vertices!"
    print("✓ No isolated vertices")

    # Test exhaustive search
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_metrics = exhaustive.find_minimum_edge_cover()

    print(f"\nExhaustive Search:")
    print(f"  Solution size: {exhaustive_metrics.solution_size}")
    print(f"  Solutions explored: {exhaustive_metrics.solutions_explored}")
    print(f"  Time: {exhaustive_metrics.execution_time:.6f}s")

    # Verify solution
    assert graph.is_edge_cover(exhaustive_metrics.solution), "Solution is not a valid edge cover!"
    print("  ✓ Solution is valid edge cover")

    # Test greedy
    greedy = GreedyHeuristic(graph)
    greedy_metrics = greedy.find_edge_cover()

    print(f"\nGreedy Heuristic:")
    print(f"  Solution size: {greedy_metrics.solution_size}")
    print(f"  Time: {greedy_metrics.execution_time:.6f}s")

    assert graph.is_edge_cover(greedy_metrics.solution), "Greedy solution is not a valid edge cover!"
    print("  ✓ Solution is valid edge cover")

    # Greedy should be close to optimal
    ratio = exhaustive_metrics.solution_size / greedy_metrics.solution_size
    print(f"\nQuality ratio: {ratio:.3f}")
    print(f"Speedup: {exhaustive_metrics.execution_time / greedy_metrics.execution_time:.1f}x")

    print("\n✓ Test 2 PASSED\n")


def test_complete_graph():
    """Test with a complete graph."""
    print("\n=== Test 3: Complete Graph (K4) ===")

    graph = Graph()

    # Create 4 vertices
    vertices = [Vertex(i, i*100, i*100) for i in range(4)]
    for v in vertices:
        graph.add_vertex(v)

    # Add all possible edges (complete graph)
    for i in range(4):
        for j in range(i+1, 4):
            graph.add_edge(Edge(vertices[i], vertices[j]))

    print(f"Graph: {graph}")
    print(f"Is complete: {graph.num_edges() == graph.max_possible_edges()}")

    # For complete graph K4, minimum edge cover should be 2
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_metrics = exhaustive.find_minimum_edge_cover()

    print(f"\nExhaustive Search:")
    print(f"  Solution size: {exhaustive_metrics.solution_size}")
    print(f"  Expected: 2 (for K4)")

    assert exhaustive_metrics.solution_size == 2, f"Expected size 2, got {exhaustive_metrics.solution_size}"
    assert graph.is_edge_cover(exhaustive_metrics.solution), "Solution is not valid!"
    print("  ✓ Optimal solution found")

    print("\n✓ Test 3 PASSED\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("RUNNING TESTS")
    print("=" * 70)

    try:
        test_simple_graph()
        test_generated_graph()
        test_complete_graph()

        print("=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
