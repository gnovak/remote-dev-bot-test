import pytest
from greet import greet


def test_greet_basic():
    """Test basic greeting functionality."""
    assert greet('World') == 'Hello, World!'


def test_greet_different_names():
    """Test greeting with different names."""
    assert greet('Alice') == 'Hello, Alice!'
    assert greet('Bob') == 'Hello, Bob!'
    assert greet('Charlie') == 'Hello, Charlie!'


def test_greet_empty_string():
    """Test greeting with empty string."""
    assert greet('') == 'Hello, !'


def test_greet_special_characters():
    """Test greeting with special characters."""
    assert greet('José') == 'Hello, José!'
    assert greet('O\'Brien') == "Hello, O'Brien!"
