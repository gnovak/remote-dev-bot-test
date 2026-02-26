from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from hello_gpt_large import hello


def test_hello_returns_expected_message() -> None:
    assert hello() == "Hello from gpt-large!"
