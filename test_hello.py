import unittest
from hello import hello


class TestHello(unittest.TestCase):
    def test_hello(self):
        result = hello()
        self.assertEqual(result, 'Hello, world!')
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
