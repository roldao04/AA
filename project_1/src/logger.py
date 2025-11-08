"""
Logging utility for Minimum Edge Cover project.
Provides consistent logging across all modules.

Student Number: 113920
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from src.config import LOG_FORMAT, DATE_FORMAT, DEFAULT_LOG_LEVEL


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Set up a logger with consistent formatting.

    Args:
        name: Name of the logger (typically __name__ of the module)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If None, uses DEFAULT_LOG_LEVEL from config
        log_file: Optional file path to write logs to

    Returns:
        Configured Logger instance

    Example:
        >>> logger = setup_logger(__name__, level='INFO')
        >>> logger.info('Starting experiment')
    """
    if level is None:
        level = DEFAULT_LOG_LEVEL

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger by name.

    Args:
        name: Name of the logger

    Returns:
        Logger instance

    Note:
        If the logger doesn't exist, creates a new one with default settings.
    """
    logger = logging.getLogger(name)

    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        logger = setup_logger(name)

    return logger


def set_log_level(logger: logging.Logger, level: str) -> None:
    """
    Change the log level of an existing logger.

    Args:
        logger: Logger instance
        level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger.setLevel(getattr(logging, level.upper()))
    for handler in logger.handlers:
        handler.setLevel(getattr(logging, level.upper()))


def disable_logging() -> None:
    """Disable all logging (useful for tests)."""
    logging.disable(logging.CRITICAL)


def enable_logging() -> None:
    """Re-enable logging after it was disabled."""
    logging.disable(logging.NOTSET)
