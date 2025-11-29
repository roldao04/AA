"""
Experiment Runner Framework

This module provides a framework for running experiments with:
- Multiple trials for statistical rigor
- Automatic computation of statistics (mean, std, CI)
- Checkpointing for long-running experiments
- Progress tracking
"""

import time
import json
import pickle
from pathlib import Path
from typing import Dict, List, Any, Callable, Tuple, Set
from datetime import datetime
import numpy as np
from scipy import stats
import pandas as pd
from tqdm import tqdm
import networkx as nx


class ExperimentRunner:
    """
    Framework for running edge cover algorithm experiments with statistical rigor.
    """

    def __init__(self, results_dir: str = 'results'):
        """
        Initialize experiment runner.

        Args:
            results_dir: Directory to save results
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        self.results = []

    def run_single_trial(
        self,
        graph: nx.Graph,
        algorithm_func: Callable,
        algorithm_name: str,
        graph_name: str,
        graph_properties: Dict[str, Any],
        **algo_params
    ) -> Dict[str, Any]:
        """
        Run a single trial of an algorithm on a graph.

        Args:
            graph: NetworkX graph
            algorithm_func: Algorithm function to run
            algorithm_name: Name of algorithm for logging
            graph_name: Name of graph for logging
            graph_properties: Graph property dictionary
            **algo_params: Parameters to pass to algorithm

        Returns:
            Dictionary with trial results including metrics
        """
        try:
            start_time = time.time()
            edge_cover, metrics = algorithm_func(graph, **algo_params)
            total_time = time.time() - start_time

            result = {
                'graph_name': graph_name,
                'algorithm': algorithm_name,
                'success': True,
                'cover_size': len(edge_cover),
                'runtime': total_time,
                'timestamp': datetime.now().isoformat(),
                **graph_properties,
                **metrics
            }

            return result

        except TimeoutError:
            return {
                'graph_name': graph_name,
                'algorithm': algorithm_name,
                'success': False,
                'error': 'timeout',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'graph_name': graph_name,
                'algorithm': algorithm_name,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def run_multi_trial(
        self,
        graph: nx.Graph,
        algorithm_func: Callable,
        algorithm_name: str,
        graph_name: str,
        graph_properties: Dict[str, Any],
        repetitions: int = 40,
        **algo_params
    ) -> List[Dict[str, Any]]:
        """
        Run multiple trials and collect results.

        Args:
            graph: NetworkX graph
            algorithm_func: Algorithm function
            algorithm_name: Algorithm name
            graph_name: Graph name
            graph_properties: Graph properties
            repetitions: Number of trials to run
            **algo_params: Algorithm parameters

        Returns:
            List of trial results
        """
        trial_results = []

        for rep in tqdm(range(repetitions), desc=f"{algorithm_name} on {graph_name}"):
            result = self.run_single_trial(
                graph, algorithm_func, algorithm_name, graph_name,
                graph_properties, **algo_params
            )
            result['repetition'] = rep
            trial_results.append(result)
            self.results.append(result)

        return trial_results

    def compute_statistics(self, trial_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute statistics from multiple trial results.

        Args:
            trial_results: List of trial result dictionaries

        Returns:
            Dictionary with mean, std, 95% CI, etc.
        """
        successful = [r for r in trial_results if r.get('success', False)]

        if not successful:
            return {'success_rate': 0.0, 'n_trials': len(trial_results)}

        cover_sizes = [r['cover_size'] for r in successful]
        runtimes = [r['runtime'] for r in successful]

        stats_dict = {
            'n_trials': len(trial_results),
            'n_successful': len(successful),
            'success_rate': len(successful) / len(trial_results),

            'cover_size_mean': np.mean(cover_sizes),
            'cover_size_std': np.std(cover_sizes, ddof=1),
            'cover_size_min': np.min(cover_sizes),
            'cover_size_max': np.max(cover_sizes),

            'runtime_mean': np.mean(runtimes),
            'runtime_std': np.std(runtimes, ddof=1),
            'runtime_min': np.min(runtimes),
            'runtime_max': np.max(runtimes),
        }

        # Compute 95% confidence intervals
        if len(successful) >= 2:
            cover_ci = stats.t.interval(
                0.95, len(cover_sizes) - 1,
                loc=stats_dict['cover_size_mean'],
                scale=stats.sem(cover_sizes)
            )
            runtime_ci = stats.t.interval(
                0.95, len(runtimes) - 1,
                loc=stats_dict['runtime_mean'],
                scale=stats.sem(runtimes)
            )

            stats_dict['cover_size_ci_lower'] = cover_ci[0]
            stats_dict['cover_size_ci_upper'] = cover_ci[1]
            stats_dict['runtime_ci_lower'] = runtime_ci[0]
            stats_dict['runtime_ci_upper'] = runtime_ci[1]

        return stats_dict

    def save_results(self, filename: str = None) -> None:
        """
        Save results to JSON file.

        Args:
            filename: Output filename (default: auto-generated with timestamp)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.json"

        filepath = self.results_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"Results saved to {filepath}")

    def save_checkpoint(self, checkpoint_file: str = None) -> None:
        """
        Save checkpoint of current results.

        Args:
            checkpoint_file: Checkpoint filename
        """
        if checkpoint_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            checkpoint_file = f"checkpoint_{timestamp}.pkl"

        filepath = self.results_dir / checkpoint_file

        with open(filepath, 'wb') as f:
            pickle.dump(self.results, f)

        print(f"Checkpoint saved to {filepath}")

    def load_checkpoint(self, checkpoint_file: str) -> None:
        """
        Load results from checkpoint.

        Args:
            checkpoint_file: Checkpoint filename
        """
        filepath = self.results_dir / checkpoint_file

        with open(filepath, 'rb') as f:
            self.results = pickle.load(f)

        print(f"Loaded {len(self.results)} results from {filepath}")

    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export results to pandas DataFrame for analysis.

        Returns:
            DataFrame with all results
        """
        return pd.DataFrame(self.results)
