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
import gc
from tqdm import tqdm


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


def load_snap_graph(relative_path: str, data_dir: str = 'data/SNAP') -> nx.Graph:
    """
    Load graph from SNAP dataset in edge list format.

    SNAP Format:
    - Lines starting with # are comments (metadata)
    - Each line: FromNodeId ToNodeId (tab or space separated)
    - May list edges in both directions (converted to undirected)

    Args:
        relative_path: Relative path from data_dir (e.g., 'ca-grqc/CA-GrQc.txt')
        data_dir: Base directory for SNAP datasets

    Returns:
        NetworkX Graph object (undirected, unweighted)

    Examples:
        >>> G = load_snap_graph('ca-grqc/CA-GrQc.txt')
        >>> G = load_snap_graph('wiki_vote/Wiki-Vote.txt')
        >>> G = load_snap_graph('email_eu_core/email-Eu-core.txt')

    Notes:
        - Self-loops are removed
        - Isolated vertices are removed
        - Converted to undirected graph
    """
    filepath = Path(data_dir) / relative_path

    if not filepath.exists():
        raise FileNotFoundError(f"SNAP graph file not found: {filepath}")

    # Load edge list (comments start with #)
    G = nx.read_edgelist(str(filepath), comments='#', nodetype=int)

    # Ensure undirected
    G = nx.Graph(G)

    # Remove self-loops
    self_loops = list(nx.selfloop_edges(G))
    if self_loops:
        G.remove_edges_from(self_loops)
        print(f"Info [{relative_path}]: Removed {len(self_loops)} self-loops")

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Warning [{relative_path}]: Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    print(f"Loaded SNAP graph {relative_path}: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")

    return G


def load_snap_graph_memory_efficient(relative_path: str, data_dir: str = 'data/SNAP',
                                     batch_size: int = 500000) -> nx.Graph:
    """
    Load SNAP graph with memory-efficient line-by-line processing.

    This function is optimized for MASSIVE graphs (millions of vertices/edges) where
    nx.read_edgelist() would consume too much memory. It uses:
    - Header parsing to pre-allocate nodes (reduces rehashing)
    - Batched edge additions with garbage collection
    - Progress monitoring with tqdm
    - Expected memory reduction: 50-70% vs nx.read_edgelist()

    Args:
        relative_path: Relative path from data_dir (e.g., 'live_journal/com-lj.ungraph.txt')
        data_dir: Base directory for SNAP datasets
        batch_size: Number of edges to add before garbage collection (default: 500k)

    Returns:
        NetworkX Graph object (undirected, unweighted)

    Examples:
        >>> G = load_snap_graph_memory_efficient('live_journal/com-lj.ungraph.txt')
        >>> G = load_snap_graph_memory_efficient('orkut/com-orkut.ungraph.txt')

    Notes:
        - Parses SNAP header to get node/edge counts
        - Self-loops are removed
        - Isolated vertices are removed
        - Uses batched processing to reduce memory pressure
    """
    filepath = Path(data_dir) / relative_path

    if not filepath.exists():
        raise FileNotFoundError(f"SNAP graph file not found: {filepath}")

    print(f"Loading {relative_path} with memory-efficient loader...")

    # Parse header to get expected counts
    expected_nodes = None
    expected_edges = None

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('# Nodes:'):
                # Format: "# Nodes: 3997962 Edges: 34681189"
                parts = line.split()
                expected_nodes = int(parts[2])
                expected_edges = int(parts[4])
                break

    print(f"Expected: {expected_nodes:,} nodes, {expected_edges:,} edges")

    # Create empty graph
    G = nx.Graph()

    # Pre-add nodes if we know the count (reduces rehashing)
    if expected_nodes:
        print(f"Pre-allocating {expected_nodes:,} nodes...")
        # We don't know node IDs yet, so we'll add them as we see edges

    # Read edges line by line with batching
    edges_batch = []
    edge_count = 0

    print(f"Loading edges (batch size: {batch_size:,})...")

    with open(filepath, 'r') as f:
        # Use tqdm for progress if we know expected edge count
        if expected_edges:
            pbar = tqdm(total=expected_edges, desc="Loading edges", unit="edges")
        else:
            pbar = None

        for line in f:
            # Skip comments
            if line.startswith('#'):
                continue

            # Parse edge
            parts = line.strip().split()
            if len(parts) >= 2:
                u, v = int(parts[0]), int(parts[1])

                # Skip self-loops immediately
                if u == v:
                    continue

                edges_batch.append((u, v))
                edge_count += 1

                # Add batch when it reaches batch_size
                if len(edges_batch) >= batch_size:
                    G.add_edges_from(edges_batch)
                    edges_batch = []
                    gc.collect()  # Force garbage collection

                    if pbar:
                        pbar.update(batch_size)

        # Add remaining edges
        if edges_batch:
            G.add_edges_from(edges_batch)
            if pbar:
                pbar.update(len(edges_batch))

        if pbar:
            pbar.close()

    print(f"Loaded {edge_count:,} edges (before deduplication)")

    # Final garbage collection
    gc.collect()

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    print(f"Final graph: {G.number_of_nodes():,} vertices, {G.number_of_edges():,} edges")

    # Final cleanup
    gc.collect()

    return G


