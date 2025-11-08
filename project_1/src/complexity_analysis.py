"""
Complexity Analysis Module - Theoretical vs Experimental Validation

This module provides tools to:
- Fit theoretical complexity curves to experimental data
- Calculate goodness of fit (R² coefficient)
- Validate Big-O claims with statistical rigor
- Extrapolate performance to larger problem instances

Student Number: 113920
"""

import numpy as np
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class ComplexityFit:
    """Results from fitting a theoretical complexity model to experimental data."""
    algorithm_name: str
    complexity_class: str  # e.g., "O(2^m)", "O(n^2.5)", "O(m*n)"
    coefficient: float  # Constant factor c in T(n) = c * f(n)
    r_squared: float  # Goodness of fit (0-1, higher is better)
    predictions: List[Tuple[float, float]]  # [(size, predicted_time), ...]
    residuals: List[float]  # Differences between actual and predicted


def exponential_model(m: float, c: float) -> float:
    """
    Exponential complexity model: T(m) = c * 2^m

    Args:
        m: Number of edges
        c: Constant coefficient

    Returns:
        Predicted execution time
    """
    return c * (2 ** m)


def polynomial_model(n: float, degree: float, c: float) -> float:
    """
    Polynomial complexity model: T(n) = c * n^degree

    Args:
        n: Problem size (vertices or edges)
        degree: Polynomial degree (e.g., 2.5 for O(n^2.5))
        c: Constant coefficient

    Returns:
        Predicted execution time
    """
    return c * (n ** degree)


def linear_model(n: float, c: float) -> float:
    """
    Linear complexity model: T(n) = c * n

    Args:
        n: Problem size
        c: Constant coefficient

    Returns:
        Predicted execution time
    """
    return c * n


def quadratic_model(m: float, n: float, c: float) -> float:
    """
    Quadratic complexity model: T(m,n) = c * m * n

    Args:
        m: Number of edges
        n: Number of vertices
        c: Constant coefficient

    Returns:
        Predicted execution time
    """
    return c * m * n


def calculate_r_squared(actual: List[float], predicted: List[float]) -> float:
    """
    Calculate R² (coefficient of determination) for goodness of fit.

    R² = 1 - (SS_res / SS_tot)
    where SS_res = Σ(actual - predicted)²
          SS_tot = Σ(actual - mean(actual))²

    Args:
        actual: Actual measured values
        predicted: Predicted values from model

    Returns:
        R² value (0-1, where 1 is perfect fit)
    """
    actual_array = np.array(actual)
    predicted_array = np.array(predicted)

    # Calculate sum of squared residuals
    ss_res = np.sum((actual_array - predicted_array) ** 2)

    # Calculate total sum of squares
    mean_actual = np.mean(actual_array)
    ss_tot = np.sum((actual_array - mean_actual) ** 2)

    # Calculate R²
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0

    r_squared = 1.0 - (ss_res / ss_tot)
    return max(0.0, r_squared)  # Ensure non-negative


def fit_exponential_complexity(
    edges: List[int],
    times: List[float],
    algorithm_name: str = "Unknown"
) -> ComplexityFit:
    """
    Fit exponential model T(m) = c * 2^m to experimental data.

    Uses logarithmic transformation: log(T) = log(c) + m*log(2)
    Then performs linear regression to find c.

    Args:
        edges: List of edge counts (m values)
        times: List of execution times
        algorithm_name: Name of the algorithm

    Returns:
        ComplexityFit object with results
    """
    if len(edges) != len(times) or len(edges) == 0:
        raise ValueError("edges and times must have same non-zero length")

    # Filter out zero or negative times (log domain issues)
    valid_data = [(m, t) for m, t in zip(edges, times) if t > 0]
    if not valid_data:
        raise ValueError("No valid (positive) time measurements")

    edges_valid = [m for m, _ in valid_data]
    times_valid = [t for _, t in valid_data]

    # Logarithmic transformation: log(T) = log(c) + m*log(2)
    log_times = np.log(times_valid)
    edges_array = np.array(edges_valid)

    # Linear regression in log space
    # log(T) = a + b*m, where a = log(c), b = log(2)
    coeffs = np.polyfit(edges_array, log_times, deg=1)
    log_c = coeffs[1]  # Intercept
    c = np.exp(log_c)

    # Generate predictions
    predictions = [(m, exponential_model(m, c)) for m in edges_valid]
    predicted_times = [pred for _, pred in predictions]

    # Calculate R²
    r_squared = calculate_r_squared(times_valid, predicted_times)

    # Calculate residuals
    residuals = [actual - pred for actual, pred in zip(times_valid, predicted_times)]

    return ComplexityFit(
        algorithm_name=algorithm_name,
        complexity_class="O(2^m)",
        coefficient=c,
        r_squared=r_squared,
        predictions=predictions,
        residuals=residuals
    )


