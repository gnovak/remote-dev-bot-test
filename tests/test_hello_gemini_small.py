
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hello_gemini_small import hello

def test_hello():
    assert hello() == 'Hello from gemini-small!'

