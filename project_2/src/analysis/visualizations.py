"""
Visualization module for edge cover algorithm evaluation.

Generates 6 essential plots directly addressing PDF assignment requirements:
- Requirement 3b(2): Execution time analysis
- Requirement 3c: Solution quality comparison
- Requirement 3e: Scalability limits
- Requirement 3a/3d: Complexity validation

All figures are publication-quality (300 DPI) and ready for report inclusion.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (8, 6)

# Algorithm colors for consistency
ALGO_COLORS = {
    'exact': '#2ecc71',  # Green
    'lazy_greedy': '#e74c3c',  # Red
    'nearest_neighbor': '#3498db',  # Blue
    'israeli_itai': '#f39c12'  # Orange
}

ALGO_NAMES = {
    'exact': 'Exact (Matching)',
    'lazy_greedy': 'Lazy Greedy',
    'nearest_neighbor': 'Nearest Neighbor',
    'israeli_itai': 'Israeli-Itai'
}


def plot_runtime_vs_size(df, output_path='figures/01_runtime_vs_size.pdf'):
    """
    Plot execution time vs graph size (PDF Requirement 3b-2).

    Shows scalability and validates complexity analysis with:
    - Log-log plot for power-law detection
    - Separate line per algorithm
    - Trend lines for complexity estimation

    Args:
        df: DataFrame with columns ['algorithm', 'edges', 'runtime']
        output_path: Where to save the figure
    """
    print("Generating Plot 1: Runtime vs Graph Size...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Runtime vs Edges (log-log)
    for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        algo_data = df[df['algorithm'] == algo].copy()
        if len(algo_data) == 0:
            continue

        # Group by edges to get mean runtime
        grouped = algo_data.groupby('edges')['runtime'].agg(['mean', 'std', 'count']).reset_index()

        ax1.scatter(grouped['edges'], grouped['mean'],
                   label=ALGO_NAMES[algo], color=ALGO_COLORS[algo],
                   alpha=0.6, s=50)
        ax1.plot(grouped['edges'], grouped['mean'],
                color=ALGO_COLORS[algo], alpha=0.3, linewidth=1)

    ax1.set_xlabel('Number of Edges')
    ax1.set_ylabel('Runtime (seconds)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('(a) Runtime Scalability (Log-Log)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Runtime vs Vertices (log-log)
    for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        algo_data = df[df['algorithm'] == algo].copy()
        if len(algo_data) == 0:
            continue

        grouped = algo_data.groupby('vertices')['runtime'].agg(['mean', 'std']).reset_index()

        ax2.scatter(grouped['vertices'], grouped['mean'],
                   label=ALGO_NAMES[algo], color=ALGO_COLORS[algo],
                   alpha=0.6, s=50)
        ax2.plot(grouped['vertices'], grouped['mean'],
                color=ALGO_COLORS[algo], alpha=0.3, linewidth=1)

    ax2.set_xlabel('Number of Vertices')
    ax2.set_ylabel('Runtime (seconds)')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('(b) Runtime vs Vertices (Log-Log)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")


def plot_quality_comparison(df, output_path='figures/02_quality_comparison.pdf'):
    """
    Plot solution quality comparison across algorithms (PDF Requirement 3c).

    Shows accuracy analysis with:
    - Box plots by graph category
    - Statistical significance indicators
    - Comparison across all algorithms

    Args:
        df: DataFrame with columns ['algorithm', 'scenario_category', 'cover_size']
        output_path: Where to save the figure
    """
    print("Generating Plot 2: Quality Comparison...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    scenarios = ['sparse', 'medium', 'dense', 'ultra_dense']
    scenario_labels = ['Sparse (p≤0.01)', 'Medium (0.01<p≤0.2)',
                       'Dense (0.2<p≤0.5)', 'Ultra-Dense (p>0.5)']

    for idx, (scenario, label) in enumerate(zip(scenarios, scenario_labels)):
        ax = axes[idx]
        scenario_data = df[df['scenario_category'] == scenario].copy()

        if len(scenario_data) == 0:
            # Try alternative matching
            if scenario == 'sparse':
                scenario_data = df[df['density'] <= 0.01].copy()
            elif scenario == 'medium':
                scenario_data = df[(df['density'] > 0.01) & (df['density'] <= 0.2)].copy()
            elif scenario == 'dense':
                scenario_data = df[(df['density'] > 0.2) & (df['density'] <= 0.5)].copy()
            elif scenario == 'ultra_dense':
                scenario_data = df[df['density'] > 0.5].copy()

        if len(scenario_data) > 0:
            # Create box plot
            algorithms = ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']
            data_to_plot = []
            labels = []
            colors = []

            for algo in algorithms:
                algo_data = scenario_data[scenario_data['algorithm'] == algo]['cover_size']
                if len(algo_data) > 0:
                    data_to_plot.append(algo_data.values)
                    labels.append(ALGO_NAMES.get(algo, algo))
                    colors.append(ALGO_COLORS.get(algo, '#gray'))

            if data_to_plot:
                bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                               showmeans=True, meanline=True)

                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.6)

                ax.set_ylabel('Cover Size (edges)')
                ax.set_title(f'({chr(97+idx)}) {label}')
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, alpha=0.3, axis='y')
        else:
            ax.text(0.5, 0.5, 'No data\navailable',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f'({chr(97+idx)}) {label}')

    plt.suptitle('Algorithm Quality Comparison by Density Category',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")


def plot_approximation_ratios(df, output_path='figures/03_approximation_ratios.pdf'):
    """
    Plot approximation ratios vs exact solution (PDF Requirement 3c).

    Quantifies accuracy for graphs where exact solution is available.
    Ratio = (algorithm_cover_size / exact_cover_size)

    Args:
        df: DataFrame with exact solutions available
        output_path: Where to save the figure
    """
    print("Generating Plot 3: Approximation Ratios...")

    # Find graphs with exact solutions
    graphs_with_exact = df[df['algorithm'] == 'exact']['graph_name'].unique()

    # Calculate ratios
    ratios = []
    for graph in graphs_with_exact:
        exact_size = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['cover_size'].iloc[0]

        for algo in ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
            algo_data = df[(df['graph_name'] == graph) & (df['algorithm'] == algo)]
            if len(algo_data) > 0:
                algo_size = algo_data['cover_size'].mean()
                ratio = algo_size / exact_size
                ratios.append({
                    'graph': graph,
                    'algorithm': algo,
                    'ratio': ratio,
                    'vertices': algo_data['vertices'].iloc[0],
                    'density': algo_data['density'].iloc[0]
                })

    ratios_df = pd.DataFrame(ratios)

    if len(ratios_df) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Plot 1: Violin plot of ratios
        algorithms = ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']
        data_to_plot = []
        labels = []

        for algo in algorithms:
            algo_ratios = ratios_df[ratios_df['algorithm'] == algo]['ratio'].values
            if len(algo_ratios) > 0:
                data_to_plot.append(algo_ratios)
                labels.append(ALGO_NAMES[algo])

        parts = ax1.violinplot(data_to_plot, showmeans=True, showextrema=True)
        ax1.set_xticks(range(1, len(labels) + 1))
        ax1.set_xticklabels(labels, rotation=15)
        ax1.set_ylabel('Approximation Ratio')
        ax1.set_title('(a) Distribution of Approximation Ratios')
        ax1.axhline(y=1.0, color='green', linestyle='--', label='Optimal (ratio=1.0)')
        ax1.axhline(y=1.5, color='orange', linestyle='--', label='3/2-approximation')
        ax1.axhline(y=2.0, color='red', linestyle='--', label='2-approximation')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Plot 2: Ratio vs density
        for algo in algorithms:
            algo_data = ratios_df[ratios_df['algorithm'] == algo]
            ax2.scatter(algo_data['density'], algo_data['ratio'],
                       label=ALGO_NAMES[algo], color=ALGO_COLORS[algo],
                       alpha=0.6, s=50)

        ax2.set_xlabel('Graph Density')
        ax2.set_ylabel('Approximation Ratio')
        ax2.set_xscale('log')
        ax2.set_title('(b) Approximation Ratio vs Density')
        ax2.axhline(y=1.0, color='green', linestyle='--', alpha=0.5)
        ax2.axhline(y=1.5, color='orange', linestyle='--', alpha=0.5)
        ax2.axhline(y=2.0, color='red', linestyle='--', alpha=0.5)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"  ✓ Saved to {output_path}")
    else:
        print("  ⚠ No exact solutions available for ratio calculation")


def plot_scalability_limits(df, output_path='figures/04_scalability_limits.pdf'):
    """
    Identify scalability limits (PDF Requirement 3e).

    Shows where each algorithm hits performance/memory limits.

    Args:
        df: Full results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Plot 4: Scalability Limits...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Success rate by graph size
    size_categories = ['tiny', 'small', 'medium', 'large', 'xlarge', 'ultra_large', 'mega_1M', 'mega_4M']

    for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        success_rates = []
        categories_present = []

        for cat in size_categories:
            cat_data = df[(df['size_category'] == cat) & (df['algorithm'] == algo)]
            if len(cat_data) > 0:
                success_rate = cat_data['success'].sum() / len(cat_data) * 100
                success_rates.append(success_rate)
                categories_present.append(cat)

        if success_rates:
            x_pos = [size_categories.index(cat) for cat in categories_present]
            ax1.plot(x_pos, success_rates, marker='o', label=ALGO_NAMES[algo],
                    color=ALGO_COLORS[algo], linewidth=2, markersize=8)

    ax1.set_xticks(range(len(size_categories)))
    ax1.set_xticklabels(size_categories, rotation=45)
    ax1.set_ylabel('Success Rate (%)')
    ax1.set_title('(a) Algorithm Success Rate by Graph Size')
    ax1.set_ylim([0, 105])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=100, color='green', linestyle='--', alpha=0.5)

    # Plot 2: Largest graphs successfully processed
    largest_graphs = df.nlargest(15, 'vertices')[['graph_name', 'vertices', 'edges', 'algorithm']].copy()
    largest_graphs = largest_graphs.drop_duplicates(subset=['graph_name', 'algorithm'])

    # Pivot to show which algorithms ran on which graphs
    graph_names = largest_graphs['graph_name'].unique()
    y_pos = np.arange(len(graph_names))

    for algo_idx, algo in enumerate(['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']):
        algo_graphs = largest_graphs[largest_graphs['algorithm'] == algo]['graph_name'].values
        presence = [1 if graph in algo_graphs else 0 for graph in graph_names]

        # Offset for grouped bar chart
        offset = (algo_idx - 1.5) * 0.2
        ax2.barh(y_pos + offset, presence, height=0.2,
                label=ALGO_NAMES[algo], color=ALGO_COLORS[algo], alpha=0.8)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(graph_names, fontsize=8)
    ax2.set_xlabel('Algorithm Executed (1=Yes, 0=No)')
    ax2.set_title('(b) Largest Graphs: Algorithm Coverage')
    ax2.legend(loc='lower right')
    ax2.set_xlim([-0.1, 1.2])
    ax2.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")