def fit_polynomial_complexity(
    sizes: List[int],
    times: List[float],
    degree: float,
    algorithm_name: str = "Unknown"
) -> ComplexityFit:
    """
    Fit polynomial model T(n) = c * n^degree to experimental data.

    Uses logarithmic transformation: log(T) = log(c) + degree*log(n)
    Then performs linear regression to find c.

    Args:
        sizes: List of problem sizes (n values)
        times: List of execution times
        degree: Expected polynomial degree (e.g., 2.5 for O(n^2.5))
        algorithm_name: Name of the algorithm

    Returns:
        ComplexityFit object with results
    """
    if len(sizes) != len(times) or len(sizes) == 0:
        raise ValueError("sizes and times must have same non-zero length")

    # Filter out zero or negative values
    valid_data = [(n, t) for n, t in zip(sizes, times) if n > 0 and t > 0]
    if not valid_data:
        raise ValueError("No valid (positive) measurements")

    sizes_valid = [n for n, _ in valid_data]
    times_valid = [t for _, t in valid_data]

    # Logarithmic transformation: log(T) = log(c) + degree*log(n)
    log_times = np.log(times_valid)
    log_sizes = np.log(sizes_valid)

    # Linear regression: log(T) = a + b*log(n)
    # We expect b ≈ degree, and a = log(c)
    coeffs = np.polyfit(log_sizes, log_times, deg=1)
    log_c = coeffs[1]  # Intercept
    actual_degree = coeffs[0]  # Slope (should be close to expected degree)
    c = np.exp(log_c)

    # Generate predictions using expected degree
    predictions = [(n, polynomial_model(n, degree, c)) for n in sizes_valid]
    predicted_times = [pred for _, pred in predictions]

    # Calculate R²
    r_squared = calculate_r_squared(times_valid, predicted_times)

    # Calculate residuals
    residuals = [actual - pred for actual, pred in zip(times_valid, predicted_times)]

    complexity_class = f"O(n^{degree})"

    return ComplexityFit(
        algorithm_name=algorithm_name,
        complexity_class=complexity_class,
        coefficient=c,
        r_squared=r_squared,
        predictions=predictions,
        residuals=residuals
    )


def fit_quadratic_complexity(
    edges: List[int],
    vertices: List[int],
    times: List[float],
    algorithm_name: str = "Unknown"
) -> ComplexityFit:
    """
    Fit quadratic model T(m,n) = c * m * n to experimental data.

    Uses logarithmic transformation: log(T) = log(c) + log(m) + log(n)

    Args:
        edges: List of edge counts
        vertices: List of vertex counts
        times: List of execution times
        algorithm_name: Name of the algorithm

    Returns:
        ComplexityFit object with results
    """
    if len(edges) != len(times) or len(vertices) != len(times) or len(edges) == 0:
        raise ValueError("edges, vertices, and times must have same non-zero length")

    # Filter out zero or negative values
    valid_data = [(m, n, t) for m, n, t in zip(edges, vertices, times) if m > 0 and n > 0 and t > 0]
    if not valid_data:
        raise ValueError("No valid (positive) measurements")

    edges_valid = [m for m, _, _ in valid_data]
    vertices_valid = [n for _, n, _ in valid_data]
    times_valid = [t for _, _, t in valid_data]

    # Compute m*n products
    products = [m * n for m, n in zip(edges_valid, vertices_valid)]

    # Linear regression: T = c * (m*n)
    # Find c by least squares: c = Σ(T_i * product_i) / Σ(product_i²)
    numerator = sum(t * p for t, p in zip(times_valid, products))
    denominator = sum(p ** 2 for p in products)

    if denominator == 0:
        raise ValueError("Cannot fit model: denominator is zero")

    c = numerator / denominator

    # Generate predictions
    predictions = [(p, c * p) for p in products]
    predicted_times = [pred for _, pred in predictions]

    # Calculate R²
    r_squared = calculate_r_squared(times_valid, predicted_times)

    # Calculate residuals
    residuals = [actual - pred for actual, pred in zip(times_valid, predicted_times)]

    return ComplexityFit(
        algorithm_name=algorithm_name,
        complexity_class="O(m*n)",
        coefficient=c,
        r_squared=r_squared,
        predictions=predictions,
        residuals=residuals
    )


def extrapolate_performance(
    fit: ComplexityFit,
    target_sizes: List[float]
) -> List[Tuple[float, float]]:
    """
    Extrapolate performance to larger problem instances.

    Args:
        fit: ComplexityFit object from fitting
        target_sizes: Sizes to extrapolate to

    Returns:
        List of (size, predicted_time) tuples
    """
    predictions = []

    for size in target_sizes:
        if fit.complexity_class.startswith("O(2^"):
            # Exponential model
            predicted_time = exponential_model(size, fit.coefficient)
        elif fit.complexity_class.startswith("O(n^"):
            # Polynomial model - extract degree
            degree_str = fit.complexity_class.split("^")[1].rstrip(")")
            degree = float(degree_str)
            predicted_time = polynomial_model(size, degree, fit.coefficient)
        elif fit.complexity_class == "O(m*n)":
            # Assume square growth (n = m)
            predicted_time = quadratic_model(size, size, fit.coefficient)
        elif fit.complexity_class == "O(n)":
            predicted_time = linear_model(size, fit.coefficient)
        else:
            raise ValueError(f"Unknown complexity class: {fit.complexity_class}")

        predictions.append((size, predicted_time))

    return predictions


def format_time(seconds: float) -> str:
    """
    Format time in human-readable format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string (e.g., "2.5 hours", "3 days")
    """
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"


def print_complexity_report(fit: ComplexityFit) -> None:
    """
    Print a formatted complexity analysis report.

    Args:
        fit: ComplexityFit object to report
    """
    print(f"\n{'='*70}")
    print(f"COMPLEXITY ANALYSIS: {fit.algorithm_name}")
    print(f"{'='*70}")
    print(f"Complexity Class: {fit.complexity_class}")
    print(f"Fitted Coefficient (c): {fit.coefficient:.2e}")
    print(f"R² (Goodness of Fit): {fit.r_squared:.4f}")

    if fit.r_squared >= 0.95:
        fit_quality = "Excellent"
    elif fit.r_squared >= 0.85:
        fit_quality = "Good"
    elif fit.r_squared >= 0.70:
        fit_quality = "Fair"
    else:
        fit_quality = "Poor"

    print(f"Fit Quality: {fit_quality}")
    print(f"{'='*70}\n")
