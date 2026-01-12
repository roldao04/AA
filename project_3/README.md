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

### Key Analyses

- **Error Metrics** - Absolute, relative, RMSE, bias, variance
- **Statistical Tests** - Unbiasedness, paired t-tests, effect sizes
- **Ranking Correlation** - Kendall's τ and Spearman's ρ for order comparison
- **Memory-Time-Accuracy Tradeoffs** - Pareto frontier analysis
- **Theoretical Validation** - Variance, concentration inequalities, guarantees
- **Computational Efficiency** - Asymptotic complexity, scalability, profiling, bottlenecks
- **Limitations Analysis** - Failure modes, constraints, deployment considerations

### Dataset

- **Source:** [Spain & Portugal Weather Data (Kaggle)](https://www.kaggle.com/datasets/luisvivas/spain-portugal-weather?select=porto.csv)
- **File:** `data/raw/porto.csv`
- **Attribute:** `mintempC` (minimum daily temperature in Celsius)
- **Size:** 3,946 observations
- **Unique values:** 30 distinct temperatures

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
│   │   ├── run_comparison.py
│   │   └── scalability_tests.py
│   ├── analysis/            # Statistical analysis & visualization
│   │   ├── statistics.py
│   │   ├── visualization.py
│   │   ├── comparison.py
│   │   └── profiling.py
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
│   ├── 01_data_exploration.ipynb
│   ├── 02_exact_counter_analysis.ipynb
│   ├── 03_fixed_probability_analysis.ipynb
│   ├── 04_space_saving_analysis.ipynb
│   ├── 05_comprehensive_comparison.ipynb
│   ├── 06_advanced_statistical_analysis.ipynb
│   ├── 07_sensitivity_and_extensions.ipynb
│   ├── 08_ranking_correlation_analysis.ipynb
│   └── 09_computational_efficiency_analysis.ipynb
├── report/                  # Final report
├── docs/                    # Documentation
└── [config files]           # .gitignore, requirements.txt, etc.
```
---

