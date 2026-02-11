import subprocess
import sys
import os


def test_hello_script_exists():
    """Test that hello.py exists."""
    assert os.path.exists('hello.py'), "hello.py should exist"


def test_hello_script_output():
    """Test that hello.py prints the correct message."""
    result = subprocess.run(
        [sys.executable, 'hello.py'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "hello.py should run without errors"
    assert result.stdout.strip() == 'Hello from remote-dev-bot-test', \
        "hello.py should print 'Hello from remote-dev-bot-test'"
