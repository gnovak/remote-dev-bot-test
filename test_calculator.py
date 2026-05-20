"""Comprehensive test suite for calculator.py — 20+ test cases."""

import pytest
from calculator import (
    add, subtract, multiply, divide, power, square_root,
    factorial, gcd, lcm, clamp, average, median, is_prime,
    fibonacci, percentage,
)


# --- add ---
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -4) == -5

def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)

def test_add_zero():
    assert add(0, 99) == 99


# --- subtract ---
def test_subtract_basic():
    assert subtract(10, 4) == 6

def test_subtract_negative_result():
    assert subtract(3, 7) == -4


# --- multiply ---
def test_multiply_basic():
    assert multiply(3, 4) == 12

def test_multiply_by_zero():
    assert multiply(999, 0) == 0

def test_multiply_negatives():
    assert multiply(-3, -5) == 15


# --- divide ---
def test_divide_basic():
    assert divide(10, 2) == 5.0

def test_divide_float_result():
    assert divide(7, 2) == pytest.approx(3.5)

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)


# --- power ---
def test_power_basic():
    assert power(2, 10) == 1024

def test_power_zero_exp():
    assert power(99, 0) == 1

def test_power_fractional():
    assert power(4, 0.5) == pytest.approx(2.0)


# --- square_root ---
def test_square_root_perfect():
    assert square_root(25) == 5.0

def test_square_root_zero():
    assert square_root(0) == 0.0

def test_square_root_negative_raises():
    with pytest.raises(ValueError):
        square_root(-1)


# --- factorial ---
def test_factorial_basic():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-3)

def test_factorial_non_int_raises():
    with pytest.raises(TypeError):
        factorial(3.5)


# --- gcd ---
def test_gcd_basic():
    assert gcd(12, 8) == 4

def test_gcd_coprime():
    assert gcd(7, 13) == 1

def test_gcd_with_negatives():
    assert gcd(-12, 8) == 4


# --- lcm ---
def test_lcm_basic():
    assert lcm(4, 6) == 12

def test_lcm_with_zero():
    assert lcm(0, 5) == 0


# --- clamp ---
def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5

def test_clamp_below_min():
    assert clamp(-3, 0, 10) == 0

def test_clamp_above_max():
    assert clamp(15, 0, 10) == 10

def test_clamp_invalid_range_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


# --- average ---
def test_average_basic():
    assert average([1, 2, 3, 4, 5]) == 3.0

def test_average_single():
    assert average([42]) == 42.0

def test_average_empty_raises():
    with pytest.raises(ValueError):
        average([])

def test_average_floats():
    assert average([0.1, 0.2, 0.3]) == pytest.approx(0.2)


# --- median ---
def test_median_odd():
    assert median([3, 1, 2]) == 2

def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5

def test_median_empty_raises():
    with pytest.raises(ValueError):
        median([])


# --- is_prime ---
def test_is_prime_true():
    assert is_prime(17) is True

def test_is_prime_false_composite():
    assert is_prime(15) is False

def test_is_prime_two():
    assert is_prime(2) is True

def test_is_prime_one():
    assert is_prime(1) is False

def test_is_prime_zero():
    assert is_prime(0) is False


# --- fibonacci ---
def test_fibonacci_basic():
    assert fibonacci(6) == [0, 1, 1, 2, 3, 5]

def test_fibonacci_zero():
    assert fibonacci(0) == []

def test_fibonacci_one():
    assert fibonacci(1) == [0]

def test_fibonacci_negative_raises():
    with pytest.raises(ValueError):
        fibonacci(-1)


# --- percentage ---
def test_percentage_basic():
    assert percentage(25, 200) == pytest.approx(12.5)

def test_percentage_full():
    assert percentage(100, 100) == pytest.approx(100.0)

def test_percentage_zero_whole_raises():
    with pytest.raises(ZeroDivisionError):
        percentage(5, 0)
