import unittest
from hello_claude_medium import hello

class TestHelloClaudeMedium(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello from claude-medium!')

if __name__ == '__main__':
    unittest.main()
