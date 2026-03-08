"""Unit tests for .remote-dev-bot/lib/config.py."""
from __future__ import annotations

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".remote-dev-bot", "lib"))

import config as cfg


class TestNormalizeArgName:
    def test_spaces_become_underscores(self) -> None:
        assert cfg.normalize_arg_name("max iterations") == "max_iterations"

    def test_dashes_become_underscores(self) -> None:
        assert cfg.normalize_arg_name("max-iterations") == "max_iterations"

    def test_uppercase_lowercased(self) -> None:
        assert cfg.normalize_arg_name("Max_Iterations") == "max_iterations"

    def test_extra_files(self) -> None:
        assert cfg.normalize_arg_name("extra files") == "extra_files"


class TestParseArgs:
    def test_empty_lines(self) -> None:
        assert cfg.parse_args([]) == {}

    def test_integer_arg(self) -> None:
        assert cfg.parse_args(["max_iterations = 75"]) == {"max_iterations": 75}

    def test_list_arg(self) -> None:
        assert cfg.parse_args(["extra_files = a.txt b.txt"]) == {
            "extra_files": ["a.txt", "b.txt"]
        }

    def test_single_file_list(self) -> None:
        assert cfg.parse_args(["extra files = README.md"]) == {
            "extra_files": ["README.md"]
        }

    def test_comment_lines_ignored(self) -> None:
        assert cfg.parse_args(["# comment", "max_iterations = 5"]) == {
            "max_iterations": 5
        }

    def test_blank_lines_ignored(self) -> None:
        assert cfg.parse_args(["", "max_iterations = 10"]) == {"max_iterations": 10}

    def test_unknown_arg_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown argument"):
            cfg.parse_args(["unknown_key = value"])

    def test_bad_int_raises(self) -> None:
        with pytest.raises(ValueError, match="must be an integer"):
            cfg.parse_args(["max_iterations = notanint"])

    def test_timeout_minutes(self) -> None:
        assert cfg.parse_args(["timeout_minutes = 1"]) == {"timeout_minutes": 1}


class TestParseCommand:
    MODES = {"resolve", "design"}

    def test_bare_mode(self) -> None:
        assert cfg.parse_command("resolve", self.MODES) == ("resolve", "")

    def test_mode_with_alias(self) -> None:
        assert cfg.parse_command("resolve-claude-large", self.MODES) == (
            "resolve",
            "claude-large",
        )

    def test_case_insensitive(self) -> None:
        assert cfg.parse_command("Resolve-Claude-Large", self.MODES) == (
            "resolve",
            "claude-large",
        )

    def test_unknown_mode_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown mode"):
            cfg.parse_command("unknown", self.MODES)

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            cfg.parse_command("", self.MODES)


class TestDeepMerge:
    def test_simple_override(self) -> None:
        base = {"a": 1, "b": 2}
        override = {"b": 99, "c": 3}
        assert cfg.deep_merge(base, override) == {"a": 1, "b": 99, "c": 3}

    def test_nested_merge(self) -> None:
        base = {"agent": {"max_iterations": 50, "pr_type": "ready"}}
        override = {"agent": {"max_iterations": 75}}
        result = cfg.deep_merge(base, override)
        assert result["agent"]["max_iterations"] == 75
        assert result["agent"]["pr_type"] == "ready"

    def test_base_not_mutated(self) -> None:
        base = {"a": {"x": 1}}
        override = {"a": {"y": 2}}
        cfg.deep_merge(base, override)
        assert "y" not in base["a"]


class TestDetectApiProvider:
    def test_anthropic(self) -> None:
        assert cfg.detect_api_provider("anthropic/claude-sonnet-4-5") == "anthropic"

    def test_openai(self) -> None:
        assert cfg.detect_api_provider("openai/gpt-4") == "openai"

    def test_gemini(self) -> None:
        assert cfg.detect_api_provider("gemini/gemini-2.5-flash") == "gemini"

    def test_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown provider"):
            cfg.detect_api_provider("mistral/mistral-7b")
