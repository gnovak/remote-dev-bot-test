
import unittest
from hello_gemini_medium import hello

class TestHelloGeminiMedium(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), 'Hello from gemini-medium!')

if __name__ == '__main__':
    unittest.main()
