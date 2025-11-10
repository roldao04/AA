#!/usr/bin/env python3
"""
Complexity Validation Script - Experimental vs Theoretical Analysis

This script validates that experimental results match theoretical Big-O predictions
by fitting complexity models and calculating goodness of fit.

Implements PDF Requirement (c): Compare experimental and formal analysis

Student Number: 113920
"""

import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.complexity_analysis import (
    fit_exponential_complexity,
    fit_polynomial_complexity,
    print_complexity_report,
    format_time,
    ComplexityFit
)


def load_results_from_csv(filepath: Path) -> List[Dict]:
    """
    Load experiment results from CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        List of result dictionaries
    """
    results = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            result = {}
            for key, value in row.items():
                if value == '' or value == 'None':
                    result[key] = None
                elif value in ['True', 'False']:
                    result[key] = (value == 'True')
                else:
                    try:
                        # Try int first
                        result[key] = int(value)
                    except ValueError:
                        try:
                            # Then float
                            result[key] = float(value)
                        except ValueError:
                            # Keep as string
                            result[key] = value
            results.append(result)
    return results


def analyze_exhaustive_complexity(results: List[Dict]) -> ComplexityFit:
    """
    Analyze exhaustive search complexity: O(2^m)

    Args:
        results: List of experiment results

    Returns:
        ComplexityFit object
    """
    # Filter results where exhaustive completed
    valid_results = [
        r for r in results
        if not r.get('exhaustive_timed_out', True) and r.get('exhaustive_time') is not None
    ]

    total_results = len(results)
    valid_count = len(valid_results)

    print(f"  Valid data points: {valid_count}/{total_results} ({100*valid_count/total_results:.1f}%)")

    if not valid_results:
        print("  WARNING: No valid exhaustive search results found")
        return None

    edges = [r['num_edges'] for r in valid_results]
    times = [r['exhaustive_time'] for r in valid_results]

    print(f"  Edge range: {min(edges)} - {max(edges)}")
    print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")
    print(f"  Unique edge counts: {len(set(edges))}")

    return fit_exponential_complexity(edges, times, "Exhaustive Search")


def analyze_branch_bound_complexity(results: List[Dict]) -> ComplexityFit:
    """
    Analyze Branch & Bound complexity: O(2^m) with better constants

    Args:
        results: List of experiment results

    Returns:
        ComplexityFit object
    """
    valid_results = [
        r for r in results
        if not r.get('branch_bound_timed_out', True) and r.get('branch_bound_time') is not None
    ]

    total_results = len(results)
    valid_count = len(valid_results)

    print(f"  Valid data points: {valid_count}/{total_results} ({100*valid_count/total_results:.1f}%)")

    if not valid_results:
        print("  WARNING: No valid Branch & Bound results found")
        return None

    edges = [r['num_edges'] for r in valid_results]
    times = [r['branch_bound_time'] for r in valid_results]

    print(f"  Edge range: {min(edges)} - {max(edges)}")
    print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")
    print(f"  Unique edge counts: {len(set(edges))}")

    return fit_exponential_complexity(edges, times, "Branch & Bound")


def analyze_optimal_matching_complexity(results: List[Dict]) -> ComplexityFit:
    """
    Analyze Optimal Matching complexity: O(n^2.5)

    Args:
        results: List of experiment results

    Returns:
        ComplexityFit object
    """
    valid_results = [
        r for r in results
        if not r.get('optimal_matching_failed', True) and r.get('optimal_matching_time') is not None
    ]

    total_results = len(results)
    valid_count = len(valid_results)

    print(f"  Valid data points: {valid_count}/{total_results} ({100*valid_count/total_results:.1f}%)")

    if not valid_results:
        print("  WARNING: No valid Optimal Matching results found")
        return None

    vertices = [r['num_vertices'] for r in valid_results]
    times = [r['optimal_matching_time'] for r in valid_results]

    print(f"  Vertex range: {min(vertices)} - {max(vertices)}")
    print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")
    print(f"  Unique vertex counts: {len(set(vertices))}")

    return fit_polynomial_complexity(vertices, times, degree=2.5, algorithm_name="Optimal Matching")


def analyze_greedy_coverage_complexity(results: List[Dict]) -> ComplexityFit:
    """
    Analyze Greedy Coverage complexity: O(m*n)

    Args:
        results: List of experiment results

    Returns:
        ComplexityFit object
    """
    valid_results = [
        r for r in results
        if r.get('greedy_time') is not None
    ]

    total_results = len(results)
    valid_count = len(valid_results)

    print(f"  Valid data points: {valid_count}/{total_results} ({100*valid_count/total_results:.1f}%)")

    if not valid_results:
        print("  WARNING: No valid Greedy Coverage results found")
        return None

    # Use m*n as the size metric
    sizes = [r['num_edges'] * r['num_vertices'] for r in valid_results]
    times = [r['greedy_time'] for r in valid_results]

    print(f"  Size (m*n) range: {min(sizes)} - {max(sizes)}")
    print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")
    print(f"  Unique sizes: {len(set(sizes))}")

    # Fit as linear in (m*n)
    return fit_polynomial_complexity(sizes, times, degree=1.0, algorithm_name="Greedy Coverage")


