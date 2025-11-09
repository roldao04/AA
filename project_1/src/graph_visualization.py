"""
Graph Visualization Module - Visual representation of graphs and edge covers.

This module provides functions to:
- Draw graphs with vertices positioned at their 2D coordinates
- Highlight edge cover solutions
- Compare multiple solutions on the same graph
- Export visualizations as PNG images

Student Number: 113920
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Set, Dict, Optional
from pathlib import Path
from src.graph import Graph, Edge


def draw_graph(
    graph: Graph,
    filename: str = "graph.png",
    output_dir: str = "results/graphs",
    title: Optional[str] = None,
    figsize: tuple = (10, 10)
) -> Path:
    """
    Draw a graph with vertices at their 2D coordinates.

    Args:
        graph: Graph object to visualize
        filename: Output filename
        output_dir: Directory to save the plot
        title: Optional title for the plot
        figsize: Figure size (width, height)

    Returns:
        Path to the saved plot
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)

    # Draw edges first (so they appear behind vertices)
    for edge in graph.edges:
        x_coords = [edge.v1.x, edge.v2.x]
        y_coords = [edge.v1.y, edge.v2.y]
        ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.3, zorder=1)

    # Draw vertices
    vertex_x = [v.x for v in graph.vertices]
    vertex_y = [v.y for v in graph.vertices]
    ax.scatter(vertex_x, vertex_y, c='lightblue', s=300, edgecolors='black',
              linewidths=2, zorder=2)

    # Add vertex labels
    for vertex in graph.vertices:
        ax.text(vertex.x, vertex.y, str(vertex.id),
               horizontalalignment='center',
               verticalalignment='center',
               fontsize=10, fontweight='bold', zorder=3)

    # Set axis properties
    ax.set_xlim(0, 510)
    ax.set_ylim(0, 510)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)

    # Set title
    if title is None:
        title = f"Graph: {graph.num_vertices()} vertices, {graph.num_edges()} edges " \
                f"(density: {graph.edge_density():.1f}%)"
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add metadata
    metadata_text = f"V={graph.num_vertices()}, E={graph.num_edges()}, " \
                   f"Density={graph.edge_density():.1f}%"
    ax.text(0.02, 0.98, metadata_text,
           transform=ax.transAxes,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
           fontsize=9)

    # Save plot
    full_path = output_path / filename
    plt.tight_layout()
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Graph visualization saved: {full_path}")
    return full_path


