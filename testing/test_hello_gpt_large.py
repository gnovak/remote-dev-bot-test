import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hello_gpt_large import hello


def test_hello_returns_expected_message():
    assert hello() == "Hello from gpt-large!"