def analyze_greedy_matching_complexity(results: List[Dict]) -> ComplexityFit:
    """
    Analyze Greedy Matching complexity: O(m)

    Args:
        results: List of experiment results

    Returns:
        ComplexityFit object
    """
    valid_results = [
        r for r in results
        if r.get('greedy_matching_time') is not None
    ]

    total_results = len(results)
    valid_count = len(valid_results)

    print(f"  Valid data points: {valid_count}/{total_results} ({100*valid_count/total_results:.1f}%)")

    if not valid_results:
        print("  WARNING: No valid Greedy Matching results found")
        return None

    edges = [r['num_edges'] for r in valid_results]
    times = [r['greedy_matching_time'] for r in valid_results]

    print(f"  Edge range: {min(edges)} - {max(edges)}")
    print(f"  Time range: {min(times):.6f}s - {max(times):.6f}s")
    print(f"  Unique edge counts: {len(set(edges))}")

    return fit_polynomial_complexity(edges, times, degree=1.0, algorithm_name="Greedy Matching")


def generate_validation_report(fits: Dict[str, ComplexityFit]) -> None:
    """
    Generate comprehensive validation report.

    Args:
        fits: Dictionary mapping algorithm names to ComplexityFit objects
    """
    print("\n" + "=" * 80)
    print("COMPLEXITY VALIDATION REPORT - Experimental vs Theoretical Analysis")
    print("=" * 80)
    print("\nThis report validates that experimental measurements match theoretical")
    print("Big-O predictions by fitting complexity models and calculating R² values.\n")

    print(f"{'Algorithm':<25} {'Complexity':<15} {'Coefficient':<15} {'R²':<10} {'Fit Quality':<15}")
    print("-" * 80)

    for name, fit in fits.items():
        if fit is None:
            print(f"{name:<25} {'N/A':<15} {'N/A':<15} {'N/A':<10} {'No data':<15}")
            continue

        # Determine fit quality
        if fit.r_squared >= 0.95:
            quality = "Excellent"
        elif fit.r_squared >= 0.85:
            quality = "Good"
        elif fit.r_squared >= 0.70:
            quality = "Fair"
        else:
            quality = "Poor"

        print(f"{name:<25} {fit.complexity_class:<15} {fit.coefficient:<15.2e} {fit.r_squared:<10.4f} {quality:<15}")

    print("-" * 80)
    print("\nR² Interpretation:")
    print("  ≥ 0.95: Excellent fit - experimental data strongly matches theoretical model")
    print("  ≥ 0.85: Good fit - experimental data aligns well with theory")
    print("  ≥ 0.70: Fair fit - experimental data somewhat matches theory")
    print("  < 0.70: Poor fit - experimental data does not match theoretical model well")

    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS BY ALGORITHM")
    print("=" * 80)

    for name, fit in fits.items():
        if fit is not None:
            print_complexity_report(fit)

    print("\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)

    # Count good fits
    good_fits = sum(1 for fit in fits.values() if fit and fit.r_squared >= 0.85)
    total_fits = sum(1 for fit in fits.values() if fit is not None)

    if total_fits > 0:
        percentage = (good_fits / total_fits) * 100
        print(f"\n{good_fits}/{total_fits} algorithms ({percentage:.0f}%) show good or excellent fit (R² ≥ 0.85)")

        if percentage >= 80:
            print("Experimental results STRONGLY VALIDATE theoretical Big-O analysis")
        elif percentage >= 60:
            print("Experimental results VALIDATE theoretical Big-O analysis")
        else:
            print("WARNING:Experimental results show MIXED alignment with theoretical analysis")

    print("\nKey Findings:")
    print("• Exponential algorithms (Exhaustive, B&B) show O(2^m) growth as predicted")
    print("• Polynomial algorithm (Optimal Matching) shows O(n^2.5) growth - scales dramatically better")
    print("• Greedy heuristics show linear/polynomial growth - very fast in practice")
    print("• Branch & Bound has same O(2^m) but lower constant factor than Exhaustive")
    print("\n" + "=" * 80 + "\n")


def analyze_single_density(results: List[Dict], density: float) -> Dict[str, ComplexityFit]:
    """Analyze results filtered to a single density."""
    # Filter to single density (within 0.1% tolerance)
    filtered = [r for r in results if abs(r.get('edge_density', 0) - density) < 0.1]

    if len(filtered) < 5:
        print(f"  WARNING: Not enough data for density {density}% ({len(filtered)} points)")
        return {}

    print(f"\n{'='*80}")
    print(f"DENSITY = {density}% ({len(filtered)} experiments)")
    print('='*80)

    fits = {}

    print("\n1. Exhaustive Search (O(2^m))...")
    try:
        fits['Exhaustive Search'] = analyze_exhaustive_complexity(filtered)
    except Exception as e:
        print(f"  Error: {e}")
        fits['Exhaustive Search'] = None

    print("\n2. Branch & Bound (O(2^m))...")
    try:
        fits['Branch & Bound'] = analyze_branch_bound_complexity(filtered)
    except Exception as e:
        print(f"  Error: {e}")
        fits['Branch & Bound'] = None

    print("\n3. Optimal Matching (O(n^2.5))...")
    try:
        fits['Optimal Matching'] = analyze_optimal_matching_complexity(filtered)
    except Exception as e:
        print(f"  Error: {e}")
        fits['Optimal Matching'] = None

    print("\n4. Greedy Coverage (O(m*n))...")
    try:
        fits['Greedy Coverage'] = analyze_greedy_coverage_complexity(filtered)
    except Exception as e:
        print(f"  Error: {e}")
        fits['Greedy Coverage'] = None

    print("\n5. Greedy Matching (O(m))...")
    try:
        fits['Greedy Matching'] = analyze_greedy_matching_complexity(filtered)
    except Exception as e:
        print(f"  Error: {e}")
        fits['Greedy Matching'] = None

    return fits


def main():
    """Main validation analysis - analyzes each density separately."""
    # Find most recent results file
    results_dir = Path("results")
    if not results_dir.exists():
        print("Error: results/ directory not found")
        print("Please run experiments first: python run_experiments.py")
        sys.exit(1)

    # Look for CSV files
    csv_files = sorted(results_dir.glob("results_*.csv"), reverse=True)
    if not csv_files:
        print("Error: No results files found in results/")
        print("Please run experiments first: python run_experiments.py")
        sys.exit(1)

    results_file = csv_files[0]

    print("=" * 80)
    print("COMPLEXITY VALIDATION - DENSITY-SEPARATED ANALYSIS")
    print("=" * 80)
    print(f"Loading results from: {results_file}\n")

    # Load results
    results = load_results_from_csv(results_file)
    print(f"Loaded {len(results)} experiment results")

    # PDF-required densities
    densities = [12.5, 25.0, 50.0, 75.0]

    # Analyze each density separately
    all_fits = {}
    for density in densities:
        fits = analyze_single_density(results, density)
        if fits:
            all_fits[density] = fits

    # Generate summary table
    print("\n" + "=" * 80)
    print("R² SUMMARY TABLE - ALL DENSITIES")
    print("=" * 80)
    print(f"\n{'Algorithm':<25} {'12.5%':<10} {'25%':<10} {'50%':<10} {'75%':<10} {'Avg R²':<10} {'Status'}")
    print("-" * 80)

    algorithms = ['Exhaustive Search', 'Branch & Bound', 'Optimal Matching', 'Greedy Coverage', 'Greedy Matching']

    for alg in algorithms:
        r2_values = []
        row = f"{alg:<25}"

        for density in densities:
            if density in all_fits and alg in all_fits[density] and all_fits[density][alg]:
                r2 = all_fits[density][alg].r_squared
                r2_values.append(r2)
                row += f" {r2:<10.4f}"
            else:
                row += f" {'N/A':<10}"

        if r2_values:
            avg_r2 = sum(r2_values) / len(r2_values)
            row += f" {avg_r2:<10.4f}"
            status = "✓ GOOD" if avg_r2 >= 0.85 else ("FAIR" if avg_r2 >= 0.70 else "✗ POOR")
            row += f" {status}"
        else:
            row += f" {'N/A':<10} {'NO DATA'}"

        print(row)

    print("-" * 80)

    # Count successes
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    good_count = 0
    total_count = 0

    for alg in algorithms:
        r2_values = []
        for density in densities:
            if density in all_fits and alg in all_fits[density] and all_fits[density][alg]:
                r2_values.append(all_fits[density][alg].r_squared)

        if r2_values:
            avg_r2 = sum(r2_values) / len(r2_values)
            total_count += 1
            if avg_r2 >= 0.85:
                good_count += 1
                print(f"✓ {alg}: Average R² = {avg_r2:.4f} (GOOD)")
            elif avg_r2 >= 0.70:
                print(f"  {alg}: Average R² = {avg_r2:.4f} (FAIR)")
            else:
                print(f"✗ {alg}: Average R² = {avg_r2:.4f} (POOR)")

    if total_count > 0:
        percentage = (good_count / total_count) * 100
        print(f"\n{good_count}/{total_count} algorithms ({percentage:.0f}%) achieve R² ≥ 0.85")

        if percentage >= 80:
            print("\n✓✓✓ EXCELLENT: Experimental results STRONGLY VALIDATE theoretical complexity!")
        elif percentage >= 60:
            print("\n✓ GOOD: Experimental results VALIDATE theoretical complexity")
        else:
            print("\n⚠ MIXED: Some algorithms validated, others need more work")

    print("\n" + "=" * 80)
    print("Complexity validation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
