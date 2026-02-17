import sys
import os

# Add the parent directory to sys.path to import hello module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello import hello


def test_hello():
    """Test that hello() returns 'Hello, world!'"""
    result = hello()
    assert result == 'Hello, world!', f"Expected 'Hello, world!' but got '{result}'"
    print("✓ test_hello passed")


if __name__ == '__main__':
    test_hello()
    print("\nAll tests passed!")
