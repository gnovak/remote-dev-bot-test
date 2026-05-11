"""
utils.py - General-purpose utility functions for the rdb-test repository.
"""

import math
import re
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# String utilities
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert *text* to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def truncate(text: str, max_len: int, ellipsis: str = "...") -> str:
    """Return *text* truncated to *max_len* characters (including ellipsis)."""
    if max_len < len(ellipsis):
        raise ValueError("max_len must be >= length of ellipsis")
    if len(text) <= max_len:
        return text
    return text[: max_len - len(ellipsis)] + ellipsis


def is_palindrome(text: str) -> bool:
    """Return True if *text* is a palindrome (case-insensitive, letters only)."""
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


def word_count(text: str) -> Dict[str, int]:
    """Return a frequency map of words in *text*."""
    words = re.findall(r"\b\w+\b", text.lower())
    return dict(Counter(words))


def camel_to_snake(name: str) -> str:
    """Convert *CamelCase* to *snake_case*."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


# ---------------------------------------------------------------------------
# Numeric utilities
# ---------------------------------------------------------------------------

def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp *value* to the inclusive range [*lo*, *hi*]."""
    if lo > hi:
        raise ValueError("lo must be <= hi")
    return max(lo, min(hi, value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide, returning *default* when *denominator* is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def is_prime(n: int) -> bool:
    """Return True if *n* is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> List[int]:
    """Return the first *n* Fibonacci numbers (n >= 0)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    seq: List[int] = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


# ---------------------------------------------------------------------------
# Collection utilities
# ---------------------------------------------------------------------------

def flatten(nested: Iterable) -> List[Any]:
    """Recursively flatten a nested iterable into a list."""
    result: List[Any] = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(lst: List[Any], size: int) -> List[List[Any]]:
    """Split *lst* into consecutive chunks of *size*."""
    if size <= 0:
        raise ValueError("size must be positive")
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique_ordered(lst: List[Any]) -> List[Any]:
    """Return *lst* with duplicates removed, preserving insertion order."""
    seen = set()
    out = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def deep_merge(base: Dict, override: Dict) -> Dict:
    """Recursively merge *override* into *base*, returning a new dict."""
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result
