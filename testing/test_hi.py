
import unittest
import sys
import os

# Add the parent directory to the Python path to import hi.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hi import hi

class TestHiFunction(unittest.TestCase):

    def test_hi_returns_hi(self):
        self.assertEqual(hi(), 'Hi!')

if __name__ == '__main__':
    unittest.main()
