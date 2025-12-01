# Edge Cover Algorithms: Randomized and Exact Approaches

Master's level project comparing various algorithms for the Minimum Edge Cover problem.

## Project Overview

This project implements and empirically evaluates five edge cover algorithms:

1. **Exact Algorithm** - Matching-based exact solution (O(n²√n))
2. **Israeli-Itai** - Randomized parallel matching (O(log n) expected rounds)
3. **Simulated Annealing** - Metaheuristic optimization
4. **Lazy Greedy** - 3/2-approximation algorithm
5. **Nearest Neighbor** - Simple 2-approximation baseline

### Unique Contribution

**"Structural Predictors of Randomized Algorithm Performance"**

This project systematically analyzes how graph structural properties (density, clustering, degree distribution) affect algorithm performance, providing actionable guidance for algorithm selection.

### Project Structure

```
project_2/
├── src/
│   ├── algorithms/          # Algorithm implementations
│   │   ├── exact.py
│   │   ├── israeli_itai.py
│   │   ├── simulated_annealing.py
│   │   ├── lazy_greedy.py
│   │   └── nearest_neighbor.py
│   ├── utils/               # Graph utilities
│   │   ├── graph_loader.py
│   │   └── graph_properties.py
│   └── experiments/         # Experiment framework
│       ├── experiment_runner.py
│       └── overnight_experiments.py
├── tests/
├── data/                    # Downloaded datasets
├── results/                 # Experiment results
├── figures/                 # Generated visualizations
└── requirements.txt
```
