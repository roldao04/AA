"""
Comprehensive Visualization Module for Algorithm Comparison.

This module provides publication-quality plotting functions with consistent
styling for all comparison visualizations across Tiers 1-3.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Union, Optional
from pathlib import Path

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13

# Color palette for algorithms
ALGORITHM_COLORS = {
    'exact': '#2E7D32',  # Dark green
    'fixed_prob': '#1976D2',  # Blue
    'space_saving': '#D32F2F',  # Red
    'space_saving_k10': '#D32F2F',
    'space_saving_k15': '#E64A19',
    'space_saving_k20': '#F57C00',
    'space_saving_k25': '#FFA000',
    'space_saving_k30': '#FBC02D',
    'space_saving_k40': '#AFB42B',
    'space_saving_k50': '#689F38',
}


def set_publication_style():
    """Set consistent publication-quality style for all plots."""
    sns.set_context("paper", font_scale=1.0)
    sns.set_style("whitegrid", {
        'grid.linestyle': '--',
        'grid.alpha': 0.6,
        'axes.edgecolor': '.2',
        'axes.linewidth': 0.8
    })


def save_figure(fig, filename: str, output_dir: str, tight: bool = True, **kwargs):
    """
    Save figure with consistent settings.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Filename (without path)
    output_dir : str
        Output directory path
    tight : bool, default=True
        Use tight_layout
    **kwargs
        Additional arguments passed to savefig
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if tight:
        fig.tight_layout()

    save_path = output_path / filename
    fig.savefig(save_path, bbox_inches='tight', dpi=300, **kwargs)
    print(f"  ✓ Saved: {save_path}")


