"""
Unit tests for Space-Saving Algorithm.

Tests the correctness of the Space-Saving implementation including:
- Basic functionality (process, query)
- Edge cases (empty, single value, all unique, all same)
- Error bound validation
- Capture guarantees
- Theoretical property validation

Author: João Roldão (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import pytest
import numpy as np
import pandas as pd
from src.algorithms.space_saving import SpaceSaving


class TestSpaceSavingBasic:
    """Test basic functionality of Space-Saving."""

    def test_initialization(self):
        """Test proper initialization."""
        ss = SpaceSaving(k=10)
        assert ss.k == 10
        assert len(ss.monitored) == 0
        assert ss.stream_length == 0

    def test_initialization_invalid_k(self):
        """Test that k < 1 raises ValueError."""
        with pytest.raises(ValueError):
            SpaceSaving(k=0)
        with pytest.raises(ValueError):
            SpaceSaving(k=-5)

    def test_process_single_item(self):
        """Test processing a single item."""
        ss = SpaceSaving(k=5)
        ss.process(12)
        assert len(ss.monitored) == 1
        assert ss.monitored[12] == (1, 0)
        assert ss.stream_length == 1

    def test_process_within_capacity(self):
        """Test processing when k is not exceeded."""
        ss = SpaceSaving(k=5)
        for temp in [12, 15, 12, 18]:
            ss.process(temp)

        assert len(ss.monitored) == 3  # Three unique items
        assert ss.monitored[12] == (2, 0)  # 12 appears twice
        assert ss.monitored[15] == (1, 0)  # 15 appears once
        assert ss.monitored[18] == (1, 0)  # 18 appears once
        assert ss.stream_length == 4

    def test_process_stream(self):
        """Test processing a stream."""
        ss = SpaceSaving(k=5)
        temps = [12, 15, 12, 18, 15, 12]
        ss.process_stream(temps)

        assert ss.stream_length == 6
        assert ss.monitored[12] == (3, 0)
        assert ss.monitored[15] == (2, 0)
        assert ss.monitored[18] == (1, 0)

    def test_process_with_eviction(self):
        """Test eviction when k is exceeded."""
        ss = SpaceSaving(k=2)
        # Process: 12, 15, 18
        # After 12, 15: monitored = {12: (1,0), 15: (1,0)}
        # After 18: evict one with min count, add 18 with (min_count+1, min_count)
        ss.process(12)
        ss.process(15)
        assert len(ss.monitored) == 2

        ss.process(18)
        # One item should be evicted, 18 added with (2, 1)
        assert len(ss.monitored) == 2
        assert 18 in ss.monitored
        count_18, error_18 = ss.monitored[18]
        assert count_18 == 2  # min_count + 1
        assert error_18 == 1  # min_count


class TestSpaceSavingQuery:
    """Test query methods."""

    def test_get_count(self):
        """Test getting counts for monitored items."""
        ss = SpaceSaving(k=5)
        ss.monitored = {12: (5, 0), 15: (3, 1)}
        assert ss.get_count(12) == 5
        assert ss.get_count(15) == 3
        assert ss.get_count(99) == 0  # Not monitored

    def test_get_error_bound(self):
        """Test getting error bounds."""
        ss = SpaceSaving(k=5)
        ss.monitored = {12: (5, 0), 15: (3, 1), 18: (2, 2)}
        assert ss.get_error_bound(12) == 0
        assert ss.get_error_bound(15) == 1
        assert ss.get_error_bound(18) == 2
        assert ss.get_error_bound(99) == 0

    def test_get_top_n(self):
        """Test getting top-n items."""
        ss = SpaceSaving(k=5)
        ss.monitored = {12: (10, 0), 15: (7, 0), 18: (5, 1), 20: (3, 2)}

        top_2 = ss.get_top_n(2)
        assert len(top_2) == 2
        assert top_2[0] == (12, (10, 0))
        assert top_2[1] == (15, (7, 0))

        top_3 = ss.get_top_n(3)
        assert len(top_3) == 3
        assert top_3[2] == (18, (5, 1))

    def test_get_top_n_invalid(self):
        """Test that n > k raises ValueError."""
        ss = SpaceSaving(k=3)
        with pytest.raises(ValueError):
            ss.get_top_n(5)

    def test_get_monitored_items(self):
        """Test getting all monitored items."""
        ss = SpaceSaving(k=3)
        ss.monitored = {12: (5, 0), 15: (3, 1)}
        items = ss.get_monitored_items()
        assert items == {12: (5, 0), 15: (3, 1)}
        # Should return a copy
        items[99] = (1, 0)
        assert 99 not in ss.monitored

    def test_get_all_with_bounds(self):
        """Test DataFrame output."""
        ss = SpaceSaving(k=3)
        ss.monitored = {12: (10, 0), 15: (7, 1), 18: (5, 2)}
        df = ss.get_all_with_bounds()

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['temperature', 'count', 'error']
        assert len(df) == 3
        # Should be sorted by count descending
        assert df.iloc[0]['temperature'] == 12
        assert df.iloc[0]['count'] == 10


class TestSpaceSavingEdgeCases:
    """Test edge cases."""

    def test_empty_stream(self):
        """Test with no items processed."""
        ss = SpaceSaving(k=5)
        assert len(ss.monitored) == 0
        assert ss.stream_length == 0
        assert ss.get_top_n(0) == []

    def test_single_unique_value(self):
        """Test stream with all same values."""
        ss = SpaceSaving(k=3)
        ss.process_stream([12] * 100)
        assert len(ss.monitored) == 1
        assert ss.monitored[12] == (100, 0)

    def test_all_unique_values(self):
        """Test stream with all unique values."""
        ss = SpaceSaving(k=5)
        temps = list(range(1, 11))  # 10 unique values
        ss.process_stream(temps)

        # Should monitor exactly k=5 items
        assert len(ss.monitored) == 5
        # All monitored items should have some error bound
        # because items were evicted

    def test_k_equals_unique_items(self):
        """Test when k equals number of unique items."""
        ss = SpaceSaving(k=3)
        ss.process_stream([12, 15, 18, 12, 15, 18])

        # Should capture all 3 items perfectly
        assert len(ss.monitored) == 3
        assert ss.monitored[12] == (2, 0)
        assert ss.monitored[15] == (2, 0)
        assert ss.monitored[18] == (2, 0)

    def test_pandas_series_input(self):
        """Test processing pandas Series."""
        ss = SpaceSaving(k=5)
        temps = pd.Series([12, 15, 12, 18])
        ss.process_stream(temps)
        assert ss.stream_length == 4
        assert ss.monitored[12][0] == 2

    def test_numpy_array_input(self):
        """Test processing numpy array."""
        ss = SpaceSaving(k=5)
        temps = np.array([12, 15, 12, 18])
        ss.process_stream(temps)
        assert ss.stream_length == 4
        assert ss.monitored[12][0] == 2


class TestSpaceSavingGuarantees:
    """Test theoretical guarantees."""

    def test_max_error_theoretical(self):
        """Test theoretical max error calculation."""
        ss = SpaceSaving(k=10)
        ss.stream_length = 1000
        assert ss.get_max_error_theoretical() == 100.0

        ss2 = SpaceSaving(k=20)
        ss2.stream_length = 1000
        assert ss2.get_max_error_theoretical() == 50.0

    def test_max_error_actual(self):
        """Test actual max error among monitored items."""
        ss = SpaceSaving(k=5)
        ss.monitored = {12: (10, 0), 15: (8, 2), 18: (6, 5), 20: (4, 3)}
        assert ss.get_max_error_actual() == 5

    def test_error_bound_never_exceeds_theoretical(self):
        """Test that actual error bounds don't exceed N/k."""
        ss = SpaceSaving(k=10)
        temps = list(range(1, 51)) * 10  # 50 unique items, each appears 10 times
        ss.process_stream(temps)

        max_error_actual = ss.get_max_error_actual()
        max_error_theoretical = ss.get_max_error_theoretical()

        assert max_error_actual <= max_error_theoretical

    def test_frequent_items_captured(self):
        """Test that items with freq > N/k are captured."""
        k = 5
        ss = SpaceSaving(k=k)

        # Create stream: some items appear frequently, others rarely
        temps = [12] * 100 + [15] * 80 + [18] * 60  # Frequent items
        temps += list(range(1, 20))  # Rare items (appear once each)

        ss.process_stream(temps)
        N = ss.stream_length
        threshold = N / k

        # Items 12, 15, 18 all appear > N/k times
        # They should all be monitored
        assert 12 in ss.monitored
        assert 15 in ss.monitored
        assert 18 in ss.monitored

    def test_deterministic_behavior(self):
        """Test that Space-Saving is deterministic."""
        temps = [12, 15, 18, 12, 20, 15, 12, 18]

        ss1 = SpaceSaving(k=3)
        ss1.process_stream(temps)
        result1 = ss1.get_monitored_items()

        ss2 = SpaceSaving(k=3)
        ss2.process_stream(temps)
        result2 = ss2.get_monitored_items()

        assert result1 == result2


