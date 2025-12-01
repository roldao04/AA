"""
Experimental Framework for Running and Analyzing Edge Cover Algorithms
"""

from .experiment_runner import ExperimentRunner
from .overnight_experiments import run_overnight_experiments, run_quick_test

__all__ = [
    'ExperimentRunner',
    'run_overnight_experiments',
    'run_quick_test'
]
