import unittest
from hello_claude_small import hello


class TestHelloClaudeSmall(unittest.TestCase):
    def test_hello(self):
        result = hello()
        self.assertEqual(result, 'Hello from claude-small!')
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
