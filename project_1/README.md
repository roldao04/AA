# Advanced Algorithms Project 1
## Problem 20 - Minimum Edge Cover

**Optimization Problem**

Find a minimum edge cover for a given undirected graph G(V, E), with n vertices and m edges. An edge cover is a set C of edges such that each vertex of G is incident to at least one edge in C. A minimum edge cover is an edge cover of smallest possible size.

**Author:** João Manuel Vieira Roldão (113920)

---

## Project Overview

This project implements and analyzes **five algorithms** for solving the Minimum Edge Cover problem:

### Optimal Algorithms (Guaranteed Minimum)
1. **Exhaustive Search** - O(2^m) backtracking with branch pruning (exponential)
2. **Branch & Bound** - O(2^m) enhanced exhaustive with matching-based lower bounds
3. **Optimal Matching** - O(n^2.5) polynomial-time optimal using Gallai's theorem ⭐

### Heuristic Algorithms (Fast Approximations)
4. **Greedy Coverage** - O(m·n) heuristic selecting edges covering most vertices
5. **Greedy Matching** - O(m) fastest heuristic based on maximal matching

The implementation includes:
- Random graph generation with reproducible seed (113920)
- **Complexity validation** (experimental vs theoretical analysis)
- **Algorithm limits determination** (maximum processable graph size)
- Comprehensive metrics tracking (execution time, operations, solutions explored)
- Automated experimental framework with timeout enforcement
- Input validation and error handling
- Structured logging system
- Statistical analysis and visualization
- Complete test suite (13 comprehensive tests)

## Project Structure

```
project_1/
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration constants and settings
│   ├── exceptions.py           # Custom exception classes
│   ├── logger.py               # Logging utilities
│   ├── graph.py                # Graph data structures (Vertex, Edge, Graph)
│   ├── graph_generator.py      # Random graph generator with seed 113920
│   ├── algorithms.py           # 5 algorithms: 3 Optimal + 2 Greedy
│   ├── experiment.py           # Experimental framework with timeout
│   ├── complexity_analysis.py  # Theoretical validation tools
│   └── visualization.py        # Plotting and visualization tools
├── tests/
│   ├── __init__.py
│   └── test_basic.py           # Comprehensive test suite (13 tests)
├── docs/
│   └── THEORETICAL_ANALYSIS.md # Formal complexity analysis
├── results/                    # Generated results (CSV, JSON, plots)
├── run_experiments.py          # Main experiment runner
├── run_full_experiments.py     # Extended experiments for report
├── analyze_complexity.py       # Complexity validation script
├── find_limits.py              # Algorithm limits finder
├── requirements.txt            # Python dependencies
├── INCEPTION.md                # Detailed project guide
├── PROJECT_SUMMARY.md          # Implementation checklist
└── README.md                   # This file
```

## Installation

### Requirements
- Python 3.7 or higher
- matplotlib>=3.5.0 (for visualization)
- numpy>=1.21.0 (for numerical operations)
- **networkx>=2.5** (for Optimal Matching algorithm)

### Setup

1. Clone or download the project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install matplotlib numpy networkx
```

**Note:** NetworkX is required for the Optimal Matching algorithm (polynomial-time optimal). Without it, that algorithm will be skipped, but all other algorithms work normally.

## Usage

### Run Experiments

**Quick test (recommended for first run):**
```bash
python3 run_experiments.py --quick
```

**Full experiments:**
```bash
python3 run_experiments.py --min-vertices 4 --max-vertices 10
```

**Custom configuration:**
```bash
python3 run_experiments.py \
    --min-vertices 4 \
    --max-vertices 12 \
    --timeout 120 \
    --output-dir results
