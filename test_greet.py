import unittest
from greet import greet


class TestGreet(unittest.TestCase):
    def test_greet_with_name(self):
        """Test greet function with a simple name"""
        self.assertEqual(greet('World'), 'Hello, World!')

    def test_greet_with_different_name(self):
        """Test greet function with different names"""
        self.assertEqual(greet('Alice'), 'Hello, Alice!')
        self.assertEqual(greet('Bob'), 'Hello, Bob!')

    def test_greet_with_empty_string(self):
        """Test greet function with empty string"""
        self.assertEqual(greet(''), 'Hello, !')


if __name__ == '__main__':
    unittest.main()
