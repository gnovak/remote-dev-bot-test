"""Simple hello world module."""

from typing import Optional


def greet(name: Optional[str] = None) -> str:
    """Return a greeting string.

    Args:
        name: Optional name to greet. Defaults to 'World'.

    Returns:
        A greeting string.
    """
    target = name if name else "World"
    return f"Hello, {target}!"


if __name__ == "__main__":
    print(greet())
