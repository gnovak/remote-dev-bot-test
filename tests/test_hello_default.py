import unittest
import sys
from pathlib import Path

# Add parent directory to path to import hello_default
sys.path.insert(0, str(Path(__file__).parent.parent))

from hello_default import hello


class TestHelloDefault(unittest.TestCase):
    def test_hello_returns_correct_message(self):
        """Test that hello() returns 'Hello from default!'"""
        result = hello()
        self.assertEqual(result, 'Hello from default!')

    def test_hello_returns_string(self):
        """Test that hello() returns a string"""
        result = hello()
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
