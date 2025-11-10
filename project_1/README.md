# Advanced Algorithms Project 1
## Problem 20 – Minimum Edge Cover

Find a minimum edge cover for an undirected graph G(V,E). An edge cover is a set of edges touching every vertex.

**Author:** João Manuel Vieira Roldão (113920)

---

## Algorithms Implemented

### Optimal
1. Exhaustive Search – backtracking over all edge subsets (O(2^m)); prunes branches when partial solution already too large.
2. Branch & Bound – same worst-case O(2^m) but prunes using a simple lower bound (current size + ceil(uncovered/2)) and greedy upper bound initialization from matching-based heuristic.
3. Optimal Matching (Gallai) – uses maximum matching (NetworkX Blossom) then adds edges for unmatched vertices; proven optimal, ~O(n^2.5).

### Heuristics
4. Greedy Coverage – repeatedly picks edge covering most uncovered vertices (O(m·n)).
5. Greedy Matching – builds a maximal matching then covers remaining vertices (O(m)).

## Metrics Collected (AlgorithmMetrics)
For each run: execution_time, basic_operations, solutions_explored, solution_size, solution (set of Edge objects), is_optimal flag (where applicable).

## Repository Layout
```
project_1/
  src/
    algorithms.py          # All 5 algorithms + comparison helper
    experiment.py          # Batch experiment runner (timeout, skipping logic)
    graph.py               # Graph, Vertex, Edge structures + validation helpers
    graph_generator.py     # Seeded (113920) random graph generator (no isolated vertices)
    graph_visualization.py # Rendering of graphs and solutions
    visualization.py       # Plot orchestration
    complexity_analysis.py # Curve fitting helpers (exponential, polynomial)
    config.py              # Defaults (seed, coordinate ranges)
    exceptions.py          # Custom exceptions (timeouts, invalid config, etc.)
    logger.py              # Structured logging setup
  tests/
    test_basic.py          # 13 tests (correctness + integration + limits)
  run_exponential_experiments.py  # Targeted R² for Exhaustive & Branch & Bound
  run_matching_experiments.py     # Targeted R² for Optimal Matching (Gallai)
  run_greedy_experiments.py       # Targeted scaling for Greedy heuristics
  analyze_complexity.py           # Fits models and prints R² report
  find_limits.py                  # Empirical max graph size per algorithm
  requirements.txt                # Dependencies (networkx, numpy, pandas, matplotlib)
  results/                        # Generated artifacts (timestamped)
```

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

Generate a small batch across default densities (12.5, 25, 50, 75) for vertices 4–8:
```bash
python3 run_exponential_experiments.py
```
Then inspect `results/exponential_targeted_YYYYMMDD_HHMMSS/` for CSV/JSON and plots.

Run polynomial matching scaling experiment:
```bash
python3 run_matching_experiments.py
```

Run greedy scaling experiment (up to 100 vertices):
```bash
python3 run_greedy_experiments.py
```

Validate complexity fits (point to any produced CSV):
```bash
python3 analyze_complexity.py results/exponential_targeted_*/data/exponential_results.csv
```

Find practical algorithm limits (prints report + saves `algorithm_limits.txt`):
```bash
python3 find_limits.py
```

## Output Structure (Actual)
Each targeted script creates: 
```
results/<type>_<timestamp>/
  data/
    <mode>_results.csv
    <mode>_results.json
  graphs/
    instances/            # .json + .png per graph
    solutions/            # Subfolders per algorithm
    comparisons/          # Multi-algorithm comparison png
  plots/                  # Performance / quality plots
```
`experiment.py` also prints a summary (greedy quality %, speedup ranges, timing stats).

## Test Suite (13 tests)
Covered areas:
- Simple / generated / complete graph optimality
- Seed behavior (advancing sequence vs reset)
- Timeout protection (multiprocessing kill)
- Input validation & exceptions
- Edge cover validation logic (rejects foreign edges)
- Greedy Matching Based correctness
- Integration of ExperimentRunner
- Optimal Matching correctness + fallback if dependency missing
- Branch & Bound correctness & speedup vs exhaustive
- Optimality comparisons (all optimal algorithms agree)
- Large graph polynomial scaling sanity check

Run:
```bash
python3 tests/test_basic.py
```

## Practical Algorithm Selection
| Scenario | Recommended | Reason |
|----------|------------|--------|
| ≤ 25 edges | Exhaustive or Branch & Bound | Full optimal baseline / pruning comparison |
| 25–100 vertices (moderate density) | Optimal Matching | Guaranteed optimal, polynomial time |
| > 100 vertices (any density) | Optimal Matching or Greedy Matching | Matching remains fast; greedy for maximum speed |
| Need near-optimal fast | Greedy Coverage | Empirically close to optimal with small overhead |
| High-volume batch runs | Greedy Matching | Lowest complexity (O(m)) |

## Key Implementation Details
- Exhaustive & B&B share validation via `Graph.is_edge_cover`.
- Branch & Bound lower bound = current_size + ceil(uncovered/2); uses matching-based greedy cover as initial upper bound.
- Optimal Matching relies on `networkx.max_weight_matching` (Edmonds/Blossom).
- Timeouts enforced per algorithm using separate processes (`_run_with_timeout`).
- Graph generation avoids isolated vertices and enforces minimum vertex spacing.

## Metrics & Derived Statistics
Computed per experiment row (see `ExperimentResult` dataclass): raw times, operations, solution sizes, greedy quality ratios (optimal_size / heuristic_size), speedups (optimal_time / heuristic_time), operation reduction, Branch & Bound vs exhaustive comparative speedup.

## Reproducibility
Seed `113920` sets initial RNG state; graphs differ across iterations intentionally (advancing state) while remaining reproducible (same sequence when re-run).

## Limit & Complexity Scripts
`find_limits.py` probes increasing sizes and reports practical cutoffs; `analyze_complexity.py` fits curves (exponential for exhaustive & B&B, polynomial for others) and outputs R² + coefficient for model confirmation.

## License / Academic Use
Academic project (MEI – Advanced Algorithms). Use for study, analysis, and reporting.

---
**Author:** João Manuel Vieira Roldão (113920)