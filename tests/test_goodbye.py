"""Tests for the goodbye script."""
import subprocess
import sys
from io import StringIO

import pytest

sys.path.insert(0, "/workspace")
from goodbye import goodbye


def test_goodbye_function(capsys):
    """Test that the goodbye function prints the correct message."""
    goodbye()
    captured = capsys.readouterr()
    assert captured.out == "goodbye until next time\n"


def test_goodbye_script():
    """Test that the goodbye script runs correctly as a standalone script."""
    result = subprocess.run(
        [sys.executable, "/workspace/goodbye.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout == "goodbye until next time\n"
