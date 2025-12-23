"""
Project-wide configuration constants.
Following research_guide.md and development_plan.md specifications.

This module centralizes all experimental parameters, file paths, and constants
used throughout the project for reproducibility and easy parameter tuning.
"""

# ============================================================================
# REPRODUCIBILITY
# ============================================================================

# Random seed for all probabilistic experiments
RANDOM_SEED = 42


# ============================================================================
# FIXED PROBABILITY COUNTER PARAMETERS
# ============================================================================

# Fixed increment probability (p = 1/4 as specified in project requirements)
FIXED_PROB_P = 0.25

# Number of independent trials to run for statistical analysis
# Development plan recommends 50-100; using 100 for maximum robustness
NUM_TRIALS = 100


# ============================================================================
# SPACE-SAVING ALGORITHM PARAMETERS
# ============================================================================

# k values to test (number of counters/monitored items)
# Tests approximation (k < 31) and exact capture (k >= 31)
SPACE_SAVING_K_VALUES = [10, 20, 30, 40, 50]

# n values for top-n queries (number of items to report)
# Project specification requires n in {5, 10, 15, 20}
TOP_N_VALUES = [5, 10, 15, 20]


# ============================================================================
# DATASET CHARACTERISTICS
# ============================================================================

# Expected total observations in porto.csv (for validation)
EXPECTED_TOTAL_OBS = 3946

# Expected number of unique temperature values (critical for Space-Saving)
EXPECTED_UNIQUE_TEMPS = 30


# ============================================================================
# STATISTICAL PARAMETERS
# ============================================================================

# Confidence level for confidence intervals
CONFIDENCE_LEVEL = 0.95

# Significance level for hypothesis testing
ALPHA = 0.05


# ============================================================================
# FILE PATHS
# ============================================================================

# Data paths
DATA_RAW_PATH = "data/raw/porto.csv"
DATA_PROCESSED_PATH = "data/processed/"

# Results paths
RESULTS_PATH = "results/"
RESULTS_EXACT_PATH = "results/exact/"
RESULTS_FIXED_PROB_PATH = "results/fixed_prob/"
RESULTS_SPACE_SAVING_PATH = "results/space_saving/"
RESULTS_COMPARISON_PATH = "results/comparison/"

# Figures paths
FIGURES_PATH = "results/figures/"
FIGURES_EXPLORATORY_PATH = "results/figures/exploratory/"
FIGURES_FIXED_PROB_PATH = "results/figures/fixed_prob/"
FIGURES_SPACE_SAVING_PATH = "results/figures/space_saving/"
FIGURES_COMPARISON_PATH = "results/figures/comparison/"
