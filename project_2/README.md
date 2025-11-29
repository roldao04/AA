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

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Project Structure

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
├── data/                    # Downloaded datasets
├── results/                 # Experiment results
├── overnight/               # Overnight run outputs
├── figures/                 # Generated visualizations
└── requirements.txt
```

## Usage

### Running Experiments

```python
from src.algorithms import exact_edge_cover, israeli_itai_edge_cover
from src.utils import load_graph

# Load a graph
G = load_graph('karate')

# Run exact algorithm
edge_cover, metrics = exact_edge_cover(G)
print(f"Cover size: {len(edge_cover)}, Runtime: {metrics['runtime']:.4f}s")

# Run randomized algorithm
edge_cover, metrics = israeli_itai_edge_cover(G, seed=42)
print(f"Cover size: {len(edge_cover)}, Runtime: {metrics['runtime']:.4f}s")
```

### Running Overnight Experiments

```bash
python src/experiments/overnight_experiments.py
```

This will:
- Run all algorithms on 45+ graph instances
- Execute 40 trials per algorithm-graph pair
- Save results to `overnight/overnight_results.csv`
- Generate checkpoints every 50 runs

## Implementation Timeline

### Day 1: Algorithm Development (8-9 hours)
- ✅ Project setup and infrastructure
- 🔲 Implement 5 algorithms
- 🔲 Create statistical experiment framework
- 🔲 Validate on small graphs
- 🔲 Configure and test overnight script

### Overnight: Automated Experiments (8-12 hours)
- 🔲 Run 3,500+ experiments across diverse graphs
- 🔲 Collect statistical data with 40 trials per configuration

### Day 2: Analysis and Report (8-9 hours)
- 🔲 Statistical analysis and hypothesis testing
- 🔲 Graph property correlation analysis
- 🔲 Generate publication-quality visualizations
- 🔲 Write 6-page research report

## Datasets

### Built-in Graphs
- Karate Club (34 vertices)
- Florentine Families (15 vertices)
- Davis Southern Women (32 vertices)

### SNAP Datasets (to be downloaded)
- ego-Facebook
- email-Eu-core
- wiki-Vote
- ca-GrQc
- ca-HepTh

### Synthetic Graphs
- Erdős-Rényi (varying density)
- Watts-Strogatz (varying clustering)
- Barabási-Albert (varying degree distribution)

## Dependencies

- `networkx` - Graph algorithms and data structures
- `numpy` - Numerical operations
- `pandas` - Data analysis and manipulation
- `matplotlib` - Visualization
- `seaborn` - Statistical visualization
- `scipy` - Statistical tests and confidence intervals
- `tqdm` - Progress tracking

## References

1. Gallai, T. (1959). "Über extreme Punkt-und Kantenmengen"
2. Israeli, A., & Itai, A. (1986). "A fast and simple randomized parallel algorithm for maximal matching"
3. Bar-Yehuda, R., & Even, S. (1981). "A linear-time approximation algorithm for the weighted vertex cover problem"

## License

This project is for academic purposes as part of a Master's level algorithms course.

## Author

Master's Student - Advanced Algorithms Course
Date: November 2025
