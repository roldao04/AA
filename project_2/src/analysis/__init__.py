"""
Analysis module for edge cover algorithm evaluation.

Provides comprehensive visualization and statistical analysis
to support the 8-page report per assignment PDF requirements.
"""

from .visualizations import (
    plot_runtime_vs_size,
    plot_quality_comparison,
    plot_approximation_ratios,
    plot_scalability_limits,
    plot_density_impact,
    plot_pareto_frontier,
    generate_all_visualizations
)

from .statistical_analysis import (
    analyze_complexity,
    analyze_scalability,
    estimate_runtime_for_larger_graphs,
    calculate_accuracy_metrics,
    perform_statistical_tests,
    generate_summary_statistics,
    extract_report_data
)

__all__ = [
    # Visualizations
    'plot_runtime_vs_size',
    'plot_quality_comparison',
    'plot_approximation_ratios',
    'plot_scalability_limits',
    'plot_density_impact',
    'plot_pareto_frontier',
    'generate_all_visualizations',
    # Analysis
    'analyze_complexity',
    'analyze_scalability',
    'estimate_runtime_for_larger_graphs',
    'calculate_accuracy_metrics',
    'perform_statistical_tests',
    'generate_summary_statistics',
    'extract_report_data',
]
