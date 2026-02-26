import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_default import hello


def test_hello_returns_correct_message():
    """Test that hello() returns the correct greeting message."""
    result = hello()
    assert result == 'Hello from default!', f"Expected 'Hello from default!' but got '{result}'"


def test_hello_returns_string():
    """Test that hello() returns a string."""
    result = hello()
    assert isinstance(result, str), f"Expected string but got {type(result)}"


if __name__ == '__main__':
    test_hello_returns_correct_message()
    test_hello_returns_string()
    print("All tests passed!")
