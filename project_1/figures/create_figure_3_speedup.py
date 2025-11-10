#!/usr/bin/env python3
"""
Create Figure 3: Speedup comparison (Greedy vs Exhaustive) with mean values.

Shows how greedy speedup varies with problem size across different densities.

Author: João Manuel Vieira Roldão (113920)
"""

import csv
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

# Configuration
INPUT_CSV = "results/exponential_targeted_20251109_235611/exponential_results.csv"
OUTPUT_DIR = "results"
OUTPUT_FILENAME = "figure_3_speedup_clean.png"

# Densities to include
DENSITIES = [12.5, 25.0, 50.0, 75.0]

# Colors for each density
DENSITY_COLORS = {
    12.5: '#1f77b4',  # Blue
    25.0: '#ff7f0e',  # Orange
    50.0: '#2ca02c',  # Green
    75.0: '#d62728',  # Red
}


def load_and_aggregate_speedup_data(csv_path):
    """
    Load CSV data and calculate mean speedup grouped by vertices and density.

    Args:
        csv_path: Path to CSV file

    Returns:
        Dictionary with aggregated speedup data
    """
    print(f"Loading data from: {csv_path}")

    # Structure: aggregated[density][vertices] = [speedup_values]
    aggregated = defaultdict(lambda: defaultdict(list))

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            density = float(row['edge_density'])
            vertices = int(row['num_vertices'])

            # Only include specified densities
            if density not in DENSITIES:
                continue

            # Only include rows where we have valid speedup
            if row.get('speedup') and row['speedup'] not in ['', 'None', 'inf']:
                try:
                    speedup = float(row['speedup'])
                    # Filter out unrealistic values (could be from very small times)
                    if speedup > 0 and speedup < 1e6:  # Cap at 1 million
                        aggregated[density][vertices].append(speedup)
                except (ValueError, OverflowError):
                    pass

    # Calculate means
    mean_data = defaultdict(lambda: {'vertices': [], 'speedups': []})

    for density in DENSITIES:
        if density in aggregated:
            for vertices in sorted(aggregated[density].keys()):
                speedups = aggregated[density][vertices]
                if speedups:  # Only include if we have data
                    # Calculate mean
                    mean_speedup = sum(speedups) / len(speedups)
                    mean_data[density]['vertices'].append(vertices)
                    mean_data[density]['speedups'].append(mean_speedup)

    # Print summary
    print("\nSpeedup data summary:")
    total_points = 0
    for density in DENSITIES:
        n_points = len(mean_data[density]['vertices'])
        total_points += n_points
        if n_points > 0:
            v_range = f"{min(mean_data[density]['vertices'])}-{max(mean_data[density]['vertices'])}"
            speedup_range = f"{min(mean_data[density]['speedups']):.1f}-{max(mean_data[density]['speedups']):.1f}"
            print(f"  {density}% density: {n_points} data points (V={v_range}, speedup={speedup_range}×)")

    print(f"\nTotal data points: {total_points}")

    return mean_data


def create_speedup_figure(mean_data, output_path):
    """
    Create clean speedup figure with mean values.

    Args:
        mean_data: Dictionary with mean aggregated data
        output_path: Path to save the figure
    """
    print("\nCreating figure...")

    # Set up the figure style
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot speedup for each density
    for density in DENSITIES:
        data = mean_data[density]
        if data['vertices']:
            ax.plot(data['vertices'], data['speedups'],
                   marker='o',
                   color=DENSITY_COLORS[density],
                   label=f'{density}% density',
                   linewidth=2.5,
                   markersize=8)

    # Add reference lines for speedup magnitudes
    xlim = ax.get_xlim()
    reference_speedups = [10, 100, 1000]
    for ref_speedup in reference_speedups:
        ax.axhline(y=ref_speedup, color='gray', linestyle=':', alpha=0.4, linewidth=1)
        ax.text(xlim[1] * 0.98, ref_speedup * 1.1, f'{ref_speedup}×',
               fontsize=8, color='gray', ha='right', style='italic')

    ax.set_xlabel('Number of Vertices', fontsize=12)
    ax.set_ylabel('Speedup Factor (Exhaustive Time / Greedy Time)', fontsize=12)
    ax.set_title('Speedup: Greedy vs Exhaustive Search', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

    # Set y-axis limits to show the full range nicely
    ax.set_ylim(1, 10000)

    # Add annotation about speedup range
    all_speedups = []
    for density in DENSITIES:
        all_speedups.extend(mean_data[density]['speedups'])

    if all_speedups:
        min_speedup = min(all_speedups)
        max_speedup = max(all_speedups)
        annotation_text = f'Speedup range: {min_speedup:.0f}× to {max_speedup:.0f}×'

        ax.text(0.02, 0.98, annotation_text,
               transform=ax.transAxes,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3),
               fontsize=9,
               family='monospace')

    plt.tight_layout()

    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure saved: {output_path}")

    if all_speedups:
        print(f"\nSpeedup statistics:")
        print(f"  Minimum: {min_speedup:.1f}×")
        print(f"  Maximum: {max_speedup:.1f}×")
        print(f"  Mean: {sum(all_speedups)/len(all_speedups):.1f}×")


def main():
    """Main execution function."""
    print("="*70)
    print("CREATING FIGURE 3: Speedup Comparison (Mean Values)")
    print("="*70)

    # Check if input file exists
    input_path = Path(INPUT_CSV)
    if not input_path.exists():
        print(f"\nERROR: Input file not found: {input_path}")
        print("Please check the path and try again.")
        return

    # Load and aggregate data
    mean_data = load_and_aggregate_speedup_data(input_path)

    # Check if we have data
    has_data = any(mean_data[d]['vertices'] for d in DENSITIES)
    if not has_data:
        print("\nERROR: No valid speedup data found.")
        return

    # Create output directory if needed
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Create and save figure
    output_path = output_dir / OUTPUT_FILENAME
    create_speedup_figure(mean_data, output_path)

    print("\n" + "="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\nClean figure saved to: {output_path}")
    print("\nThis figure shows mean speedup (Exhaustive/Greedy) averaged across")
    print("all repetitions for each (vertices, density) combination.")
    print("\nYou can now use this figure in your report as Figure 3.")
    print("\nNote: Speedup generally decreases with larger graphs because greedy")
    print("      also gets slower (though still much faster than exhaustive).")


if __name__ == "__main__":
    main()