class TestSpaceSavingMisc:
    """Test miscellaneous functionality."""

    def test_len(self):
        """Test __len__ method."""
        ss = SpaceSaving(k=10)
        assert len(ss) == 0

        ss.monitored = {12: (5, 0), 15: (3, 1)}
        assert len(ss) == 2

    def test_repr(self):
        """Test __repr__ method."""
        ss = SpaceSaving(k=10)
        ss.stream_length = 100
        ss.monitored = {12: (10, 0), 15: (8, 2)}

        repr_str = repr(ss)
        assert 'SpaceSaving' in repr_str
        assert 'k=10' in repr_str
        assert 'monitored=2/10' in repr_str
        assert 'stream_length=100' in repr_str


class TestSpaceSavingRealWorld:
    """Test with realistic scenarios."""

    def test_small_k_many_unique(self):
        """Test behavior when k << number of unique items."""
        ss = SpaceSaving(k=5)
        # 20 unique items, each appears different number of times
        temps = []
        for i in range(1, 21):
            temps += [i] * (21 - i)  # Item 1 appears 20 times, item 20 appears 1 time

        ss.process_stream(temps)

        # Should monitor exactly k items
        assert len(ss.monitored) == 5

        # Top items (1, 2, 3, 4, 5) should be captured
        top_5 = ss.get_top_n(5)
        temps_in_top_5 = {temp for temp, _ in top_5}
        # The most frequent items should be there
        assert 1 in temps_in_top_5

    def test_precision_recall_concept(self):
        """Test setup for precision/recall calculation."""
        ss = SpaceSaving(k=10)

        # Known distribution
        temps = [1] * 50 + [2] * 40 + [3] * 30 + [4] * 20
        temps += list(range(5, 15))  # 10 items appearing once each

        ss.process_stream(temps)

        # Get top 5 from Space-Saving
        ss_top_5 = {temp for temp, _ in ss.get_top_n(5)}

        # True top 5 are: 1, 2, 3, 4, and one of the others
        # Space-Saving should capture at least 1, 2, 3, 4
        assert 1 in ss_top_5
        assert 2 in ss_top_5
        assert 3 in ss_top_5
        assert 4 in ss_top_5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
