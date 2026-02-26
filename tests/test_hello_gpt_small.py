import sys
from pathlib import Path

sys.path.append(Path(__file__).resolve().parents[1].as_posix())

from hello_gpt_small import hello

def test_hello_returns_expected_string():
    assert hello() == "Hello from gpt-small!"
