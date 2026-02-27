import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from hello_gpt_large import hello


def test_hello():
    assert hello() == "Hello from gpt-large!"
