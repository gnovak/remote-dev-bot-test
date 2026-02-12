from greet_openai import greet

def test_greet_returns_openai_message() -> None:
    assert greet("World") == "Hello, World! (from OpenAI)"
