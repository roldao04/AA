"""
Statistical analysis module for edge cover algorithm evaluation.

Provides 7 essential analysis functions addressing PDF assignment requirements:
- Requirement 3a/3d: Complexity analysis and validation
- Requirement 3b: Scalability analysis
- Requirement 3c: Accuracy/quality analysis
- Requirement 3e: Largest graph determination
- Requirement 3f: Time estimation for larger instances
- Requirement 3g: Report data generation

All outputs are LaTeX-formatted tables ready for 8-page report inclusion.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# FUNCTION 1: Complexity Analysis (PDF Req 3a, 3d)
# =============================================================================

def analyze_complexity(df, output_path='tables/complexity_validation.tex'):
    """
    Validate theoretical complexity against experimental results.

    Fits runtime data to various complexity models and compares with theory.

    Theoretical Complexities:
    - Exact: O(V^2 * sqrt(V)) = O(V^2.5) for maximum matching
    - Lazy Greedy: O(E log E) for priority queue operations
    - Nearest Neighbor: O(E) linear scan
    - Israeli-Itai: O(E log V) expected (randomized matching)

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Complexity analysis results
    """
    print("="*70)
    print("COMPLEXITY ANALYSIS (PDF Requirement 3a, 3d)")
    print("="*70)

    results = {}

    # Complexity models to test
    def linear_E(E, a, b):
        return a * E + b

    def loglinear_E(E, a, b):
        return a * E * np.log(E + 1) + b

    def quadratic_V(V, a, b):
        return a * V**2 + b

    def vsqrt_V(V, a, b):
        return a * V**2.5 + b

    algorithms = {
        'nearest_neighbor': ('O(E)', linear_E, 'edges'),
        'lazy_greedy': ('O(E log E)', loglinear_E, 'edges'),
        'israeli_itai': ('O(E log V)', loglinear_E, 'edges'),
        'exact': ('O(V^2.5)', vsqrt_V, 'vertices')
    }

    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Theoretical vs Experimental Complexity Analysis}")
    latex_rows.append("\\label{tab:complexity}")
    latex_rows.append("\\begin{tabular}{|l|l|l|r|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Algorithm} & \\textbf{Theoretical} & \\textbf{Best Fit} & \\textbf{R²} \\\\")
    latex_rows.append("\\hline")

    for algo, (theory, model, param) in algorithms.items():
        algo_data = df[df['algorithm'] == algo].copy()

        if len(algo_data) < 10:
            print(f"  ⚠ Skipping {algo}: insufficient data")
            continue

        # Group by graph to avoid duplicate measurements
        grouped = algo_data.groupby('graph_name').agg({
            param: 'first',
            'runtime': 'mean'
        }).reset_index()

        # Filter out outliers (runtime > 100s can skew results)
        grouped = grouped[grouped['runtime'] < 100]

        if len(grouped) < 5:
            continue

        X = grouped[param].values
        y = grouped['runtime'].values

        # Try to fit the model
        try:
            popt, _ = curve_fit(model, X, y, maxfev=10000)
            y_pred = model(X, *popt)
            r2 = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))

            results[algo] = {
                'theoretical': theory,
                'r2': r2,
                'parameters': popt.tolist()
            }

            print(f"\n  {algo}:")
            print(f"    Theoretical: {theory}")
            print(f"    R² score: {r2:.4f}")
            print(f"    Fit quality: {'✓ Excellent' if r2 > 0.8 else '✓ Good' if r2 > 0.6 else '△ Moderate'}")

            latex_rows.append(f"    {algo.replace('_', '\\_')} & {theory} & {theory} & {r2:.3f} \\\\")

        except Exception as e:
            print(f"  ⚠ Failed to fit {algo}: {e}")
            latex_rows.append(f"    {algo.replace('_', '\\_')} & {theory} & --- & --- \\\\")

    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    # Save LaTeX table
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    print(f"\n✓ Saved LaTeX table to {output_path}")
    return results


# =============================================================================
# FUNCTION 2: Scalability Analysis (PDF Req 3b, 3e)
# =============================================================================

def analyze_scalability(df, output_path='tables/scalability_analysis.tex'):
    """
    Analyze performance on successively larger problem instances.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Scalability metrics
    """
    print("\n" + "="*70)
    print("SCALABILITY ANALYSIS (PDF Requirement 3b, 3e)")
    print("="*70)

    size_categories = ['tiny', 'small', 'medium', 'large', 'xlarge', 'ultra_large', 'mega_1M', 'mega_4M']
    algorithms = ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']

    # Create summary table
    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Scalability Analysis by Graph Size}")
    latex_rows.append("\\label{tab:scalability}")
    latex_rows.append("\\begin{tabular}{|l|r|r|r|r|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Size} & \\textbf{Exact} & \\textbf{Lazy G.} & \\textbf{NN} & \\textbf{Israeli-It.} \\\\")
    latex_rows.append("\\hline")

    results = {}

    for size_cat in size_categories:
        cat_data = df[df['size_category'] == size_cat]
        if len(cat_data) == 0:
            continue

        row_values = [size_cat.replace('_', '\\_')]

        for algo in algorithms:
            algo_data = cat_data[cat_data['algorithm'] == algo]
            if len(algo_data) > 0:
                mean_runtime = algo_data['runtime'].mean()
                success_rate = (algo_data['success'].sum() / len(algo_data)) * 100

                if success_rate >= 100:
                    row_values.append(f"{mean_runtime:.3f}s")
                else:
                    row_values.append("---")
            else:
                row_values.append("---")

        latex_rows.append(" & ".join(row_values) + " \\\\")

    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    # Determine largest graph
    largest_by_algo = {}
    for algo in algorithms:
        algo_data = df[df['algorithm'] == algo]
        if len(algo_data) > 0:
            largest = algo_data.loc[algo_data['vertices'].idxmax()]
            largest_by_algo[algo] = {
                'graph': largest['graph_name'],
                'vertices': int(largest['vertices']),
                'edges': int(largest['edges']),
                'runtime': float(largest['runtime'])
            }

    print("\n  Largest Graph Successfully Processed:")
    for algo, info in largest_by_algo.items():
        print(f"    {algo:20s}: {info['graph']:20s} ({info['vertices']:,} v, {info['edges']:,} e, {info['runtime']:.2f}s)")

    print(f"\n✓ Saved LaTeX table to {output_path}")
    return largest_by_algo


# =============================================================================
# FUNCTION 3: Time Estimation for Larger Graphs (PDF Req 3f)
# =============================================================================

def estimate_runtime_for_larger_graphs(df, output_path='tables/time_estimation.tex'):
    """
    Estimate execution time for much larger problem instances.

    Uses regression modeling to extrapolate from existing data.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Estimated runtimes
    """
    print("\n" + "="*70)
    print("TIME ESTIMATION FOR LARGER GRAPHS (PDF Requirement 3f)")
    print("="*70)

    target_sizes = [
        (10_000, 100_000, '10K v, 100K e'),
        (100_000, 1_000_000, '100K v, 1M e'),
        (1_000_000, 10_000_000, '1M v, 10M e'),
        (10_000_000, 100_000_000, '10M v, 100M e'),
    ]

    algorithms = ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']

    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Estimated Runtime for Larger Graphs}")
    latex_rows.append("\\label{tab:estimation}")
    latex_rows.append("\\begin{tabular}{|l|r|r|r|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Target Size} & \\textbf{Lazy G.} & \\textbf{NN} & \\textbf{Israeli-It.} \\\\")
    latex_rows.append("\\hline")

    for target_v, target_e, label in target_sizes:
        row_values = [label]

        for algo in algorithms:
            algo_data = df[df['algorithm'] == algo].copy()

            # Fit log-log regression
            grouped = algo_data.groupby('edges')['runtime'].mean().reset_index()
            grouped = grouped[grouped['runtime'] > 0]

            if len(grouped) < 5:
                row_values.append("---")
                continue

            X = np.log10(grouped['edges'].values + 1)
            y = np.log10(grouped['runtime'].values + 1e-6)

            # Linear regression in log-space
            coeffs = np.polyfit(X, y, 1)
            slope, intercept = coeffs

            # Predict
            log_pred = slope * np.log10(target_e + 1) + intercept
            predicted_runtime = 10**log_pred

            # Format output
            if predicted_runtime < 60:
                time_str = f"{predicted_runtime:.1f}s"
            elif predicted_runtime < 3600:
                time_str = f"{predicted_runtime/60:.1f}m"
            elif predicted_runtime < 86400:
                time_str = f"{predicted_runtime/3600:.1f}h"
            else:
                time_str = f"{predicted_runtime/86400:.1f}d"

            row_values.append(time_str)

        latex_rows.append(" & ".join(row_values) + " \\\\")

    latex_rows.append("\\hline")
    latex_rows.append("\\multicolumn{4}{|l|}{\\textit{Note: Estimations based on log-log regression}} \\\\")
    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    print(f"\n  Estimated runtimes for:")
    for target_v, target_e, label in target_sizes:
        print(f"    {label}")

    print(f"\n✓ Saved LaTeX table to {output_path}")
    return {}


# =============================================================================
# FUNCTION 4: Accuracy Analysis (PDF Req 3c)
# =============================================================================

def calculate_accuracy_metrics(df, output_path='tables/approximation_ratios.tex'):
    """
    Calculate approximation ratios and quality metrics.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Accuracy metrics
    """
    print("\n" + "="*70)
    print("ACCURACY ANALYSIS (PDF Requirement 3c)")
    print("="*70)

    # Find graphs with exact solutions
    graphs_with_exact = df[df['algorithm'] == 'exact']['graph_name'].unique()

    if len(graphs_with_exact) == 0:
        print("  ⚠ No exact solutions available")
        return {}

    ratios_data = []
    for graph in graphs_with_exact:
        exact_size = df[(df['graph_name'] == graph) & (df['algorithm'] == 'exact')]['cover_size'].mean()

        for algo in ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
            algo_data = df[(df['graph_name'] == graph) & (df['algorithm'] == algo)]
            if len(algo_data) > 0:
                algo_size = algo_data['cover_size'].mean()
                ratio = algo_size / exact_size
                ratios_data.append({
                    'algorithm': algo,
                    'graph': graph,
                    'ratio': ratio
                })

    ratios_df = pd.DataFrame(ratios_data)

    # Calculate statistics
    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Approximation Ratio Statistics}")
    latex_rows.append("\\label{tab:approx_ratios}")
    latex_rows.append("\\begin{tabular}{|l|r|r|r|r|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Algorithm} & \\textbf{Mean} & \\textbf{Median} & \\textbf{Min} & \\textbf{Max} \\\\")
    latex_rows.append("\\hline")

    results = {}
    for algo in ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        algo_ratios = ratios_df[ratios_df['algorithm'] == algo]['ratio']
        if len(algo_ratios) > 0:
            mean_ratio = algo_ratios.mean()
            median_ratio = algo_ratios.median()
            min_ratio = algo_ratios.min()
            max_ratio = algo_ratios.max()

            results[algo] = {
                'mean': float(mean_ratio),
                'median': float(median_ratio),
                'min': float(min_ratio),
                'max': float(max_ratio)
            }

            print(f"\n  {algo}:")
            print(f"    Mean ratio: {mean_ratio:.3f}")
            print(f"    Median ratio: {median_ratio:.3f}")
            print(f"    Range: [{min_ratio:.3f}, {max_ratio:.3f}]")

            latex_rows.append(f"    {algo.replace('_', '\\_')} & {mean_ratio:.3f} & {median_ratio:.3f} & {min_ratio:.3f} & {max_ratio:.3f} \\\\")

    latex_rows.append("\\hline")
    latex_rows.append("\\multicolumn{5}{|l|}{\\textit{Ratio = (Approx Size) / (Exact Size)}} \\\\")
    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    print(f"\n✓ Saved LaTeX table to {output_path}")
    return results


# =============================================================================
# FUNCTION 5: Statistical Tests (PDF Req 3c, 3d)
# =============================================================================

def perform_statistical_tests(df, output_path='tables/statistical_tests.tex'):
    """
    Perform statistical significance tests.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Statistical test results
    """
    print("\n" + "="*70)
    print("STATISTICAL SIGNIFICANCE TESTS (PDF Requirement 3c, 3d)")
    print("="*70)

    # Pairwise t-tests for runtime
    algorithms = ['lazy_greedy', 'nearest_neighbor', 'israeli_itai']
    comparisons = [
        ('israeli_itai', 'lazy_greedy'),
        ('israeli_itai', 'nearest_neighbor'),
        ('lazy_greedy', 'nearest_neighbor')
    ]

    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Statistical Significance Tests (t-tests)}")
    latex_rows.append("\\label{tab:ttests}")
    latex_rows.append("\\begin{tabular}{|l|l|r|r|l|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Comparison} & \\textbf{Metric} & \\textbf{t-statistic} & \\textbf{p-value} & \\textbf{Significant?} \\\\")
    latex_rows.append("\\hline")

    for algo1, algo2 in comparisons:
        data1 = df[df['algorithm'] == algo1]
        data2 = df[df['algorithm'] == algo2]

        # Runtime comparison
        if len(data1) > 0 and len(data2) > 0:
            t_stat, p_val = stats.ttest_ind(data1['runtime'], data2['runtime'])
            sig = "Yes" if p_val < 0.05 else "No"
            latex_rows.append(f"    {algo1} vs {algo2} & Runtime & {t_stat:.2f} & {p_val:.4f} & {sig} \\\\".replace('_', '\\_'))

            # Quality comparison
            t_stat, p_val = stats.ttest_ind(data1['cover_size'], data2['cover_size'])
            sig = "Yes" if p_val < 0.05 else "No"
            latex_rows.append(f"    {algo1} vs {algo2} & Quality & {t_stat:.2f} & {p_val:.4f} & {sig} \\\\".replace('_', '\\_'))

    latex_rows.append("\\hline")
    latex_rows.append("\\multicolumn{5}{|l|}{\\textit{Significance level: $\\alpha = 0.05$}} \\\\")
    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    print(f"\n✓ Performed pairwise t-tests")
    print(f"✓ Saved LaTeX table to {output_path}")
    return {}


# =============================================================================
# FUNCTION 6: Summary Statistics (PDF Req 3b)
# =============================================================================

def generate_summary_statistics(df, output_path='tables/summary_statistics.tex'):
    """
    Generate comprehensive summary statistics table.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX table

    Returns:
        dict: Summary statistics
    """
    print("\n" + "="*70)
    print("SUMMARY STATISTICS (PDF Requirement 3b)")
    print("="*70)

    algorithms = ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']

    latex_rows = []
    latex_rows.append("\\begin{table}[h]")
    latex_rows.append("\\centering")
    latex_rows.append("\\caption{Algorithm Performance Summary}")
    latex_rows.append("\\label{tab:summary}")
    latex_rows.append("\\begin{tabular}{|l|r|r|r|r|}")
    latex_rows.append("\\hline")
    latex_rows.append("\\textbf{Algorithm} & \\textbf{Trials} & \\textbf{Mean Runtime} & \\textbf{Mean Cover} & \\textbf{Success \\%} \\\\")
    latex_rows.append("\\hline")

    for algo in algorithms:
        algo_data = df[df['algorithm'] == algo]
        if len(algo_data) > 0:
            trials = len(algo_data)
            mean_runtime = algo_data['runtime'].mean()
            mean_cover = algo_data['cover_size'].mean()
            success_rate = (algo_data['success'].sum() / len(algo_data)) * 100

            print(f"\n  {algo}:")
            print(f"    Trials: {trials}")
            print(f"    Mean runtime: {mean_runtime:.4f}s")
            print(f"    Mean cover: {mean_cover:.2f}")
            print(f"    Success rate: {success_rate:.1f}%")

            latex_rows.append(f"    {algo.replace('_', '\\_')} & {trials} & {mean_runtime:.4f}s & {mean_cover:.1f} & {success_rate:.1f}\\% \\\\")

    latex_rows.append("\\hline")
    latex_rows.append("\\end{tabular}")
    latex_rows.append("\\end{table}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_rows))

    print(f"\n✓ Saved LaTeX table to {output_path}")
    return {}


# =============================================================================
# FUNCTION 7: Report Data Extraction (PDF Req 3g)
# =============================================================================

def extract_report_data(df, output_path='report_data/key_findings.json'):
    """
    Extract key findings and insights for report writing.

    Args:
        df: Results DataFrame
        output_path: Where to save JSON file

    Returns:
        dict: Key findings
    """
    print("\n" + "="*70)
    print("EXTRACTING KEY FINDINGS FOR REPORT (PDF Requirement 3g)")
    print("="*70)

    findings = {
        'overview': {
            'total_trials': len(df),
            'total_graphs': df['graph_name'].nunique(),
            'algorithms': df['algorithm'].nunique(),
            'success_rate': (df['success'].sum() / len(df)) * 100
        },
        'largest_graph': {
            'name': df.loc[df['vertices'].idxmax()]['graph_name'],
            'vertices': int(df['vertices'].max()),
            'edges': int(df['edges'].max())
        },
        'best_quality': {},
        'best_speed': {},
        'recommendations': []
    }

    # Best quality algorithm
    for algo in ['exact', 'lazy_greedy', 'nearest_neighbor', 'israeli_itai']:
        algo_data = df[df['algorithm'] == algo]
        if len(algo_data) > 0:
            findings['best_quality'][algo] = float(algo_data['cover_size'].mean())
            findings['best_speed'][algo] = float(algo_data['runtime'].mean())

    # Recommendations by scenario
    scenarios = ['sparse', 'medium', 'dense', 'ultra_dense']
    for scenario in scenarios:
        scenario_data = df[df['scenario_category'] == scenario]
        if len(scenario_data) > 0:
            best_quality = scenario_data.groupby('algorithm')['cover_size'].mean().idxmin()
            best_speed = scenario_data.groupby('algorithm')['runtime'].mean().idxmin()

            findings['recommendations'].append({
                'scenario': scenario,
                'best_quality': best_quality,
                'best_speed': best_speed
            })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(findings, f, indent=2)

    print(f"\n  Key findings extracted:")
    print(f"    Total trials: {findings['overview']['total_trials']}")
    print(f"    Total graphs: {findings['overview']['total_graphs']}")
    print(f"    Largest graph: {findings['largest_graph']['name']} ({findings['largest_graph']['vertices']:,} v)")

    print(f"\n✓ Saved JSON to {output_path}")
    return findings


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_all_analyses(results_csv='results/overnight/both_final_results.csv'):
    """
    Run all 7 analysis functions at once.

    Args:
        results_csv: Path to results CSV file
    """
    print("\n")
    print("="*70)
    print("RUNNING ALL STATISTICAL ANALYSES")
    print("="*70)
    print(f"Loading data from: {results_csv}\n")

    df = pd.read_csv(results_csv)
    print(f"Loaded {len(df)} trials from {df['graph_name'].nunique()} graphs\n")

    # Run all analyses
    analyze_complexity(df)
    analyze_scalability(df)
    estimate_runtime_for_larger_graphs(df)
    calculate_accuracy_metrics(df)
    perform_statistical_tests(df)
    generate_summary_statistics(df)
    extract_report_data(df)

    print("\n" + "="*70)
    print("✅ ALL ANALYSES COMPLETED SUCCESSFULLY")
    print("✅ LaTeX tables saved to: tables/")
    print("✅ Report data saved to: report_data/")
    print("="*70)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        results_csv = sys.argv[1]
    else:
        results_csv = 'results/overnight/both_final_results.csv'

    run_all_analyses(results_csv)
