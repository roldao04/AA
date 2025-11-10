#!/usr/bin/env python3
"""
Create Figure 2: Solution quality distribution for greedy heuristic.

Shows histogram of quality ratios and percentage of optimal solutions found.

Author: João Manuel Vieira Roldão (113920)
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuration
INPUT_CSV = "results/exponential_targeted_20251109_235611/exponential_results.csv"
OUTPUT_DIR = "results"
OUTPUT_FILENAME = "figure_2_quality_distribution.png"


def load_quality_data(csv_path):
    """
    Load quality data from CSV file.

    Args:
        csv_path: Path to CSV file

    Returns:
        Tuple of (quality_ratios, is_optimal_list, total_count, optimal_count)
    """
    print(f"Loading data from: {csv_path}")

    quality_ratios = []
    is_optimal_list = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include rows where we can compare greedy to optimal
            if row.get('is_optimal') in ['True', 'False']:
                is_optimal_list.append(row['is_optimal'] == 'True')

                # Get quality ratio
                if row.get('quality_ratio'):
                    quality_ratios.append(float(row['quality_ratio']))

    total_count = len(is_optimal_list)
    optimal_count = sum(is_optimal_list)

    print(f"\nData loaded:")
    print(f"  Total comparisons: {total_count}")
    print(f"  Greedy found optimal: {optimal_count}")
    print(f"  Optimal rate: {100*optimal_count/total_count:.1f}%")
    print(f"  Quality ratios collected: {len(quality_ratios)}")

    return quality_ratios, is_optimal_list, total_count, optimal_count


def create_quality_figure(quality_ratios, is_optimal_list, total_count, optimal_count, output_path):
    """
    Create quality distribution figure.

    Args:
        quality_ratios: List of quality ratios
        is_optimal_list: List of boolean optimal flags
        total_count: Total number of comparisons
        optimal_count: Number of optimal solutions
        output_path: Path to save figure
    """
    print("\nCreating figure...")

    # Calculate statistics
    optimal_rate = 100 * optimal_count / total_count
    suboptimal_count = total_count - optimal_count
    suboptimal_rate = 100 - optimal_rate
    mean_quality = np.mean(quality_ratios)
    min_quality = np.min(quality_ratios)
    max_quality = np.max(quality_ratios)

    # Set up figure style
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # ===== LEFT PANEL: Histogram of quality ratios =====
    bins = np.arange(0.65, 1.05, 0.05)  # Bins from 0.65 to 1.0 in 0.05 steps
    counts, bin_edges, patches = ax1.hist(quality_ratios, bins=bins,
                                          edgecolor='black',
                                          alpha=0.7,
                                          color='steelblue')

    # Color the optimal bin (1.0) differently
    for i, patch in enumerate(patches):
        if bin_edges[i] >= 0.95:  # The 1.0 bin
            patch.set_facecolor('#2ca02c')  # Green for optimal
            patch.set_alpha(0.8)

    ax1.set_xlabel('Quality Ratio (Optimal Size / Greedy Size)', fontsize=11)
    ax1.set_ylabel('Frequency (Number of Cases)', fontsize=11)
    ax1.set_title('Distribution of Greedy Solution Quality', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_xlim(0.65, 1.05)

    # Add statistics text box
    stats_text = f'Statistics:\n'
    stats_text += f'Mean: {mean_quality:.3f}\n'
    stats_text += f'Min: {min_quality:.3f}\n'
    stats_text += f'Max: {max_quality:.3f}\n'
    stats_text += f'Optimal: {optimal_count}/{total_count}'

    ax1.text(0.02, 0.98, stats_text,
             transform=ax1.transAxes,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=9,
             family='monospace')

    # ===== RIGHT PANEL: Optimal vs Suboptimal bar chart =====
    categories = ['Optimal\n(Quality = 1.0)', 'Suboptimal\n(Quality < 1.0)']
    counts_bar = [optimal_count, suboptimal_count]
    percentages = [optimal_rate, suboptimal_rate]
    colors_bar = ['#2ca02c', '#ff7f0e']  # Green for optimal, orange for suboptimal

    bars = ax2.bar(categories, counts_bar, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=1.5)

    ax2.set_ylabel('Number of Cases', fontsize=11)
    ax2.set_title('Greedy Heuristic: Optimal Solution Rate', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add percentage labels on bars
    for bar, count, pct in zip(bars, counts_bar, percentages):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({pct:.1f}%)',
                ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    # Add horizontal line at 50%
    max_y = ax2.get_ylim()[1]
    ax2.axhline(y=total_count/2, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax2.text(1.02, total_count/2, '50%',
             transform=ax2.get_yaxis_transform(),
             fontsize=8, color='gray')

    # Add summary text
    summary_text = f'Total cases: {total_count}\n'
    summary_text += f'Optimal rate: {optimal_rate:.1f}%\n'
    summary_text += f'Mean quality: {mean_quality:.3f}'

    ax2.text(0.5, 0.02, summary_text,
             transform=ax2.transAxes,
             ha='center',
             va='bottom',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3),
             fontsize=9,
             family='monospace')

    plt.tight_layout()

    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure saved: {output_path}")
    print(f"\nKey findings:")
    print(f"  - {optimal_rate:.1f}% of greedy solutions are optimal")
    print(f"  - Mean quality ratio: {mean_quality:.3f}")
    print(f"  - Quality range: {min_quality:.3f} - {max_quality:.3f}")


def main():
    """Main execution function."""
    print("="*70)
    print("CREATING FIGURE 2: Greedy Solution Quality Distribution")
    print("="*70)

    # Check if input file exists
    input_path = Path(INPUT_CSV)
    if not input_path.exists():
        print(f"\nERROR: Input file not found: {input_path}")
        print("Please check the path and try again.")
        return

    # Load quality data
    quality_ratios, is_optimal_list, total_count, optimal_count = load_quality_data(input_path)

    if total_count == 0:
        print("\nERROR: No valid data found in CSV file.")
        return

    # Create output directory if needed
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Create and save figure
    output_path = output_dir / OUTPUT_FILENAME
    create_quality_figure(quality_ratios, is_optimal_list, total_count, optimal_count, output_path)

    print("\n" + "="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\nFigure 2 saved to: {output_path}")
    print("\nThis figure shows:")
    print("  - LEFT: Histogram of quality ratio distribution")
    print("  - RIGHT: Bar chart showing optimal vs suboptimal rates")
    print("\nYou can now use this figure in your report as Figure 2.")


if __name__ == "__main__":
    main()
