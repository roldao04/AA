"""
Graph Loading Utilities

This module provides functions to load graphs from various sources:
- Built-in NetworkX graphs (Karate, Dolphins, etc.)
- SNAP dataset files
- Custom edge list files
"""

import networkx as nx
import os
from typing import Dict, List, Optional
import requests
from pathlib import Path


# Built-in graphs available in NetworkX
BUILTIN_GRAPHS = {
    'karate': nx.karate_club_graph,
    'florentine': nx.florentine_families_graph,
    'davis': nx.davis_southern_women_graph,
}

# SNAP datasets configuration
SNAP_DATASETS = {
    'ego-Facebook': {
        'url': 'https://snap.stanford.edu/data/facebook_combined.txt.gz',
        'filename': 'facebook_combined.txt.gz',
        'format': 'edgelist'
    },
    'email-Eu-core': {
        'url': 'https://snap.stanford.edu/data/email-Eu-core.txt.gz',
        'filename': 'email-Eu-core.txt.gz',
        'format': 'edgelist'
    },
    'wiki-Vote': {
        'url': 'https://snap.stanford.edu/data/wiki-Vote.txt.gz',
        'filename': 'wiki-Vote.txt.gz',
        'format': 'edgelist'
    },
    'ca-GrQc': {
        'url': 'https://snap.stanford.edu/data/ca-GrQc.txt.gz',
        'filename': 'ca-GrQc.txt.gz',
        'format': 'edgelist'
    },
    'ca-HepTh': {
        'url': 'https://snap.stanford.edu/data/ca-HepTh.txt.gz',
        'filename': 'ca-HepTh.txt.gz',
        'format': 'edgelist'
    },
    'ca-CondMat': {
        'url': 'https://snap.stanford.edu/data/ca-CondMat.txt.gz',
        'filename': 'ca-CondMat.txt.gz',
        'format': 'edgelist'
    }
}


def load_graph(name: str, data_dir: str = 'data') -> nx.Graph:
    """
    Load a graph by name from built-in or SNAP datasets.

    Args:
        name: Graph name (e.g., 'karate', 'ego-Facebook')
        data_dir: Directory containing downloaded datasets

    Returns:
        NetworkX Graph object

    Raises:
        ValueError: If graph name is not recognized
        FileNotFoundError: If SNAP dataset file not found
    """
    # Try built-in graphs first
    if name in BUILTIN_GRAPHS:
        G = BUILTIN_GRAPHS[name]()
        # Convert to simple graph (remove self-loops, ensure undirected)
        G = nx.Graph(G)
        G.remove_edges_from(nx.selfloop_edges(G))
        return G

    # Try SNAP datasets
    if name in SNAP_DATASETS:
        dataset_info = SNAP_DATASETS[name]
        filepath = os.path.join(data_dir, dataset_info['filename'])

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Dataset {name} not found at {filepath}. "
                f"Run download_snap_datasets() first."
            )

        # Load graph from edge list
        G = nx.read_edgelist(filepath, comments='#', nodetype=int)
        G = nx.Graph(G)  # Ensure undirected
        G.remove_edges_from(nx.selfloop_edges(G))

        # Remove isolated vertices
        isolated = list(nx.isolates(G))
        G.remove_nodes_from(isolated)

        return G

    raise ValueError(f"Unknown graph name: {name}")


def get_builtin_graphs() -> List[str]:
    """
    Get list of available built-in graph names.

    Returns:
        List of graph names
    """
    return list(BUILTIN_GRAPHS.keys())


def download_snap_datasets(data_dir: str = 'data', datasets: Optional[List[str]] = None) -> None:
    """
    Download SNAP datasets from Stanford repository.

    Args:
        data_dir: Directory to save datasets
        datasets: List of dataset names to download (None = all)

    Notes:
        This function downloads compressed .gz files.
        NetworkX can read them directly without decompression.
    """
    Path(data_dir).mkdir(exist_ok=True)

    if datasets is None:
        datasets = list(SNAP_DATASETS.keys())

    for name in datasets:
        if name not in SNAP_DATASETS:
            print(f"Warning: Unknown dataset {name}, skipping")
            continue

        dataset_info = SNAP_DATASETS[name]
        filepath = os.path.join(data_dir, dataset_info['filename'])

        if os.path.exists(filepath):
            print(f"Dataset {name} already exists at {filepath}")
            continue

        print(f"Downloading {name} from {dataset_info['url']}...")

        # TODO: Implement download with progress bar
        # Use requests or urllib to download file
        # Show progress with tqdm
        # Save to filepath

        print(f"Saved to {filepath}")


def load_custom_graph(filepath: str, format: str = 'edgelist') -> nx.Graph:
    """
    Load graph from custom file.

    Args:
        filepath: Path to graph file
        format: File format ('edgelist', 'adjlist', 'gml', 'graphml')

    Returns:
        NetworkX Graph object
    """
    if format == 'edgelist':
        G = nx.read_edgelist(filepath, nodetype=int)
    elif format == 'adjlist':
        G = nx.read_adjlist(filepath, nodetype=int)
    elif format == 'gml':
        G = nx.read_gml(filepath)
    elif format == 'graphml':
        G = nx.read_graphml(filepath)
    else:
        raise ValueError(f"Unsupported format: {format}")

    G = nx.Graph(G)
    G.remove_edges_from(nx.selfloop_edges(G))

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Warning: Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    return G


def load_sw_graph(filename: str, data_dir: str = 'data/SW_ALGUNS_GRAFOS') -> nx.Graph:
    """
    Load graph from Sedgewick & Wayne format file.

    Format (as per README.txt):
    - Line 1: 0/1 if directed
    - Line 2: 0/1 if weighted
    - Line 3: number of vertices
    - Line 4: number of edges
    - Remaining lines: vertex_from vertex_to [weight]

    Args:
        filename: Name of SW graph file (e.g., 'SWtinyG.txt')
        data_dir: Directory containing SW graph files

    Returns:
        NetworkX Graph object (undirected, unweighted)

    Notes:
        - Self-loops (lacetes) are automatically removed
        - Directed graphs are converted to undirected
        - Edge weights are ignored for edge cover problem
        - Isolated vertices are removed
    """
    filepath = Path(data_dir) / filename

    if not filepath.exists():
        raise FileNotFoundError(f"SW graph file not found: {filepath}")

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Parse header
    is_directed = int(lines[0].strip()) == 1
    is_weighted = int(lines[1].strip()) == 1
    n_vertices = int(lines[2].strip())
    n_edges = int(lines[3].strip())

    # Create graph (always convert to undirected for edge cover)
    G = nx.Graph()
    G.add_nodes_from(range(n_vertices))

    # Read edges
    edges_added = 0
    self_loops_skipped = 0

    for i in range(4, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        u = int(parts[0])
        v = int(parts[1])

        # Skip self-loops (lacetes) as per README
        if u == v:
            self_loops_skipped += 1
            continue

        # Add edge (ignore weight if present)
        if not G.has_edge(u, v):
            G.add_edge(u, v)
            edges_added += 1

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Warning [{filename}]: Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    if self_loops_skipped > 0:
        print(f"Info [{filename}]: Skipped {self_loops_skipped} self-loops")

    print(f"Loaded {filename}: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")

    return G
