"""
Unit tests for FixedProbabilityCounter class.

Tests the probabilistic counting implementation to ensure correctness
of the approximation algorithm and its statistical properties.

Author: Joao Roldao (113920)
Project: AA Project 3 - Approximate Counting and Frequent Items
"""

import pytest
import pandas as pd
import numpy as np
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms.fixed_probability_counter import FixedProbabilityCounter


class TestFixedProbabilityCounterBasic:
    """Basic functionality tests."""

    def test_initialization(self):
        """Test counter initializes correctly."""
        counter = FixedProbabilityCounter(p=0.25)
        assert counter.p == 0.25
        assert len(counter) == 0
        assert counter.counters == {}

    def test_initialization_invalid_p(self):
        """Test that invalid p values raise ValueError."""
        with pytest.raises(ValueError):
            FixedProbabilityCounter(p=0.0)
        with pytest.raises(ValueError):
            FixedProbabilityCounter(p=1.5)
        with pytest.raises(ValueError):
            FixedProbabilityCounter(p=-0.1)

    def test_initialization_edge_cases(self):
        """Test valid edge cases for p."""
        counter1 = FixedProbabilityCounter(p=1.0)
        assert counter1.p == 1.0

        counter2 = FixedProbabilityCounter(p=0.01)
        assert counter2.p == 0.01

    def test_process_with_p_equals_1(self):
        """Test that p=1.0 always increments (deterministic)."""
        counter = FixedProbabilityCounter(p=1.0)
        random.seed(113920)

        for _ in range(10):
            counter.process(15)

        assert counter.get_counter_value(15) == 10
        assert counter.estimate(15) == 10.0


class TestFixedProbabilityCounterProbabilistic:
    """Tests for probabilistic increment behavior."""

    def test_probabilistic_increment_p_half(self):
        """Test that p=0.5 increments approximately half the time."""
        random.seed(113920)
        counter = FixedProbabilityCounter(p=0.5)

        n_processes = 1000
        for _ in range(n_processes):
            counter.process(15)

        raw_count = counter.get_counter_value(15)

        # Should be around 500 ± some tolerance
        # With n=1000, expect mean=500, std=sqrt(1000*0.5*0.5)≈15.8
        # Allow ±3 std deviations (≈99.7% confidence)
        assert 450 < raw_count < 550

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        temps = [12, 15, 12, 18, 15, 12, 18, 15]

        # Run 1
        random.seed(113920)
        counter1 = FixedProbabilityCounter(p=0.25)
        counter1.process_stream(temps)
        estimates1 = counter1.get_all_estimates()

        # Run 2 with same seed
        random.seed(113920)
        counter2 = FixedProbabilityCounter(p=0.25)
        counter2.process_stream(temps)
        estimates2 = counter2.get_all_estimates()

        assert estimates1 == estimates2

    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        temps = [12] * 100

        random.seed(113920)
        counter1 = FixedProbabilityCounter(p=0.25)
        counter1.process_stream(temps)
        estimate1 = counter1.estimate(12)

        random.seed(42)
        counter2 = FixedProbabilityCounter(p=0.25)
        counter2.process_stream(temps)
        estimate2 = counter2.estimate(12)

        # Very unlikely to be exactly the same
        assert estimate1 != estimate2


class TestFixedProbabilityCounterEstimate:
    """Tests for estimate calculation."""

    def test_estimate_calculation(self):
        """Test that estimate = counter / p."""
        counter = FixedProbabilityCounter(p=0.25)
        counter.counters[15] = 10
        assert counter.estimate(15) == 40.0

        counter.counters[12] = 5
        assert counter.estimate(12) == 20.0

    def test_estimate_nonexistent_temp(self):
        """Test estimating count for temperature never seen."""
        counter = FixedProbabilityCounter(p=0.25)
        assert counter.estimate(99) == 0.0

    def test_get_all_estimates(self):
        """Test getting all estimates."""
        counter = FixedProbabilityCounter(p=0.5)
        counter.counters = {12: 10, 15: 5, 18: 2}

        estimates = counter.get_all_estimates()

        assert estimates == {12: 20.0, 15: 10.0, 18: 4.0}

    def test_estimate_with_different_p(self):
        """Test estimates scale correctly with different p."""
        counter1 = FixedProbabilityCounter(p=0.5)
        counter1.counters[15] = 10
        assert counter1.estimate(15) == 20.0

        counter2 = FixedProbabilityCounter(p=0.1)
        counter2.counters[15] = 10
        assert counter2.estimate(15) == 100.0


class TestFixedProbabilityCounterStream:
    """Tests for stream processing."""

    def test_process_stream_list(self):
        """Test processing a list of temperatures."""
        random.seed(113920)
        counter = FixedProbabilityCounter(p=1.0)  # p=1 for deterministic
        temps = [12, 15, 12, 18, 15, 12]

        counter.process_stream(temps)

        assert counter.estimate(12) == 3.0
        assert counter.estimate(15) == 2.0
        assert counter.estimate(18) == 1.0

    def test_process_stream_pandas_series(self):
        """Test processing a pandas Series."""
        random.seed(113920)
        counter = FixedProbabilityCounter(p=1.0)
        temps = pd.Series([12, 15, 12, 18])

        counter.process_stream(temps)

        assert counter.estimate(12) == 2.0
        assert counter.estimate(15) == 1.0

    def test_process_stream_numpy_array(self):
        """Test processing a numpy array."""
        random.seed(113920)
        counter = FixedProbabilityCounter(p=1.0)
        temps = np.array([12, 15, 12, 18])

        counter.process_stream(temps)

        assert counter.estimate(12) == 2.0


