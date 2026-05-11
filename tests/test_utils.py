"""
Comprehensive test suite for utils.py — 20+ test cases covering
normal paths, edge cases, and error paths.
"""

import pytest
from utils import (
    camel_to_snake,
    chunk,
    clamp,
    deep_merge,
    fibonacci,
    flatten,
    is_palindrome,
    is_prime,
    safe_divide,
    slugify,
    truncate,
    unique_ordered,
    word_count,
)


# ===========================================================================
# slugify
# ===========================================================================

class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_characters_removed(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_multiple_spaces(self):
        assert slugify("foo   bar") == "foo-bar"

    def test_leading_trailing_hyphens(self):
        assert slugify("  --hello--  ") == "hello"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_already_slug(self):
        assert slugify("already-a-slug") == "already-a-slug"


# ===========================================================================
# truncate
# ===========================================================================

class TestTruncate:
    def test_short_string_unchanged(self):
        assert truncate("hi", 10) == "hi"

    def test_exact_length_unchanged(self):
        assert truncate("hello", 5) == "hello"

    def test_truncation_adds_ellipsis(self):
        assert truncate("hello world", 8) == "hello..."

    def test_custom_ellipsis(self):
        assert truncate("hello world", 7, "…") == "hello …"

    def test_max_len_too_small_raises(self):
        with pytest.raises(ValueError):
            truncate("hello", 2)

    def test_empty_string(self):
        assert truncate("", 5) == ""


# ===========================================================================
# is_palindrome
# ===========================================================================

class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_case_insensitive(self):
        assert is_palindrome("Racecar") is True

    def test_phrase_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_char(self):
        assert is_palindrome("a") is True


# ===========================================================================
# word_count
# ===========================================================================

class TestWordCount:
    def test_basic(self):
        assert word_count("hello world") == {"hello": 1, "world": 1}

    def test_repeated_words(self):
        result = word_count("the cat sat on the mat")
        assert result["the"] == 2

    def test_case_insensitive(self):
        result = word_count("Hello hello HELLO")
        assert result["hello"] == 3

    def test_empty_string(self):
        assert word_count("") == {}


# ===========================================================================
# camel_to_snake
# ===========================================================================

class TestCamelToSnake:
    def test_basic(self):
        assert camel_to_snake("CamelCase") == "camel_case"

    def test_already_snake(self):
        assert camel_to_snake("already_snake") == "already_snake"

    def test_mixed(self):
        assert camel_to_snake("myVariableName") == "my_variable_name"

    def test_consecutive_caps(self):
        assert camel_to_snake("HTTPSResponse") == "https_response"


# ===========================================================================
# clamp
# ===========================================================================

class TestClamp:
    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_lo(self):
        assert clamp(-3, 0, 10) == 0

    def test_above_hi(self):
        assert clamp(15, 0, 10) == 10

    def test_equal_lo(self):
        assert clamp(0, 0, 10) == 0

    def test_equal_hi(self):
        assert clamp(10, 0, 10) == 10

    def test_invalid_range_raises(self):
        with pytest.raises(ValueError):
            clamp(5, 10, 0)


# ===========================================================================
# safe_divide
# ===========================================================================

class TestSafeDivide:
    def test_normal_division(self):
        assert safe_divide(10, 2) == 5.0

    def test_divide_by_zero_default(self):
        assert safe_divide(10, 0) == 0.0

    def test_divide_by_zero_custom_default(self):
        assert safe_divide(10, 0, default=-1) == -1

    def test_zero_numerator(self):
        assert safe_divide(0, 5) == 0.0


# ===========================================================================
# is_prime
# ===========================================================================

class TestIsPrime:
    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13]:
            assert is_prime(p) is True

    def test_composites(self):
        for c in [0, 1, 4, 6, 8, 9, 10]:
            assert is_prime(c) is False

    def test_negative(self):
        assert is_prime(-7) is False

    def test_large_prime(self):
        assert is_prime(7919) is True


# ===========================================================================
# fibonacci
# ===========================================================================

class TestFibonacci:
    def test_zero_terms(self):
        assert fibonacci(0) == []

    def test_one_term(self):
        assert fibonacci(1) == [0]

    def test_five_terms(self):
        assert fibonacci(5) == [0, 1, 1, 2, 3]

    def test_ten_terms(self):
        assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            fibonacci(-1)


# ===========================================================================
# flatten
# ===========================================================================

class TestFlatten:
    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_nested_list(self):
        assert flatten([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]

    def test_empty(self):
        assert flatten([]) == []

    def test_deeply_nested(self):
        assert flatten([[[[1]]]]) == [1]


# ===========================================================================
# chunk
# ===========================================================================

class TestChunk:
    def test_even_split(self):
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_chunk_larger_than_list(self):
        assert chunk([1, 2], 10) == [[1, 2]]

    def test_empty_list(self):
        assert chunk([], 3) == []

    def test_zero_size_raises(self):
        with pytest.raises(ValueError):
            chunk([1, 2, 3], 0)


# ===========================================================================
# unique_ordered
# ===========================================================================

class TestUniqueOrdered:
    def test_no_duplicates(self):
        assert unique_ordered([1, 2, 3]) == [1, 2, 3]

    def test_with_duplicates(self):
        assert unique_ordered([1, 2, 2, 3, 1]) == [1, 2, 3]

    def test_empty(self):
        assert unique_ordered([]) == []

    def test_preserves_order(self):
        assert unique_ordered([3, 1, 2, 1, 3]) == [3, 1, 2]


# ===========================================================================
# deep_merge
# ===========================================================================

class TestDeepMerge:
    def test_simple_merge(self):
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_override_value(self):
        assert deep_merge({"a": 1}, {"a": 99}) == {"a": 99}

    def test_nested_merge(self):
        base = {"a": {"x": 1, "y": 2}}
        override = {"a": {"y": 99, "z": 3}}
        result = deep_merge(base, override)
        assert result == {"a": {"x": 1, "y": 99, "z": 3}}

    def test_does_not_mutate_base(self):
        base = {"a": 1}
        deep_merge(base, {"b": 2})
        assert base == {"a": 1}

    def test_empty_override(self):
        assert deep_merge({"a": 1}, {}) == {"a": 1}

    def test_empty_base(self):
        assert deep_merge({}, {"a": 1}) == {"a": 1}
