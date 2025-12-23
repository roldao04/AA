"""
Exact Counter Implementation.

This module implements the baseline exact counting algorithm that maintains
a dictionary of exact frequencies for all items seen in a stream. This serves
as the ground truth for comparing approximate counting algorithms.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import json
from typing import Dict, List, Tuple, Union
import pandas as pd
import numpy as np


class ExactCounter:
    """
    Exact frequency counter using a dictionary.

    This class maintains exact counts for all unique items seen in a stream.
    It serves as the baseline ground truth for evaluating approximate counting
    algorithms.

    Attributes
    ----------
    counts : Dict[int, int]
        Dictionary mapping temperature values to their exact counts

    Examples
    --------
    >>> counter = ExactCounter()
    >>> counter.process_stream([12, 15, 12, 18, 15, 12])
    >>> counter.get_count(12)
    3
    >>> counter.get_top_k(2)
    [(12, 3), (15, 2)]
    """

    def __init__(self):
        """Initialize an empty exact counter."""
        self.counts: Dict[int, int] = {}

    def process(self, temperature: int) -> None:
        """
        Process a single temperature value from the stream.

        Increments the counter for the given temperature, creating a new
        entry if this temperature is seen for the first time.

        Parameters
        ----------
        temperature : int
            Temperature value to count

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process(15)
        >>> counter.get_count(15)
        1
        """
        self.counts[temperature] = self.counts.get(temperature, 0) + 1

    def process_stream(self, temperatures: Union[list, pd.Series, np.ndarray]) -> None:
        """
        Process a stream of temperature values.

        Processes each temperature in the input sequence by calling process()
        for each element. Accepts lists, pandas Series, or numpy arrays.

        Parameters
        ----------
        temperatures : list, pd.Series, or np.ndarray
            Sequence of temperature values to process

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12, 18])
        >>> counter.get_count(12)
        2
        """
        for temp in temperatures:
            self.process(temp)

    def get_count(self, temperature: int) -> int:
        """
        Get the exact count for a specific temperature.

        Parameters
        ----------
        temperature : int
            Temperature value to query

        Returns
        -------
        int
            Exact count for this temperature, or 0 if never seen

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12])
        >>> counter.get_count(12)
        2
        >>> counter.get_count(99)
        0
        """
        return self.counts.get(temperature, 0)

    def get_top_k(self, n: int) -> List[Tuple[int, int]]:
        """
        Get the n most frequent temperatures.

        Returns temperatures sorted by frequency (descending), with ties
        broken by temperature value (ascending) for consistency.

        Parameters
        ----------
        n : int
            Number of top items to return

        Returns
        -------
        List[Tuple[int, int]]
            List of (temperature, count) tuples, sorted by count descending

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12, 18, 15, 12])
        >>> counter.get_top_k(2)
        [(12, 3), (15, 2)]
        """
        # Sort by count (descending), then by temperature (ascending) for tie-breaking
        sorted_items = sorted(
            self.counts.items(),
            key=lambda item: (-item[1], item[0])
        )
        return sorted_items[:n]

    def get_all_counts(self) -> Dict[int, int]:
        """
        Get the complete dictionary of all counts.

        Returns
        -------
        Dict[int, int]
            Dictionary mapping temperatures to their exact counts

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12])
        >>> counter.get_all_counts()
        {12: 2, 15: 1}
        """
        return dict(self.counts)

    def save_to_csv(self, filepath: str) -> None:
        """
        Save frequency distribution to CSV file.

        Creates a CSV with columns 'temperature' and 'count', sorted by
        count in descending order.

        Parameters
        ----------
        filepath : str
            Path to output CSV file

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12])
        >>> counter.save_to_csv('results/exact/counts.csv')
        """
        # Convert to DataFrame for easy CSV export
        df = pd.DataFrame(
            list(self.counts.items()),
            columns=['temperature', 'count']
        )

        # Sort by count (descending), then by temperature (ascending)
        df = df.sort_values(
            by=['count', 'temperature'],
            ascending=[False, True]
        )

        # Save to CSV
        df.to_csv(filepath, index=False)

    def save_statistics(self, filepath: str) -> None:
        """
        Save summary statistics to JSON file.

        Exports comprehensive statistics including total observations,
        unique values, top-10 items, min/max counts, and cumulative
        coverage percentages.

        Parameters
        ----------
        filepath : str
            Path to output JSON file

        Examples
        --------
        >>> counter = ExactCounter()
        >>> counter.process_stream([12, 15, 12, 18])
        >>> counter.save_statistics('results/exact/stats.json')
        """
        # Calculate statistics
        total_obs = sum(self.counts.values())
        unique_values = len(self.counts)

        # Get top-10
        top_10 = self.get_top_k(10)

        # Get min and max counts
        if self.counts:
            min_count = min(self.counts.values())
            max_count = max(self.counts.values())
        else:
            min_count = 0
            max_count = 0

        # Calculate cumulative percentages for top-5, 10, 15, 20
        cumulative_coverage = {}
        for n in [5, 10, 15, 20]:
            top_n = self.get_top_k(n)
            top_n_sum = sum(count for _, count in top_n)
            coverage_pct = (top_n_sum / total_obs * 100) if total_obs > 0 else 0
            cumulative_coverage[f'top_{n}'] = round(coverage_pct, 2)

        # Build statistics dictionary
        stats = {
            'total_observations': total_obs,
            'unique_values': unique_values,
            'min_count': min_count,
            'max_count': max_count,
            'top_10': [
                {'temperature': temp, 'count': count}
                for temp, count in top_10
            ],
            'cumulative_coverage': cumulative_coverage
        }

        # Save to JSON with pretty formatting
        with open(filepath, 'w') as f:
            json.dump(stats, f, indent=2)

    def __len__(self) -> int:
        """Return the number of unique temperatures seen."""
        return len(self.counts)

    def __repr__(self) -> str:
        """Return string representation of the counter."""
        total_obs = sum(self.counts.values())
        unique_temps = len(self.counts)
        return f"ExactCounter(observations={total_obs}, unique_temps={unique_temps})"
