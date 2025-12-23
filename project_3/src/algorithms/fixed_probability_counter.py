"""
Fixed Probability Counter Implementation.

This module implements a probabilistic counting algorithm that increments
counters with a fixed probability p, providing space-efficient approximate
counting with unbiased estimates.

Author: Joao Roldao (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import random
from typing import Dict, Union
import pandas as pd
import numpy as np


class FixedProbabilityCounter:
    """
    Probabilistic counter that increments with fixed probability p.

    This class maintains separate probabilistic counters for each unique item,
    where each counter increments with probability p. The estimate is obtained
    by dividing the counter value by p, giving an unbiased estimator of the
    true count.

    Theoretical Properties:
    - Unbiased: E[estimate] = true_count
    - Variance: Var[estimate] = (1-p)/p * true_count
    - Relative error ∝ 1/√n for large n

    Attributes
    ----------
    p : float
        Probability of incrementing (0 < p <= 1)
    counters : Dict[int, int]
        Dictionary mapping items to their probabilistic counter values

    Parameters
    ----------
    p : float, default=0.25
        Fixed probability of incrementing (must be in (0, 1])

    Examples
    --------
    >>> counter = FixedProbabilityCounter(p=0.25)
    >>> random.seed(42)
    >>> for temp in [12, 15, 12, 12, 15]:
    ...     counter.process(temp)
    >>> counter.estimate(12)  # doctest: +SKIP
    3.0  # Approximately, depends on random outcomes
    """

    def __init__(self, p: float = 0.25):
        """
        Initialize fixed probability counter.

        Parameters
        ----------
        p : float, default=0.25
            Probability of incrementing (must be in (0, 1])

        Raises
        ------
        ValueError
            If p is not in the valid range (0, 1]
        """
        if not 0 < p <= 1:
            raise ValueError(f"Probability p must be in (0, 1], got {p}")

        self.p = p
        self.counters: Dict[int, int] = {}

    def process(self, temperature: int) -> None:
        """
        Process a single temperature value from the stream.

        With probability p, increments the counter for this temperature.
        Otherwise, leaves the counter unchanged.

        Parameters
        ----------
        temperature : int
            Temperature value to process

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.5)
        >>> random.seed(42)
        >>> counter.process(15)
        >>> counter.counters[15]  # doctest: +SKIP
        1  # or 0, depending on random outcome
        """
        # Initialize counter if this is first occurrence
        if temperature not in self.counters:
            self.counters[temperature] = 0

        # Probabilistic increment
        if random.random() < self.p:
            self.counters[temperature] += 1

    def process_stream(self, temperatures: Union[list, pd.Series, np.ndarray]) -> None:
        """
        Process a stream of temperature values.

        Processes each temperature in the input sequence by calling process()
        for each element.

        Parameters
        ----------
        temperatures : list, pd.Series, or np.ndarray
            Sequence of temperature values to process

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> random.seed(42)
        >>> counter.process_stream([12, 15, 12, 18])
        >>> len(counter.counters)  # doctest: +SKIP
        3  # All three unique temperatures seen
        """
        for temp in temperatures:
            self.process(temp)

    def estimate(self, temperature: int) -> float:
        """
        Get the estimated count for a specific temperature.

        Returns the unbiased estimate by dividing the counter value by p.

        Parameters
        ----------
        temperature : int
            Temperature value to query

        Returns
        -------
        float
            Estimated count for this temperature (counter / p)

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> counter.counters[15] = 10  # Directly set for example
        >>> counter.estimate(15)
        40.0
        >>> counter.estimate(99)  # Never seen
        0.0
        """
        if temperature not in self.counters:
            return 0.0
        return self.counters[temperature] / self.p

    def get_all_estimates(self) -> Dict[int, float]:
        """
        Get estimated counts for all temperatures.

        Returns
        -------
        Dict[int, float]
            Dictionary mapping temperatures to their estimated counts

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> counter.counters = {12: 5, 15: 3}
        >>> counter.get_all_estimates()
        {12: 20.0, 15: 12.0}
        """
        return {temp: self.counters[temp] / self.p
                for temp in self.counters}

    def get_counter_value(self, temperature: int) -> int:
        """
        Get the raw counter value (before scaling by 1/p).

        Useful for debugging and understanding the probabilistic behavior.

        Parameters
        ----------
        temperature : int
            Temperature to query

        Returns
        -------
        int
            Raw counter value

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> counter.counters[15] = 10
        >>> counter.get_counter_value(15)
        10
        """
        return self.counters.get(temperature, 0)

    def reset(self) -> None:
        """
        Reset all counters to start a fresh trial.

        Clears all counters while keeping the probability parameter p.

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> counter.counters = {12: 5, 15: 3}
        >>> counter.reset()
        >>> len(counter.counters)
        0
        >>> counter.p
        0.25
        """
        self.counters = {}

    def get_variance_theoretical(self, true_count: int) -> float:
        """
        Calculate theoretical variance for a given true count.

        Theoretical variance: Var = (1-p)/p * n

        Parameters
        ----------
        true_count : int
            True frequency of an item

        Returns
        -------
        float
            Theoretical variance of the estimate

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> counter.get_variance_theoretical(100)
        300.0
        """
        return ((1 - self.p) / self.p) * true_count

    def get_std_theoretical(self, true_count: int) -> float:
        """
        Calculate theoretical standard deviation for a given true count.

        Parameters
        ----------
        true_count : int
            True frequency of an item

        Returns
        -------
        float
            Theoretical standard deviation of the estimate

        Examples
        --------
        >>> counter = FixedProbabilityCounter(p=0.25)
        >>> round(counter.get_std_theoretical(100), 2)
        17.32
        """
        return np.sqrt(self.get_variance_theoretical(true_count))

    def __len__(self) -> int:
        """Return the number of unique temperatures seen."""
        return len(self.counters)

    def __repr__(self) -> str:
        """Return string representation of the counter."""
        total_raw = sum(self.counters.values())
        total_est = sum(self.get_all_estimates().values())
        return (f"FixedProbabilityCounter(p={self.p}, "
                f"unique_items={len(self)}, "
                f"raw_counts={total_raw}, "
                f"estimated_total={total_est:.1f})")
