import unittest
from hello_default import hello


class TestHelloDefault(unittest.TestCase):
    def test_hello(self):
        result = hello()
        self.assertEqual(result, 'Hello from default!')


if __name__ == '__main__':
    unittest.main()