def plot_master_comparison_table(
    comparison_df: pd.DataFrame,
    output_dir: str = None,
    filename: str = 'master_comparison_table.png'
) -> plt.Figure:
    """
    Create formatted table visualization of master comparison.

    Parameters
    ----------
    comparison_df : pd.DataFrame
        Master comparison table from create_master_comparison_table()
    output_dir : str, optional
        Directory to save figure
    filename : str, default='master_comparison_table.png'
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(12, len(comparison_df) * 0.4 + 1))
    ax.axis('tight')
    ax.axis('off')

    # Create table
    table = ax.table(
        cellText=comparison_df.values,
        colLabels=comparison_df.columns,
        cellLoc='center',
        loc='center',
        colWidths=[0.18] * len(comparison_df.columns)
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)

    # Style header
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_facecolor('#4CAF50')
            cell.set_text_props(weight='bold', color='white')
        else:
            if j == 0:
                cell.set_text_props(weight='bold')
            # Alternate row colors
            if i % 2 == 0:
                cell.set_facecolor('#F5F5F5')

    plt.title('Master Algorithm Comparison Table', pad=20, fontsize=14, weight='bold')

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_error_boxplots(
    cross_errors_df: pd.DataFrame,
    algorithms: List[str],
    output_dir: str = None,
    filename: str = 'error_boxplots.png'
) -> plt.Figure:
    """
    Create box plots comparing error distributions across algorithms.

    Parameters
    ----------
    cross_errors_df : pd.DataFrame
        Cross-algorithm errors from calculate_cross_algorithm_errors()
    algorithms : List[str]
        List of algorithm column prefixes to plot (e.g., ['fp', 'ss_k10', 'ss_k20'])
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    # Collect error data
    error_data = []
    for alg in algorithms:
        if f'{alg}_rel_error' in cross_errors_df.columns:
            errors = cross_errors_df[f'{alg}_rel_error'].dropna() * 100  # Convert to percentage
            for err in errors:
                error_data.append({
                    'Algorithm': alg.replace('_', ' ').replace('fp', 'Fixed Prob').replace('ss ', 'SS '),
                    'Relative Error (%)': err
                })

    error_df = pd.DataFrame(error_data)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(
        data=error_df,
        x='Algorithm',
        y='Relative Error (%)',
        ax=ax,
        palette='Set2'
    )

    ax.set_title('Error Distribution Comparison Across Algorithms', fontsize=14, weight='bold')
    ax.set_xlabel('Algorithm', fontsize=12)
    ax.set_ylabel('Relative Error (%)', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_error_vs_frequency(
    cross_errors_df: pd.DataFrame,
    algorithms: List[Dict[str, str]],
    log_scale: bool = True,
    output_dir: str = None,
    filename: str = 'error_vs_frequency.png'
) -> plt.Figure:
    """
    Plot relative error vs true frequency for all algorithms.

    Parameters
    ----------
    cross_errors_df : pd.DataFrame
        Cross-algorithm errors
    algorithms : List[Dict[str, str]]
        List of dicts with 'column', 'label', 'color', 'marker'
    log_scale : bool, default=True
        Use log scale for frequency axis
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    for alg in algorithms:
        col = alg['column']
        if f'{col}_rel_error' in cross_errors_df.columns:
            x = cross_errors_df['true_count']
            y = cross_errors_df[f'{col}_rel_error'] * 100  # Percentage

            # Remove NaN
            mask = ~(x.isna() | y.isna())
            x_clean = x[mask]
            y_clean = y[mask]

            ax.scatter(
                x_clean,
                y_clean,
                label=alg['label'],
                color=alg.get('color'),
                marker=alg.get('marker', 'o'),
                alpha=0.7,
                s=60,
                edgecolors='black',
                linewidths=0.5
            )

    if log_scale:
        ax.set_xscale('log')

    ax.set_xlabel('True Frequency (log scale)' if log_scale else 'True Frequency', fontsize=12)
    ax.set_ylabel('Relative Error (%)', fontsize=12)
    ax.set_title('Relative Error vs True Frequency', fontsize=14, weight='bold')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_pareto_frontier(
    comparison_df: pd.DataFrame,
    output_dir: str = None,
    filename: str = 'pareto_frontier.png'
) -> plt.Figure:
    """
    Plot memory-accuracy Pareto frontier.

    Parameters
    ----------
    comparison_df : pd.DataFrame
        Master comparison table
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(10, 7))

    memory = comparison_df['Memory_KB'].values
    error = comparison_df['Mean_Rel_Error_%'].values
    labels = comparison_df['Algorithm'].values

    # Identify Pareto frontier
    is_pareto = np.ones(len(memory), dtype=bool)
    for i in range(len(memory)):
        for j in range(len(memory)):
            if i != j:
                if memory[j] <= memory[i] and error[j] < error[i]:
                    is_pareto[i] = False
                    break
                if memory[j] < memory[i] and error[j] <= error[i]:
                    is_pareto[i] = False
                    break

    # Plot all points
    colors = ['red' if 'Fixed' in lbl else 'blue' if 'Space' in lbl else 'green'
              for lbl in labels]

    for i, (mem, err, lbl, color) in enumerate(zip(memory, error, labels, colors)):
        marker = 's' if is_pareto[i] else 'o'
        size = 150 if is_pareto[i] else 80
        ax.scatter(mem, err, s=size, c=color, marker=marker, alpha=0.7,
                   edgecolors='black', linewidths=1.5 if is_pareto[i] else 0.5,
                   label=lbl if i == 0 or is_pareto[i] else '')

        # Annotate
        ax.annotate(lbl, (mem, err), xytext=(5, 5), textcoords='offset points',
                    fontsize=8, alpha=0.8)

    # Connect Pareto frontier points
    pareto_points = sorted([(mem, err) for mem, err, pareto in zip(memory, error, is_pareto) if pareto])
    if len(pareto_points) > 1:
        pareto_mem, pareto_err = zip(*pareto_points)
        ax.plot(pareto_mem, pareto_err, 'k--', alpha=0.4, linewidth=1, label='Pareto Frontier')

    ax.set_xlabel('Memory Usage (KB)', fontsize=12)
    ax.set_ylabel('Mean Relative Error (%)', fontsize=12)
    ax.set_title('Memory-Accuracy Pareto Frontier', fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)

    # Legend without duplicates
    handles, labels_legend = ax.get_legend_handles_labels()
    by_label = dict(zip(labels_legend, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_multipanel_comparison(
    comparison_df: pd.DataFrame,
    output_dir: str = None,
    filename: str = 'multipanel_comparison.png'
) -> plt.Figure:
    """
    Create 3-panel comparison figure (memory | error | time).

    Parameters
    ----------
    comparison_df : pd.DataFrame
        Master comparison table
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    algorithms = comparison_df['Algorithm'].values
    memory = comparison_df['Memory_KB'].values
    error = comparison_df['Mean_Rel_Error_%'].values
    time = comparison_df['Time_ms'].values

    colors = ['green' if 'Exact' in alg else 'blue' if 'Fixed' in alg else 'red'
              for alg in algorithms]

    # Panel 1: Memory
    axes[0].barh(algorithms, memory, color=colors, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Memory (KB)', fontsize=11)
    axes[0].set_title('Memory Usage', fontsize=12, weight='bold')
    axes[0].grid(axis='x', alpha=0.3)

    # Panel 2: Error
    axes[1].barh(algorithms, error, color=colors, alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('Relative Error (%)', fontsize=11)
    axes[1].set_title('Mean Relative Error', fontsize=12, weight='bold')
    axes[1].grid(axis='x', alpha=0.3)

    # Panel 3: Time
    axes[2].barh(algorithms, time, color=colors, alpha=0.7, edgecolor='black')
    axes[2].set_xlabel('Time (ms)', fontsize=11)
    axes[2].set_title('Execution Time', fontsize=12, weight='bold')
    axes[2].grid(axis='x', alpha=0.3)

    plt.suptitle('Comprehensive Algorithm Performance Comparison', fontsize=14, weight='bold', y=1.02)

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_bootstrap_distribution(
    bootstrap_results: Dict,
    output_dir: str = None,
    filename: str = 'bootstrap_distribution.png'
) -> plt.Figure:
    """
    Plot bootstrap distribution with confidence intervals.

    Parameters
    ----------
    bootstrap_results : Dict
        Results from bootstrap_confidence_intervals()
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    bootstrap_dist = bootstrap_results['bootstrap_distribution']
    observed = bootstrap_results['observed_statistic']
    ci_lower = bootstrap_results['ci_lower']
    ci_upper = bootstrap_results['ci_upper']
    conf_level = bootstrap_results['confidence_level']

    # Histogram
    ax.hist(bootstrap_dist, bins=50, density=True, alpha=0.6, color='skyblue',
            edgecolor='black', label='Bootstrap Distribution')

    # Observed statistic
    ax.axvline(observed, color='red', linestyle='--', linewidth=2,
               label=f'Observed: {observed:.3f}')

    # Confidence interval
    ax.axvline(ci_lower, color='green', linestyle=':', linewidth=1.5,
               label=f'{conf_level*100:.0f}% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
    ax.axvline(ci_upper, color='green', linestyle=':', linewidth=1.5)

    # Shade CI region
    ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='green')

    ax.set_xlabel('Statistic Value', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title(f'Bootstrap Distribution ({bootstrap_results["n_bootstrap"]} iterations)',
                 fontsize=14, weight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_permutation_distribution(
    perm_results: Dict,
    output_dir: str = None,
    filename: str = 'permutation_distribution.png'
) -> plt.Figure:
    """
    Plot permutation test distribution.

    Parameters
    ----------
    perm_results : Dict
        Results from permutation_test()
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    perm_dist = perm_results['permutation_distribution']
    observed = perm_results['observed_statistic']
    p_value = perm_results['p_value']

    # Histogram
    ax.hist(perm_dist, bins=50, density=True, alpha=0.6, color='lightcoral',
            edgecolor='black', label='Permutation Distribution')

    # Observed statistic
    ax.axvline(observed, color='darkred', linestyle='--', linewidth=2,
               label=f'Observed: {observed:.3f}')

    # Shade extreme region
    if perm_results['alternative'] == 'two-sided':
        extreme_vals = perm_dist[np.abs(perm_dist) >= np.abs(observed)]
    elif perm_results['alternative'] == 'greater':
        extreme_vals = perm_dist[perm_dist >= observed]
    else:  # 'less'
        extreme_vals = perm_dist[perm_dist <= observed]

    if len(extreme_vals) > 0:
        ax.hist(extreme_vals, bins=20, density=True, alpha=0.4, color='red',
                label=f'Extreme Values (p={p_value:.4f})')

    ax.set_xlabel('Test Statistic', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title(f'Permutation Test Distribution ({perm_results["n_permutations"]} permutations)',
                 fontsize=14, weight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_qq_normality(
    qq_results: Dict,
    output_dir: str = None,
    filename: str = 'qq_plot.png'
) -> plt.Figure:
    """
    Plot Q-Q plot for normality assessment.

    Parameters
    ----------
    qq_results : Dict
        Results from qq_plot_normality_test()
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(8, 8))

    theoretical = qq_results['theoretical_quantiles']
    sample = qq_results['sample_quantiles']

    # Q-Q plot
    ax.scatter(theoretical, sample, alpha=0.6, s=30, edgecolors='black', linewidths=0.5)

    # Reference line
    min_val = min(theoretical.min(), sample.min())
    max_val = max(theoretical.max(), sample.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Normal')

    # Add Shapiro-Wilk test result
    if not np.isnan(qq_results['shapiro_pvalue']):
        test_text = f"Shapiro-Wilk: p={qq_results['shapiro_pvalue']:.4f}"
        ax.text(0.05, 0.95, test_text, transform=ax.transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.set_xlabel('Theoretical Quantiles', fontsize=12)
    ax.set_ylabel('Sample Quantiles', fontsize=12)
    ax.set_title('Q-Q Plot for Normality Assessment', fontsize=14, weight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_confidence_interval_comparison(
    intervals_df: pd.DataFrame,
    output_dir: str = None,
    filename: str = 'ci_comparison.png'
) -> plt.Figure:
    """
    Compare different confidence interval methods.

    Parameters
    ----------
    intervals_df : pd.DataFrame
        DataFrame with columns: method, estimate, ci_lower, ci_upper
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    methods = intervals_df['method'].values
    estimates = intervals_df['estimate'].values
    ci_lower = intervals_df['ci_lower'].values
    ci_upper = intervals_df['ci_upper'].values

    y_pos = np.arange(len(methods))

    # Plot intervals
    for i, (est, lower, upper, method) in enumerate(zip(estimates, ci_lower, ci_upper, methods)):
        ax.plot([lower, upper], [i, i], 'o-', linewidth=2, markersize=8, label=method)
        ax.plot(est, i, 'rs', markersize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    ax.set_xlabel('Estimate Value', fontsize=12)
    ax.set_title('Confidence Interval Method Comparison', fontsize=14, weight='bold')
    ax.grid(axis='x', alpha=0.3)
    ax.legend(['Point Estimate'], loc='best')

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig


def plot_sensitivity_heatmap(
    sensitivity_df: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    output_dir: str = None,
    filename: str = 'sensitivity_heatmap.png'
) -> plt.Figure:
    """
    Create heatmap for sensitivity analysis.

    Parameters
    ----------
    sensitivity_df : pd.DataFrame
        Sensitivity analysis results
    x_col : str
        Column for x-axis
    y_col : str
        Column for y-axis
    value_col : str
        Column for heatmap values
    output_dir : str, optional
        Directory to save figure
    filename : str
        Output filename

    Returns
    -------
    plt.Figure
        The created figure
    """
    set_publication_style()

    pivot_table = sensitivity_df.pivot(index=y_col, columns=x_col, values=value_col)

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(pivot_table, annot=True, fmt='.3f', cmap='RdYlGn_r',
                cbar_kws={'label': value_col}, ax=ax, linewidths=0.5)

    ax.set_title(f'Sensitivity Analysis: {value_col}', fontsize=14, weight='bold')
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)

    if output_dir:
        save_figure(fig, filename, output_dir)

    return fig
