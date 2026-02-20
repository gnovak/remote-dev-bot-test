
import unittest
from hi import hi

class TestHiFunction(unittest.TestCase):
    def test_hi(self):
        self.assertEqual(hi(), 'Hi!')

if __name__ == '__main__':
    unittest.main()
