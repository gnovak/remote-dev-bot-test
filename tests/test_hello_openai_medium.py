from hello_openai_medium import hello


def test_hello_returns_expected_greeting() -> None:
    assert hello() == "Hello from openai-medium!"
