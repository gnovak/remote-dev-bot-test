"""Comprehensive test suite for calculator.py — 20+ test cases."""

import pytest
from calculator import (
    add, subtract, multiply, divide, power,
    factorial, is_prime, clamp, average, flatten, fizzbuzz,
)


# --- add ---

def test_add_positive_integers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-4, -6) == -10

def test_add_mixed_sign():
    assert add(-1, 1) == 0

def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)

def test_add_zero():
    assert add(0, 99) == 99


# --- subtract ---

def test_subtract_basic():
    assert subtract(10, 3) == 7

def test_subtract_negative_result():
    assert subtract(3, 10) == -7

def test_subtract_same_numbers():
    assert subtract(5, 5) == 0


# --- multiply ---

def test_multiply_positive():
    assert multiply(4, 5) == 20

def test_multiply_by_zero():
    assert multiply(99, 0) == 0

def test_multiply_negative():
    assert multiply(-3, 4) == -12


# --- divide ---

def test_divide_exact():
    assert divide(10, 2) == 5.0

def test_divide_float_result():
    assert divide(1, 3) == pytest.approx(1 / 3)

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)

def test_divide_negative():
    assert divide(-9, 3) == -3.0


# --- power ---

def test_power_positive():
    assert power(2, 10) == 1024

def test_power_zero_exponent():
    assert power(999, 0) == 1

def test_power_negative_exponent():
    assert power(2, -1) == pytest.approx(0.5)


# --- factorial ---

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_positive():
    assert factorial(5) == 120

def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-3)

def test_factorial_non_integer_raises():
    with pytest.raises(TypeError):
        factorial(3.5)


# --- is_prime ---

def test_is_prime_two():
    assert is_prime(2) is True

def test_is_prime_three():
    assert is_prime(3) is True

def test_is_prime_composite():
    assert is_prime(9) is False

def test_is_prime_one():
    assert is_prime(1) is False

def test_is_prime_large_prime():
    assert is_prime(97) is True

def test_is_prime_zero():
    assert is_prime(0) is False

def test_is_prime_even_non_two():
    assert is_prime(100) is False


# --- clamp ---

def test_clamp_within_range():
    assert clamp(5, 1, 10) == 5

def test_clamp_below_min():
    assert clamp(-5, 0, 10) == 0

def test_clamp_above_max():
    assert clamp(15, 0, 10) == 10

def test_clamp_at_boundary():
    assert clamp(10, 10, 10) == 10

def test_clamp_invalid_range_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 1)


# --- average ---

def test_average_basic():
    assert average([1, 2, 3, 4, 5]) == 3.0

def test_average_single_element():
    assert average([42]) == 42.0

def test_average_empty_raises():
    with pytest.raises(ValueError):
        average([])

def test_average_floats():
    assert average([1.5, 2.5]) == pytest.approx(2.0)


# --- flatten ---

def test_flatten_nested():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

def test_flatten_mixed():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

def test_flatten_empty():
    assert flatten([]) == []

def test_flatten_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]


# --- fizzbuzz ---

def test_fizzbuzz_fizz():
    assert fizzbuzz(3) == "Fizz"

def test_fizzbuzz_buzz():
    assert fizzbuzz(5) == "Buzz"

def test_fizzbuzz_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"

def test_fizzbuzz_number():
    assert fizzbuzz(7) == "7"


# --- integration: combined operations ---

def test_integration_add_then_divide():
    total = add(10, 20)
    assert divide(total, 3) == 10.0

def test_integration_factorial_is_prime():
    # 5! = 120, not prime
    assert is_prime(factorial(5)) is False

def test_integration_power_and_average():
    values = [power(2, i) for i in range(5)]   # [1,2,4,8,16]
    assert average(values) == pytest.approx(6.2)
