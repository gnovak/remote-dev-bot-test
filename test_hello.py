from hello_gpt_small import hello

def test_hello_returns_message():
    assert hello() == "Hello from gpt-small!"
