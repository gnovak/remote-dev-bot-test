# AGENTS.md

This is the test repository for [remote-dev-bot](https://github.com/gnovak/remote-dev-bot).

Issues here are created by the e2e test suite to verify that the agent can
resolve them. The issues are intentionally simple.

## Commit Attribution

Sign every commit with a `Co-Authored-By` trailer that identifies you (the
model) by name and version:

```
Co-Authored-By: <Your Model Name and Version> <noreply@your-provider.com>
```

Fill in your actual model name, version, and your provider's noreply address.

## gemini-large

```python
def hello_gemini_large():
    return 'Hello from gemini-large!'
```
