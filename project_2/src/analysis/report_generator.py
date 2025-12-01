"""
Report generator module - Creates all tables and figures for 8-page report.

Runs all visualization and analysis scripts to produce report-ready materials.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analysis.visualizations import generate_all_visualizations
from src.analysis.statistical_analysis import run_all_analyses
from src.analysis.complexity_validation import generate_complexity_validation_report
import pandas as pd


def generate_full_report_package(results_csv='results/overnight/both_final_results.csv'):
    """
    Generate complete report package:
    - 6 figures (PDF)
    - 6+ LaTeX tables
    - Key findings JSON
    - Executive summary

    Args:
        results_csv: Path to results CSV file
    """
    print("="*70)
    print("GENERATING COMPLETE REPORT PACKAGE")
    print("="*70)
    print()

    # Load data
    print(f"Loading data from: {results_csv}")
    df = pd.read_csv(results_csv)
    print(f"  ✓ Loaded {len(df)} trials from {df['graph_name'].nunique()} graphs")
    print()

    # Step 1: Generate all visualizations
    print("STEP 1: Generating visualizations...")
    print("-" * 70)
    generate_all_visualizations(results_csv, output_dir='figures')
    print()

    # Step 2: Run all statistical analyses
    print("STEP 2: Running statistical analyses...")
    print("-" * 70)
    run_all_analyses(results_csv)
    print()

    # Step 3: Generate complexity validation
    print("STEP 3: Complexity validation...")
    print("-" * 70)
    generate_complexity_validation_report(df)
    print()

    # Step 4: Generate executive summary
    print("STEP 4: Generating executive summary...")
    print("-" * 70)
    generate_executive_summary(df)
    print()

    # Summary
    print("="*70)
    print("✅ COMPLETE REPORT PACKAGE GENERATED")
    print("="*70)
    print()
    print("Generated files:")
    print("  Figures (6 PDFs):")
    print("    - figures/01_runtime_vs_size.pdf")
    print("    - figures/02_quality_comparison.pdf")
    print("    - figures/03_approximation_ratios.pdf")
    print("    - figures/04_scalability_limits.pdf")
    print("    - figures/05_density_impact.pdf")
    print("    - figures/06_pareto_frontier.pdf")
    print()
    print("  Tables (6+ LaTeX files):")
    print("    - tables/summary_statistics.tex")
    print("    - tables/complexity_validation.tex")
    print("    - tables/scalability_analysis.tex")
    print("    - tables/approximation_ratios.tex")
    print("    - tables/time_estimation.tex")
    print("    - tables/statistical_tests.tex")
    print()
    print("  Report Data:")
    print("    - report_data/key_findings.json")
    print("    - report_data/executive_summary.txt")
    print()
    print("="*70)
    print("Ready for report writing!")
    print("="*70)


def generate_executive_summary(df, output_path='report_data/executive_summary.txt'):
    """
    Generate executive summary text for report introduction.

    Args:
        df: Results DataFrame
        output_path: Where to save summary
    """
    total_trials = len(df)
    total_graphs = df['graph_name'].nunique()
    total_algos = df['algorithm'].nunique()
    success_rate = (df['success'].sum() / len(df)) * 100

    largest_graph = df.loc[df['vertices'].idxmax()]

    # Generate summary text
    summary_lines = []
    summary_lines.append("EXECUTIVE SUMMARY")
    summary_lines.append("=" * 70)
    summary_lines.append("")
    summary_lines.append(f"This report presents a comprehensive empirical evaluation of {total_algos} ")
    summary_lines.append(f"edge cover algorithms across {total_graphs} graph instances, comprising ")
    summary_lines.append(f"{total_trials} total experimental trials.")
    summary_lines.append("")
    summary_lines.append("KEY ACHIEVEMENTS:")
    summary_lines.append(f"  • {success_rate:.1f}% success rate across all trials")
    summary_lines.append(f"  • Largest graph processed: {largest_graph['graph_name']} ")
    summary_lines.append(f"    ({int(largest_graph['vertices']):,} vertices, {int(largest_graph['edges']):,} edges)")
    summary_lines.append(f"  • Full density spectrum coverage: {df['density'].min():.6f} to {df['density'].max():.6f}")
    summary_lines.append("")
    summary_lines.append("ALGORITHM RANKINGS:")

    # Quality ranking
    quality_ranking = df.groupby('algorithm')['cover_size'].mean().sort_values()
    summary_lines.append("  Quality (smaller is better):")
    for idx, (algo, size) in enumerate(quality_ranking.items(), 1):
        summary_lines.append(f"    {idx}. {algo}: {size:.2f} (average cover size)")

    summary_lines.append("")

    # Speed ranking
    speed_ranking = df.groupby('algorithm')['runtime'].mean().sort_values()
    summary_lines.append("  Speed (smaller is better):")
    for idx, (algo, time) in enumerate(speed_ranking.items(), 1):
        summary_lines.append(f"    {idx}. {algo}: {time:.4f}s (average runtime)")

    summary_lines.append("")
    summary_lines.append("="*70)

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(summary_lines))

    print(f"✓ Executive summary saved to {output_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        results_csv = sys.argv[1]
    else:
        results_csv = 'results/overnight/both_final_results.csv'

    generate_full_report_package(results_csv)
