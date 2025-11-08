"""
Visualization tools for Edge Cover experiment results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
from collections import defaultdict

from src.experiment import ExperimentResult


class ResultVisualizer:
    """Creates visualizations from experiment results."""

    def __init__(self, results: List[ExperimentResult], output_dir: str = "results"):
        """
        Initialize visualizer with experiment results.

        Args:
            results: List of ExperimentResult objects
            output_dir: Directory to save plots
        """
        self.results = results
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Set up matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    def plot_execution_time_vs_vertices(self, filename: str = "time_vs_vertices.png") -> Path:
        """
        Plot execution time vs number of vertices for both algorithms.

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        # Group results by edge density
        density_groups = defaultdict(lambda: {'vertices': [], 'exhaustive': [], 'greedy': []})

        for result in self.results:
            if not result.exhaustive_timed_out and result.exhaustive_time is not None:
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['exhaustive'].append(result.exhaustive_time)
                density_groups[result.edge_density]['greedy'].append(result.greedy_time)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Plot exhaustive search
        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax1.plot(data['vertices'], data['exhaustive'], marker='o', label=f'{density}% density')

        ax1.set_xlabel('Number of Vertices')
        ax1.set_ylabel('Execution Time (seconds)')
        ax1.set_title('Exhaustive Search: Time vs Vertices')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')

        # Plot greedy search
        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax2.plot(data['vertices'], data['greedy'], marker='s', label=f'{density}% density')

        ax2.set_xlabel('Number of Vertices')
        ax2.set_ylabel('Execution Time (seconds)')
        ax2.set_title('Greedy Heuristic: Time vs Vertices')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_operations_vs_vertices(self, filename: str = "operations_vs_vertices.png") -> Path:
        """
        Plot number of basic operations vs vertices.

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        density_groups = defaultdict(lambda: {'vertices': [], 'exhaustive': [], 'greedy': []})

        for result in self.results:
            if not result.exhaustive_timed_out and result.exhaustive_operations is not None:
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['exhaustive'].append(result.exhaustive_operations)
                density_groups[result.edge_density]['greedy'].append(result.greedy_operations)

        fig, ax = plt.subplots(figsize=(10, 6))

        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax.plot(data['vertices'], data['exhaustive'], marker='o',
                   label=f'Exhaustive {density}%', linestyle='-')
            ax.plot(data['vertices'], data['greedy'], marker='s',
                   label=f'Greedy {density}%', linestyle='--', alpha=0.7)

        ax.set_xlabel('Number of Vertices')
        ax.set_ylabel('Basic Operations (log scale)')
        ax.set_title('Number of Basic Operations vs Vertices')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_solutions_explored(self, filename: str = "solutions_explored.png") -> Path:
        """
        Plot number of solutions explored by exhaustive search.

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        density_groups = defaultdict(lambda: {'vertices': [], 'solutions': []})

        for result in self.results:
            if not result.exhaustive_timed_out and result.exhaustive_solutions_explored is not None:
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['solutions'].append(result.exhaustive_solutions_explored)

        fig, ax = plt.subplots(figsize=(10, 6))

        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax.plot(data['vertices'], data['solutions'], marker='o', label=f'{density}% density')

        ax.set_xlabel('Number of Vertices')
        ax.set_ylabel('Solutions Explored (log scale)')
        ax.set_title('Exhaustive Search: Solutions Explored vs Vertices')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_greedy_quality(self, filename: str = "greedy_quality.png") -> Path:
        """
        Plot greedy algorithm quality (optimality ratio).

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        density_groups = defaultdict(lambda: {'vertices': [], 'quality': []})

        for result in self.results:
            if result.quality_ratio is not None:
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['quality'].append(result.quality_ratio)

        fig, ax = plt.subplots(figsize=(10, 6))

        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax.plot(data['vertices'], data['quality'], marker='o', label=f'{density}% density')

        ax.axhline(y=1.0, color='r', linestyle='--', label='Optimal (1.0)', alpha=0.5)
        ax.set_xlabel('Number of Vertices')
        ax.set_ylabel('Quality Ratio (Optimal/Greedy)')
        ax.set_title('Greedy Algorithm Quality vs Vertices')
        ax.set_ylim([0, 1.1])
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_speedup(self, filename: str = "speedup.png") -> Path:
        """
        Plot speedup (exhaustive time / greedy time).

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        density_groups = defaultdict(lambda: {'vertices': [], 'speedup': []})

        for result in self.results:
            if result.speedup is not None and result.speedup != float('inf'):
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['speedup'].append(result.speedup)

        fig, ax = plt.subplots(figsize=(10, 6))

        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax.plot(data['vertices'], data['speedup'], marker='o', label=f'{density}% density')

        ax.set_xlabel('Number of Vertices')
        ax.set_ylabel('Speedup Factor (log scale)')
        ax.set_title('Speedup: Exhaustive vs Greedy')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_solution_size_comparison(self, filename: str = "solution_sizes.png") -> Path:
        """
        Compare solution sizes between exhaustive and greedy.

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        density_groups = defaultdict(lambda: {'vertices': [], 'exhaustive': [], 'greedy': []})

        for result in self.results:
            if not result.exhaustive_timed_out and result.exhaustive_solution_size is not None:
                density_groups[result.edge_density]['vertices'].append(result.num_vertices)
                density_groups[result.edge_density]['exhaustive'].append(result.exhaustive_solution_size)
                density_groups[result.edge_density]['greedy'].append(result.greedy_solution_size)

        fig, ax = plt.subplots(figsize=(10, 6))

        for density in sorted(density_groups.keys()):
            data = density_groups[density]
            ax.plot(data['vertices'], data['exhaustive'], marker='o',
                   label=f'Optimal {density}%', linestyle='-')
            ax.plot(data['vertices'], data['greedy'], marker='s',
                   label=f'Greedy {density}%', linestyle='--', alpha=0.7)

        ax.set_xlabel('Number of Vertices')
        ax.set_ylabel('Edge Cover Size')
        ax.set_title('Solution Size Comparison: Optimal vs Greedy')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_complexity_validation(
        self,
        algorithm_name: str,
        size_key: str,
        time_key: str,
        complexity_fit,
        filename: str = None
    ) -> Path:
        """
        Plot experimental data vs theoretical complexity curve.

        Args:
            algorithm_name: Name of algorithm
            size_key: Key for problem size ('num_edges' or 'num_vertices')
            time_key: Key for execution time
            complexity_fit: ComplexityFit object from complexity_analysis module
            filename: Output filename (default: complexity_{algorithm}.png)

        Returns:
            Path to saved plot
        """
        if filename is None:
            safe_name = algorithm_name.lower().replace(' ', '_').replace('&', 'and')
            filename = f"complexity_{safe_name}.png"

        # Extract experimental data
        sizes = []
        times = []
        for result in self.results:
            size = getattr(result, size_key, None)
            time_val = getattr(result, time_key, None)
            if size is not None and time_val is not None and time_val > 0:
                sizes.append(size)
                times.append(time_val)

        if not sizes:
            print(f"No data available for {algorithm_name}")
            return None

        # Sort by size
        sorted_data = sorted(zip(sizes, times))
        sizes, times = zip(*sorted_data)

        # Create plot
        plt.figure(figsize=(10, 6))

        # Plot experimental data
        plt.scatter(sizes, times, alpha=0.6, s=50, label='Experimental', color='blue')

        # Plot theoretical curve if available
        if complexity_fit:
            theo_sizes = [p[0] for p in complexity_fit.predictions]
            theo_times = [p[1] for p in complexity_fit.predictions]
            sorted_theo = sorted(zip(theo_sizes, theo_times))
            theo_sizes, theo_times = zip(*sorted_theo)

            plt.plot(theo_sizes, theo_times, 'r--', linewidth=2,
                    label=f'Theoretical {complexity_fit.complexity_class}', alpha=0.7)

            # Add R² to plot
            plt.text(0.05, 0.95, f'R² = {complexity_fit.r_squared:.4f}',
                    transform=plt.gca().transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.xlabel(f'{size_key.replace("_", " ").title()}', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.title(f'Complexity Validation: {algorithm_name}', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save plot
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_all_algorithms_comparison(self, filename: str = "all_algorithms_comparison.png") -> Path:
        """
        Plot all 5 algorithms on single comparison chart (log scale).

        Args:
            filename: Output filename

        Returns:
            Path to saved plot
        """
        plt.figure(figsize=(12, 7))

        # Define algorithm configurations
        algorithms = [
            ('exhaustive_time', 'exhaustive_timed_out', 'Exhaustive Search', 'red', 'o'),
            ('branch_bound_time', 'branch_bound_timed_out', 'Branch & Bound', 'orange', 's'),
            ('optimal_matching_time', 'optimal_matching_failed', 'Optimal Matching (O(n^2.5))', 'green', '^'),
            ('greedy_time', None, 'Greedy Coverage', 'blue', 'D'),
            ('greedy_matching_time', None, 'Greedy Matching (O(m))', 'purple', 'v'),
        ]

        for time_key, failed_key, label, color, marker in algorithms:
            sizes = []
            times = []

            for result in self.results:
                # Check if algorithm failed/timed out
                if failed_key and getattr(result, failed_key, False):
                    continue

                time_val = getattr(result, time_key, None)
                if time_val is not None and time_val > 0:
                    # Use num_edges as x-axis for comparison
                    sizes.append(result.num_edges)
                    times.append(time_val)

            if sizes:
                # Sort by size
                sorted_data = sorted(zip(sizes, times))
                sizes, times = zip(*sorted_data)
                plt.plot(sizes, times, marker=marker, label=label, color=color,
                        linewidth=2, markersize=6, alpha=0.7)

        plt.xlabel('Number of Edges', fontsize=12)
        plt.ylabel('Execution Time (seconds, log scale)', fontsize=12)
        plt.title('Algorithm Comparison: All 5 Algorithms', fontsize=14, fontweight='bold')
        plt.yscale('log')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3, which='both')
        plt.tight_layout()

        # Save plot
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def plot_performance_projection(
        self,
        complexity_fits: Dict,
        target_sizes: List[int] = None,
        filename: str = "performance_projection.png"
    ) -> Path:
        """
        Plot performance extrapolation to larger problem sizes.

        Args:
            complexity_fits: Dictionary of ComplexityFit objects by algorithm name
            target_sizes: List of sizes to project to (default: [10, 20, 30, 40, 50])
            filename: Output filename

        Returns:
            Path to saved plot
        """
        if target_sizes is None:
            target_sizes = list(range(10, 51, 5))

        plt.figure(figsize=(12, 8))

        colors = {
            'Exhaustive Search': 'red',
            'Branch & Bound': 'orange',
            'Optimal Matching': 'green',
            'Greedy Coverage': 'blue',
            'Greedy Matching': 'purple'
        }

        for algo_name, fit in complexity_fits.items():
            if fit is None:
                continue

            # Extrapolate
            from src.complexity_analysis import extrapolate_performance
            projections = extrapolate_performance(fit, target_sizes)

            sizes = [p[0] for p in projections]
            times = [p[1] for p in projections]

            color = colors.get(algo_name, 'gray')
            plt.plot(sizes, times, label=f'{algo_name} {fit.complexity_class}',
                    color=color, linewidth=2, alpha=0.7)

        # Add horizontal line for "reasonable time" (e.g., 1 hour)
        plt.axhline(y=3600, color='black', linestyle='--', linewidth=1, alpha=0.5, label='1 hour')

        plt.xlabel('Problem Size (edges)', fontsize=12)
        plt.ylabel('Projected Execution Time (seconds, log scale)', fontsize=12)
        plt.title('Performance Projection: Scalability to Larger Graphs', fontsize=14, fontweight='bold')
        plt.yscale('log')
        plt.legend(loc='best', fontsize=9)
        plt.grid(True, alpha=0.3, which='both')
        plt.tight_layout()

        # Save plot
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved: {output_path}")
        return output_path

    def generate_all_plots(self) -> List[Path]:
        """
        Generate all available plots.

        Returns:
            List of paths to saved plots
        """
        print("\n=== Generating Plots ===\n")

        plots = []

        try:
            plots.append(self.plot_execution_time_vs_vertices())
        except Exception as e:
            print(f"Error generating time plot: {e}")

        try:
            plots.append(self.plot_operations_vs_vertices())
        except Exception as e:
            print(f"Error generating operations plot: {e}")

        try:
            plots.append(self.plot_solutions_explored())
        except Exception as e:
            print(f"Error generating solutions explored plot: {e}")

        try:
            plots.append(self.plot_greedy_quality())
        except Exception as e:
            print(f"Error generating quality plot: {e}")

        try:
            plots.append(self.plot_speedup())
        except Exception as e:
            print(f"Error generating speedup plot: {e}")

        try:
            plots.append(self.plot_solution_size_comparison())
        except Exception as e:
            print(f"Error generating solution size plot: {e}")

        try:
            plots.append(self.plot_all_algorithms_comparison())
        except Exception as e:
            print(f"Error generating all algorithms comparison plot: {e}")

        print(f"\n=== Generated {len(plots)} plots ===\n")
        return plots
