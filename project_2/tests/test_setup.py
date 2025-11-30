"""
Quick test script to verify project setup.
"""

import sys
from pathlib import Path

# Test imports
print("Testing imports...")

try:
    import networkx as nx
    print("✓ NetworkX imported")
except ImportError as e:
    print(f"✗ NetworkX import failed: {e}")

try:
    import numpy as np
    print("✓ NumPy imported")
except ImportError as e:
    print(f"✗ NumPy import failed: {e}")

try:
    import pandas as pd
    print("✓ Pandas imported")
except ImportError as e:
    print(f"✗ Pandas import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("✓ Matplotlib imported")
except ImportError as e:
    print(f"✗ Matplotlib import failed: {e}")

try:
    import seaborn as sns
    print("✓ Seaborn imported")
except ImportError as e:
    print(f"✗ Seaborn import failed: {e}")

try:
    from scipy import stats
    print("✓ SciPy imported")
except ImportError as e:
    print(f"✗ SciPy import failed: {e}")

try:
    from tqdm import tqdm
    print("✓ tqdm imported")
except ImportError as e:
    print(f"✗ tqdm import failed: {e}")

print("\nTesting project modules...")

try:
    from src.algorithms import (
        exact_edge_cover,
        israeli_itai_edge_cover,
        simulated_annealing_edge_cover,
        lazy_greedy_edge_cover,
        nearest_neighbor_edge_cover
    )
    print("✓ Algorithm modules imported")
except ImportError as e:
    print(f"✗ Algorithm modules import failed: {e}")

try:
    from src.utils import (
        load_graph,
        get_builtin_graphs,
        compute_graph_properties,
        generate_synthetic_graphs
    )
    print("✓ Utility modules imported")
except ImportError as e:
    print(f"✗ Utility modules import failed: {e}")

try:
    from src.experiments import ExperimentRunner
    print("✓ Experiment runner imported")
except ImportError as e:
    print(f"✗ Experiment runner import failed: {e}")

print("\nTesting basic functionality...")

# Test loading a simple graph
try:
    G = nx.karate_club_graph()
    print(f"✓ Loaded Karate Club graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
except Exception as e:
    print(f"✗ Failed to load graph: {e}")

# Test graph properties computation
try:
    from src.utils.graph_properties import compute_graph_properties
    G = nx.karate_club_graph()
    props = compute_graph_properties(G)
    print(f"✓ Computed graph properties: density={props['density']:.3f}, avg_clustering={props['avg_clustering']:.3f}")
except Exception as e:
    print(f"✗ Failed to compute properties: {e}")

# Test directory structure
print("\nChecking directory structure...")
dirs = ['src', 'src/algorithms', 'src/utils', 'src/experiments',
        'data', 'results', 'overnight', 'figures']
for d in dirs:
    if Path(d).exists():
        print(f"✓ {d}/ exists")
    else:
        print(f"✗ {d}/ missing")

print("\n" + "="*50)
print("Setup verification complete!")
print("="*50)
print("\nNext steps:")
print("1. Implement the algorithm functions (TODO markers in src/algorithms/)")
print("2. Download SNAP datasets (optional for now)")
print("3. Run validation tests on small graphs")
print("4. Configure and test overnight experiments")
