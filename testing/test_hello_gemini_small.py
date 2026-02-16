
import unittest
from hello_gemini_small import hello

class TestHelloGeminiSmall(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello from gemini-small!')

if __name__ == '__main__':
    unittest.main()
