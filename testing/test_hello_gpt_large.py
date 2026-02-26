import unittest

from hello_gpt_large import hello


class TestHelloGptLarge(unittest.TestCase):
    def test_hello_returns_expected_message(self) -> None:
        self.assertEqual(hello(), "Hello from gpt-large!")


if __name__ == "__main__":
    unittest.main()
