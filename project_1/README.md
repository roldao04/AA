# Advanced Algorithms Project 1
## Problem 20 - Minimum Edge Cover

**Optimization Problem**

Find a minimum edge cover for a given undirected graph G(V, E), with n vertices and m edges. An edge cover is a set C of edges such that each vertex of G is incident to at least one edge in C. A minimum edge cover is an edge cover of smallest possible size.

**Author:** João Manuel Vieira Roldão (113920)

---

## Project Overview

This project implements and analyzes three algorithms for solving the Minimum Edge Cover problem:

1. **Exhaustive Search** - Optimal algorithm using backtracking with branch pruning
2. **Greedy Coverage** - Fast heuristic selecting edges that cover most uncovered vertices
3. **Greedy Matching** - Fast heuristic based on maximal matching

The implementation includes:
- Random graph generation with reproducible seed (113920)
- Comprehensive metrics tracking (execution time, operations, solutions explored)
- Automated experimental framework with timeout enforcement
- Input validation and error handling
- Structured logging system
- Statistical analysis and visualization
- Complete test suite (9 comprehensive tests)

## Project Structure

```
project_1/
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration constants and settings
│   ├── exceptions.py         # Custom exception classes
│   ├── logger.py             # Logging utilities
│   ├── graph.py              # Graph data structures (Vertex, Edge, Graph)
│   ├── graph_generator.py    # Random graph generator with seed 113920
│   ├── algorithms.py         # 3 algorithms: Exhaustive + 2 Greedy variants
│   ├── experiment.py         # Experimental framework with timeout
│   └── visualization.py      # Plotting and visualization tools
├── tests/
│   ├── __init__.py
│   └── test_basic.py         # Comprehensive test suite (9 tests)
├── results/                  # Generated results (CSV, JSON, plots)
├── run_experiments.py        # Main experiment runner
├── run_full_experiments.py   # Extended experiments for report
├── requirements.txt          # Python dependencies
├── INCEPTION.md              # Detailed project guide
├── PROJECT_SUMMARY.md        # Implementation checklist
└── README.md                 # This file
```

## Installation

### Requirements
- Python 3.7 or higher
- matplotlib (for visualization)
- numpy (for numerical operations)

### Setup

1. Clone or download the project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install matplotlib numpy
```

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

- `results_TIMESTAMP.csv`: Tabular results data
- `results_TIMESTAMP.json`: Structured JSON results
- `time_vs_vertices.png`: Execution time comparison
- `operations_vs_vertices.png`: Operation count comparison
- `solutions_explored.png`: Solution space exploration
- `greedy_quality.png`: Greedy algorithm quality analysis
- `speedup.png`: Performance speedup visualization
- `solution_sizes.png`: Solution size comparison

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

1. **Exhaustive search scalability:** Exponential growth limits practical use to ~10-12 vertices
2. **Greedy effectiveness:** Finds optimal solution in ~78% of test cases
3. **Performance gap:** Greedy is 3-140x faster than exhaustive search
4. **Edge density impact:** Higher density graphs have more solutions to explore
5. **Quality vs speed tradeoff:** Greedy sacrifices ~6.5% quality for massive speedup

## Testing

The comprehensive test suite (9 tests) validates:

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

All tests include assertions to verify correctness. Run with: `python3 tests/test_basic.py`

## Theoretical Analysis

### Minimum Edge Cover Problem

- **Problem class:** NP-hard (decision version)
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