"""
Scalability Testing Framework for Streaming Algorithms

This module provides utilities for testing algorithm performance across
varying stream sizes and cardinalities.

Author: João Roldão (113920)
"""

import numpy as np
import pandas as pd
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Callable
import tracemalloc

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.exact_counter import ExactCounter
from algorithms.fixed_probability_counter import FixedProbabilityCounter
from algorithms.space_saving import SpaceSaving


def generate_zipf_stream(n: int, cardinality: int, alpha: float = 1.5, seed: int = None) -> List[int]:
    """
    Generate a synthetic data stream following Zipfian distribution.

    Zipf distribution models real-world frequency distributions where
    a few items are very frequent and most items are rare.

    Parameters:
    -----------
    n : int
        Number of elements in the stream
    cardinality : int
        Number of unique items
    alpha : float
        Zipf parameter (higher = more skewed, typical: 1.0-2.0)
    seed : int
        Random seed for reproducibility

    Returns:
    --------
    list : Stream of integers
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate Zipfian probabilities
    ranks = np.arange(1, cardinality + 1)
    probabilities = 1.0 / (ranks ** alpha)
    probabilities /= probabilities.sum()

    # Sample from distribution
    stream = np.random.choice(cardinality, size=n, p=probabilities)

    return stream.tolist()


def generate_uniform_stream(n: int, cardinality: int, seed: int = None) -> List[int]:
    """
    Generate uniform random stream.

    Parameters:
    -----------
    n : int
        Number of elements
    cardinality : int
        Number of unique items
    seed : int
        Random seed

    Returns:
    --------
    list : Stream of integers
    """
    if seed is not None:
        np.random.seed(seed)

    return np.random.randint(0, cardinality, size=n).tolist()


def generate_skewed_stream(n: int, cardinality: int, heavy_items: int = 5,
                           heavy_weight: float = 0.8, seed: int = None) -> List[int]:
    """
    Generate stream with explicitly skewed distribution.

    heavy_items get heavy_weight of probability mass,
    remaining items share (1-heavy_weight) uniformly.

    Parameters:
    -----------
    n : int
        Number of elements
    cardinality : int
        Number of unique items
    heavy_items : int
        Number of heavy hitters
    heavy_weight : float
        Fraction of stream from heavy hitters (0-1)
    seed : int
        Random seed

    Returns:
    --------
    list : Stream of integers
    """
    if seed is not None:
        np.random.seed(seed)

    # Create probability distribution
    probs = np.ones(cardinality)
    probs[:heavy_items] = heavy_weight / heavy_items * cardinality
    probs[heavy_items:] = (1 - heavy_weight) / (cardinality - heavy_items) * cardinality
    probs /= probs.sum()

    return np.random.choice(cardinality, size=n, p=probs).tolist()


def measure_algorithm_performance(algorithm_class, stream: List,
                                  init_params: Dict = None,
                                  process_method: str = 'process_stream') -> Dict:
    """
    Measure time and memory performance of an algorithm.

    Parameters:
    -----------
    algorithm_class : class
        Algorithm class to test
    stream : list
        Data stream to process
    init_params : dict
        Parameters for algorithm initialization
    process_method : str
        Method name to call for processing stream

    Returns:
    --------
    dict : Performance metrics
    """
    if init_params is None:
        init_params = {}

    # Handle seed for FixedProbabilityCounter (doesn't accept seed in constructor)
    seed_value = init_params.pop('seed', None)
    if seed_value is not None and 'FixedProbability' in algorithm_class.__name__:
        import random
        random.seed(seed_value)

    # Initialize algorithm
    algo = algorithm_class(**init_params)

    # Start memory tracking
    tracemalloc.start()
    baseline_memory = tracemalloc.get_traced_memory()[0]

    # Measure execution time
    start_time = time.perf_counter()

    # Process stream
    if hasattr(algo, process_method):
        getattr(algo, process_method)(stream)
    else:
        # Fallback to manual processing
        for item in stream:
            algo.add(item)

    end_time = time.perf_counter()

    # Get peak memory
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Calculate metrics
    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = (peak_memory - baseline_memory) / 1024
    time_per_element_us = execution_time_ms * 1000 / len(stream)

    return {
        'execution_time_ms': execution_time_ms,
        'peak_memory_kb': peak_memory_kb,
        'time_per_element_us': time_per_element_us,
        'stream_size': len(stream),
        'algorithm': algo
    }


def run_exact_counter_scalability(stream_sizes: List[int], cardinality: int,
                                  distribution: str = 'zipf', seed: int = 113920) -> pd.DataFrame:
    """
    Test Exact Counter across different stream sizes.

    Parameters:
    -----------
    stream_sizes : list
        List of stream sizes to test
    cardinality : int
        Number of unique items
    distribution : str
        'zipf', 'uniform', or 'skewed'
    seed : int
        Random seed

    Returns:
    --------
    DataFrame : Scalability results
    """
    results = []

    for n in stream_sizes:
        print(f"  Exact Counter: n={n:,}...", end='', flush=True)

        # Generate stream
        if distribution == 'zipf':
            stream = generate_zipf_stream(n, cardinality, seed=seed)
        elif distribution == 'uniform':
            stream = generate_uniform_stream(n, cardinality, seed=seed)
        else:  # skewed
            stream = generate_skewed_stream(n, cardinality, seed=seed)

        # Measure performance
        perf = measure_algorithm_performance(ExactCounter, stream)

        results.append({
            'algorithm': 'Exact Counter',
            'stream_size': n,
            'cardinality': cardinality,
            'distribution': distribution,
            'execution_time_ms': perf['execution_time_ms'],
            'peak_memory_kb': perf['peak_memory_kb'],
            'time_per_element_us': perf['time_per_element_us']
        })

        print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

    return pd.DataFrame(results)


def run_fixed_prob_scalability(stream_sizes: List[int], cardinality: int,
                               p: float = 0.25, distribution: str = 'zipf',
                               seed: int = 113920) -> pd.DataFrame:
    """
    Test Fixed Probability Counter across different stream sizes.

    Parameters:
    -----------
    stream_sizes : list
        List of stream sizes to test
    cardinality : int
        Number of unique items
    p : float
        Sampling probability
    distribution : str
        'zipf', 'uniform', or 'skewed'
    seed : int
        Random seed

    Returns:
    --------
    DataFrame : Scalability results
    """
    results = []

    for n in stream_sizes:
        print(f"  Fixed Prob (p={p}): n={n:,}...", end='', flush=True)

        # Generate stream
        if distribution == 'zipf':
            stream = generate_zipf_stream(n, cardinality, seed=seed)
        elif distribution == 'uniform':
            stream = generate_uniform_stream(n, cardinality, seed=seed)
        else:  # skewed
            stream = generate_skewed_stream(n, cardinality, seed=seed)

        # Measure performance
        perf = measure_algorithm_performance(
            FixedProbabilityCounter,
            stream,
            init_params={'p': p, 'seed': seed}
        )

        results.append({
            'algorithm': f'Fixed Prob (p={p})',
            'stream_size': n,
            'cardinality': cardinality,
            'distribution': distribution,
            'execution_time_ms': perf['execution_time_ms'],
            'peak_memory_kb': perf['peak_memory_kb'],
            'time_per_element_us': perf['time_per_element_us']
        })

        print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

    return pd.DataFrame(results)


def run_space_saving_scalability(stream_sizes: List[int], cardinality: int,
                                 k_values: List[int], distribution: str = 'zipf',
                                 seed: int = 113920) -> pd.DataFrame:
    """
    Test Space-Saving across different stream sizes and k values.

    Parameters:
    -----------
    stream_sizes : list
        List of stream sizes to test
    cardinality : int
        Number of unique items
    k_values : list
        List of k values to test
    distribution : str
        'zipf', 'uniform', or 'skewed'
    seed : int
        Random seed

    Returns:
    --------
    DataFrame : Scalability results
    """
    results = []

    for n in stream_sizes:
        for k in k_values:
            print(f"  Space-Saving (k={k}): n={n:,}...", end='', flush=True)

            # Generate stream
            if distribution == 'zipf':
                stream = generate_zipf_stream(n, cardinality, seed=seed)
            elif distribution == 'uniform':
                stream = generate_uniform_stream(n, cardinality, seed=seed)
            else:  # skewed
                stream = generate_skewed_stream(n, cardinality, seed=seed)

            # Measure performance
            perf = measure_algorithm_performance(
                SpaceSaving,
                stream,
                init_params={'k': k}
            )

            results.append({
                'algorithm': f'Space-Saving (k={k})',
                'k': k,
                'stream_size': n,
                'cardinality': cardinality,
                'distribution': distribution,
                'execution_time_ms': perf['execution_time_ms'],
                'peak_memory_kb': perf['peak_memory_kb'],
                'time_per_element_us': perf['time_per_element_us']
            })

            print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

    return pd.DataFrame(results)


def run_cardinality_scalability(cardinalities: List[int], stream_size: int = 10000,
                                distribution: str = 'zipf', k_ratio: float = 1.5,
                                seed: int = 113920) -> pd.DataFrame:
    """
    Test how algorithms scale with varying cardinality (unique items).

    Parameters:
    -----------
    cardinalities : list
        List of cardinality values to test
    stream_size : int
        Fixed stream size
    distribution : str
        'zipf', 'uniform', or 'skewed'
    k_ratio : float
        For Space-Saving, k = cardinality * k_ratio
    seed : int
        Random seed

    Returns:
    --------
    DataFrame : Scalability results
    """
    results = []

    for d in cardinalities:
        print(f"\nCardinality d={d}:")

        # Generate stream
        if distribution == 'zipf':
            stream = generate_zipf_stream(stream_size, d, seed=seed)
        elif distribution == 'uniform':
            stream = generate_uniform_stream(stream_size, d, seed=seed)
        else:  # skewed
            stream = generate_skewed_stream(stream_size, d, seed=seed)

        # Test Exact Counter
        print(f"  Exact Counter...", end='', flush=True)
        perf = measure_algorithm_performance(ExactCounter, stream)
        results.append({
            'algorithm': 'Exact Counter',
            'cardinality': d,
            'stream_size': stream_size,
            'execution_time_ms': perf['execution_time_ms'],
            'peak_memory_kb': perf['peak_memory_kb']
        })
        print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

        # Test Fixed Prob
        print(f"  Fixed Prob...", end='', flush=True)
        perf = measure_algorithm_performance(
            FixedProbabilityCounter, stream, init_params={'p': 0.25, 'seed': seed}
        )
        results.append({
            'algorithm': 'Fixed Prob',
            'cardinality': d,
            'stream_size': stream_size,
            'execution_time_ms': perf['execution_time_ms'],
            'peak_memory_kb': perf['peak_memory_kb']
        })
        print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

        # Test Space-Saving
        k = int(d * k_ratio)
        print(f"  Space-Saving (k={k})...", end='', flush=True)
        perf = measure_algorithm_performance(
            SpaceSaving, stream, init_params={'k': k}
        )
        results.append({
            'algorithm': f'Space-Saving',
            'k': k,
            'cardinality': d,
            'stream_size': stream_size,
            'execution_time_ms': perf['execution_time_ms'],
            'peak_memory_kb': perf['peak_memory_kb']
        })
        print(f" {perf['execution_time_ms']:.2f}ms, {perf['peak_memory_kb']:.2f}KB")

    return pd.DataFrame(results)


def comprehensive_scalability_suite(output_dir: Path = None) -> Dict[str, pd.DataFrame]:
    """
    Run comprehensive scalability test suite.

    Returns:
    --------
    dict : Dictionary of DataFrames with all results
    """
    print("="*80)
    print("COMPREHENSIVE SCALABILITY TEST SUITE")
    print("="*80)

    results = {}

    # Test 1: Stream size scalability (fixed cardinality)
    print("\n[1/3] STREAM SIZE SCALABILITY (cardinality=100, Zipf α=1.5)")
    print("-"*80)
    stream_sizes = [1000, 5000, 10000, 25000, 50000, 100000]
    cardinality = 100

    print("\nExact Counter:")
    results['exact_stream_size'] = run_exact_counter_scalability(stream_sizes, cardinality)

    print("\nFixed Probability:")
    results['fixed_prob_stream_size'] = run_fixed_prob_scalability(stream_sizes, cardinality)

    print("\nSpace-Saving:")
    results['space_saving_stream_size'] = run_space_saving_scalability(
        stream_sizes, cardinality, k_values=[20, 50, 100, 200]
    )

    # Test 2: Cardinality scalability (fixed stream size)
    print("\n\n[2/3] CARDINALITY SCALABILITY (stream_size=10000)")
    print("-"*80)
    cardinalities = [10, 50, 100, 250, 500, 1000]
    results['cardinality_scaling'] = run_cardinality_scalability(cardinalities)

    # Test 3: Distribution comparison (fixed size and cardinality)
    print("\n\n[3/3] DISTRIBUTION COMPARISON (n=10000, d=100)")
    print("-"*80)
    distributions = ['zipf', 'uniform', 'skewed']
    dist_results = []

    for dist in distributions:
        print(f"\nDistribution: {dist}")
        ec_res = run_exact_counter_scalability([10000], 100, distribution=dist)
        fp_res = run_fixed_prob_scalability([10000], 100, distribution=dist)
        ss_res = run_space_saving_scalability([10000], 100, [50], distribution=dist)

        dist_results.append(pd.concat([ec_res, fp_res, ss_res], ignore_index=True))

    results['distribution_comparison'] = pd.concat(dist_results, ignore_index=True)

    # Save results if output directory specified
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for name, df in results.items():
            filepath = output_dir / f'{name}.csv'
            df.to_csv(filepath, index=False)
            print(f"\n✓ Saved {name} to {filepath}")

    print("\n" + "="*80)
    print("✓ SCALABILITY TEST SUITE COMPLETE")
    print("="*80)

    return results


if __name__ == '__main__':
    # Run comprehensive suite
    output_path = Path(__file__).parent.parent.parent / 'results' / 'scalability'
    comprehensive_scalability_suite(output_path)
