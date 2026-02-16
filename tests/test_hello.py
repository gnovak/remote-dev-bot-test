import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello import hello


def test_hello():
    assert hello() == 'Hello, world!'


if __name__ == '__main__':
    test_hello()
    print("All tests passed!")