def draw_graph_with_solution(
    graph: Graph,
    edge_cover: Set[Edge],
    filename: str = "graph_solution.png",
    output_dir: str = "results/graphs",
    algorithm_name: str = "Edge Cover",
    is_optimal: bool = True,
    figsize: tuple = (10, 10)
) -> Path:
    """
    Draw a graph with an edge cover solution highlighted.

    Args:
        graph: Graph object to visualize
        edge_cover: Set of edges forming the edge cover
        filename: Output filename
        output_dir: Directory to save the plot
        algorithm_name: Name of the algorithm that produced this solution
        is_optimal: Whether this solution is optimal
        figsize: Figure size (width, height)

    Returns:
        Path to the saved plot
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)

    # Draw non-selected edges (gray, thin, faded)
    for edge in graph.edges:
        if edge not in edge_cover:
            x_coords = [edge.v1.x, edge.v2.x]
            y_coords = [edge.v1.y, edge.v2.y]
            ax.plot(x_coords, y_coords, 'gray', linewidth=0.5, alpha=0.2, zorder=1)

    # Draw selected edges (red, thick, prominent)
    for edge in edge_cover:
        x_coords = [edge.v1.x, edge.v2.x]
        y_coords = [edge.v1.y, edge.v2.y]
        ax.plot(x_coords, y_coords, 'red', linewidth=3, alpha=0.8, zorder=2,
               label='Edge Cover' if edge == list(edge_cover)[0] else '')

    # Draw vertices (green if covered, red if not)
    covered_vertices = set()
    for edge in edge_cover:
        covered_vertices.add(edge.v1.id)
        covered_vertices.add(edge.v2.id)

    for vertex in graph.vertices:
        color = 'lightgreen' if vertex.id in covered_vertices else 'red'
        ax.scatter([vertex.x], [vertex.y], c=color, s=300, edgecolors='black',
                  linewidths=2, zorder=3)

    # Add vertex labels
    for vertex in graph.vertices:
        ax.text(vertex.x, vertex.y, str(vertex.id),
               horizontalalignment='center',
               verticalalignment='center',
               fontsize=10, fontweight='bold', zorder=4)

    # Set axis properties
    ax.set_xlim(0, 510)
    ax.set_ylim(0, 510)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)

    # Set title
    optimal_str = " (OPTIMAL)" if is_optimal else ""
    title = f"{algorithm_name} Solution{optimal_str}\n" \
            f"{len(edge_cover)} edges covering {len(covered_vertices)}/{graph.num_vertices()} vertices"
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add metadata
    metadata_text = f"Graph: V={graph.num_vertices()}, E={graph.num_edges()}\n" \
                   f"Solution: |C|={len(edge_cover)} edges\n" \
                   f"Coverage: {len(covered_vertices)}/{graph.num_vertices()} vertices" \
                   f"{' [OPTIMAL]' if is_optimal else ''}"
    ax.text(0.02, 0.98, metadata_text,
           transform=ax.transAxes,
           verticalalignment='top',
           bbox=dict(boxstyle='round',
                    facecolor='lightgreen' if is_optimal else 'wheat',
                    alpha=0.7),
           fontsize=9)

    # Add legend
    ax.legend(loc='upper right', fontsize=10)

    # Save plot
    full_path = output_path / filename
    plt.tight_layout()
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Solution visualization saved: {full_path}")
    return full_path


def draw_solution_comparison(
    graph: Graph,
    solutions: Dict[str, Set[Edge]],
    filename: str = "solution_comparison.png",
    output_dir: str = "results/graphs",
    optimal_algorithms: Set[str] = None,
    figsize: tuple = (16, 10)
) -> Path:
    """
    Draw multiple edge cover solutions side by side for comparison.

    Args:
        graph: Graph object to visualize
        solutions: Dictionary mapping algorithm names to edge covers
        filename: Output filename
        output_dir: Directory to save the plot
        optimal_algorithms: Set of algorithm names that produce optimal solutions
        figsize: Figure size (width, height)

    Returns:
        Path to the saved plot
    """
    if optimal_algorithms is None:
        optimal_algorithms = set()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    num_solutions = len(solutions)
    if num_solutions == 0:
        raise ValueError("No solutions provided")

    # Create subplots (2 rows if more than 3 solutions)
    if num_solutions <= 3:
        ncols = num_solutions
        nrows = 1
    else:
        ncols = 3
        nrows = (num_solutions + 2) // 3

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    # Ensure axes is always iterable
    if num_solutions == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if nrows > 1 else axes

    for idx, (algo_name, edge_cover) in enumerate(solutions.items()):
        ax = axes[idx]

        # Draw non-selected edges
        for edge in graph.edges:
            if edge not in edge_cover:
                x_coords = [edge.v1.x, edge.v2.x]
                y_coords = [edge.v1.y, edge.v2.y]
                ax.plot(x_coords, y_coords, 'gray', linewidth=0.5, alpha=0.2, zorder=1)

        # Draw selected edges
        for edge in edge_cover:
            x_coords = [edge.v1.x, edge.v2.x]
            y_coords = [edge.v1.y, edge.v2.y]
            ax.plot(x_coords, y_coords, 'red', linewidth=2, alpha=0.8, zorder=2)

        # Draw vertices
        covered_vertices = set()
        for edge in edge_cover:
            covered_vertices.add(edge.v1.id)
            covered_vertices.add(edge.v2.id)

        for vertex in graph.vertices:
            color = 'lightgreen' if vertex.id in covered_vertices else 'red'
            ax.scatter([vertex.x], [vertex.y], c=color, s=200, edgecolors='black',
                      linewidths=1.5, zorder=3)

        # Add vertex labels
        for vertex in graph.vertices:
            ax.text(vertex.x, vertex.y, str(vertex.id),
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=8, fontweight='bold', zorder=4)

        # Set axis properties
        ax.set_xlim(0, 510)
        ax.set_ylim(0, 510)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2)

        # Set title for this subplot
        is_optimal = algo_name in optimal_algorithms
        optimal_str = " [OPT]" if is_optimal else ""
        ax.set_title(f"{algo_name}{optimal_str}\n|C|={len(edge_cover)}",
                    fontsize=11, fontweight='bold')

    # Hide unused subplots
    for idx in range(num_solutions, len(axes)):
        axes[idx].axis('off')

    # Overall title
    fig.suptitle(f"Edge Cover Solution Comparison\n"
                f"Graph: V={graph.num_vertices()}, E={graph.num_edges()}, "
                f"Density={graph.edge_density():.1f}%",
                fontsize=14, fontweight='bold')

    # Save plot
    full_path = output_path / filename
    plt.tight_layout()
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Comparison visualization saved: {full_path}")
    return full_path


def visualize_graph_instance(
    graph: Graph,
    instance_name: str,
    output_dir: str = "results/graphs/instances"
) -> Path:
    """
    Save a visual representation of a graph instance for documentation.

    Args:
        graph: Graph to visualize
        instance_name: Descriptive name for this instance
        output_dir: Directory to save the visualization

    Returns:
        Path to saved visualization
    """
    filename = f"{instance_name.replace(' ', '_').lower()}.png"
    return draw_graph(
        graph,
        filename=filename,
        output_dir=output_dir,
        title=f"Graph Instance: {instance_name}"
    )
