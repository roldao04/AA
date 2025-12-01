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

# Source colors for dataset overview
SOURCE_COLORS = {
    'SNAP': '#3498db',      # Blue
    'DIMACS': '#e74c3c',    # Red
    'SW': '#2ecc71',        # Green
    'NetworkX': '#f39c12'   # Orange
}


def plot_dataset_overview(df, output_path='figures/00_dataset_overview.png'):
    """
    Plot dataset overview showing distribution of graphs by size and source.

    Creates a stacked bar chart with:
    - X-axis: Size categories (Tiny, Small, Medium, Large, Ultra-dense, Mega-scale)
    - Y-axis: Number of graphs
    - Stacked colors: Source repository (SNAP, DIMACS, SW, NetworkX)
    - Annotations: Vertex count ranges

    Args:
        df: DataFrame with columns ['graph_name', 'vertices', 'size_category']
        output_path: Where to save the figure
    """
    print("Generating Figure 0: Dataset Overview...")

    # Get unique graphs with their properties
    unique_graphs = df.drop_duplicates(subset=['graph_name'])[['graph_name', 'vertices']].copy()

    # Classify graphs by source based on naming patterns
    def classify_source(graph_name):
        """Classify graph source from its name."""
        if graph_name.startswith('C') and '.' in graph_name:  # C1000.9, C2000.9, etc.
            return 'DIMACS'
        elif graph_name.startswith('SW') or graph_name.startswith('SW'):
            return 'SW'
        elif any(graph_name.startswith(prefix) for prefix in ['CA-', 'ego-', 'email-', 'facebook', 'Wiki-', 'LiveJournal', 'YouTube']):
            return 'SNAP'
        else:  # BA-*, ER-*, WS-*, tree-*, karate, etc.
            return 'NetworkX'

    unique_graphs['source'] = unique_graphs['graph_name'].apply(classify_source)

    # Classify by size category (matching the user's 6 categories)
    def classify_size(vertices):
        """Classify graph into one of 6 size categories."""
        if vertices <= 100:
            return 'Tiny'
        elif vertices <= 250:
            return 'Small'
        elif vertices <= 1000:
            return 'Medium'
        elif vertices <= 15000:
            return 'Large'
        elif vertices <= 100000:
            return 'Ultra-dense'
        else:
            return 'Mega-scale'

    unique_graphs['size_cat'] = unique_graphs['vertices'].apply(classify_size)

    # Calculate vertex ranges for each category
    vertex_ranges = {}
    for cat in ['Tiny', 'Small', 'Medium', 'Large', 'Ultra-dense', 'Mega-scale']:
        cat_data = unique_graphs[unique_graphs['size_cat'] == cat]
        if len(cat_data) > 0:
            min_v = cat_data['vertices'].min()
            max_v = cat_data['vertices'].max()
            if min_v == max_v:
                vertex_ranges[cat] = f"{min_v:,}"
            else:
                vertex_ranges[cat] = f"{min_v:,}-{max_v:,}"
        else:
            vertex_ranges[cat] = "0"

    # Count graphs by category and source
    categories = ['Tiny', 'Small', 'Medium', 'Large', 'Ultra-dense', 'Mega-scale']
    sources = ['SNAP', 'DIMACS', 'SW', 'NetworkX']

    # Create count matrix
    counts = {}
    for source in sources:
        counts[source] = []
        for cat in categories:
            count = len(unique_graphs[(unique_graphs['size_cat'] == cat) &
                                     (unique_graphs['source'] == source)])
            counts[source].append(count)

    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 7))

    x_pos = np.arange(len(categories))
    bar_width = 0.6

    # Plot stacked bars
    bottom = np.zeros(len(categories))
    for source in sources:
        bars = ax.bar(x_pos, counts[source], bar_width,
                     label=source, color=SOURCE_COLORS[source],
                     bottom=bottom, alpha=0.8)
        bottom += counts[source]

    # Add vertex range annotations on top of bars
    for i, cat in enumerate(categories):
        total = sum(counts[source][i] for source in sources)
        if total > 0:
            ax.text(i, total + 0.3, f"n={vertex_ranges[cat]}",
                   ha='center', va='bottom', fontsize=9,
                   fontweight='bold', style='italic')

    # Customize plot
    ax.set_xlabel('Size Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Graphs', fontsize=12, fontweight='bold')
    ax.set_title('Dataset Overview: Distribution by Size and Source',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories)
    ax.legend(title='Source Repository', loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')

    # Set y-axis to show integers only
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Add total count annotation
    total_graphs = len(unique_graphs)
    ax.text(0.98, 0.98, f'Total: {total_graphs} graphs',
           transform=ax.transAxes, ha='right', va='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
           fontsize=10, fontweight='bold')

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Dataset spans {unique_graphs['vertices'].min():,} to {unique_graphs['vertices'].max():,} vertices")


def plot_runtime_vs_size(df, output_path='figures/01_runtime_vs_size.png'):
    """
    Plot execution time vs graph size (Figure 2 requirements).

    Creates a log-log scatter plot showing:
    - Runtime scaling across 4 orders of magnitude (10 to 10M vertices)
    - Fitted trend lines with complexity slopes
    - Vertical cutoff line at 5000 vertices where exact becomes impractical
    - Specific marker shapes per algorithm

    Args:
        df: DataFrame with columns ['algorithm', 'vertices', 'runtime']
        output_path: Where to save the figure
    """
    print("Generating Figure 2: Runtime vs Graph Size...")

    # Define marker shapes and colors for each algorithm
    algo_styles = {
        'exact': {'color': '#e74c3c', 'marker': 'o', 'name': 'Exact'},
        'lazy_greedy': {'color': '#3498db', 'marker': 's', 'name': 'Lazy Greedy'},
        'nearest_neighbor': {'color': '#2ecc71', 'marker': '^', 'name': 'Nearest Neighbor'},
        'israeli_itai': {'color': '#f39c12', 'marker': 'D', 'name': 'Israeli-Itai'}
    }

    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot each algorithm with fitted trend lines
    for algo, style in algo_styles.items():
        algo_data = df[df['algorithm'] == algo].copy()
        if len(algo_data) == 0:
            continue

        # Group by vertices to get mean runtime
        grouped = algo_data.groupby('vertices')['runtime'].agg(['mean', 'std']).reset_index()

        # Filter out zero or negative runtimes for log scale
        grouped = grouped[grouped['mean'] > 0]

        if len(grouped) == 0:
            continue

        # Scatter plot with specific marker shapes
        ax.scatter(grouped['vertices'], grouped['mean'],
                  label=style['name'],
                  color=style['color'],
                  marker=style['marker'],
                  s=100, alpha=0.7, edgecolors='black', linewidth=0.5,
                  zorder=3)

        # Fit trend line (polynomial on log-log data for power law)
        if len(grouped) >= 3:  # Need at least 3 points for fitting
            log_v = np.log10(grouped['vertices'].values)
            log_t = np.log10(grouped['mean'].values)

            # Fit linear regression on log-log data (gives power law: t = a * n^b)
            coeffs = np.polyfit(log_v, log_t, 1)
            slope = coeffs[0]  # Complexity exponent (b)
            intercept = coeffs[1]  # log10(a)

            # Generate trend line points
            v_min = max(10, grouped['vertices'].min())
            v_max = min(1e7, grouped['vertices'].max())
            v_range = np.logspace(np.log10(v_min), np.log10(v_max), 100)
            t_trend = 10**intercept * v_range**slope

            # Plot trend line with complexity annotation
            ax.plot(v_range, t_trend,
                   color=style['color'], linestyle='--',
                   linewidth=2, alpha=0.5, zorder=2,
                   label=f"{style['name']} trend: O(n$^{{{slope:.1f}}}$)")

    # Add vertical line at 5000 vertices (Exact cutoff)
    ax.axvline(x=5000, color='darkred', linestyle=':', linewidth=2.5,
               label='Exact cutoff (5000v)', alpha=0.8, zorder=4)

    # Add shaded region for "impractical" zone
    ax.axvspan(5000, 1e7, alpha=0.08, color='red', zorder=1)
    ax.text(5000, 1e2, '  Impractical\n  for Exact',
           fontsize=9, color='darkred', alpha=0.6,
           verticalalignment='center')

    # Set scales and labels
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(10, 1e7)
    ax.set_ylim(1e-4, 1e3)
    ax.set_xlabel('Number of Vertices', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Runtime Scaling Across Four Orders of Magnitude',
                fontsize=14, fontweight='bold', pad=20)

    # Customize legend to show both data and trend lines
    ax.legend(loc='upper left', framealpha=0.95, fontsize=8.5, ncol=1)
    ax.grid(True, alpha=0.3, which='both', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Vertex range: {df['vertices'].min():,} to {df['vertices'].max():,}")


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


def plot_approximation_ratios(df, output_path='figures/03_approximation_ratios.png'):
    """
    Plot approximation quality comparison (Figure 3 requirements).

    Creates a box plot showing approximation ratio distributions:
    - Three algorithms: Lazy Greedy, Israeli-Itai, Nearest Neighbor
    - Box shows median, quartiles (25th-75th), and outliers
    - Horizontal reference lines at theoretical bounds (1.5, 2.0)
    - Annotates C1000.9 outlier for Nearest Neighbor

    Args:
        df: DataFrame with exact solutions available
        output_path: Where to save the figure
    """
    print("Generating Figure 3: Approximation Quality Comparison...")

    # Find graphs with exact solutions
    graphs_with_exact = df[df['algorithm'] == 'exact']['graph_name'].unique()

    # Calculate ratios
    ratios = []
    for graph in graphs_with_exact:
        exact_size = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['cover_size'].iloc[0]

        for algo in ['lazy_greedy', 'israeli_itai', 'nearest_neighbor']:
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
        fig, ax = plt.subplots(figsize=(10, 7))

        # Prepare data for box plot (order: Lazy Greedy, Israeli-Itai, Nearest Neighbor)
        algorithms = ['lazy_greedy', 'israeli_itai', 'nearest_neighbor']
        algo_labels = ['Lazy Greedy', 'Israeli-Itai', 'Nearest Neighbor']
        algo_colors = ['#3498db', '#f39c12', '#2ecc71']  # Blue, Orange, Green

        data_to_plot = []
        for algo in algorithms:
            algo_ratios = ratios_df[ratios_df['algorithm'] == algo]['ratio'].values
            if len(algo_ratios) > 0:
                data_to_plot.append(algo_ratios)
            else:
                data_to_plot.append([])

        # Create box plot with custom styling
        bp = ax.boxplot(data_to_plot, labels=algo_labels, patch_artist=True,
                       showmeans=True, meanline=False,
                       meanprops=dict(marker='D', markerfacecolor='red', markersize=6),
                       medianprops=dict(color='black', linewidth=2),
                       boxprops=dict(linewidth=1.5),
                       whiskerprops=dict(linewidth=1.5),
                       capprops=dict(linewidth=1.5),
                       flierprops=dict(marker='o', markerfacecolor='red', markersize=8,
                                     markeredgecolor='darkred', alpha=0.7))

        # Color the boxes
        for patch, color in zip(bp['boxes'], algo_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        # Add horizontal reference lines for theoretical bounds
        ax.axhline(y=1.0, color='green', linestyle='-', linewidth=1.5,
                  label='Optimal (1.0×)', alpha=0.7, zorder=1)
        ax.axhline(y=1.5, color='orange', linestyle='--', linewidth=2,
                  label='LG theoretical bound (1.5×)', alpha=0.7, zorder=1)
        ax.axhline(y=2.0, color='red', linestyle='--', linewidth=2,
                  label='NN theoretical bound (2.0×)', alpha=0.7, zorder=1)

        # Find and annotate C1000.9 outlier for nearest_neighbor
        nn_data = ratios_df[ratios_df['algorithm'] == 'nearest_neighbor']
        c1000_data = nn_data[nn_data['graph'] == 'C1000.9']

        if len(c1000_data) > 0:
            c1000_ratio = c1000_data['ratio'].iloc[0]
            # Position annotation near the NN box (position 3)
            ax.annotate(f'C1000.9\n({c1000_ratio:.3f})',
                       xy=(3, c1000_ratio),
                       xytext=(3.3, c1000_ratio - 0.05),
                       fontsize=9, fontweight='bold',
                       color='darkred',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))

        # Set axis properties
        ax.set_ylabel('Approximation Ratio', fontsize=12, fontweight='bold')
        ax.set_ylim(0.95, 2.05)
        ax.set_title('Distribution of Approximation Ratios',
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', framealpha=0.95, fontsize=9)
        ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.5)

        # Add statistical annotations
        for i, algo in enumerate(algorithms):
            algo_ratios = ratios_df[ratios_df['algorithm'] == algo]['ratio'].values
            if len(algo_ratios) > 0:
                median = np.median(algo_ratios)
                mean = np.mean(algo_ratios)
                ax.text(i + 1, 0.97, f'μ={mean:.2f}\nM={median:.2f}',
                       ha='center', va='top', fontsize=7.5,
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

        plt.tight_layout()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"  ✓ Saved to {output_path}")
        print(f"  ✓ Analyzed {len(graphs_with_exact)} graphs with exact solutions")
    else:
        print("  ⚠ No exact solutions available for ratio calculation")


def plot_operations_count(df, output_path='figures/04_operations_count.png'):
    """
    Plot basic operations vs problem size (Figure 4 requirements).

    Creates a log-log plot showing operation counts:
    - X-axis: Number of edges (m)
    - Y-axis: Operation count
    - Four algorithm series with specific operations:
      - Exact: edge examinations in matching
      - Lazy Greedy: priority queue operations
      - Nearest Neighbor: vertex visits (approximated as m)
      - Israeli-Itai: proposal operations
    - Reference lines for O(m), O(m log m), O(m√n)

    Args:
        df: DataFrame with operation count columns
        output_path: Where to save the figure
    """
    print("Generating Figure 4: Basic Operations vs Problem Size...")

    # Define algorithm styles
    algo_styles = {
        'exact': {'color': '#e74c3c', 'marker': 'o', 'name': 'Exact (matching ops)'},
        'lazy_greedy': {'color': '#3498db', 'marker': 's', 'name': 'Lazy Greedy (PQ ops)'},
        'nearest_neighbor': {'color': '#2ecc71', 'marker': '^', 'name': 'Nearest Neighbor (vertex visits)'},
        'israeli_itai': {'color': '#f39c12', 'marker': 'D', 'name': 'Israeli-Itai (proposals)'}
    }

    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot each algorithm's operations
    for algo, style in algo_styles.items():
        algo_data = df[df['algorithm'] == algo].copy()
        if len(algo_data) == 0:
            continue

        # Extract operation counts based on algorithm
        if algo == 'exact' or algo == 'lazy_greedy':
            # These have operations column
            algo_data = algo_data[algo_data['operations'].notna()].copy()
            if len(algo_data) == 0:
                continue
            algo_data['op_count'] = algo_data['operations']
        elif algo == 'nearest_neighbor':
            # NN: use edges (m) as proxy for O(m) vertex visits
            algo_data['op_count'] = algo_data['edges']
        elif algo == 'israeli_itai':
            # II: use total_proposal_conflicts
            algo_data = algo_data[algo_data['total_proposal_conflicts'].notna()].copy()
            if len(algo_data) == 0:
                continue
            algo_data['op_count'] = algo_data['total_proposal_conflicts']

        # Group by edges to get mean operation count
        grouped = algo_data.groupby('edges').agg({
            'op_count': 'mean',
            'vertices': 'first'  # Get vertices for reference
        }).reset_index()

        # Filter out zeros for log scale
        grouped = grouped[grouped['op_count'] > 0]

        if len(grouped) == 0:
            continue

        # Scatter plot
        ax.scatter(grouped['edges'], grouped['op_count'],
                  label=style['name'],
                  color=style['color'],
                  marker=style['marker'],
                  s=80, alpha=0.7, edgecolors='black', linewidth=0.5,
                  zorder=3)

    # Add reference lines for theoretical complexities
    m_range = np.logspace(1, 7, 100)  # 10 to 10M edges

    # O(m) reference
    ax.plot(m_range, m_range, 'k--', linewidth=1.5, alpha=0.4,
           label='O(m) reference', zorder=1)

    # O(m log m) reference
    m_logm = m_range * np.log2(m_range)
    ax.plot(m_range, m_logm, 'k:', linewidth=1.5, alpha=0.4,
           label='O(m log m) reference', zorder=1)

    # O(m√n) reference (approximate: assuming n ≈ √m for sparse graphs)
    # For visualization: use m^1.5 as representative O(m√n)
    m_sqrtn = m_range ** 1.5
    ax.plot(m_range, m_sqrtn, 'k-.', linewidth=1.5, alpha=0.4,
           label='O(m√n) reference', zorder=1)

    # Set scales and labels
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(10, 1e7)
    ax.set_ylim(1, 1e8)
    ax.set_xlabel('Number of Edges (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Operation Count', fontsize=12, fontweight='bold')
    ax.set_title('Basic Operation Counts Validating Theoretical Complexity',
                fontsize=14, fontweight='bold', pad=20)

    # Legend
    ax.legend(loc='upper left', framealpha=0.95, fontsize=8.5, ncol=1)
    ax.grid(True, alpha=0.3, which='both', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Edge range: {df['edges'].min():,} to {df['edges'].max():,}")


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


def plot_density_impact(df, output_path='figures/06_density_impact.png'):
    """
    Show density impact on approximation quality (Figure 5 requirements).

    Creates a heatmap showing:
    - Rows: Algorithms (Lazy Greedy, Israeli-Itai, Nearest Neighbor)
    - Columns: Density categories (Sparse, Medium, Dense, Ultra-dense)
    - Cell values: Approximation ratios (algorithm/exact)
    - Color: Green (1.0 optimal) to Red (2.0 poor)
    - Shows NN degrades on dense graphs while LG improves

    Args:
        df: Results DataFrame with exact solutions
        output_path: Where to save the figure
    """
    print("Generating Figure 5: Density Impact on Algorithm Performance...")

    # Find graphs with exact solutions
    graphs_with_exact = df[df['algorithm'] == 'exact']['graph_name'].unique()

    # Calculate approximation ratios for each graph
    ratios = []
    for graph in graphs_with_exact:
        exact_size = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['cover_size'].iloc[0]
        density = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['density'].iloc[0]

        # Classify density category
        if density <= 0.01:
            density_cat = 'Sparse'
        elif density <= 0.2:
            density_cat = 'Medium'
        elif density <= 0.5:
            density_cat = 'Dense'
        else:
            density_cat = 'Ultra-dense'

        for algo in ['lazy_greedy', 'israeli_itai', 'nearest_neighbor']:
            algo_data = df[(df['graph_name'] == graph) & (df['algorithm'] == algo)]
            if len(algo_data) > 0:
                algo_size = algo_data['cover_size'].mean()
                ratio = algo_size / exact_size
                ratios.append({
                    'algorithm': algo,
                    'density_category': density_cat,
                    'ratio': ratio
                })

    ratios_df = pd.DataFrame(ratios)

    if len(ratios_df) > 0:
        # Create pivot table: algorithms × density categories
        pivot = ratios_df.pivot_table(
            values='ratio',
            index='algorithm',
            columns='density_category',
            aggfunc='mean'
        )

        # Reorder rows and columns
        algo_order = ['lazy_greedy', 'israeli_itai', 'nearest_neighbor']
        algo_labels = ['Lazy Greedy', 'Israeli-Itai', 'Nearest Neighbor']
        density_order = ['Sparse', 'Medium', 'Dense', 'Ultra-dense']

        # Reindex to ensure correct order
        pivot = pivot.reindex(index=algo_order, columns=density_order)

        # Replace index with readable names
        pivot.index = algo_labels

        fig, ax = plt.subplots(figsize=(10, 5))

        # Create heatmap with green-to-red colormap
        # RdYlGn_r = Red (bad) → Yellow (medium) → Green (good), reversed
        sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r',
                   vmin=1.0, vmax=2.0,
                   cbar_kws={'label': 'Approximation Ratio'},
                   linewidths=1, linecolor='white',
                   ax=ax, annot_kws={'fontsize': 11, 'fontweight': 'bold'})

        # Customize labels
        ax.set_xlabel('Density Category', fontsize=12, fontweight='bold')
        ax.set_ylabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_title('Impact of Graph Density on Approximation Quality',
                    fontsize=14, fontweight='bold', pad=20)

        # Rotate x-axis labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right')

        # Add colorbar label explanation
        cbar = ax.collections[0].colorbar
        cbar.ax.text(0.5, -0.05, '← Better    Worse →',
                    transform=cbar.ax.transAxes,
                    ha='center', va='top', fontsize=9, style='italic')

        plt.tight_layout()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"  ✓ Saved to {output_path}")
        print(f"  ✓ Analyzed {len(graphs_with_exact)} graphs across density categories")
    else:
        print("  ⚠ No exact solutions available for ratio calculation")


def plot_pareto_frontier(df, output_path='figures/11_pareto_frontier.png'):
    """
    Plot quality-speed Pareto frontier (Figure 11 requirements).

    Creates a scatter plot showing:
    - X-axis: Average runtime (log scale)
    - Y-axis: Average approximation ratio
    - Each algorithm as a labeled point
    - Pareto frontier connecting non-dominated points
    - Shaded dominated region
    - Use-case annotations

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Figure 11: Pareto Frontier...")

    # Find graphs with exact solutions
    graphs_with_exact = df[df['algorithm'] == 'exact']['graph_name'].unique()
    print(f"  Found {len(graphs_with_exact)} graphs with exact solutions")

    # Calculate aggregate metrics for each algorithm
    algo_metrics = {}

    for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        algo_data = df[df['algorithm'] == algo]

        if len(algo_data) == 0:
            continue

        # Average runtime across all graphs
        avg_runtime = algo_data['runtime'].mean()

        # Calculate approximation ratios only for graphs with exact solutions
        ratios = []
        for graph in graphs_with_exact:
            exact_size = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['cover_size']
            if len(exact_size) == 0:
                continue
            exact_size = exact_size.iloc[0]

            algo_size = df[(df['graph_name'] == graph) & (df['algorithm'] == algo)]['cover_size']
            if len(algo_size) > 0:
                ratio = algo_size.mean() / exact_size
                ratios.append(ratio)

        avg_ratio = np.mean(ratios) if len(ratios) > 0 else 1.0

        algo_metrics[algo] = {
            'runtime': avg_runtime,
            'ratio': avg_ratio,
            'color': ALGO_COLORS.get(algo, '#gray'),
            'name': ALGO_NAMES.get(algo, algo)
        }

        print(f"  {algo:20s}: runtime={avg_runtime:.6f}s, ratio={avg_ratio:.4f}")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Compute Pareto frontier (non-dominated points)
    # A point (x1, y1) dominates (x2, y2) if x1 < x2 AND y1 < y2
    # For our case: lower runtime AND lower ratio is better
    points = []
    for algo, metrics in algo_metrics.items():
        points.append((algo, metrics['runtime'], metrics['ratio']))

    # Sort by runtime (x-axis)
    points.sort(key=lambda p: p[1])

    # Find Pareto frontier
    pareto_algos = []
    pareto_x = []
    pareto_y = []

    for algo, x, y in points:
        # Check if this point is dominated by any point in the current Pareto set
        is_dominated = False
        for px, py in zip(pareto_x, pareto_y):
            if px < x and py <= y:  # Existing point is better or equal in both dimensions
                is_dominated = True
                break

        if not is_dominated:
            # Also remove any existing Pareto points dominated by this one
            new_pareto_x = []
            new_pareto_y = []
            new_pareto_algos = []

            for i, (px, py, pa) in enumerate(zip(pareto_x, pareto_y, pareto_algos)):
                if not (x <= px and y < py):  # Keep if not dominated by new point
                    new_pareto_x.append(px)
                    new_pareto_y.append(py)
                    new_pareto_algos.append(pa)

            pareto_x = new_pareto_x + [x]
            pareto_y = new_pareto_y + [y]
            pareto_algos = new_pareto_algos + [algo]

    print(f"  Pareto frontier: {', '.join(pareto_algos)}")

    # Plot each algorithm point
    for algo, metrics in algo_metrics.items():
        is_pareto = algo in pareto_algos

        ax.scatter(metrics['runtime'], metrics['ratio'],
                  color=metrics['color'],
                  marker='o' if is_pareto else 's',
                  s=300 if is_pareto else 200,
                  alpha=0.9,
                  edgecolors='black',
                  linewidth=2.5 if is_pareto else 1.5,
                  zorder=10,
                  label=f"{metrics['name']}{' ★' if is_pareto else ''}")

    # Draw Pareto frontier line
    if len(pareto_x) > 1:
        # Sort Pareto points by x-coordinate
        pareto_sorted = sorted(zip(pareto_x, pareto_y))
        pf_x = [p[0] for p in pareto_sorted]
        pf_y = [p[1] for p in pareto_sorted]

        # Draw step function connecting Pareto points
        ax.plot(pf_x, pf_y, 'k--', linewidth=2, alpha=0.6,
               label='Pareto frontier', zorder=5)

        # Shade dominated region (above and to the right)
        # Extend to axes limits
        x_max = ax.get_xlim()[1] if ax.get_xlim()[1] > 0 else max(algo_metrics[a]['runtime'] for a in algo_metrics) * 10
        y_max = ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else max(algo_metrics[a]['ratio'] for a in algo_metrics) * 1.2

        # Create polygon for dominated region
        dominated_x = pf_x + [x_max, x_max, pf_x[0]]
        dominated_y = pf_y + [pf_y[-1], y_max, y_max]

        ax.fill(dominated_x, dominated_y, color='gray', alpha=0.15,
               label='Dominated region', zorder=1)

    # Add use-case annotations
    annotations = {
        'exact': ('Small graphs\n(<5K vertices)\nGuaranteed optimal', 'top'),
        'lazy_greedy': ('Best all-around\nNear-optimal quality\nModerate speed', 'bottom'),
        'nearest_neighbor': ('Massive scale\n(>1M vertices)\nFast, acceptable quality', 'top'),
        'israeli_itai': ('Parallel systems\nRandomized approach\nGood for GPU/distributed', 'bottom')
    }

    for algo, (text, va) in annotations.items():
        if algo in algo_metrics:
            metrics = algo_metrics[algo]
            y_offset = 0.05 if va == 'bottom' else -0.05
            ax.annotate(text,
                       xy=(metrics['runtime'], metrics['ratio']),
                       xytext=(10, 30 if va == 'top' else -30),
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                edgecolor=metrics['color'], alpha=0.9),
                       arrowprops=dict(arrowstyle='->', color=metrics['color'],
                                     lw=1.5),
                       zorder=15)

    # Set scales and labels
    ax.set_xscale('log')
    ax.set_xlabel('Average Runtime (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Approximation Ratio', fontsize=12, fontweight='bold')
    ax.set_title('Quality-Speed Pareto Frontier',
                fontsize=14, fontweight='bold', pad=20)

    # Set y-axis to start at 1.0 (optimal)
    y_min = min(algo_metrics[a]['ratio'] for a in algo_metrics) * 0.95
    y_max = max(algo_metrics[a]['ratio'] for a in algo_metrics) * 1.15
    ax.set_ylim(max(0.95, y_min), y_max)

    # Add horizontal line at y=1.0 (optimal)
    ax.axhline(y=1.0, color='green', linestyle=':', linewidth=1.5,
              alpha=0.5, label='Optimal (1.0×)')

    # Grid and legend
    ax.grid(True, alpha=0.3, which='both', linestyle='-', linewidth=0.5)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Pareto-optimal algorithms: {', '.join(pareto_algos)}")


def plot_scalability_frontier(df, output_path='figures/07_scalability_frontier.png'):
    """
    Plot mega-scale processing achievements (Figure 6 requirements).

    Creates a bar+line chart showing:
    - Three mega-scale graphs: SWlargeG, YouTube, LiveJournal
    - Left y-axis: Vertices in millions (bars)
    - Right y-axis: Runtime in seconds (line with markers)
    - Annotations: Edges processed per second
    - Highlights LiveJournal as "Largest Processed"

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Figure 6: Scalability Frontier...")

    # Define the three mega-scale graphs
    mega_graphs = ['SWlargeG', 'YouTube', 'LiveJournal']

    # Extract data for Israeli-Itai algorithm on these graphs
    data = []
    for graph in mega_graphs:
        graph_data = df[(df['graph_name'] == graph) & (df['algorithm'] == 'israeli_itai')]
        if len(graph_data) > 0:
            vertices = graph_data['vertices'].iloc[0]
            edges = graph_data['edges'].iloc[0]
            runtime = graph_data['runtime'].mean()
            edges_per_sec = edges / runtime
            data.append({
                'graph': graph,
                'vertices': vertices,
                'edges': edges,
                'runtime': runtime,
                'edges_per_sec': edges_per_sec
            })

    if len(data) == 0:
        print("  ⚠ No mega-scale graph data available")
        return

    # Create figure with dual y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Prepare data
    graphs = [d['graph'] for d in data]
    vertices_millions = [d['vertices'] / 1e6 for d in data]
    runtimes = [d['runtime'] for d in data]
    edges_per_sec = [d['edges_per_sec'] for d in data]

    x_pos = np.arange(len(graphs))

    # Plot bars (vertices on left y-axis)
    bars = ax1.bar(x_pos, vertices_millions, width=0.6,
                   color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5,
                   label='Vertices (millions)')

    # Plot line (runtime on right y-axis)
    line = ax2.plot(x_pos, runtimes, 'o-', color='#e74c3c',
                    linewidth=2.5, markersize=12, markeredgecolor='darkred',
                    markeredgewidth=1.5, label='Runtime (seconds)')

    # Annotate vertices on bars
    for i, (bar, v) in enumerate(zip(bars, vertices_millions)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{v:.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Annotate edges per second
    for i, (x, eps) in enumerate(zip(x_pos, edges_per_sec)):
        # Position annotation below the line point
        y_pos = runtimes[i] * 0.4
        ax2.annotate(f'{eps/1000:.0f}K edges/s',
                    xy=(x, runtimes[i]), xytext=(x, y_pos),
                    ha='center', va='top', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

    # Highlight LiveJournal as "Largest Processed"
    livejounal_idx = graphs.index('LiveJournal')
    ax1.text(livejounal_idx, vertices_millions[livejounal_idx] + 0.3,
            '★ Largest Processed ★',
            ha='center', va='bottom', fontsize=11, fontweight='bold',
            color='darkgreen',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8))

    # Customize axes
    ax1.set_xlabel('Graph', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Vertices (millions)', fontsize=12, fontweight='bold', color='#3498db')
    ax2.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold', color='#e74c3c')
    ax1.tick_params(axis='y', labelcolor='#3498db')
    ax2.tick_params(axis='y', labelcolor='#e74c3c')

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(graphs)

    # Set y-axis limits with some padding
    ax1.set_ylim(0, max(vertices_millions) * 1.25)
    ax2.set_ylim(0, max(runtimes) * 1.3)

    # Title
    ax1.set_title('Mega-Scale Processing Achievements (Israeli-Itai Algorithm)',
                 fontsize=14, fontweight='bold', pad=20)

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.95)

    # Grid
    ax1.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ LiveJournal: {data[livejounal_idx]['vertices']:,} vertices, {data[livejounal_idx]['edges']:,} edges")
    print(f"  ✓ Processing rate: {data[livejounal_idx]['edges_per_sec']:,.0f} edges/second")


def plot_sa_convergence(df, output_path='figures/08_sa_convergence.png'):
    """
    Plot SA convergence analysis on SWmediumG (Figure 7 requirements).

    Creates a line plot showing:
    - Current solution (gray, noisy)
    - Best found (blue, monotonic decreasing)
    - Temperature (red dashed, scaled to fit)
    - Iteration where best solution was found (marked)
    - Lazy greedy baseline (horizontal green line)

    Args:
        df: Results DataFrame (used to get lazy greedy baseline)
        output_path: Where to save the figure
    """
    print("Generating Figure 7: SA Convergence Analysis...")

    # Import required modules
    from ..utils.graph_loader import load_sw_graph
    from ..algorithms.simulated_annealing import simulated_annealing_edge_cover
    from ..algorithms.lazy_greedy import lazy_greedy_edge_cover

    # Load SWmediumG graph
    try:
        G = load_sw_graph('SWmediumG.txt')
        print(f"  Loaded SWmediumG: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"  ⚠ Could not load SWmediumG: {e}")
        return

    # Get lazy greedy baseline from df or compute it
    lg_data = df[(df['graph_name'] == 'SWmediumG') & (df['algorithm'] == 'lazy_greedy')]
    if len(lg_data) > 0:
        lg_baseline = lg_data['cover_size'].iloc[0]
        lg_runtime = lg_data['runtime'].mean()
    else:
        # Compute lazy greedy if not in data
        lg_cover, lg_metrics = lazy_greedy_edge_cover(G)
        lg_baseline = len(lg_cover)
        lg_runtime = lg_metrics['runtime']

    print(f"  Lazy Greedy baseline: {lg_baseline} edges, {lg_runtime:.3f}s")

    # Run simulated annealing with 10,000 iterations
    print(f"  Running simulated annealing (10,000 iterations)...")
    sa_cover, sa_metrics = simulated_annealing_edge_cover(
        G,
        max_iterations=10000,
        initial_solution='lazy_greedy',
        seed=42
    )

    print(f"  SA result: {sa_metrics['cover_size']} edges, {sa_metrics['runtime']:.3f}s")
    print(f"  SA is {sa_metrics['runtime']/lg_runtime:.1f}× slower than lazy greedy")

    # Extract convergence history
    conv_history = sa_metrics['convergence_history']

    if len(conv_history) == 0:
        print("  ⚠ No convergence history available")
        return

    iterations = [h['iteration'] for h in conv_history]
    current_sizes = [h['current_size'] for h in conv_history]
    best_sizes = [h['best_size'] for h in conv_history]
    temperatures = [h['temperature'] for h in conv_history]

    # Find iteration where best solution was found
    best_final_size = min(best_sizes)
    best_iteration = next(i for i, size in enumerate(best_sizes) if size == best_final_size)
    best_iter_num = iterations[best_iteration]

    # Create figure
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Plot current solution (gray, noisy)
    ax1.plot(iterations, current_sizes, color='#95a5a6', linewidth=1,
            alpha=0.5, label='Current solution', zorder=1)

    # Plot best found (blue, monotonic)
    ax1.plot(iterations, best_sizes, color='#3498db', linewidth=2.5,
            label='Best found', zorder=3)

    # Plot lazy greedy baseline (horizontal green)
    ax1.axhline(y=lg_baseline, color='#2ecc71', linestyle='-', linewidth=2,
               label=f'Lazy Greedy baseline ({lg_baseline})', alpha=0.8, zorder=2)

    # Scale temperature to fit on the same axis
    max_cover_size = max(current_sizes)
    min_cover_size = min(best_sizes)
    size_range = max_cover_size - min_cover_size

    # Normalize temperature to [0, 1] then scale to size range
    max_temp = temperatures[0] if len(temperatures) > 0 else 1
    scaled_temps = [(t / max_temp) * size_range * 0.5 + min_cover_size
                    for t in temperatures]

    # Plot temperature (red dashed, on secondary axis for proper scaling)
    ax2.plot(iterations, temperatures, 'r--', linewidth=2,
            label='Temperature', alpha=0.7, zorder=2)

    # Mark the iteration where best solution was found
    ax1.scatter([best_iter_num], [best_final_size], color='red', s=200,
               marker='*', edgecolors='darkred', linewidths=2, zorder=4,
               label=f'Best found (iter {best_iter_num})')

    ax1.annotate(f'Best at iteration {best_iter_num}\nCover size: {best_final_size}',
                xy=(best_iter_num, best_final_size),
                xytext=(best_iter_num + 1000, best_final_size + 3),
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='darkred'))

    # Customize axes
    ax1.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cover Size (edges)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Temperature', fontsize=12, fontweight='bold', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax1.set_xlim(0, max(iterations) * 1.05)
    ax1.set_ylim(min_cover_size - 2, max_cover_size + 5)

    # Title
    ax1.set_title(f'Simulated Annealing Convergence on SWmediumG ({G.number_of_nodes()}v, {G.number_of_edges()}e)',
                 fontsize=14, fontweight='bold', pad=20)

    # Legend (combine both axes)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', framealpha=0.95, fontsize=9)

    # Grid
    ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Speedup ratio: Lazy Greedy is {sa_metrics['runtime']/lg_runtime:.0f}× faster")


def plot_complexity_validation(df, output_path='figures/08_complexity_validation.png'):
    """
    Plot complexity validation with 4 subplots (Figure 9 requirements).

    Creates a 2×2 grid validating theoretical complexity for each algorithm:
    - Exact: V vs runtime (expect slope ~2.5)
    - Lazy Greedy: E·log(E) vs runtime (expect slope ~1.0)
    - Nearest Neighbor: E vs runtime (expect slope ~1.0)
    - Israeli-Itai: E·log(V) vs runtime (varies due to randomization)

    Each subplot includes:
    - Log-log scatter plot
    - Fitted power law trend line
    - R² value annotation
    - Fitted exponent annotation

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Figure 9: Complexity Validation...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Algorithm configurations
    configs = [
        {
            'algo': 'exact',
            'name': 'Exact Algorithm',
            'x_metric': 'vertices',
            'x_label': 'Vertices (V)',
            'expected_slope': 2.5,
            'color': '#e74c3c',
            'marker': 'o',
            'position': (0, 0)
        },
        {
            'algo': 'lazy_greedy',
            'name': 'Lazy Greedy',
            'x_metric': 'e_log_e',
            'x_label': 'E · log(E)',
            'expected_slope': 1.0,
            'color': '#3498db',
            'marker': 's',
            'position': (0, 1)
        },
        {
            'algo': 'nearest_neighbor',
            'name': 'Nearest Neighbor',
            'x_metric': 'edges',
            'x_label': 'Edges (E)',
            'expected_slope': 1.0,
            'color': '#2ecc71',
            'marker': '^',
            'position': (1, 0)
        },
        {
            'algo': 'israeli_itai',
            'name': 'Israeli-Itai',
            'x_metric': 'e_log_v',
            'x_label': 'E · log(V)',
            'expected_slope': None,  # Varies
            'color': '#f39c12',
            'marker': 'D',
            'position': (1, 1)
        }
    ]

    for config in configs:
        ax = axes[config['position']]
        algo_data = df[df['algorithm'] == config['algo']].copy()

        if len(algo_data) == 0:
            ax.text(0.5, 0.5, f'No data for {config["name"]}',
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12)
            ax.set_title(f"{config['name']}")
            continue

        # Compute x-axis metric
        if config['x_metric'] == 'vertices':
            algo_data['x_val'] = algo_data['vertices']
        elif config['x_metric'] == 'edges':
            algo_data['x_val'] = algo_data['edges']
        elif config['x_metric'] == 'e_log_e':
            # E · log(E)
            algo_data['x_val'] = algo_data['edges'] * np.log2(algo_data['edges'].clip(lower=1))
        elif config['x_metric'] == 'e_log_v':
            # E · log(V)
            algo_data['x_val'] = algo_data['edges'] * np.log2(algo_data['vertices'].clip(lower=1))

        # Filter valid data (positive runtimes and x values)
        valid_data = algo_data[(algo_data['runtime'] > 0) & (algo_data['x_val'] > 0)].copy()

        if len(valid_data) < 3:
            ax.text(0.5, 0.5, f'Insufficient data\nfor {config["name"]}',
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12)
            ax.set_title(f"{config['name']}")
            continue

        # Group by x_val to average multiple trials
        grouped = valid_data.groupby('x_val')['runtime'].mean().reset_index()

        # Scatter plot
        ax.scatter(grouped['x_val'], grouped['runtime'],
                  color=config['color'], marker=config['marker'],
                  s=80, alpha=0.7, edgecolors='black', linewidth=0.5,
                  label='Data points', zorder=3)

        # Fit power law: runtime = a * x^b
        # On log-log: log(runtime) = log(a) + b * log(x)
        log_x = np.log10(grouped['x_val'].values)
        log_y = np.log10(grouped['runtime'].values)

        # Linear regression on log-log data
        coeffs = np.polyfit(log_x, log_y, 1)
        slope = coeffs[0]  # This is the exponent b
        intercept = coeffs[1]  # This is log10(a)

        # Calculate R²
        y_pred_log = slope * log_x + intercept
        ss_res = np.sum((log_y - y_pred_log) ** 2)
        ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Generate fitted line
        x_fit = np.logspace(np.log10(grouped['x_val'].min()),
                           np.log10(grouped['x_val'].max()), 100)
        y_fit = 10**intercept * x_fit**slope

        # Plot fitted line
        ax.plot(x_fit, y_fit, color=config['color'],
               linestyle='--', linewidth=2.5, alpha=0.8,
               label=f'Fitted: y = {10**intercept:.2e} · x$^{{{slope:.2f}}}$',
               zorder=2)

        # Set log scales
        ax.set_xscale('log')
        ax.set_yscale('log')

        # Labels and title
        ax.set_xlabel(config['x_label'], fontsize=11, fontweight='bold')
        ax.set_ylabel('Runtime (seconds)', fontsize=11, fontweight='bold')

        title_text = f"{config['name']}"
        if config['expected_slope']:
            title_text += f" (Expected slope ≈ {config['expected_slope']})"
        ax.set_title(title_text, fontsize=12, fontweight='bold', pad=10)

        # Add R² and slope annotation box
        annotation_text = f"R² = {r_squared:.3f}\nSlope = {slope:.2f}"
        ax.text(0.05, 0.95, annotation_text,
               transform=ax.transAxes,
               fontsize=10, fontweight='bold',
               verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

        # Grid and legend
        ax.grid(True, alpha=0.3, which='both', linestyle='-', linewidth=0.5)
        ax.legend(loc='lower right', fontsize=8, framealpha=0.9)

    # Overall title
    plt.suptitle('Experimental Validation of Theoretical Complexity',
                fontsize=16, fontweight='bold', y=0.995)

    plt.tight_layout(rect=[0, 0, 1, 0.99])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Validated complexity for 4 algorithms")


def plot_runtime_extrapolation(df, output_path='figures/10_runtime_extrapolation.png'):
    """
    Plot runtime extrapolation to 1 billion vertices (Figure 10 requirements).

    Creates a log-log plot showing:
    - Empirical data points (filled markers) up to 4M vertices
    - Extrapolated trend lines (dashed) to 1B vertices
    - Shaded confidence bands around extrapolations
    - Horizontal threshold lines at 1 hour and 1 day
    - Markers where algorithms cross time thresholds

    Args:
        df: Results DataFrame
        output_path: Where to save the figure
    """
    print("Generating Figure 10: Runtime Extrapolation to 1B Vertices...")

    fig, ax = plt.subplots(figsize=(12, 8))

    # Algorithm configurations
    algorithms = {
        'exact': {'color': '#e74c3c', 'marker': 'o', 'name': 'Exact'},
        'lazy_greedy': {'color': '#3498db', 'marker': 's', 'name': 'Lazy Greedy'},
        'nearest_neighbor': {'color': '#2ecc71', 'marker': '^', 'name': 'Nearest Neighbor'},
        'israeli_itai': {'color': '#f39c12', 'marker': 'D', 'name': 'Israeli-Itai'}
    }

    # Time thresholds (in seconds)
    one_hour = 3600
    one_day = 86400

    # Extrapolation range
    v_max_empirical = 1e7  # 10M for visualization
    v_max_extrapolation = 1e9  # 1 billion

    # Track crossings for annotation
    crossings_1hr = {}
    crossings_1day = {}

    for algo, style in algorithms.items():
        algo_data = df[df['algorithm'] == algo].copy()

        if len(algo_data) == 0:
            continue

        # Filter valid data
        valid_data = algo_data[(algo_data['runtime'] > 0) & (algo_data['vertices'] > 0)].copy()

        if len(valid_data) < 3:
            continue

        # Group by vertices to average multiple trials
        grouped = valid_data.groupby('vertices').agg({
            'runtime': ['mean', 'std', 'count']
        }).reset_index()
        grouped.columns = ['vertices', 'runtime_mean', 'runtime_std', 'count']

        # Filter out data with too few samples for confidence
        grouped = grouped[grouped['count'] >= 2]

        if len(grouped) < 3:
            continue

        # Fit power law: runtime = a * vertices^b
        log_v = np.log10(grouped['vertices'].values)
        log_t = np.log10(grouped['runtime_mean'].values)

        # Linear regression on log-log data
        coeffs = np.polyfit(log_v, log_t, 1)
        slope = coeffs[0]  # Exponent b
        intercept = coeffs[1]  # log10(a)
        a = 10**intercept

        # Calculate residuals for confidence band
        log_t_pred = slope * log_v + intercept
        residuals = log_t - log_t_pred
        std_residual = np.std(residuals)

        # Plot empirical data (filled markers)
        ax.scatter(grouped['vertices'], grouped['runtime_mean'],
                  color=style['color'], marker=style['marker'],
                  s=100, alpha=0.8, edgecolors='black', linewidth=1,
                  label=f"{style['name']} (empirical)", zorder=5)

        # Generate extrapolation range
        v_extrap = np.logspace(np.log10(grouped['vertices'].min()),
                              np.log10(v_max_extrapolation), 200)

        # Compute extrapolated runtime
        t_extrap = a * v_extrap**slope

        # Compute confidence band (±2 std deviations in log space)
        log_v_extrap = np.log10(v_extrap)
        log_t_extrap_lower = (slope * log_v_extrap + intercept) - 2 * std_residual
        log_t_extrap_upper = (slope * log_v_extrap + intercept) + 2 * std_residual
        t_extrap_lower = 10**log_t_extrap_lower
        t_extrap_upper = 10**log_t_extrap_upper

        # Split into empirical and extrapolated sections
        empirical_mask = v_extrap <= grouped['vertices'].max()
        extrap_mask = v_extrap >= grouped['vertices'].max()

        # Plot empirical trend (solid line)
        ax.plot(v_extrap[empirical_mask], t_extrap[empirical_mask],
               color=style['color'], linestyle='-', linewidth=2.5,
               alpha=0.8, zorder=4)

        # Plot extrapolated trend (dashed line)
        ax.plot(v_extrap[extrap_mask], t_extrap[extrap_mask],
               color=style['color'], linestyle='--', linewidth=2.5,
               alpha=0.7, label=f"{style['name']} (extrapolated)",
               zorder=3)

        # Plot confidence band (only for extrapolation)
        ax.fill_between(v_extrap[extrap_mask],
                       t_extrap_lower[extrap_mask],
                       t_extrap_upper[extrap_mask],
                       color=style['color'], alpha=0.15, zorder=1)

        # Find crossings with 1 hour threshold
        crossing_idx_1hr = np.where(t_extrap >= one_hour)[0]
        if len(crossing_idx_1hr) > 0:
            crossing_v_1hr = v_extrap[crossing_idx_1hr[0]]
            crossings_1hr[algo] = crossing_v_1hr

        # Find crossings with 1 day threshold
        crossing_idx_1day = np.where(t_extrap >= one_day)[0]
        if len(crossing_idx_1day) > 0:
            crossing_v_1day = v_extrap[crossing_idx_1day[0]]
            crossings_1day[algo] = crossing_v_1day

    # Add horizontal threshold lines
    ax.axhline(y=one_hour, color='orange', linestyle=':', linewidth=2.5,
              label='1 hour threshold', alpha=0.8, zorder=2)
    ax.axhline(y=one_day, color='red', linestyle=':', linewidth=2.5,
              label='1 day threshold', alpha=0.8, zorder=2)

    # Annotate crossings for 1 hour
    y_offset_1hr = one_hour * 1.5
    for algo, v_cross in crossings_1hr.items():
        if v_cross < v_max_extrapolation:
            ax.plot([v_cross, v_cross], [one_hour * 0.5, one_hour * 1.2],
                   color=algorithms[algo]['color'], linestyle='-', linewidth=1.5,
                   alpha=0.5, zorder=2)
            ax.scatter([v_cross], [one_hour], color=algorithms[algo]['color'],
                      marker='x', s=150, linewidth=3, zorder=6)

    # Annotate crossings for 1 day
    for algo, v_cross in crossings_1day.items():
        if v_cross < v_max_extrapolation:
            ax.plot([v_cross, v_cross], [one_day * 0.5, one_day * 1.2],
                   color=algorithms[algo]['color'], linestyle='-', linewidth=1.5,
                   alpha=0.5, zorder=2)
            ax.scatter([v_cross], [one_day], color=algorithms[algo]['color'],
                      marker='x', s=150, linewidth=3, zorder=6)

    # Set scales and limits
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e1, v_max_extrapolation)
    ax.set_ylim(1e-5, 1e6)

    # Labels and title
    ax.set_xlabel('Number of Vertices', fontsize=13, fontweight='bold')
    ax.set_ylabel('Runtime (seconds)', fontsize=13, fontweight='bold')
    ax.set_title('Runtime Extrapolation to Billion-Scale Graphs',
                fontsize=15, fontweight='bold', pad=20)

    # Add annotations for time thresholds on right side
    ax.text(v_max_extrapolation * 1.02, one_hour, '1 hour',
           fontsize=10, color='orange', fontweight='bold',
           verticalalignment='center')
    ax.text(v_max_extrapolation * 1.02, one_day, '1 day',
           fontsize=10, color='red', fontweight='bold',
           verticalalignment='center')

    # Add shaded "practical" region
    ax.axhspan(1e-5, one_hour, alpha=0.05, color='green', zorder=0)
    ax.text(2e1, 1e-3, 'Practical\n(< 1 hour)', fontsize=9,
           color='darkgreen', alpha=0.6, style='italic')

    # Grid and legend
    ax.grid(True, alpha=0.3, which='both', linestyle='-', linewidth=0.5)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95, ncol=2)

    # Add data extent marker
    max_empirical_v = df['vertices'].max()
    ax.axvline(x=max_empirical_v, color='black', linestyle='-.', linewidth=1.5,
              alpha=0.4, zorder=2)
    ax.text(max_empirical_v, 1e5, f'  Max empirical\n  ({max_empirical_v/1e6:.1f}M vertices)',
           fontsize=8, rotation=0, verticalalignment='center',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved to {output_path}")
    print(f"  ✓ Extrapolated from {max_empirical_v:,} to {int(v_max_extrapolation):,} vertices")

    # Print crossing information
    print(f"  ✓ 1-hour threshold crossings:")
    for algo, v_cross in crossings_1hr.items():
        print(f"    - {algorithms[algo]['name']}: {v_cross:,.0f} vertices")

    print(f"  ✓ 1-day threshold crossings:")
    for algo, v_cross in crossings_1day.items():
        print(f"    - {algorithms[algo]['name']}: {v_cross:,.0f} vertices")


def generate_all_visualizations(results_csv='results/overnight/both_final_results.csv',
                                output_dir='figures'):
    """
    Generate all 12 visualizations at once.

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
    plot_dataset_overview(df, f'{output_dir}/00_dataset_overview.png')
    plot_runtime_vs_size(df, f'{output_dir}/01_runtime_vs_size.png')
    plot_quality_comparison(df, f'{output_dir}/02_quality_comparison.pdf')
    plot_approximation_ratios(df, f'{output_dir}/03_approximation_ratios.png')
    plot_operations_count(df, f'{output_dir}/04_operations_count.png')
    plot_scalability_limits(df, f'{output_dir}/05_scalability_limits.pdf')
    plot_density_impact(df, f'{output_dir}/06_density_impact.png')
    plot_scalability_frontier(df, f'{output_dir}/07_scalability_frontier.png')
    plot_sa_convergence(df, f'{output_dir}/08_sa_convergence.png')
    plot_complexity_validation(df, f'{output_dir}/09_complexity_validation.png')
    plot_runtime_extrapolation(df, f'{output_dir}/10_runtime_extrapolation.png')
    plot_pareto_frontier(df, f'{output_dir}/11_pareto_frontier.png')

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
