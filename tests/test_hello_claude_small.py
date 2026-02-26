import sys
sys.path.insert(0, '/workspace')

from hello_claude_small import hello


def test_hello():
    assert hello() == 'Hello from claude-small!'


if __name__ == '__main__':
    test_hello()
    print("All tests passed!")
