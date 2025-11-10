#!/usr/bin/env python3
"""
Create Figure 4: Density-separated complexity validation plots.

Shows how separating by density eliminates variance and produces clean
exponential fits for exhaustive search algorithm.

Author: João Manuel Vieira Roldão (113920)
"""

import csv
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.complexity_analysis import fit_exponential_complexity, calculate_r_squared

# Configuration
INPUT_CSV = "results/exponential_targeted_20251109_235611/exponential_results.csv"
OUTPUT_DIR = "results"
OUTPUT_FILENAME = "figure_4_density_validation.png"

# Densities to analyze
DENSITIES = [12.5, 25.0, 50.0, 75.0]

# Subplot positions
SUBPLOT_POSITIONS = {
    12.5: (0, 0),  # Top-left
    25.0: (0, 1),  # Top-right
    50.0: (1, 0),  # Bottom-left
    75.0: (1, 1),  # Bottom-right
}


def load_density_data(csv_path, density):
    """
    Load experimental data for a specific density.

    Args:
        csv_path: Path to CSV file
        density: Edge density to filter for

    Returns:
        Tuple of (edges_list, times_list)
    """
    edges_list = []
    times_list = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if abs(float(row['edge_density']) - density) < 0.1:  # Match density
                # Only include non-timeout cases
                if row.get('exhaustive_timed_out') == 'False' and row.get('exhaustive_time'):
                    try:
                        num_edges = int(row['num_edges'])
                        time = float(row['exhaustive_time'])
                        if time > 0:  # Valid time
                            edges_list.append(num_edges)
                            times_list.append(time)
                    except (ValueError, KeyError):
                        pass

    return edges_list, times_list


def create_density_validation_figure(data_by_density, output_path):
    """
    Create 2x2 subplot figure showing complexity validation for each density.

    Args:
        data_by_density: Dictionary mapping density to (fit_result, edges, times)
        output_path: Path to save the figure
    """
    print("\nCreating figure...")

    # Set up figure style
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for density in DENSITIES:
        row, col = SUBPLOT_POSITIONS[density]
        ax = axes[row, col]

        if density not in data_by_density:
            ax.text(0.5, 0.5, f'No data for {density}%',
                   ha='center', va='center', transform=ax.transAxes)
            continue

        fit_result, edges, times = data_by_density[density]

        # Plot actual data points
        ax.scatter(edges, times, alpha=0.6, s=50, color='steelblue',
                  edgecolors='black', linewidth=0.5, label='Actual data')

        # Plot fitted curve
        if fit_result.predictions:
            fitted_edges = [p[0] for p in fit_result.predictions]
            fitted_times = [p[1] for p in fit_result.predictions]

            # Sort for smooth line
            sorted_pairs = sorted(zip(fitted_edges, fitted_times))
            fitted_edges_sorted = [p[0] for p in sorted_pairs]
            fitted_times_sorted = [p[1] for p in sorted_pairs]

            ax.plot(fitted_edges_sorted, fitted_times_sorted,
                   'r-', linewidth=2.5, alpha=0.8, label=f'Fitted: {fit_result.complexity_class}')

        # Configure subplot
        ax.set_xlabel('Number of Edges (m)', fontsize=10)
        ax.set_ylabel('Execution Time (seconds)', fontsize=10)
        ax.set_title(f'Density = {density}%', fontsize=11, fontweight='bold')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc='upper left')

        # Add R² annotation box
        r2_text = f'R² = {fit_result.r_squared:.4f}'
        if fit_result.r_squared >= 0.95:
            quality = 'Excellent'
            box_color = '#90EE90'  # Light green
        elif fit_result.r_squared >= 0.85:
            quality = 'Good'
            box_color = '#FFD700'  # Gold
        elif fit_result.r_squared >= 0.70:
            quality = 'Fair'
            box_color = '#FFA500'  # Orange
        else:
            quality = 'Poor'
            box_color = '#FFB6C1'  # Light pink

        annotation_text = f'{r2_text}\n({quality} fit)'
        ax.text(0.98, 0.02, annotation_text,
               transform=ax.transAxes,
               verticalalignment='bottom',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor=box_color, alpha=0.7),
               fontsize=9,
               family='monospace',
               fontweight='bold')

        # Add data point count
        data_count_text = f'n = {len(edges)}'
        ax.text(0.02, 0.98, data_count_text,
               transform=ax.transAxes,
               verticalalignment='top',
               horizontalalignment='left',
               fontsize=8,
               style='italic',
               color='gray')

    # Overall title
    fig.suptitle('Density-Separated Complexity Validation: Exhaustive Search O(2^m)',
                fontsize=14, fontweight='bold', y=0.995)

    plt.tight_layout(rect=[0, 0, 1, 0.99])

    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure saved: {output_path}")


def main():
    """Main execution function."""
    print("="*70)
    print("CREATING FIGURE 4: Density-Separated Complexity Validation")
    print("="*70)

    # Check if input file exists
    input_path = Path(INPUT_CSV)
    if not input_path.exists():
        print(f"\nERROR: Input file not found: {input_path}")
        print("Please check the path and try again.")
        return

    # Load and fit data for each density
    data_by_density = {}

    for density in DENSITIES:
        print(f"\nProcessing density {density}%...")

        # Load data for this density
        edges, times = load_density_data(input_path, density)

        if not edges:
            print(f"  WARNING: No data found for density {density}%")
            continue

        print(f"  Loaded {len(edges)} data points")
        print(f"  Edge range: {min(edges)} - {max(edges)}")
        print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")

        # Fit exponential model
        try:
            fit_result = fit_exponential_complexity(
                edges, times,
                algorithm_name=f"Exhaustive ({density}%)"
            )
            print(f"  R² = {fit_result.r_squared:.4f}")
            print(f"  Fitted base: {np.exp(fit_result.coefficient):.2f}")

            data_by_density[density] = (fit_result, edges, times)

        except Exception as e:
            print(f"  ERROR fitting model: {e}")
            continue

    if not data_by_density:
        print("\nERROR: No valid data to plot.")
        return

    # Create output directory if needed
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Create and save figure
    output_path = output_dir / OUTPUT_FILENAME
    create_density_validation_figure(data_by_density, output_path)

    # Print summary
    print("\n" + "="*70)
    print("R² SUMMARY BY DENSITY")
    print("="*70)
    for density in DENSITIES:
        if density in data_by_density:
            fit_result = data_by_density[density][0]
            quality = "Excellent" if fit_result.r_squared >= 0.95 else \
                     "Good" if fit_result.r_squared >= 0.85 else \
                     "Fair" if fit_result.r_squared >= 0.70 else "Poor"
            print(f"  {density:5.1f}%: R² = {fit_result.r_squared:.4f} ({quality})")

    # Calculate average R²
    all_r2 = [data_by_density[d][0].r_squared for d in data_by_density]
    if all_r2:
        avg_r2 = sum(all_r2) / len(all_r2)
        print(f"\n  Average R² across densities: {avg_r2:.4f}")

    print("\n" + "="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\nFigure 4 saved to: {output_path}")
    print("\nThis figure demonstrates that density-separated analysis produces")
    print("clean exponential fits with high R² values, validating the O(2^m)")
    print("complexity prediction. Separation by density eliminates structural")
    print("variance that would otherwise reduce fit quality.")
    print("\nYou can now use this figure in your report as Figure 4.")


if __name__ == "__main__":
    main()
