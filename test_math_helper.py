import unittest
from math_helper import add, subtract


class TestMathHelper(unittest.TestCase):
    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, 20), 30)

    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        self.assertEqual(add(-5, -3), -8)
        self.assertEqual(add(-10, 5), -5)

    def test_add_zero(self):
        """Test adding zero"""
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, 5), 5)

    def test_add_floats(self):
        """Test adding floating point numbers"""
        self.assertAlmostEqual(add(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        self.assertEqual(subtract(5, 2), 3)
        self.assertEqual(subtract(10, 20), -10)
        self.assertEqual(subtract(-5, -3), -2)
        self.assertEqual(subtract(-10, 5), -15)
        self.assertEqual(subtract(5, 0), 5)
        self.assertEqual(subtract(0, 5), -5)
        self.assertAlmostEqual(subtract(2.5, 1.5), 1.0)
        self.assertAlmostEqual(subtract(0.3, 0.1), 0.2)


if __name__ == '__main__':
    unittest.main()
