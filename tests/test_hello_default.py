import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_default import hello


def test_hello():
    """Test that hello() returns 'Hello from default!'"""
    result = hello()
    assert result == 'Hello from default!', f"Expected 'Hello from default!' but got '{result}'"
    print("✓ test_hello passed")


if __name__ == "__main__":
    test_hello()
    print("\nAll tests passed!")
