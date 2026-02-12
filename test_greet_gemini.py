
import unittest
from greet_gemini import greet

class TestGreetGemini(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World! (from Gemini)")
        self.assertEqual(greet("OpenHands"), "Hello, OpenHands! (from Gemini)")
        self.assertEqual(greet("Agent"), "Hello, Agent! (from Gemini)")

if __name__ == '__main__':
    unittest.main()
