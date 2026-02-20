import unittest

try:
    from hello_claude_small import hello
except Exception:
    hello = None  # type: ignore


class TestHelloClaudeSmall(unittest.TestCase):
    def test_hello_returns_expected_string(self):
        if hello is None:
            self.fail("hello_claude_small module could not be imported for testing.")
        self.assertEqual(hello(), 'Hello from claude-small!')


if __name__ == '__main__':
    unittest.main()
