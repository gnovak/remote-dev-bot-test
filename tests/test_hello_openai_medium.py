from hello_openai_medium import hello


def test_hello_returns_expected_string():
    assert hello() == "Hello from openai-medium!"
