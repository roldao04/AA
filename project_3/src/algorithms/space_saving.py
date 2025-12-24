"""
Space-Saving Algorithm Implementation.

This module implements the Space-Saving algorithm for identifying frequent items
in a data stream using limited memory. The algorithm maintains k counters and
provides deterministic guarantees about capturing high-frequency items.

Reference:
    Metwally, A., Agrawal, D., & Abbadi, A. E. (2005).
    Efficient computation of frequent and top-k elements in data streams.
    International Conference on Database Theory (ICDT).

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

from typing import Dict, List, Tuple, Union
import pandas as pd
import numpy as np


class SpaceSaving:
    """
    Space-Saving algorithm for frequent items in streams.

    Maintains exactly k counters (monitored items) with associated counts and
    error bounds. Guarantees that all items with frequency > N/k are captured,
    where N is the stream length.

    Theoretical Properties:
    - All items with frequency > N/k are guaranteed to be monitored
    - Maximum overestimation error ≤ N/k
    - Per-item error bounds tracked explicitly
    - Deterministic (no randomness)

    Attributes
    ----------
    k : int
        Space budget (maximum number of items to monitor)
    monitored : Dict[int, Tuple[int, int]]
        Dictionary mapping temperature -> (count, error)
        count: estimated frequency
        error: maximum possible overestimation
    stream_length : int
        Total number of items processed so far

    Parameters
    ----------
    k : int
        Maximum number of items to monitor (must be >= 1)

    Examples
    --------
    >>> ss = SpaceSaving(k=3)
    >>> for temp in [12, 15, 12, 18, 15, 12]:
    ...     ss.process(temp)
    >>> ss.get_top_n(2)  # doctest: +SKIP
    [(12, (3, 0)), (15, (2, 0))]
    """

    def __init__(self, k: int):
        """
        Initialize Space-Saving with space budget k.

        Parameters
        ----------
        k : int
            Maximum number of items to monitor (must be >= 1)

        Raises
        ------
        ValueError
            If k < 1
        """
        if k < 1:
            raise ValueError(f"Space budget k must be >= 1, got {k}")

        self.k = k
        self.monitored: Dict[int, Tuple[int, int]] = {}
        self.stream_length = 0

    def process(self, temperature: int) -> None:
        """
        Process a single temperature value from the stream.

        Implements the Space-Saving update rule:
        - If temperature is already monitored: increment count, preserve error
        - If not monitored and space available: add with (count=1, error=0)
        - If not monitored and full: evict minimum, add new item with
          (count=min_count+1, error=min_count)

        Parameters
        ----------
        temperature : int
            Temperature value to process

        Examples
        --------
        >>> ss = SpaceSaving(k=2)
        >>> ss.process(12)
        >>> ss.monitored[12]
        (1, 0)
        >>> ss.process(15)
        >>> ss.process(12)
        >>> ss.monitored[12]
        (2, 0)
        """
        self.stream_length += 1

        if temperature in self.monitored:
            # Already monitoring: increment count, preserve error
            count, error = self.monitored[temperature]
            self.monitored[temperature] = (count + 1, error)

        elif len(self.monitored) < self.k:
            # Have space: add new item with no error
            self.monitored[temperature] = (1, 0)

        else:
            # No space: evict minimum and add new item
            # Find item with minimum count
            min_temp = min(self.monitored.keys(),
                          key=lambda t: self.monitored[t][0])
            min_count, _ = self.monitored[min_temp]

            # Evict minimum
            del self.monitored[min_temp]

            # Add new item with inherited count and error
            self.monitored[temperature] = (min_count + 1, min_count)

    def process_stream(self, temperatures: Union[list, pd.Series, np.ndarray]) -> None:
        """
        Process a stream of temperature values.

        Processes each temperature in order by calling process() for each element.

        Parameters
        ----------
        temperatures : list, pd.Series, or np.ndarray
            Sequence of temperature values to process

        Examples
        --------
        >>> ss = SpaceSaving(k=3)
        >>> ss.process_stream([12, 15, 12, 18])
        >>> len(ss.monitored)
        3
        """
        for temp in temperatures:
            self.process(temp)

    def get_count(self, temperature: int) -> int:
        """
        Get the estimated count for a specific temperature.

        Parameters
        ----------
        temperature : int
            Temperature value to query

        Returns
        -------
        int
            Estimated count (0 if not monitored)

        Examples
        --------
        >>> ss = SpaceSaving(k=2)
        >>> ss.monitored[12] = (5, 1)
        >>> ss.get_count(12)
        5
        >>> ss.get_count(99)
        0
        """
        if temperature not in self.monitored:
            return 0
        return self.monitored[temperature][0]

    def get_error_bound(self, temperature: int) -> int:
        """
        Get the error bound for a specific temperature.

        The error bound represents the maximum possible overestimation
        of the true count.

        Parameters
        ----------
        temperature : int
            Temperature value to query

        Returns
        -------
        int
            Maximum overestimation error (0 if not monitored)

        Examples
        --------
        >>> ss = SpaceSaving(k=2)
        >>> ss.monitored[12] = (5, 1)
        >>> ss.get_error_bound(12)
        1
        """
        if temperature not in self.monitored:
            return 0
        return self.monitored[temperature][1]

    def get_top_n(self, n: int) -> List[Tuple[int, Tuple[int, int]]]:
        """
        Get the n most frequent items with their counts and error bounds.

        Items are sorted by count in descending order.

        Parameters
        ----------
        n : int
            Number of top items to return

        Returns
        -------
        List[Tuple[int, Tuple[int, int]]]
            List of (temperature, (count, error)) tuples
            Sorted by count (descending)

        Raises
        ------
        ValueError
            If n > k (cannot report more items than monitored)

        Examples
        --------
        >>> ss = SpaceSaving(k=3)
        >>> ss.monitored = {12: (5, 0), 15: (3, 0), 18: (2, 1)}
        >>> ss.get_top_n(2)
        [(12, (5, 0)), (15, (3, 0))]
        """
        if n > self.k:
            raise ValueError(f"Cannot query top-{n} with k={self.k} (n must be <= k)")

        # Sort by count descending
        sorted_items = sorted(
            self.monitored.items(),
            key=lambda item: item[1][0],  # Sort by count
            reverse=True
        )

        return sorted_items[:n]

    def get_monitored_items(self) -> Dict[int, Tuple[int, int]]:
        """
        Get all monitored items with their counts and error bounds.

        Returns
        -------
        Dict[int, Tuple[int, int]]
            Copy of monitored dictionary: {temperature: (count, error)}

        Examples
        --------
        >>> ss = SpaceSaving(k=2)
        >>> ss.monitored = {12: (5, 0), 15: (3, 1)}
        >>> ss.get_monitored_items()
        {12: (5, 0), 15: (3, 1)}
        """
        return dict(self.monitored)

    def get_all_with_bounds(self) -> pd.DataFrame:
        """
        Get all monitored items as a DataFrame with separate columns.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: temperature, count, error
            Sorted by count (descending)

        Examples
        --------
        >>> ss = SpaceSaving(k=2)
        >>> ss.monitored = {12: (5, 0), 15: (3, 1)}
        >>> df = ss.get_all_with_bounds()
        >>> list(df.columns)
        ['temperature', 'count', 'error']
        """
        data = []
        for temp, (count, error) in self.monitored.items():
            data.append({
                'temperature': temp,
                'count': count,
                'error': error
            })

        df = pd.DataFrame(data)
        if len(df) > 0:
            df = df.sort_values('count', ascending=False).reset_index(drop=True)
        return df

    def get_max_error_theoretical(self) -> float:
        """
        Get the theoretical maximum error bound (N/k).

        Returns
        -------
        float
            Theoretical maximum overestimation = stream_length / k

        Examples
        --------
        >>> ss = SpaceSaving(k=10)
        >>> ss.stream_length = 100
        >>> ss.get_max_error_theoretical()
        10.0
        """
        if self.stream_length == 0:
            return 0.0
        return self.stream_length / self.k

    def get_max_error_actual(self) -> int:
        """
        Get the actual maximum error bound among all monitored items.

        Returns
        -------
        int
            Maximum error bound across all monitored items

        Examples
        --------
        >>> ss = SpaceSaving(k=3)
        >>> ss.monitored = {12: (5, 0), 15: (3, 1), 18: (2, 2)}
        >>> ss.get_max_error_actual()
        2
        """
        if not self.monitored:
            return 0
        return max(error for _, error in self.monitored.values())

    def __len__(self) -> int:
        """Return the number of currently monitored items."""
        return len(self.monitored)

    def __repr__(self) -> str:
        """Return string representation of the Space-Saving instance."""
        total_count = sum(count for count, _ in self.monitored.values())
        max_error = self.get_max_error_actual()
        return (f"SpaceSaving(k={self.k}, "
                f"monitored={len(self)}/{self.k}, "
                f"stream_length={self.stream_length}, "
                f"total_monitored_count={total_count}, "
                f"max_error={max_error})")
