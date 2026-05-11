"""Simple calculator and utility module."""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base, exp):
    """Raise base to the power of exp."""
    return base ** exp


def factorial(n):
    """Return the factorial of n. Raises ValueError for negative input."""
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def is_prime(n):
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def clamp(value, min_val, max_val):
    """Clamp value between min_val and max_val."""
    if min_val > max_val:
        raise ValueError("min_val must be <= max_val")
    return max(min_val, min(max_val, value))


def average(numbers):
    """Return the average of a list of numbers. Raises ValueError for empty list."""
    if not numbers:
        raise ValueError("Cannot compute average of empty sequence")
    return sum(numbers) / len(numbers)


def flatten(nested):
    """Flatten a nested list one level deep."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def fizzbuzz(n):
    """Return FizzBuzz string for n."""
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
