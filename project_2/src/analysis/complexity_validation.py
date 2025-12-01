"""
Detailed complexity validation module.

Provides in-depth analysis comparing theoretical vs experimental complexity
for the 8-page report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


def validate_algorithm_complexity(df, algorithm, theoretical_complexity, output_dir='figures'):
    """
    Validate a single algorithm's complexity against theory.

    Args:
        df: Results DataFrame
        algorithm: Algorithm name
        theoretical_complexity: String description (e.g., "O(E)")
        output_dir: Where to save validation plots

    Returns:
        dict: Validation results with R² scores
    """
    algo_data = df[df['algorithm'] == algorithm].copy()

    if len(algo_data) < 10:
        return {'error': 'Insufficient data'}

    # Group by graph to avoid duplicate trials
    grouped = algo_data.groupby('graph_name').agg({
        'vertices': 'first',
        'edges': 'first',
        'runtime': 'mean'
    }).reset_index()

    # Filter outliers
    grouped = grouped[grouped['runtime'] < 100]

    if len(grouped) < 5:
        return {'error': 'Insufficient non-outlier data'}

    # Test multiple complexity models
    results = {}

    # Model 1: O(E) - Linear in edges
    if 'E' in theoretical_complexity:
        X = grouped['edges'].values
        y = grouped['runtime'].values

        try:
            coeffs = np.polyfit(X, y, 1)
            y_pred = np.polyval(coeffs, X)
            r2_linear = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))
            results['O(E)_linear'] = r2_linear
        except:
            results['O(E)_linear'] = 0.0

    # Model 2: O(E log E)
    if 'log' in theoretical_complexity.lower():
        X = grouped['edges'].values * np.log(grouped['edges'].values + 1)
        y = grouped['runtime'].values

        try:
            coeffs = np.polyfit(X, y, 1)
            y_pred = np.polyval(coeffs, X)
            r2_loglinear = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))
            results['O(E_log_E)'] = r2_loglinear
        except:
            results['O(E_log_E)'] = 0.0

    # Model 3: O(V²) or O(V^2.5)
    if 'V' in theoretical_complexity:
        X = grouped['vertices'].values ** 2
        y = grouped['runtime'].values

        try:
            coeffs = np.polyfit(X, y, 1)
            y_pred = np.polyval(coeffs, X)
            r2_quadratic = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))
            results['O(V^2)'] = r2_quadratic
        except:
            results['O(V^2)'] = 0.0

    results['algorithm'] = algorithm
    results['theoretical'] = theoretical_complexity
    results['data_points'] = len(grouped)

    return results


def generate_complexity_validation_report(df, output_path='tables/complexity_detailed.tex'):
    """
    Generate detailed complexity validation report.

    Args:
        df: Results DataFrame
        output_path: Where to save LaTeX report
    """
    algorithms = {
        'exact': 'O(V^{2.5})',
        'lazy_greedy': 'O(E \\log E)',
        'nearest_neighbor': 'O(E)',
        'israeli_itai': 'O(E \\log V)'
    }

    results = []
    for algo, theory in algorithms.items():
        result = validate_algorithm_complexity(df, algo, theory)
        if 'error' not in result:
            results.append(result)

    # Generate LaTeX report
    latex_lines = []
    latex_lines.append("\\subsection{Complexity Validation}")
    latex_lines.append("\\begin{itemize}")

    for result in results:
        algo = result['algorithm']
        theory = result['theoretical']
        best_model = max(result.items(), key=lambda x: x[1] if isinstance(x[1], float) else 0)

        latex_lines.append(f"\\item \\textbf{{{algo.replace('_', ' ').title()}}}: Theoretical complexity {theory}")
        latex_lines.append(f"      Best fit: {best_model[0]} with R² = {best_model[1]:.3f}")

    latex_lines.append("\\end{itemize}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_lines))

    print(f"✓ Complexity validation report saved to {output_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        results_csv = sys.argv[1]
    else:
        results_csv = 'results/overnight/both_final_results.csv'

    df = pd.read_csv(results_csv)
    generate_complexity_validation_report(df)
