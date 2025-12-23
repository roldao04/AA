# AA Project 3: Approximate Counting and Frequent Items

**Author:** João Roldão (113920)
**Course:** Advanced Algorithms (AA) 2025/2026
**Institution:** Universidade do Aveiro
**Python Version:** 3.12.3

---

## Project Overview

Implementation and empirical analysis of approximate counting algorithms for streaming data, comparing their performance against exact counting baselines.

### Algorithms Implemented

- **Exact Counter** - Baseline ground truth using dictionary-based counting
- **Fixed Probability Counter** - Probabilistic counter with p = 1/4
- **Space-Saving Algorithm** - Deterministic frequent items mining

### Dataset

- **Source:** [Spain & Portugal Weather Data (Kaggle)](https://www.kaggle.com/datasets/luisvivas/spain-portugal-weather?select=porto.csv)
- **File:** `data/raw/porto.csv`
- **Attribute:** `mintempC` (minimum daily temperature in Celsius)
- **Size:** 3,946 observations
- **Unique values:** 31 distinct temperatures

---

## Project Structure

```bash
project_3/
├── src/
│   ├── algorithms/          # Core algorithm implementations
│   │   ├── exact_counter.py
│   │   ├── fixed_prob_counter.py
│   │   └── space_saving.py
│   ├── experiments/         # Runnable experiment scripts
│   │   ├── run_exact.py
│   │   ├── run_fixed_prob.py
│   │   ├── run_space_saving.py
│   │   └── run_comparison.py
│   ├── analysis/            # Statistical analysis & visualization
│   │   ├── statistics.py
│   │   ├── visualization.py
│   │   └── comparison.py
│   ├── utils/               # Configuration and utilities
│   │   ├── config.py       # Project constants
│   │   └── data_loader.py  # Data loading functions
│   └── tests/               # Unit tests
│       ├── test_exact_counter.py
│       ├── test_fixed_prob_counter.py
│       └── test_space_saving.py
├── data/
│   ├── raw/                 # Original porto.csv
│   └── processed/           # Preprocessed data (if needed)
├── results/                 # Experimental outputs
│   ├── exact/
│   ├── fixed_prob/
│   ├── space_saving/
│   ├── comparison/
│   └── figures/             # All visualizations
├── notebooks/               # Jupyter notebooks
│   └── data_exploration.ipynb
├── report/                  # Final report
│   ├── draft/
│   └── final/
├── docs/                    # Documentation
└── [config files]           # .gitignore, requirements.txt, etc.
```