class TestFixedProbabilityCounterStatistical:
    """Tests for statistical properties."""

    def test_unbiased_estimator(self):
        """Test that estimator is unbiased over many trials."""
        true_count = 100
        temps = [15] * true_count
        p = 0.25
        num_trials = 100  # More trials for more stable mean

        estimates = []
        for trial in range(num_trials):
            random.seed(113920 + trial)
            counter = FixedProbabilityCounter(p=p)
            counter.process_stream(temps)
            estimates.append(counter.estimate(15))

        mean_estimate = np.mean(estimates)

        # Mean should be close to true count (within 10% with 100 trials)
        assert abs(mean_estimate - true_count) / true_count < 0.10

    def test_variance_scales_with_frequency(self):
        """Test that variance decreases as frequency increases."""
        p = 0.25
        num_trials = 30

        # Low frequency
        temps_low = [15] * 10
        estimates_low = []
        for trial in range(num_trials):
            random.seed(113920 + trial)
            counter = FixedProbabilityCounter(p=p)
            counter.process_stream(temps_low)
            estimates_low.append(counter.estimate(15))

        var_low = np.var(estimates_low)

        # High frequency
        temps_high = [15] * 100
        estimates_high = []
        for trial in range(num_trials):
            random.seed(113920 + trial)
            counter = FixedProbabilityCounter(p=p)
            counter.process_stream(temps_high)
            estimates_high.append(counter.estimate(15))

        var_high = np.var(estimates_high)

        # Higher frequency should have lower relative variance
        rel_var_low = var_low / 10
        rel_var_high = var_high / 100

        assert rel_var_high < rel_var_low


class TestFixedProbabilityCounterHelpers:
    """Tests for helper methods."""

    def test_get_counter_value(self):
        """Test getting raw counter value."""
        counter = FixedProbabilityCounter(p=0.25)
        counter.counters[15] = 10
        assert counter.get_counter_value(15) == 10
        assert counter.get_counter_value(99) == 0

    def test_reset(self):
        """Test resetting counters."""
        counter = FixedProbabilityCounter(p=0.25)
        counter.counters = {12: 5, 15: 3}
        assert len(counter) == 2

        counter.reset()

        assert len(counter) == 0
        assert counter.counters == {}
        assert counter.p == 0.25  # p should be preserved

    def test_len(self):
        """Test __len__ returns number of unique items."""
        counter = FixedProbabilityCounter(p=0.25)
        assert len(counter) == 0

        counter.counters = {12: 5, 15: 3, 18: 7}
        assert len(counter) == 3

    def test_repr(self):
        """Test string representation."""
        counter = FixedProbabilityCounter(p=0.25)
        counter.counters = {12: 4, 15: 2}  # Estimates: 16.0, 8.0

        repr_str = repr(counter)

        assert 'FixedProbabilityCounter' in repr_str
        assert 'p=0.25' in repr_str
        assert 'unique_items=2' in repr_str


class TestFixedProbabilityCounterTheoretical:
    """Tests for theoretical variance calculations."""

    def test_theoretical_variance(self):
        """Test theoretical variance calculation."""
        counter = FixedProbabilityCounter(p=0.25)
        true_count = 100

        # Var = (1-p)/p * n = 0.75/0.25 * 100 = 300
        expected_variance = 300.0

        assert counter.get_variance_theoretical(true_count) == expected_variance

    def test_theoretical_std(self):
        """Test theoretical standard deviation calculation."""
        counter = FixedProbabilityCounter(p=0.25)
        true_count = 100

        # Std = sqrt(300) ≈ 17.32
        expected_std = np.sqrt(300.0)

        assert abs(counter.get_std_theoretical(true_count) - expected_std) < 0.01

    def test_variance_with_different_p(self):
        """Test variance changes with different p."""
        true_count = 100

        counter1 = FixedProbabilityCounter(p=0.5)
        var1 = counter1.get_variance_theoretical(true_count)

        counter2 = FixedProbabilityCounter(p=0.25)
        var2 = counter2.get_variance_theoretical(true_count)

        # Lower p should have higher variance
        assert var2 > var1


class TestFixedProbabilityCounterIntegration:
    """Integration tests with realistic scenarios."""

    def test_realistic_temperature_stream(self):
        """Test with realistic temperature data."""
        # Simulate a week of temperatures
        temps = [12, 15, 13, 14, 15, 16, 14, 12, 13, 15]
        random.seed(113920)

        counter = FixedProbabilityCounter(p=0.5)
        counter.process_stream(temps)

        # Verify all temperatures were seen
        estimates = counter.get_all_estimates()
        unique_temps = set(temps)
        assert set(estimates.keys()) == unique_temps

        # Verify estimates are positive
        for estimate in estimates.values():
            assert estimate >= 0

    def test_large_stream_performance(self):
        """Test with larger stream to verify scalability."""
        # Generate 1000 random temperatures
        random.seed(113920)
        temps = [random.randint(10, 20) for _ in range(1000)]

        random.seed(113920)
        counter = FixedProbabilityCounter(p=0.25)
        counter.process_stream(temps)

        # Verify total estimated count is reasonable
        total_estimate = sum(counter.get_all_estimates().values())
        assert 800 < total_estimate < 1200  # Should be around 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
