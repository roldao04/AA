"""
Data loading utilities for Porto weather dataset.

This module provides functions to load, validate, and preprocess the
temperature data from porto.csv for use in all experiments.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from .config import (
    DATA_RAW_PATH,
    EXPECTED_TOTAL_OBS,
    EXPECTED_UNIQUE_TEMPS
)


def load_porto_temperatures(validate=True, verbose=True):
    """
    Load and validate minimum temperature data from Porto weather dataset.

    Parameters
    ----------
    validate : bool, default=True
        Whether to validate data characteristics against expected values
    verbose : bool, default=True
        Whether to print loading information

    Returns
    -------
    pd.Series
        Series containing minimum temperature values (mintempC)

    Raises
    ------
    FileNotFoundError
        If porto.csv is not found at DATA_RAW_PATH
    ValueError
        If validation fails and validate=True

    Notes
    -----
    - Automatically drops NaN values from mintempC column
    - Expected: 3,946 observations with 31 unique temperature values
    - See development_plan.md Phase 2 for data exploration requirements
    """
    # Check if file exists
    data_path = Path(DATA_RAW_PATH)
    if not data_path.exists():
        raise FileNotFoundError(
            f"Porto dataset not found at {DATA_RAW_PATH}. "
            f"Please ensure porto.csv is in the data/raw/ directory."
        )

    # Load dataset
    df = pd.read_csv(DATA_RAW_PATH)

    # Extract mintempC column and drop missing values
    if 'mintempC' not in df.columns:
        raise ValueError(
            f"Column 'mintempC' not found in dataset. "
            f"Available columns: {list(df.columns)}"
        )

    temps = df['mintempC'].dropna()

    # Validation
    if validate:
        n_obs = len(temps)
        n_unique = temps.nunique()

        # Check total observations
        if n_obs != EXPECTED_TOTAL_OBS:
            raise ValueError(
                f"Expected {EXPECTED_TOTAL_OBS} observations, found {n_obs}. "
                f"Dataset may be corrupted or incomplete."
            )

        # Check unique temperatures
        if n_unique != EXPECTED_UNIQUE_TEMPS:
            raise ValueError(
                f"Expected {EXPECTED_UNIQUE_TEMPS} unique temperatures, found {n_unique}. "
                f"Dataset characteristics differ from specification."
            )

    # Print loading information
    if verbose:
        print(f"✓ Loaded Porto weather data from {DATA_RAW_PATH}")
        print(f"  • Total observations: {len(temps)}")
        print(f"  • Unique temperatures: {temps.nunique()}")
        print(f"  • Temperature range: [{temps.min():.1f}°C, {temps.max():.1f}°C]")
        print(f"  • Missing values: {df['mintempC'].isna().sum()}")

    return temps


def get_temperature_stream(as_list=False):
    """
    Get temperature data as a stream (list or Series).

    Convenience function for streaming algorithm experiments.

    Parameters
    ----------
    as_list : bool, default=False
        If True, returns list. If False, returns pandas Series.

    Returns
    -------
    list or pd.Series
        Temperature values in original order
    """
    temps = load_porto_temperatures(verbose=False)

    if as_list:
        return temps.tolist()
    return temps


def get_exact_frequencies():
    """
    Compute exact frequency distribution of temperatures.

    Useful for validation and ground truth comparison.

    Returns
    -------
    pd.Series
        Series with temperatures as index and counts as values,
        sorted by count (descending)

    Examples
    --------
    >>> freqs = get_exact_frequencies()
    >>> print(freqs.head())
    12.0    450
    13.0    420
    ...
    """
    temps = load_porto_temperatures(verbose=False)
    freqs = temps.value_counts().sort_values(ascending=False)
    return freqs


if __name__ == "__main__":
    # Test data loading
    print("Testing data loader...")
    print("=" * 60)

    temps = load_porto_temperatures()

    print("\nExact frequency distribution (top 10):")
    print("-" * 60)
    freqs = get_exact_frequencies()
    print(freqs.head(10))

    print("\n" + "=" * 60)
    print("✓ Data loader test complete!")
