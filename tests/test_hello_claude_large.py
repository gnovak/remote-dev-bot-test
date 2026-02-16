import sys
sys.path.insert(0, '/workspace')

from hello_claude_large import hello


def test_hello():
    result = hello()
    assert result == 'Hello from claude-large!'
