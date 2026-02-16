import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_claude_medium import hello


def test_hello():
    assert hello() == 'Hello from claude-medium!'


if __name__ == '__main__':
    test_hello()
    print("Test passed!")
