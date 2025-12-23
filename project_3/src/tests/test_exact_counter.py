"""
Unit tests for ExactCounter class.

Tests the baseline exact counting implementation to ensure correctness
before using it as ground truth for approximate algorithm evaluation.

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import pytest
import pandas as pd
import numpy as np
import json
import tempfile
import os
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms.exact_counter import ExactCounter


class TestExactCounterBasic:
    """Basic functionality tests for ExactCounter."""

    def test_initialization(self):
        """Test that counter initializes with empty counts."""
        counter = ExactCounter()
        assert len(counter) == 0
        assert counter.get_all_counts() == {}

    def test_process_single_value(self):
        """Test processing a single temperature value."""
        counter = ExactCounter()
        counter.process(15)
        assert counter.get_count(15) == 1
        assert len(counter) == 1

    def test_process_multiple_same_value(self):
        """Test processing the same temperature multiple times."""
        counter = ExactCounter()
        counter.process(15)
        counter.process(15)
        counter.process(15)
        assert counter.get_count(15) == 3
        assert len(counter) == 1

    def test_process_different_values(self):
        """Test processing different temperature values."""
        counter = ExactCounter()
        counter.process(12)
        counter.process(15)
        counter.process(18)
        assert counter.get_count(12) == 1
        assert counter.get_count(15) == 1
        assert counter.get_count(18) == 1
        assert len(counter) == 3

    def test_get_count_nonexistent(self):
        """Test querying count for temperature that was never seen."""
        counter = ExactCounter()
        counter.process(15)
        assert counter.get_count(99) == 0


class TestExactCounterStream:
    """Tests for stream processing functionality."""

    def test_process_stream_list(self):
        """Test processing a list of temperatures."""
        counter = ExactCounter()
        temps = [12, 15, 12, 18, 15, 12]
        counter.process_stream(temps)
        assert counter.get_count(12) == 3
        assert counter.get_count(15) == 2
        assert counter.get_count(18) == 1

    def test_process_stream_pandas_series(self):
        """Test processing a pandas Series."""
        counter = ExactCounter()
        temps = pd.Series([12, 15, 12, 18, 15, 12])
        counter.process_stream(temps)
        assert counter.get_count(12) == 3
        assert counter.get_count(15) == 2
        assert counter.get_count(18) == 1

    def test_process_stream_numpy_array(self):
        """Test processing a numpy array."""
        counter = ExactCounter()
        temps = np.array([12, 15, 12, 18, 15, 12])
        counter.process_stream(temps)
        assert counter.get_count(12) == 3
        assert counter.get_count(15) == 2
        assert counter.get_count(18) == 1

    def test_process_stream_empty(self):
        """Test processing an empty stream."""
        counter = ExactCounter()
        counter.process_stream([])
        assert len(counter) == 0


class TestExactCounterEdgeCases:
    """Edge case tests as specified in development plan."""

    def test_single_value_once(self):
        """Test counting a single value that appears once."""
        counter = ExactCounter()
        counter.process(15)
        assert counter.get_count(15) == 1
        assert len(counter) == 1

    def test_all_values_same(self):
        """Test when all values are identical."""
        counter = ExactCounter()
        counter.process_stream([15, 15, 15, 15, 15])
        assert counter.get_count(15) == 5
        assert len(counter) == 1

    def test_all_values_different(self):
        """Test when all values are unique."""
        counter = ExactCounter()
        counter.process_stream([10, 11, 12, 13, 14])
        assert len(counter) == 5
        for temp in [10, 11, 12, 13, 14]:
            assert counter.get_count(temp) == 1

    def test_known_frequencies(self):
        """Test with dataset with known frequencies: 5×15°C, 3×12°C, 2×18°C."""
        counter = ExactCounter()
        test_data = [15] * 5 + [12] * 3 + [18] * 2
        counter.process_stream(test_data)

        assert counter.get_count(15) == 5
        assert counter.get_count(12) == 3
        assert counter.get_count(18) == 2
        assert len(counter) == 3


class TestExactCounterTopK:
    """Tests for get_top_k functionality."""

    def test_get_top_k_basic(self):
        """Test getting top-k items."""
        counter = ExactCounter()
        counter.process_stream([12, 15, 12, 18, 15, 12])
        top_2 = counter.get_top_k(2)
        assert top_2 == [(12, 3), (15, 2)]

    def test_get_top_k_ordering(self):
        """Test that top-k returns items in correct order."""
        counter = ExactCounter()
        counter.process_stream([10, 11, 10, 12, 10, 11, 10])
        top_3 = counter.get_top_k(3)
        assert top_3[0] == (10, 4)  # Most frequent
        assert top_3[1] == (11, 2)  # Second most
        assert top_3[2] == (12, 1)  # Least frequent

    def test_get_top_k_tie_breaking(self):
        """Test tie-breaking by temperature (ascending) when counts are equal."""
        counter = ExactCounter()
        counter.process_stream([15, 12, 18])  # All have count=1
        top_3 = counter.get_top_k(3)

        # All have same count, should be sorted by temperature ascending
        assert top_3 == [(12, 1), (15, 1), (18, 1)]

    def test_get_top_k_more_than_available(self):
        """Test requesting more items than available."""
        counter = ExactCounter()
        counter.process_stream([12, 15])
        top_10 = counter.get_top_k(10)
        assert len(top_10) == 2  # Only 2 items available

    def test_get_top_k_zero(self):
        """Test requesting top-0 items."""
        counter = ExactCounter()
        counter.process_stream([12, 15, 18])
        top_0 = counter.get_top_k(0)
        assert top_0 == []


class TestExactCounterExport:
    """Tests for CSV and JSON export functionality."""

    def test_save_to_csv(self):
        """Test saving frequency distribution to CSV."""
        counter = ExactCounter()
        counter.process_stream([12, 15, 12, 18, 15, 12])

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, 'test_counts.csv')
            counter.save_to_csv(csv_path)

            # Verify file was created
            assert os.path.exists(csv_path)

            # Load and verify contents
            df = pd.read_csv(csv_path)
            assert list(df.columns) == ['temperature', 'count']
            assert len(df) == 3

            # Verify sorting (by count descending, temp ascending)
            assert df.iloc[0]['temperature'] == 12
            assert df.iloc[0]['count'] == 3
            assert df.iloc[1]['temperature'] == 15
            assert df.iloc[1]['count'] == 2

    def test_save_statistics(self):
        """Test saving statistics to JSON."""
        counter = ExactCounter()
        counter.process_stream([12, 15, 12, 18, 15, 12])

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, 'test_stats.json')
            counter.save_statistics(json_path)

            # Verify file was created
            assert os.path.exists(json_path)

            # Load and verify contents
            with open(json_path, 'r') as f:
                stats = json.load(f)

            assert stats['total_observations'] == 6
            assert stats['unique_values'] == 3
            assert stats['min_count'] == 1
            assert stats['max_count'] == 3
            assert len(stats['top_10']) == 3  # Only 3 unique temps
            assert 'cumulative_coverage' in stats

    def test_statistics_cumulative_coverage(self):
        """Test that cumulative coverage is calculated correctly."""
        counter = ExactCounter()
        # Create dataset: 10 items total, 5 at temp 10, 3 at temp 11, 2 at temp 12
        counter.process_stream([10]*5 + [11]*3 + [12]*2)

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, 'test_stats.json')
            counter.save_statistics(json_path)

            with open(json_path, 'r') as f:
                stats = json.load(f)

            # Top-5 should include all 3 items = 100%
            assert stats['cumulative_coverage']['top_5'] == 100.0
            # Top-10 should include all 3 items = 100%
            assert stats['cumulative_coverage']['top_10'] == 100.0


class TestExactCounterRepr:
    """Tests for string representation."""

    def test_repr(self):
        """Test string representation."""
        counter = ExactCounter()
        counter.process_stream([12, 15, 12, 18])
        repr_str = repr(counter)
        assert 'ExactCounter' in repr_str
        assert 'observations=4' in repr_str
        assert 'unique_temps=3' in repr_str


class TestExactCounterIntegration:
    """Integration tests using realistic scenarios."""

    def test_realistic_scenario(self):
        """Test with a realistic temperature dataset."""
        # Simulate a week of temperature readings (7 days)
        temps = [12, 15, 13, 14, 15, 16, 14]
        counter = ExactCounter()
        counter.process_stream(temps)

        # Verify counts
        assert counter.get_count(15) == 2
        assert counter.get_count(14) == 2
        assert sum(counter.get_all_counts().values()) == 7

        # Verify top-3
        top_3 = counter.get_top_k(3)
        assert len(top_3) == 3

    def test_large_stream(self):
        """Test with a larger stream to verify performance."""
        # Generate 1000 random temperatures between 10-20
        np.random.seed(42)
        temps = np.random.randint(10, 21, size=1000)
        counter = ExactCounter()
        counter.process_stream(temps)

        # Verify basic properties
        assert len(counter) <= 11  # At most 11 unique values (10-20)
        assert sum(counter.get_all_counts().values()) == 1000

        # Verify top-5 is valid
        top_5 = counter.get_top_k(5)
        assert len(top_5) == 5
        # Verify descending order
        for i in range(len(top_5) - 1):
            assert top_5[i][1] >= top_5[i + 1][1]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