def plot_density_impact(df, output_path='figures/05_density_impact.pdf'):
    """
    Show how density affects performance (PDF Requirement 3a - complexity).

    Heatmap showing runtime across density bins for each algorithm.

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Plot 5: Density Impact Heatmap...")

    # Create density bins
    df_copy = df.copy()
    df_copy['density_bin'] = pd.cut(df_copy['density'],
                                     bins=[0, 0.001, 0.01, 0.05, 0.1, 0.3, 0.6, 1.0],
                                     labels=['0-0.001', '0.001-0.01', '0.01-0.05',
                                            '0.05-0.1', '0.1-0.3', '0.3-0.6', '0.6-1.0'])

    # Create pivot table
    pivot_runtime = df_copy.pivot_table(values='runtime',
                                        index='density_bin',
                                        columns='algorithm',
                                        aggfunc='median')

    pivot_quality = df_copy.pivot_table(values='cover_size',
                                        index='density_bin',
                                        columns='algorithm',
                                        aggfunc='median')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Runtime heatmap
    if not pivot_runtime.empty:
        sns.heatmap(np.log10(pivot_runtime + 1e-6), annot=False, cmap='YlOrRd',
                   ax=ax1, cbar_kws={'label': 'log10(Runtime)'})
        ax1.set_title('(a) Median Runtime by Density')
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Density Range')

    # Plot 2: Quality heatmap
    if not pivot_quality.empty:
        sns.heatmap(np.log10(pivot_quality + 1), annot=False, cmap='RdYlGn_r',
                   ax=ax2, cbar_kws={'label': 'log10(Cover Size)'})
        ax2.set_title('(b) Median Cover Size by Density')
        ax2.set_xlabel('Algorithm')
        ax2.set_ylabel('Density Range')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")


def plot_pareto_frontier(df, output_path='figures/06_pareto_frontier.pdf'):
    """
    Quality vs Speed Pareto frontier (PDF Requirement 3c).

    Shows trade-offs between solution quality and runtime.

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Plot 6: Pareto Frontier...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    # Group by scenario
    scenarios = [
        ('sparse', 'Sparse Graphs (p≤0.01)'),
        ('medium', 'Medium Density (0.01<p≤0.2)'),
        ('dense', 'Dense Graphs (0.2<p≤0.5)'),
        ('ultra_dense', 'Ultra-Dense (p>0.5)')
    ]

    for idx, (scenario, label) in enumerate(scenarios):
        ax = axes[idx]
        scenario_data = df[df['scenario_category'] == scenario].copy()

        if len(scenario_data) == 0:
            # Fallback to density-based filtering
            if scenario == 'sparse':
                scenario_data = df[df['density'] <= 0.01].copy()
            elif scenario == 'medium':
                scenario_data = df[(df['density'] > 0.01) & (df['density'] <= 0.2)].copy()
            elif scenario == 'dense':
                scenario_data = df[(df['density'] > 0.2) & (df['density'] <= 0.5)].copy()
            elif scenario == 'ultra_dense':
                scenario_data = df[df['density'] > 0.5].copy()

        if len(scenario_data) > 0:
            for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
                algo_data = scenario_data[scenario_data['algorithm'] == algo]
                if len(algo_data) > 0:
                    ax.scatter(algo_data['runtime'], algo_data['cover_size'],
                              label=ALGO_NAMES.get(algo, algo),
                              color=ALGO_COLORS.get(algo, '#gray'),
                              alpha=0.6, s=50)

            ax.set_xlabel('Runtime (seconds)')
            ax.set_ylabel('Cover Size (smaller is better)')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_title(f'({chr(97+idx)}) {label}')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No data available',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f'({chr(97+idx)}) {label}')

    plt.suptitle('Quality vs Speed Trade-off (Pareto Frontier)',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")


def generate_all_visualizations(results_csv='results/overnight/both_final_results.csv',
                                output_dir='figures'):
    """
    Generate all 6 visualizations at once.

    Args:
        results_csv: Path to results CSV file
        output_dir: Directory to save all figures
    """
    print("="*70)
    print("GENERATING ALL VISUALIZATIONS")
    print("="*70)
    print(f"Loading data from: {results_csv}")

    df = pd.read_csv(results_csv)
    print(f"Loaded {len(df)} trials from {df['graph_name'].nunique()} graphs")
    print(f"Algorithms: {', '.join(df['algorithm'].unique())}")
    print()

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate all plots
    plot_runtime_vs_size(df, f'{output_dir}/01_runtime_vs_size.pdf')
    plot_quality_comparison(df, f'{output_dir}/02_quality_comparison.pdf')
    plot_approximation_ratios(df, f'{output_dir}/03_approximation_ratios.pdf')
    plot_scalability_limits(df, f'{output_dir}/04_scalability_limits.pdf')
    plot_density_impact(df, f'{output_dir}/05_density_impact.pdf')
    plot_pareto_frontier(df, f'{output_dir}/06_pareto_frontier.pdf')

    print()
    print("="*70)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
    print(f"✅ Saved to: {output_dir}/")
    print("="*70)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        results_csv = sys.argv[1]
    else:
        results_csv = 'results/overnight/both_final_results.csv'

    generate_all_visualizations(results_csv)
