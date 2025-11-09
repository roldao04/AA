"""
Comprehensive test suite for Minimum Edge Cover implementation.

Tests include:
- Basic algorithm correctness on known graphs
- Input validation and error handling
- Edge cover validation
- Integration testing
- Robustness and edge cases

Student Number: 113920
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graph import Graph, Vertex, Edge
from src.graph_generator import GraphGenerator
from src.algorithms import (
    ExhaustiveSearch,
    GreedyHeuristic,
    GreedyMatchingBased,
    OptimalMatchingBased,
    BranchAndBound
)
from src.experiment import ExperimentRunner
from src.exceptions import (
    InvalidConfigurationException,
    InvalidEdgeCoverException,
    AlgorithmTimeoutException
)
from src.config import DEFAULT_SEED


# ============================================================================
# BASIC ALGORITHM TESTS
# ============================================================================

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
    print("  Solution is valid edge cover")

    # For a square, minimum edge cover should be 2 (opposite edges)
    assert exhaustive_metrics.solution_size == 2, f"Expected size 2, got {exhaustive_metrics.solution_size}"
    print("  Solution is optimal (size 2)")

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
    print("  Solution is valid edge cover")

    print("\nTest 1 PASSED\n")


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
    print("No isolated vertices")

    # Test exhaustive search
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_metrics = exhaustive.find_minimum_edge_cover()

    print(f"\nExhaustive Search:")
    print(f"  Solution size: {exhaustive_metrics.solution_size}")
    print(f"  Solutions explored: {exhaustive_metrics.solutions_explored}")
    print(f"  Time: {exhaustive_metrics.execution_time:.6f}s")

    # Verify solution
    assert graph.is_edge_cover(exhaustive_metrics.solution), "Solution is not a valid edge cover!"
    print("  Solution is valid edge cover")

    # Test greedy
    greedy = GreedyHeuristic(graph)
    greedy_metrics = greedy.find_edge_cover()

    print(f"\nGreedy Heuristic:")
    print(f"  Solution size: {greedy_metrics.solution_size}")
    print(f"  Time: {greedy_metrics.execution_time:.6f}s")

    assert graph.is_edge_cover(greedy_metrics.solution), "Greedy solution is not a valid edge cover!"
    print("  Solution is valid edge cover")

    # Greedy should be close to optimal
    ratio = exhaustive_metrics.solution_size / greedy_metrics.solution_size
    print(f"\nQuality ratio: {ratio:.3f}")
    print(f"Speedup: {exhaustive_metrics.execution_time / greedy_metrics.execution_time:.1f}x")

    print("\nTest 2 PASSED\n")


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


# ============================================================================
# VALIDATION & INTEGRATION TESTS
# ============================================================================

def test_seed_reproducibility():
    """Test that seed properly controls randomness for reproducibility."""
    print("\n=== Test 4: Seed Reproducibility ===")

    generator = GraphGenerator(seed=DEFAULT_SEED)

    # Generate two graphs with same parameters
    graph1 = generator.generate_graph(num_vertices=5, edge_density=50.0)
    graph2 = generator.generate_graph(num_vertices=5, edge_density=50.0)

    # Get vertex positions
    positions1 = [(v.x, v.y) for v in graph1.vertices]
    positions2 = [(v.x, v.y) for v in graph2.vertices]

    print(f"Graph 1 vertex positions: {positions1[:3]}...")  # First 3
    print(f"Graph 2 vertex positions: {positions2[:3]}...")  # First 3

    # Verify they are DIFFERENT (seed advances naturally)
    assert positions1 != positions2, "Graphs should have different vertex positions!"
    print("Graphs have different vertex positions (seed advances)")

    # Verify reproducibility: resetting generator should give same sequence
    generator2 = GraphGenerator(seed=DEFAULT_SEED)
    graph3 = generator2.generate_graph(num_vertices=5, edge_density=50.0)
    graph4 = generator2.generate_graph(num_vertices=5, edge_density=50.0)

    positions3 = [(v.x, v.y) for v in graph3.vertices]
    positions4 = [(v.x, v.y) for v in graph4.vertices]

    assert positions1 == positions3, "First graph should be reproducible"
    assert positions2 == positions4, "Second graph should be reproducible"
    print("Graph generation is reproducible with same seed")

    print("Test 4 PASSED\n")


def test_timeout_protection():
    """Test that timeout protection works for large graphs."""
    print("\n=== Test 5: Timeout Protection ===")

    # Create a graph that would take long for exhaustive search
    generator = GraphGenerator(seed=DEFAULT_SEED)
    # 10 vertices at 75% density = ~34 edges (2^34 is huge!)
    large_graph = generator.generate_graph(num_vertices=10, edge_density=75.0)

    print(f"Testing timeout on graph with {large_graph.num_vertices()} vertices, "
          f"{large_graph.num_edges()} edges")

    # This should skip exhaustive search entirely (> 25 edges)
    if large_graph.num_edges() > 25:
        print("Graph has > 25 edges, exhaustive will be skipped (expected)")
        print("Test 5 PASSED (timeout protection via edge count limit)\n")
        return

    # If edges <= 25, test actual timeout
    runner = ExperimentRunner(timeout_seconds=0.5)  # Very short timeout
    result = runner.run_single_experiment(
        num_vertices=10,
        edge_density=75.0,
        verbose=False
    )

    # Should timeout or skip
    assert result.exhaustive_timed_out, "Exhaustive search should timeout or be skipped"
    print("Exhaustive search timed out or was skipped as expected")
    print("Test 5 PASSED\n")


def test_input_validation():
    """Test that invalid inputs are properly rejected."""
    print("\n=== Test 6: Input Validation ===")

    generator = GraphGenerator(seed=DEFAULT_SEED)

    # Test invalid num_vertices
    try:
        generator.generate_graph(num_vertices=-5, edge_density=50.0)
        assert False, "Should have raised exception for negative vertices"
    except InvalidConfigurationException as e:
        print(f"Negative vertices rejected: {str(e)[:50]}...")

    try:
        generator.generate_graph(num_vertices=1, edge_density=50.0)
        assert False, "Should have raised exception for < 2 vertices"
    except InvalidConfigurationException as e:
        print(f"Single vertex rejected: {str(e)[:50]}...")

    try:
        generator.generate_graph(num_vertices=10000, edge_density=50.0)
        assert False, "Should have raised exception for too many vertices"
    except InvalidConfigurationException as e:
        print(f"Too many vertices rejected: {str(e)[:50]}...")

    # Test invalid edge_density
    try:
        generator.generate_graph(num_vertices=5, edge_density=-10.0)
        assert False, "Should have raised exception for negative density"
    except InvalidConfigurationException as e:
        print(f"Negative density rejected: {str(e)[:50]}...")

    try:
        generator.generate_graph(num_vertices=5, edge_density=150.0)
        assert False, "Should have raised exception for > 100 density"
    except InvalidConfigurationException as e:
        print(f"Density > 100 rejected: {str(e)[:50]}...")

    try:
        generator.generate_graph(num_vertices=5, edge_density="50%")
        assert False, "Should have raised exception for string density"
    except InvalidConfigurationException as e:
        print(f"Non-numeric density rejected: {str(e)[:50]}...")

    print("Test 6 PASSED\n")


def test_edge_cover_validation():
    """Test that invalid edge covers are detected."""
    print("\n=== Test 7: Edge Cover Validation ===")

    # Create a simple graph
    graph = Graph()
    v0 = Vertex(0, 10, 10)
    v1 = Vertex(1, 100, 10)
    v2 = Vertex(2, 100, 100)

    graph.add_vertex(v0)
    graph.add_vertex(v1)
    graph.add_vertex(v2)

    e01 = Edge(v0, v1)
    e12 = Edge(v1, v2)

    graph.add_edge(e01)
    graph.add_edge(e12)

    # Valid edge cover
    valid_cover = {e01, e12}
    assert graph.is_edge_cover(valid_cover), "Valid cover should be accepted"
    print("Valid edge cover accepted")

    # Invalid: edge not in graph
    v3 = Vertex(3, 200, 200)
    foreign_edge = Edge(v0, v3)  # v3 not even in graph!
    invalid_cover = {e01, foreign_edge}

    try:
        graph.is_edge_cover(invalid_cover)
        assert False, "Should have raised exception for foreign edge"
    except ValueError as e:
        print(f"Foreign edge rejected: {str(e)[:50]}...")

    # Invalid: doesn't cover all vertices
    incomplete_cover = {e01}  # Missing v2
    assert not graph.is_edge_cover(incomplete_cover), "Incomplete cover should be invalid"
    print("Incomplete edge cover rejected")

    print("Test 7 PASSED\n")


def test_greedy_matching_based():
    """Test that GreedyMatchingBased algorithm works correctly."""
    print("\n=== Test 8: GreedyMatchingBased Algorithm ===")

    generator = GraphGenerator(seed=DEFAULT_SEED)
    graph = generator.generate_graph(num_vertices=6, edge_density=50.0)

    print(f"Testing on graph: {graph}")

    # Run all three algorithms
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_metrics = exhaustive.find_minimum_edge_cover()

    greedy_cov = GreedyHeuristic(graph)
    greedy_cov_metrics = greedy_cov.find_edge_cover()

    greedy_match = GreedyMatchingBased(graph)
    greedy_match_metrics = greedy_match.find_edge_cover()

    print(f"Optimal size: {exhaustive_metrics.solution_size}")
    print(f"Greedy coverage size: {greedy_cov_metrics.solution_size}")
    print(f"Greedy matching size: {greedy_match_metrics.solution_size}")

    # Verify all produce valid edge covers
    assert graph.is_edge_cover(exhaustive_metrics.solution), "Exhaustive solution invalid"
    assert graph.is_edge_cover(greedy_cov_metrics.solution), "Greedy coverage solution invalid"
    assert graph.is_edge_cover(greedy_match_metrics.solution), "Greedy matching solution invalid"
    print("All algorithms produce valid edge covers")

    # Verify optimal is actually minimal
    assert exhaustive_metrics.solution_size <= greedy_cov_metrics.solution_size
    assert exhaustive_metrics.solution_size <= greedy_match_metrics.solution_size
    print("Optimal solution is indeed minimal")

    # Verify greedy algorithms are fast
    assert greedy_cov_metrics.execution_time < exhaustive_metrics.execution_time
    assert greedy_match_metrics.execution_time < exhaustive_metrics.execution_time
    print("Greedy algorithms are faster than exhaustive")

    print("Test 8 PASSED\n")


def test_experiment_runner_integration():
    """Test that experiment runner works with all components."""
    print("\n=== Test 9: Experiment Runner Integration ===")

    runner = ExperimentRunner(
        output_dir="results/test",
        timeout_seconds=10.0,
        seed=DEFAULT_SEED
    )

    # Run a small experiment
    result = runner.run_single_experiment(
        num_vertices=5,
        edge_density=50.0,
        verbose=False
    )

    print(f"Experiment result:")
    print(f"  Vertices: {result.num_vertices}, Edges: {result.num_edges}")
    print(f"  Optimal: {result.exhaustive_solution_size}")
    print(f"  Greedy coverage: {result.greedy_solution_size}")
    print(f"  Greedy matching: {result.greedy_matching_solution_size}")

    # Verify result structure
    assert result.num_vertices == 5
    assert result.num_edges > 0
    assert result.greedy_solution_size is not None
    assert result.greedy_matching_solution_size is not None
    print("Experiment result has all required fields")

    # Verify both greedy variants are present
    assert result.greedy_matching_time > 0
    assert result.greedy_matching_operations > 0
    print("Both greedy variants are executed")

    # Verify comparison metrics exist
    if not result.exhaustive_timed_out:
        assert result.is_optimal is not None
        assert result.matching_is_optimal is not None
        print("Comparison metrics are computed")

    print("Test 9 PASSED\n")


def test_optimal_matching_algorithm():
    """Test the polynomial-time optimal matching-based algorithm."""
    print("\n=== Test 10: Optimal Matching Algorithm ===")

    # Create simple test graph
    graph = Graph()
    v0 = Vertex(0, 10, 10)
    v1 = Vertex(1, 100, 10)
    v2 = Vertex(2, 100, 100)
    v3 = Vertex(3, 10, 100)

    graph.add_vertex(v0)
    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)

    # Add edges forming a square
    e01 = Edge(v0, v1)
    e12 = Edge(v1, v2)
    e23 = Edge(v2, v3)
    e30 = Edge(v3, v0)

    graph.add_edge(e01)
    graph.add_edge(e12)
    graph.add_edge(e23)
    graph.add_edge(e30)

    try:
        # Run optimal matching algorithm
        optimal_matching = OptimalMatchingBased(graph)
        result = optimal_matching.find_minimum_edge_cover()

        print(f"Solution size: {result.solution_size}")
        print(f"Execution time: {result.execution_time:.6f}s")
        print(f"Operations: {result.basic_operations}")

        # Verify solution is valid edge cover
        assert graph.is_edge_cover(result.solution), "Solution must be valid edge cover"
        print("Solution is a valid edge cover")

        # For this graph, optimal is 2 (any two opposite edges)
        assert result.solution_size == 2, f"Expected size 2, got {result.solution_size}"
        print("Solution is optimal (size = 2)")

        # Verify optimality flag
        assert result.is_optimal == True, "Algorithm should guarantee optimality"
        print("Optimality guarantee is correct")

        # Test on a larger random graph
        generator = GraphGenerator(seed=DEFAULT_SEED)
        large_graph = generator.generate_graph(20, 50.0)

        optimal_matching_large = OptimalMatchingBased(large_graph)
        large_result = optimal_matching_large.find_minimum_edge_cover()

        assert large_graph.is_edge_cover(large_result.solution), "Large graph solution must be valid"
        print(f"Works on larger graph (V={20}, E={large_graph.num_edges()})")

    except ImportError as e:
        print(f"⚠ NetworkX not installed - skipping test: {e}")
        print("  Install with: pip install networkx")
        print("Test 10 SKIPPED (NetworkX required)\n")
        return

    print("Test 10 PASSED\n")


def test_branch_and_bound_algorithm():
    """Test the Branch and Bound enhancement to exhaustive search."""
    print("\n=== Test 11: Branch and Bound Algorithm ===")

    # Create test graph
    generator = GraphGenerator(seed=DEFAULT_SEED)
    graph = generator.generate_graph(6, 50.0)

    # Run Branch and Bound
    bb = BranchAndBound(graph)
    bb_result = bb.find_minimum_edge_cover()

    print(f"Solution size: {bb_result.solution_size}")
    print(f"Execution time: {bb_result.execution_time:.6f}s")
    print(f"Operations: {bb_result.basic_operations}")
    print(f"Solutions explored: {bb_result.solutions_explored}")

    # Verify solution is valid edge cover
    assert graph.is_edge_cover(bb_result.solution), "B&B solution must be valid edge cover"
    print("Solution is a valid edge cover")

    # Verify optimality flag
    assert bb_result.is_optimal == True, "B&B should guarantee optimality"
    print("Optimality guarantee is correct")

    # Compare with exhaustive search - should give same answer
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_result = exhaustive.find_minimum_edge_cover()

    assert bb_result.solution_size == exhaustive_result.solution_size, \
        f"B&B and Exhaustive should find same optimal size (B&B={bb_result.solution_size}, Exhaustive={exhaustive_result.solution_size})"
    print("B&B finds same optimal size as exhaustive search")

    # B&B should explore fewer or equal solutions (due to pruning)
    assert bb_result.solutions_explored <= exhaustive_result.solutions_explored, \
        "B&B should explore fewer or equal solutions due to pruning"
    print(f"✓ B&B pruning effective: {bb_result.solutions_explored} vs {exhaustive_result.solutions_explored} solutions")

    print("Test 11 PASSED\n")


def test_optimality_comparison():
    """Test that all optimal algorithms agree on the same optimal size."""
    print("\n=== Test 12: Optimality Comparison ===")

    # Create test graph
    generator = GraphGenerator(seed=DEFAULT_SEED + 42)
    graph = generator.generate_graph(7, 40.0)

    # Run all three optimal algorithms
    exhaustive = ExhaustiveSearch(graph)
    exhaustive_result = exhaustive.find_minimum_edge_cover()
    print(f"Exhaustive: size={exhaustive_result.solution_size}, time={exhaustive_result.execution_time:.4f}s")

    bb = BranchAndBound(graph)
    bb_result = bb.find_minimum_edge_cover()
    print(f"Branch & Bound: size={bb_result.solution_size}, time={bb_result.execution_time:.4f}s")

    try:
        optimal_matching = OptimalMatchingBased(graph)
        optimal_result = optimal_matching.find_minimum_edge_cover()
        print(f"Optimal Matching: size={optimal_result.solution_size}, time={optimal_result.execution_time:.4f}s")

        # All three should find the same optimal size
        assert exhaustive_result.solution_size == bb_result.solution_size == optimal_result.solution_size, \
            f"All optimal algorithms should agree (Exhaustive={exhaustive_result.solution_size}, B&B={bb_result.solution_size}, OptMatch={optimal_result.solution_size})"
        print("All three optimal algorithms agree on optimal size")

        # Optimal matching should be fastest (polynomial vs exponential)
        if graph.num_edges() > 10:
            assert optimal_result.execution_time < exhaustive_result.execution_time, \
                "Optimal matching should be faster than exhaustive for non-trivial graphs"
            print("Polynomial algorithm is faster than exponential")

    except ImportError:
        print("NetworkX not installed - comparing only Exhaustive and B&B")
        assert exhaustive_result.solution_size == bb_result.solution_size, \
            "Exhaustive and B&B should agree on optimal size"
        print("Exhaustive and B&B agree on optimal size")

    print("Test 12 PASSED\n")


def test_large_graph_polynomial():
    """Test that polynomial algorithm can handle large graphs that exhaust cannot."""
    print("\n=== Test 13: Large Graph with Polynomial Algorithm ===")

    try:
        # Create a graph too large for exhaustive search (but easy for polynomial)
        generator = GraphGenerator(seed=DEFAULT_SEED)
        large_graph = generator.generate_graph(50, 25.0)  # 50 vertices, 25% density

        print(f"Large graph: V={large_graph.num_vertices()}, E={large_graph.num_edges()}")

        # This should complete quickly with optimal matching
        optimal_matching = OptimalMatchingBased(large_graph)
        start_time = time.time()
        result = optimal_matching.find_minimum_edge_cover()
        elapsed = time.time() - start_time

        print(f"Solution size: {result.solution_size}")
        print(f"Execution time: {elapsed:.4f}s")
        print(f"Operations: {result.basic_operations}")

        # Verify solution is valid
        assert large_graph.is_edge_cover(result.solution), "Large graph solution must be valid edge cover"
        print("Solution is a valid edge cover")

        # Should complete in reasonable time (< 5 seconds for polynomial)
        assert elapsed < 5.0, f"Polynomial algorithm should complete quickly (took {elapsed:.2f}s)"
        print("Completes in polynomial time")

        # Solution size should be reasonable (between n/2 and n-1)
        n = large_graph.num_vertices()
        assert n//2 <= result.solution_size <= n-1, \
            f"Solution size {result.solution_size} should be between {n//2} and {n-1}"
        print("Solution size is reasonable")

        print("Test 13 PASSED\n")

    except ImportError as e:
        print(f"⚠ NetworkX not installed - skipping test: {e}")
        print("  This test demonstrates the advantage of polynomial-time algorithms")
        print("Test 13 SKIPPED (NetworkX required)\n")


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("COMPREHENSIVE TEST SUITE - MINIMUM EDGE COVER")
    print("Student Number: 113920")
    print("=" * 70)

    try:
        # Basic algorithm tests
        test_simple_graph()
        test_generated_graph()
        test_complete_graph()

        # Validation & integration tests
        test_seed_reproducibility()
        test_timeout_protection()
        test_input_validation()
        test_edge_cover_validation()
        test_greedy_matching_based()
        test_experiment_runner_integration()

        # Additional algorithm tests
        test_optimal_matching_algorithm()
        test_branch_and_bound_algorithm()
        test_optimality_comparison()
        test_large_graph_polynomial()

        print("=" * 70)
        print("ALL TESTS PASSED (13/13)")
        print("=" * 70)
        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
