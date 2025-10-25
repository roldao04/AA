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

        print(f"\n=== Generated {len(plots)} plots ===\n")
        return plots
