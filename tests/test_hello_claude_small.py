import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_claude_small import hello


def test_hello():
    result = hello()
    assert result == 'Hello from claude-small!'
    print(f"Test passed! Function returned: {result}")


if __name__ == "__main__":
    test_hello()
    print("All tests passed!")
