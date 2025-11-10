#!/usr/bin/env python3
"""
Create clean Figure 1: Execution time vs vertices with mean values.

This script creates a publication-ready figure showing execution time vs number
of vertices for Exhaustive Search and Greedy Heuristic algorithms, with mean
values averaged across repetitions for each (vertices, density) combination.

Author: João Manuel Vieira Roldão (113920)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import defaultdict

# Configuration
INPUT_CSV = "results/matching_targeted_20251110_000253/matching_results.csv"
OUTPUT_DIR = "results"
OUTPUT_FILENAME = "figure_1_time_vs_vertices_clean.png"

# Densities to include
DENSITIES = [12.5, 25.0, 50.0, 75.0]

# Colors for each density
DENSITY_COLORS = {
    12.5: '#1f77b4',  # Blue
    25.0: '#ff7f0e',  # Orange
    50.0: '#2ca02c',  # Green
    75.0: '#d62728',  # Red
}

def load_and_aggregate_data(csv_path):
    """
    Load CSV data and calculate mean execution times grouped by vertices and density.

    Args:
        csv_path: Path to CSV file

    Returns:
        Dictionary with aggregated data for each algorithm
    """
    print(f"Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)

    print(f"Total rows loaded: {len(df)}")

    # Prepare aggregated data structure
    aggregated = {
        'exhaustive': defaultdict(lambda: defaultdict(list)),
        'greedy': defaultdict(lambda: defaultdict(list))
    }

    # Group data by density and vertices
    for _, row in df.iterrows():
        density = row['edge_density']
        vertices = row['num_vertices']

        # Only include specified densities
        if density not in DENSITIES:
            continue

        # Exhaustive Search
        if not row.get('exhaustive_timed_out', True) and pd.notna(row.get('exhaustive_time')):
            aggregated['exhaustive'][density][vertices].append(row['exhaustive_time'])

        # Greedy Heuristic
        if pd.notna(row.get('greedy_time')):
            aggregated['greedy'][density][vertices].append(row['greedy_time'])

    # Calculate means
    mean_data = {
        'exhaustive': defaultdict(lambda: {'vertices': [], 'times': []}),
        'greedy': defaultdict(lambda: {'vertices': [], 'times': []})
    }

    for alg in ['exhaustive', 'greedy']:
        for density in DENSITIES:
            if density in aggregated[alg]:
                for vertices in sorted(aggregated[alg][density].keys()):
                    times = aggregated[alg][density][vertices]
                    if times:  # Only include if we have data
                        mean_time = np.mean(times)
                        mean_data[alg][density]['vertices'].append(vertices)
                        mean_data[alg][density]['times'].append(mean_time)

    # Print summary
    print("\nData summary:")
    for alg in ['exhaustive', 'greedy']:
        print(f"\n{alg.capitalize()}:")
        for density in DENSITIES:
            n_points = len(mean_data[alg][density]['vertices'])
            if n_points > 0:
                v_range = f"{min(mean_data[alg][density]['vertices'])}-{max(mean_data[alg][density]['vertices'])}"
                print(f"  {density}% density: {n_points} data points (V={v_range})")

    return mean_data


def create_clean_figure(mean_data, output_path):
    """
    Create clean figure with mean execution times.

    Args:
        mean_data: Dictionary with mean aggregated data
        output_path: Path to save the figure
    """
    print("\nCreating figure...")

    # Set up the figure style
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot Exhaustive Search
    for density in DENSITIES:
        data = mean_data['exhaustive'][density]
        if data['vertices']:
            ax1.plot(data['vertices'], data['times'],
                    marker='o',
                    color=DENSITY_COLORS[density],
                    label=f'{density}% density',
                    linewidth=2,
                    markersize=6)

    ax1.set_xlabel('Number of Vertices', fontsize=11)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=11)
    ax1.set_title('Exhaustive Search: Time vs Vertices', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Plot Greedy Heuristic
    for density in DENSITIES:
        data = mean_data['greedy'][density]
        if data['vertices']:
            ax2.plot(data['vertices'], data['times'],
                    marker='s',
                    color=DENSITY_COLORS[density],
                    label=f'{density}% density',
                    linewidth=2,
                    markersize=6)

    ax2.set_xlabel('Number of Vertices', fontsize=11)
    ax2.set_ylabel('Execution Time (seconds)', fontsize=11)
    ax2.set_title('Greedy Heuristic: Time vs Vertices', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')

    plt.tight_layout()

    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure saved: {output_path}")


def main():
    """Main execution function."""
    print("="*70)
    print("CREATING CLEAN FIGURE 1: Time vs Vertices (Mean Values)")
    print("="*70)

    # Check if input file exists
    input_path = Path(INPUT_CSV)
    if not input_path.exists():
        print(f"\nERROR: Input file not found: {input_path}")
        print("Please check the path and try again.")
        return

    # Load and aggregate data
    mean_data = load_and_aggregate_data(input_path)

    # Create output directory if needed
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Create and save figure
    output_path = output_dir / OUTPUT_FILENAME
    create_clean_figure(mean_data, output_path)

    print("\n" + "="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\nClean figure saved to: {output_path}")
    print("\nThis figure shows mean execution times averaged across all")
    print("repetitions for each (vertices, density) combination.")
    print("\nYou can now use this figure in your report as Figure 1.")


if __name__ == "__main__":
    main()
