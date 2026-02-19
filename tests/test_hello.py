import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello import hello


class TestHello(unittest.TestCase):
    def test_hello_returns_hello_world(self):
        result = hello()
        self.assertEqual(result, 'Hello, world!')


if __name__ == '__main__':
    unittest.main()
