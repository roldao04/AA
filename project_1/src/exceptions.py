"""
Custom exceptions for Minimum Edge Cover project.
Provides specific exception types for better error handling and debugging.

Student Number: 113920
"""


class EdgeCoverException(Exception):
    """Base exception for all Edge Cover related errors."""
    pass


class InvalidGraphException(EdgeCoverException):
    """
    Raised when graph parameters or structure is invalid.

    Examples:
        - Negative number of vertices
        - Number of vertices exceeds safety limits
        - Graph structure inconsistencies
    """
    pass


class InvalidEdgeCoverException(EdgeCoverException):
    """
    Raised when an edge cover is invalid.

    Examples:
        - Edge cover contains edges not in the graph
        - Edge cover doesn't cover all vertices
        - Empty edge cover for non-empty graph
    """
    pass


class AlgorithmTimeoutException(EdgeCoverException):
    """
    Raised when an algorithm exceeds its allowed execution time.

    This is used to signal that an algorithm was terminated due to timeout
    rather than completing normally.
    """
    pass


class InvalidConfigurationException(EdgeCoverException):
    """
    Raised when configuration parameters are invalid.

    Examples:
        - Invalid edge density (< 0 or > 100)
        - Invalid timeout value
        - Invalid coordinate ranges
        - Conflicting parameters
    """
    pass


class GraphGenerationException(EdgeCoverException):
    """
    Raised when graph generation fails.

    Examples:
        - Cannot generate vertices satisfying distance constraints
        - Cannot generate requested number of edges
        - Random seed issues
    """
    pass


class InsufficientDataException(EdgeCoverException):
    """
    Raised when there is insufficient data for analysis.

    Examples:
        - No experiment results to visualize
        - Empty result set for statistical analysis
    """
    pass
