import unittest

try:
    from hello_openai_small import hello
except Exception:
    hello = None  # type: ignore


class TestHelloOpenAISmall(unittest.TestCase):
    def test_hello_returns_expected_string(self):
        if hello is None:
            self.fail("hello_openai_small module could not be imported for testing.")
        self.assertEqual(hello(), 'Hello from openai-small!')


if __name__ == '__main__':
    unittest.main()
