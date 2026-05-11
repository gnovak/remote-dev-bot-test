"""Utility functions for rdb-test repository."""

import math
import re
from typing import Any, Dict, List, Optional, Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return the product of two numbers."""
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Return the quotient of two numbers. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return math.factorial(n)


def is_palindrome(s: str) -> bool:
    """Return True if the string is a palindrome (ignoring case and spaces)."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]


def flatten(lst: List[Any]) -> List[Any]:
    """Flatten a nested list into a single-level list."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(lst: List[Any], size: int) -> List[List[Any]]:
    """Split a list into chunks of the given size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dicts; later dicts override earlier ones."""
    result: Dict = {}
    for d in dicts:
        result.update(d)
    return result


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp value to the range [lo, hi]."""
    if lo > hi:
        raise ValueError("lo must be <= hi")
    return max(lo, min(value, hi))


def word_count(text: str) -> Dict[str, int]:
    """Return a dict mapping each word (lowercased) to its frequency."""
    counts: Dict[str, int] = {}
    for word in re.findall(r'[a-zA-Z]+', text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts
