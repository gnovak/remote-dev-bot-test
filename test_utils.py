"""Unit tests for utils.py."""

import pytest

from utils import add, clamp, greet


class TestAdd:
    def test_integers(self) -> None:
        assert add(2, 3) == 5

    def test_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0

    def test_negative(self) -> None:
        assert add(-1, 1) == 0

    def test_zero(self) -> None:
        assert add(0, 0) == 0


class TestGreet:
    def test_basic(self) -> None:
        assert greet("World") == "Hello, World!"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="name must not be empty"):
            greet("")

    def test_whitespace_name(self) -> None:
        assert greet("  ") == "Hello,   !"


class TestClamp:
    def test_within_range(self) -> None:
        assert clamp(5, 0, 10) == 5

    def test_below_lo(self) -> None:
        assert clamp(-1, 0, 10) == 0

    def test_above_hi(self) -> None:
        assert clamp(11, 0, 10) == 10

    def test_at_lo(self) -> None:
        assert clamp(0, 0, 10) == 0

    def test_at_hi(self) -> None:
        assert clamp(10, 0, 10) == 10

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError, match="lo"):
            clamp(5, 10, 0)

    def test_equal_bounds(self) -> None:
        assert clamp(5, 5, 5) == 5
