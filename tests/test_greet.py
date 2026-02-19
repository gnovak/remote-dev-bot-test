import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greet import greet


def test_greet_basic():
    """Test basic greeting functionality"""
    assert greet('World') == 'Hello, World!'


def test_greet_with_different_names():
    """Test greeting with different names"""
    assert greet('Alice') == 'Hello, Alice!'
    assert greet('Bob') == 'Hello, Bob!'
    assert greet('Charlie') == 'Hello, Charlie!'


def test_greet_empty_string():
    """Test greeting with empty string"""
    assert greet('') == 'Hello, !'


def test_greet_with_spaces():
    """Test greeting with names containing spaces"""
    assert greet('John Doe') == 'Hello, John Doe!'


if __name__ == '__main__':
    test_greet_basic()
    test_greet_with_different_names()
    test_greet_empty_string()
    test_greet_with_spaces()
    print("All tests passed!")
