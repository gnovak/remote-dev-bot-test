import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_default import hello


def test_hello():
    """Test that hello() returns the correct greeting."""
    result = hello()
    assert result == 'Hello from default!', f"Expected 'Hello from default!' but got '{result}'"


if __name__ == '__main__':
    test_hello()
    print("All tests passed!")