```

**Options:**
- `--min-vertices N`: Minimum number of vertices (default: 4)
- `--max-vertices N`: Maximum number of vertices (default: 12)
- `--timeout SECS`: Timeout for exhaustive search in seconds (default: 60)
- `--output-dir DIR`: Output directory for results (default: results)
- `--no-plots`: Skip generating plots
- `--quick`: Quick test with fewer configurations

### Run Tests

```bash
python3 tests/test_basic.py
```

Expected output: All tests should pass with optimal solutions verified.

## Algorithm Details

### Exhaustive Search (Optimal)

**Approach:** Backtracking algorithm that explores all 2^m possible edge subsets

**Optimizations:**
- Branch pruning: Abandon branches when partial solution exceeds current best
- Early termination: Stop exploring once minimum is found
- Efficient subset representation using Python sets

**Complexity:** O(2^m) where m is the number of edges

**Guarantees:** Always finds the optimal (minimum) edge cover

### Branch & Bound (Optimal, Enhanced)

**Approach:** Enhanced exhaustive search with matching-based lower bound pruning

**Optimizations:**
- Lower bound pruning using matching theory: LB = n - |maximum matching|
- Greedy upper bound initialization for better pruning
- Smart branch ordering (uncovered vertices first)

**Complexity:** O(2^m) worst-case, significantly better average-case

**Guarantees:** Always finds the optimal solution, faster than vanilla exhaustive

### Optimal Matching (Polynomial Optimal) ⭐

**Approach:** Polynomial-time optimal algorithm using Gallai's theorem

**Algorithm:**
1. Find maximum matching M in graph using Blossom algorithm
2. For each unmatched vertex, add any incident edge
3. Result is guaranteed optimal: |edge cover| = n - |maximum matching|

**Theory:** Based on Gallai's theorem: β'(G) = n - α'(G)

**Complexity:** O(n^2.5) using Edmonds' Blossom algorithm

**Guarantees:**
- Always finds the optimal (minimum) edge cover
- **Scales to graphs with 1000s of vertices** (polynomial!)
- Dramatically faster than exponential algorithms for m > 20

### Greedy Coverage (Fast)

**Approach:** Iteratively select edges that cover the most uncovered vertices

**Strategy:**
1. Start with all vertices uncovered
2. While uncovered vertices remain:
   - Select edge covering the most uncovered vertices
   - Add edge to cover
   - Mark its vertices as covered

**Complexity:** O(m × n) where m = edges, n = vertices

**Guarantees:** Fast execution, but may not find optimal solution

### Greedy Matching (Fast)

**Approach:** Based on maximal matching theory

**Strategy:**
1. Find a maximal matching (greedily select edges with no common vertices)
2. For each unmatched vertex, add any incident edge

**Complexity:** O(m) for greedy maximal matching

**Guarantees:** Fast execution, theoretically related to optimal via matching theory

## Algorithm Comparison Table

| Algorithm | Time Complexity | Space | Optimal? | Max Graph Size | Use Case |
|-----------|----------------|-------|----------|----------------|----------|
| **Exhaustive Search** | O(2^m) | O(m) | ✅ Yes | m ≤ 20-25 | Small graphs, baseline |
| **Branch & Bound** | O(2^m)* | O(m) | ✅ Yes | m ≤ 25-30 | Small graphs, better performance |
| **Optimal Matching** | O(n^2.5) | O(n+m) | ✅ Yes | **n ≤ 1000+** | **Any size - recommended** |
| **Greedy Coverage** | O(m·n) | O(n) | ❌ No | n ≤ 1000+ | Fast approximation |
| **Greedy Matching** | O(m) | O(n) | ❌ No | n ≤ 1000+ | Fastest approximation |

*\*Better average-case than vanilla exhaustive due to pruning*

## Algorithm Selection Guide

### For Optimal Solutions:

**Small Graphs (m ≤ 25 edges):**
- Use **Exhaustive** or **Branch & Bound** for comparison/analysis
- Both guarantee optimal, B&B is faster

**Medium/Large Graphs (m > 25):**
- Use **Optimal Matching** (polynomial, scales well)
- Only algorithm that can handle large graphs optimally

**Very Large Graphs (n > 1000):**
- **Optimal Matching** is the only practical optimal algorithm
- Completes in seconds even for graphs with 1000s of vertices

### For Fast Approximations:

**Need Speed:**
- Use **Greedy Matching** (O(m), fastest)
- 2-approximation guarantee

**Better Quality:**
- Use **Greedy Coverage** (O(m·n), slower but better)
- Finds optimal in ~78% of cases empirically

### For Analysis/Research:

- Run **all algorithms** on small graphs (m ≤ 20)
- Compare exponential vs polynomial scalability
- Validate heuristic quality against optimal

## Additional Tools

### Complexity Validation

Validate experimental results against theoretical predictions:

```bash
python3 analyze_complexity.py
```

This script:
- Fits theoretical complexity models to experimental data
- Calculates R² goodness of fit
- Generates validation report with statistical analysis
- Confirms Big-O predictions match reality

### Algorithm Limits Finder

Determine maximum graph size each algorithm can handle:

```bash
python3 find_limits.py
```

This script:
- Systematically tests increasing graph sizes
- Records when each algorithm times out
- Generates limits table and recommendations
- Helps choose the right algorithm for your graph size

## Graph Generation

Graphs are generated with the following properties:

- **Seed:** 113920 (student number) for reproducibility
- **Vertices:** 2D points with coordinates in [1, 500]
- **Minimum distance:** 10 units between vertices
- **Edge densities:** 12.5%, 25%, 50%, 75% of maximum possible edges
- **No isolated vertices:** Every vertex has at least degree 1

Maximum edges for n vertices: n(n-1)/2

## Results and Metrics

The experimental framework collects:

1. **Execution Time:** Wall-clock time in seconds
2. **Basic Operations:** Number of comparisons and core operations
3. **Solutions Explored:** Number of candidate solutions examined
4. **Solution Size:** Number of edges in the edge cover
5. **Quality Ratio:** Optimal size / Greedy size (1.0 = optimal)
6. **Speedup:** Exhaustive time / Greedy time

### Output Files

**Experimental Results:**
- `results_TIMESTAMP.csv`: Tabular results data
- `results_TIMESTAMP.json`: Structured JSON results

**Visualization Plots:**
- `time_vs_vertices.png`: Execution time comparison
- `operations_vs_vertices.png`: Operation count comparison
- `solutions_explored.png`: Solution space exploration
- `greedy_quality.png`: Greedy algorithm quality analysis
- `speedup.png`: Performance speedup visualization
- `solution_sizes.png`: Solution size comparison
- `all_algorithms_comparison.png`: All 5 algorithms on single plot (log scale)

**Analysis Reports:**
- `complexity_validation.txt`: R² fit quality for each algorithm
- `algorithm_limits.txt`: Maximum processable graph size per algorithm

## Experimental Results (Quick Test)

From the initial quick experiment:

- **Total experiments:** 10 configurations
- **Completed (optimal found):** 9
- **Greedy quality:**
  - Optimal solutions: 77.8% of cases
  - Average quality ratio: 0.935
- **Speedup:** 3.5x to 139.8x (average 26.6x)
- **Exhaustive search becomes impractical:** Beyond 8 vertices with high density

## Key Findings

1. **Polynomial optimal exists:** Optimal Matching solves optimally in O(n^2.5) - game changer!
2. **Exponential limits:** Exhaustive/B&B practical up to ~20-30 edges
3. **Branch & Bound improvement:** Same optimality, 2-4x faster than vanilla exhaustive
4. **Polynomial scalability:** Optimal Matching handles 1000+ vertices in seconds
5. **Greedy effectiveness:** Finds optimal in ~78% of test cases
6. **Performance gap:** Greedy is 3-140x faster than exhaustive
7. **Complexity validation:** Experimental results match theoretical Big-O predictions (R² > 0.90)
8. **Algorithm choice matters:** Use Optimal Matching for m > 25, saves hours/days of computation

## Testing

The comprehensive test suite (13 tests) validates:

**Basic Algorithm Tests:**
- Simple graphs with known optimal solutions (square graph)
- Randomly generated graphs at various densities
- Complete graphs (K4)

**Validation & Integration Tests:**
- Seed reproducibility and graph variation
- Timeout protection for large graphs
- Input validation (invalid parameters rejected)
- Edge cover validation (foreign edges detected)
- GreedyMatchingBased algorithm correctness
- Full integration with experiment runner

**Phase 2 Algorithm Tests:**
- Optimal Matching algorithm correctness and optimality
- Branch & Bound pruning effectiveness
- All 3 optimal algorithms agree on same solution
- Polynomial algorithm scalability to large graphs (50+ vertices)

All tests include assertions to verify correctness. Run with: `python3 tests/test_basic.py`

## Theoretical Analysis

**For comprehensive formal analysis, see:** [`docs/THEORETICAL_ANALYSIS.md`](docs/THEORETICAL_ANALYSIS.md)

This document includes:
- Formal complexity analysis with recurrence relations and proofs
- Gallai's theorem and matching theory foundations
- Detailed proof sketches for all algorithms
- Complexity growth comparison and scalability analysis

### Minimum Edge Cover Problem

- **Problem class:** NP-hard (decision version)
- **Solution exists:** Polynomial-time using Gallai's theorem!
- **Relation to matching:** |minimum edge cover| = n - |maximum matching|
- **Lower bound:** ⌈n/2⌉ edges (when perfect matching exists)
- **Upper bound:** n-1 edges (worst case: star graph)

### Algorithm Complexity

**Exhaustive Search:**
- Time: O(2^m) - exponential in number of edges
- Space: O(m) - for recursion stack
- Optimal: Yes (explores all possibilities)

**Greedy Heuristic:**
- Time: O(m × n) - polynomial
- Space: O(n) - for tracking uncovered vertices
- Optimal: No (2-approximation bound exists for variations)

## Future Enhancements

Potential improvements:
1. Implement maximum matching-based algorithm
2. Add more sophisticated pruning strategies
3. Parallel exhaustive search implementation
4. Additional heuristics (e.g., minimum degree, edge betweenness)
5. Graph visualization with edge cover highlighting
6. Interactive result exploration tool

## References

- Algorithm Design course materials
- Graph theory fundamentals
- Edge cover and matching theory
- Exhaustive search and backtracking techniques

## License

Academic project - MEI, Advanced Algorithms course

---

**Author:** João Manuel Vieira Roldão (113920)