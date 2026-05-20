"""A simple calculator module with various utility functions."""

import math
from typing import List, Optional, Union


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(base: float, exp: float) -> float:
    """Return base raised to the power of exp."""
    return base ** exp


def square_root(n: float) -> float:
    """Return the square root of n. Raises ValueError if n is negative."""
    if n < 0:
        raise ValueError(f"Cannot take square root of negative number: {n}")
    return math.sqrt(n)


def factorial(n: int) -> int:
    """Return the factorial of n. Raises ValueError for negative inputs."""
    if not isinstance(n, int):
        raise TypeError(f"Factorial requires an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers: {n}")
    return math.factorial(n)


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b."""
    return math.gcd(abs(a), abs(b))


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min_val and max_val."""
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) must be <= max_val ({max_val})")
    return max(min_val, min(max_val, value))


def average(numbers: List[float]) -> float:
    """Return the arithmetic mean of a list of numbers. Raises ValueError for empty list."""
    if not numbers:
        raise ValueError("Cannot compute average of an empty list")
    return sum(numbers) / len(numbers)


def median(numbers: List[float]) -> float:
    """Return the median of a list of numbers. Raises ValueError for empty list."""
    if not numbers:
        raise ValueError("Cannot compute median of an empty list")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        return sorted_nums[mid]
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> List[int]:
    """Return the first n Fibonacci numbers. Raises ValueError for negative n."""
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        return []
    result = [0, 1]
    for _ in range(2, n):
        result.append(result[-1] + result[-2])
    return result[:n]


def percentage(part: float, whole: float) -> float:
    """Return what percentage 'part' is of 'whole'. Raises ZeroDivisionError if whole is 0."""
    if whole == 0:
        raise ZeroDivisionError("'whole' cannot be zero")
    return (part / whole) * 100
