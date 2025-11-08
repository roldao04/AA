"""
Configuration constants for Minimum Edge Cover project.
Centralizes all configuration values for easy maintenance.

Student Number: 113920
"""

# ============================================================================
# Graph Generation Configuration
# ============================================================================

# Coordinate range for 2D vertex positions
MIN_COORD = 1
MAX_COORD = 500

# Minimum Euclidean distance between vertices to avoid clustering
MIN_DISTANCE = 10.0

# Default random seed (student number for reproducibility)
DEFAULT_SEED = 113920

# ============================================================================
# Experiment Configuration
# ============================================================================

# Default timeout for exhaustive search (in seconds)
DEFAULT_TIMEOUT = 300.0  # 5 minutes

# Default edge densities as percentage of maximum possible edges
DEFAULT_EDGE_DENSITIES = [12.5, 25.0, 50.0, 75.0]

# Default vertex range for experiments
DEFAULT_MIN_VERTICES = 4
DEFAULT_MAX_VERTICES = 15

# Number of repetitions for statistical validation
DEFAULT_REPETITIONS = 1

# ============================================================================
# Safety Limits
# ============================================================================

# Maximum number of vertices allowed (safety limit for memory)
MAX_VERTICES = 1000

# Maximum number of edges for exhaustive search (beyond this, skip exhaustive)
# 2^25 ≈ 33 million subsets - practical limit
MAX_EDGES_FOR_EXHAUSTIVE = 25

# Minimum number of vertices for a valid graph
MIN_VERTICES = 2

# Maximum attempts to generate vertices with MIN_DISTANCE constraint
MAX_VERTEX_GENERATION_ATTEMPTS = 10000

# ============================================================================
# Visualization Configuration
# ============================================================================

# DPI for saved plots
PLOT_DPI = 300

# Default figure size for plots (width, height in inches)
DEFAULT_FIGURE_SIZE = (10, 6)

# Matplotlib style
PLOT_STYLE = 'seaborn-v0_8-darkgrid'

# ============================================================================
# Logging Configuration
# ============================================================================

# Default log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Date format for logs
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Default log level
DEFAULT_LOG_LEVEL = 'INFO'

# ============================================================================
# Output Configuration
# ============================================================================

# Default output directory for results
DEFAULT_OUTPUT_DIR = 'results'

# CSV field separator
CSV_SEPARATOR = ','

# JSON indent for pretty printing
JSON_INDENT = 2

# ============================================================================
# Validation Ranges
# ============================================================================

# Valid range for edge density percentage
MIN_EDGE_DENSITY = 0.0
MAX_EDGE_DENSITY = 100.0

# Valid range for timeout
MIN_TIMEOUT = 0.1  # Minimum 0.1 seconds
MAX_TIMEOUT = 3600.0  # Maximum 1 hour
