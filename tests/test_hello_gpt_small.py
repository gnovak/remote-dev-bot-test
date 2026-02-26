from hello_gpt_small import hello

def test_hello_returns_expected_greeting():
    assert hello() == 'Hello from gpt-small!'