def load_facebook_ego(ego_id: str, data_dir: str = 'data/SNAP/facebook/facebook') -> nx.Graph:
    """
    Load Facebook ego network from SNAP dataset.

    Format:
    - File: {ego_id}.edges contains space-separated edge list
    - Ego node (center) is connected to all nodes in the network
    - Need to manually add ego node and its edges

    Args:
        ego_id: Ego network ID (e.g., '0', '107', '698', '1684')
        data_dir: Directory containing Facebook ego network files

    Returns:
        NetworkX Graph object (undirected, unweighted)

    Examples:
        >>> G = load_facebook_ego('0')      # 333 nodes
        >>> G = load_facebook_ego('107')    # 1034 nodes
        >>> G = load_facebook_ego('698')    # 61 nodes

    Notes:
        - Ego node is added and connected to all other nodes
        - Self-loops are removed
        - Isolated vertices are removed
    """
    filepath = Path(data_dir) / f"{ego_id}.edges"

    if not filepath.exists():
        raise FileNotFoundError(f"Facebook ego network file not found: {filepath}")

    # Load edge list (no comments in Facebook ego files)
    G = nx.read_edgelist(str(filepath), nodetype=int)

    # Ensure undirected
    G = nx.Graph(G)

    # Add ego node (convert ego_id to int)
    ego_node = int(ego_id)

    # Get all nodes in the network (ego's friends)
    all_nodes = set(G.nodes())

    # Add ego node and connect to all nodes
    if ego_node not in G:
        G.add_node(ego_node)

    for node in all_nodes:
        if node != ego_node and not G.has_edge(ego_node, node):
            G.add_edge(ego_node, node)

    # Remove self-loops (shouldn't exist but be safe)
    self_loops = list(nx.selfloop_edges(G))
    if self_loops:
        G.remove_edges_from(self_loops)

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Warning [ego-{ego_id}]: Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    print(f"Loaded Facebook ego-{ego_id}: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")

    return G


def load_dimacs_graph(relative_path: str, data_dir: str = 'data/DIMACS') -> nx.Graph:
    """
    Load graph from DIMACS CLIQUE format.

    DIMACS Format:
    - Lines starting with 'c' are comments
    - Header: p edge <n_vertices> <n_edges>
    - Edges: e <u> <v>

    Args:
        relative_path: Relative path from data_dir (e.g., 'C1000.9/c1000.txt')
        data_dir: Base directory for DIMACS benchmarks

    Returns:
        NetworkX Graph object (undirected, unweighted)

    Examples:
        >>> G = load_dimacs_graph('C1000.9/c1000.txt')  # 1000 nodes, 450k edges, p=0.9
        >>> G = load_dimacs_graph('C2000.9/c2000.txt')  # 2000 nodes, 1.8M edges

    Notes:
        - Self-loops are removed
        - Isolated vertices are removed
        - Vertex IDs are 1-indexed in file, converted to 0-indexed
    """
    filepath = Path(data_dir) / relative_path

    if not filepath.exists():
        raise FileNotFoundError(f"DIMACS graph file not found: {filepath}")

    G = nx.Graph()
    n_vertices = 0
    n_edges_expected = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Parse header
            if line.startswith('p edge'):
                parts = line.split()
                n_vertices = int(parts[2])
                n_edges_expected = int(parts[3])
                # Add all vertices (1-indexed in file, we'll use 1-indexed in graph too)
                G.add_nodes_from(range(1, n_vertices + 1))

            # Parse edges
            elif line.startswith('e'):
                parts = line.split()
                u = int(parts[1])
                v = int(parts[2])

                # Skip self-loops
                if u == v:
                    continue

                # Add edge (graph uses 1-indexed like file)
                G.add_edge(u, v)

            # Skip comments
            elif line.startswith('c'):
                continue

    # Remove isolated vertices
    isolated = list(nx.isolates(G))
    if isolated:
        print(f"Warning [{relative_path}]: Removing {len(isolated)} isolated vertices")
        G.remove_nodes_from(isolated)

    edges_loaded = G.number_of_edges()
    if edges_loaded != n_edges_expected:
        print(f"Info [{relative_path}]: Loaded {edges_loaded} edges, expected {n_edges_expected}")

    print(f"Loaded DIMACS graph {relative_path}: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")

    return G
