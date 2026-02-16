import unittest
from hello import hello


class TestHello(unittest.TestCase):
    def test_hello(self):
        """Test that hello() returns 'Hello, world!'"""
        self.assertEqual(hello(), 'Hello, world!')


if __name__ == '__main__':
    unittest.main()
