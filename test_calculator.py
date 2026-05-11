"""Comprehensive test suite for calculator.py — 20+ test cases."""

import pytest
from calculator import (
    add, subtract, multiply, divide, power, square_root,
    factorial, gcd, lcm, is_prime, average, clamp, fibonacci,
)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_add_positive_integers(self):
        assert add(2, 3) == 5

    def test_add_negative_integers(self):
        assert add(-4, -6) == -10

    def test_add_mixed_sign(self):
        assert add(-1, 1) == 0

    def test_add_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_zero(self):
        assert add(0, 99) == 99


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(10, 4) == 6

    def test_subtract_to_negative(self):
        assert subtract(3, 7) == -4

    def test_subtract_zero(self):
        assert subtract(5, 0) == 5


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_multiply_positive(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(100, 0) == 0

    def test_multiply_negatives(self):
        assert multiply(-3, -3) == 9

    def test_multiply_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_divide_basic(self):
        assert divide(10, 2) == 5.0

    def test_divide_float_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)

    def test_divide_negative(self):
        assert divide(-9, 3) == -3.0


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

class TestPower:
    def test_power_basic(self):
        assert power(2, 10) == 1024

    def test_power_zero_exponent(self):
        assert power(999, 0) == 1

    def test_power_fractional(self):
        assert power(4, 0.5) == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

class TestSquareRoot:
    def test_sqrt_perfect_square(self):
        assert square_root(25) == pytest.approx(5.0)

    def test_sqrt_zero(self):
        assert square_root(0) == 0.0

    def test_sqrt_non_perfect(self):
        assert square_root(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_negative_raises(self):
        with pytest.raises(ValueError):
            square_root(-1)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

class TestFactorial:
    def test_factorial_zero(self):
        assert factorial(0) == 1

    def test_factorial_one(self):
        assert factorial(1) == 1

    def test_factorial_five(self):
        assert factorial(5) == 120

    def test_factorial_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_factorial_non_integer_raises(self):
        with pytest.raises(TypeError):
            factorial(3.5)


# ---------------------------------------------------------------------------
# gcd / lcm
# ---------------------------------------------------------------------------

class TestGcdLcm:
    def test_gcd_basic(self):
        assert gcd(12, 8) == 4

    def test_gcd_coprime(self):
        assert gcd(7, 13) == 1

    def test_gcd_negative_inputs(self):
        assert gcd(-12, 8) == 4

    def test_lcm_basic(self):
        assert lcm(4, 6) == 12

    def test_lcm_with_zero(self):
        assert lcm(0, 5) == 0


# ---------------------------------------------------------------------------
# is_prime
# ---------------------------------------------------------------------------

class TestIsPrime:
    def test_prime_two(self):
        assert is_prime(2) is True

    def test_prime_small(self):
        assert is_prime(17) is True

    def test_not_prime_one(self):
        assert is_prime(1) is False

    def test_not_prime_composite(self):
        assert is_prime(15) is False

    def test_not_prime_negative(self):
        assert is_prime(-7) is False


# ---------------------------------------------------------------------------
# average
# ---------------------------------------------------------------------------

class TestAverage:
    def test_average_basic(self):
        assert average([1, 2, 3, 4, 5]) == 3.0

    def test_average_single_element(self):
        assert average([42]) == 42.0

    def test_average_empty_raises(self):
        with pytest.raises(ValueError):
            average([])

    def test_average_floats(self):
        assert average([1.0, 2.0, 3.0]) == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# clamp
# ---------------------------------------------------------------------------

class TestClamp:
    def test_clamp_within_range(self):
        assert clamp(5, 1, 10) == 5

    def test_clamp_below_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_clamp_above_max(self):
        assert clamp(15, 0, 10) == 10

    def test_clamp_at_boundary(self):
        assert clamp(10, 10, 10) == 10

    def test_clamp_invalid_range_raises(self):
        with pytest.raises(ValueError):
            clamp(5, 10, 1)


# ---------------------------------------------------------------------------
# fibonacci
# ---------------------------------------------------------------------------

class TestFibonacci:
    def test_fibonacci_zero(self):
        assert fibonacci(0) == []

    def test_fibonacci_one(self):
        assert fibonacci(1) == [0]

    def test_fibonacci_five(self):
        assert fibonacci(5) == [0, 1, 1, 2, 3]

    def test_fibonacci_ten(self):
        assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_fibonacci_negative_raises(self):
        with pytest.raises(ValueError):
            fibonacci(-1)


# ---------------------------------------------------------------------------
# Integration-style tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_divide_then_add(self):
        result = add(divide(10, 2), divide(6, 3))
        assert result == pytest.approx(7.0)

    def test_prime_in_fibonacci(self):
        fibs = fibonacci(10)
        primes_in_fibs = [f for f in fibs if is_prime(f)]
        assert primes_in_fibs == [2, 3, 5, 13]

    def test_average_of_squares(self):
        squares = [power(i, 2) for i in range(1, 6)]  # 1,4,9,16,25
        assert average(squares) == pytest.approx(11.0)

    def test_gcd_lcm_relationship(self):
        a, b = 12, 18
        assert gcd(a, b) * lcm(a, b) == a * b


import math  # needed by TestSquareRoot.test_sqrt_non_perfect
