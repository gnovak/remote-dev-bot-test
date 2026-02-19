import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greet import greet


def test_greet_basic():
    """Test the greet function with a basic name"""
    assert greet("World") == "Hello, World!"


def test_greet_different_name():
    """Test the greet function with different names"""
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


def test_greet_empty_string():
    """Test the greet function with an empty string"""
    assert greet("") == "Hello, !"


if __name__ == "__main__":
    test_greet_basic()
    test_greet_different_name()
    test_greet_empty_string()
    print("All tests passed!")
