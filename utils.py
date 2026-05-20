"""Utility functions for the rdb-test repository.

This module provides a small collection of general-purpose helper functions
demonstrating best-practice Python: type hints, docstrings, and full unit-test
coverage.
"""

from __future__ import annotations


def add(a: int | float, b: int | float) -> int | float:
    """Return the sum of *a* and *b*.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The arithmetic sum of *a* and *b*.

    Examples:
        >>> add(1, 2)
        3
        >>> add(1.5, 2.5)
        4.0
    """
    return a + b


def greet(name: str) -> str:
    """Return a friendly greeting string.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting of the form ``"Hello, <name>!"``.

    Examples:
        >>> greet("World")
        'Hello, World!'
    """
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp *value* to the inclusive range [*lo*, *hi*].

    Args:
        value: The value to clamp.
        lo: The lower bound (inclusive).
        hi: The upper bound (inclusive).

    Returns:
        *value* if it is within [*lo*, *hi*], *lo* if it is below, or *hi* if
        it is above.

    Raises:
        ValueError: If *lo* > *hi*.

    Examples:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-1, 0, 10)
        0
        >>> clamp(11, 0, 10)
        10
    """
    if lo > hi:
        raise ValueError(f"lo ({lo}) must be <= hi ({hi})")
    return max(lo, min(value, hi))
