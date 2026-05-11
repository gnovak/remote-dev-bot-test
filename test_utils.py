"""Comprehensive test suite for utils.py — 20+ test cases covering
normal paths, edge cases, error paths, and integration scenarios."""

import pytest
from utils import (
    add, subtract, multiply, divide,
    factorial, is_palindrome,
    flatten, chunk, merge_dicts, clamp, word_count,
)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

def test_add_integers():
    assert add(2, 3) == 5

def test_add_floats():
    assert add(1.5, 2.5) == pytest.approx(4.0)

def test_add_negative_numbers():
    assert add(-4, -6) == -10

def test_add_zero():
    assert add(0, 99) == 99


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

def test_subtract_positive_result():
    assert subtract(10, 3) == 7

def test_subtract_negative_result():
    assert subtract(3, 10) == -7


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

def test_multiply_integers():
    assert multiply(6, 7) == 42

def test_multiply_by_zero():
    assert multiply(999, 0) == 0

def test_multiply_floats():
    assert multiply(2.5, 4.0) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

def test_divide_exact():
    assert divide(10, 2) == pytest.approx(5.0)

def test_divide_float_result():
    assert divide(1, 3) == pytest.approx(1 / 3)

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

def test_divide_negative_denominator():
    assert divide(-10, 2) == pytest.approx(-5.0)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_positive():
    assert factorial(5) == 120

def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_non_integer_raises():
    with pytest.raises(TypeError):
        factorial(3.5)


# ---------------------------------------------------------------------------
# is_palindrome
# ---------------------------------------------------------------------------

def test_palindrome_simple():
    assert is_palindrome("racecar") is True

def test_palindrome_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True

def test_palindrome_not():
    assert is_palindrome("hello") is False

def test_palindrome_empty_string():
    assert is_palindrome("") is True

def test_palindrome_single_char():
    assert is_palindrome("z") is True


# ---------------------------------------------------------------------------
# flatten
# ---------------------------------------------------------------------------

def test_flatten_nested():
    assert flatten([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]

def test_flatten_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]

def test_flatten_empty():
    assert flatten([]) == []

def test_flatten_deeply_nested():
    assert flatten([[[1]], [[2, [3]]]]) == [1, 2, 3]


# ---------------------------------------------------------------------------
# chunk
# ---------------------------------------------------------------------------

def test_chunk_even_split():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

def test_chunk_uneven_split():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

def test_chunk_size_larger_than_list():
    assert chunk([1, 2], 10) == [[1, 2]]

def test_chunk_invalid_size_raises():
    with pytest.raises(ValueError):
        chunk([1, 2, 3], 0)

def test_chunk_empty_list():
    assert chunk([], 3) == []


# ---------------------------------------------------------------------------
# merge_dicts
# ---------------------------------------------------------------------------

def test_merge_dicts_basic():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

def test_merge_dicts_override():
    assert merge_dicts({"a": 1}, {"a": 99}) == {"a": 99}

def test_merge_dicts_three_dicts():
    result = merge_dicts({"x": 1}, {"y": 2}, {"z": 3})
    assert result == {"x": 1, "y": 2, "z": 3}

def test_merge_dicts_empty():
    assert merge_dicts({}, {}) == {}


# ---------------------------------------------------------------------------
# clamp
# ---------------------------------------------------------------------------

def test_clamp_within_range():
    assert clamp(5, 1, 10) == 5

def test_clamp_below_lo():
    assert clamp(-5, 0, 10) == 0

def test_clamp_above_hi():
    assert clamp(15, 0, 10) == 10

def test_clamp_invalid_range_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)

def test_clamp_at_boundary():
    assert clamp(10, 10, 10) == 10


# ---------------------------------------------------------------------------
# word_count
# ---------------------------------------------------------------------------

def test_word_count_basic():
    assert word_count("hello world") == {"hello": 1, "world": 1}

def test_word_count_repeated_words():
    result = word_count("the cat sat on the mat")
    assert result["the"] == 2

def test_word_count_case_insensitive():
    result = word_count("Hello hello HELLO")
    assert result["hello"] == 3

def test_word_count_punctuation_ignored():
    result = word_count("well, well... well!")
    assert result["well"] == 3

def test_word_count_empty_string():
    assert word_count("") == {}


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

def test_arithmetic_pipeline():
    """add → multiply → divide in sequence."""
    result = divide(multiply(add(1, 2), 4), 6)
    assert result == pytest.approx(2.0)

def test_flatten_then_chunk():
    nested = [[1, 2], [3, 4], [5, 6]]
    flat = flatten(nested)
    chunks = chunk(flat, 3)
    assert chunks == [[1, 2, 3], [4, 5, 6]]

def test_merge_and_word_count():
    texts = {"a": "hello world", "b": "hello python"}
    merged_text = " ".join(texts.values())
    counts = word_count(merged_text)
    assert counts["hello"] == 2
    assert counts["world"] == 1
    assert counts["python"] == 1
