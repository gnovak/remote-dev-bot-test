"""Comprehensive unit tests for .remote-dev-bot/lib/config.py.

Tests cover:
- normalize_arg_name: string normalization of argument names
- parse_args: parsing inline argument lines
- parse_command: parsing command strings into (mode, model_alias)
- parse_invocation: parsing full comment bodies
- deep_merge: recursive dict merging
- resolve_config: full config resolution with file I/O (via temp files)
- detect_api_provider: provider detection from model ID strings
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Allow importing from .remote-dev-bot/lib without installing
sys.path.insert(0, str(Path(__file__).parent.parent / ".remote-dev-bot" / "lib"))

import config


class TestNormalizeArgName(unittest.TestCase):
    """Tests for config.normalize_arg_name."""

    def test_lowercase_passthrough(self) -> None:
        """Already-lowercase names with underscores pass through unchanged."""
        self.assertEqual(config.normalize_arg_name("max_iterations"), "max_iterations")

    def test_spaces_become_underscores(self) -> None:
        """Spaces are replaced with underscores."""
        self.assertEqual(config.normalize_arg_name("max iterations"), "max_iterations")

    def test_dashes_become_underscores(self) -> None:
        """Dashes are replaced with underscores."""
        self.assertEqual(config.normalize_arg_name("max-iterations"), "max_iterations")

    def test_mixed_separators(self) -> None:
        """Mixed separators are all normalized to underscores."""
        self.assertEqual(config.normalize_arg_name("extra files"), "extra_files")
        self.assertEqual(config.normalize_arg_name("extra-files"), "extra_files")

    def test_uppercase_lowercased(self) -> None:
        """Uppercase letters are lowercased."""
        self.assertEqual(config.normalize_arg_name("Max_Iterations"), "max_iterations")
        self.assertEqual(config.normalize_arg_name("MAX_ITERATIONS"), "max_iterations")

    def test_leading_trailing_whitespace_stripped(self) -> None:
        """Leading and trailing whitespace is stripped."""
        self.assertEqual(config.normalize_arg_name("  max_iterations  "), "max_iterations")

    def test_consecutive_spaces(self) -> None:
        """Multiple consecutive spaces collapse to a single underscore."""
        self.assertEqual(config.normalize_arg_name("max  iterations"), "max_iterations")

    def test_single_word(self) -> None:
        """Single words are just lowercased."""
        self.assertEqual(config.normalize_arg_name("Branch"), "branch")


class TestParseArgs(unittest.TestCase):
    """Tests for config.parse_args."""

    def test_empty_list(self) -> None:
        """Empty input yields empty dict."""
        self.assertEqual(config.parse_args([]), {})

    def test_max_iterations_int(self) -> None:
        """max_iterations is parsed as an integer."""
        result = config.parse_args(["max iterations = 75"])
        self.assertEqual(result, {"max_iterations": 75})

    def test_dashed_name(self) -> None:
        """Dashed argument names are normalized."""
        result = config.parse_args(["max-iterations = 100"])
        self.assertEqual(result, {"max_iterations": 100})

    def test_timeout_minutes(self) -> None:
        """timeout_minutes is parsed as an integer."""
        result = config.parse_args(["timeout_minutes = 30"])
        self.assertEqual(result, {"timeout_minutes": 30})

    def test_extra_files_single(self) -> None:
        """Single extra file is returned as a one-element list."""
        result = config.parse_args(["extra files = README.md"])
        self.assertEqual(result, {"extra_files": ["README.md"]})

    def test_extra_files_multiple(self) -> None:
        """Multiple extra files are space-split into a list."""
        result = config.parse_args(["extra_files = file1.txt file2.txt"])
        self.assertEqual(result, {"extra_files": ["file1.txt", "file2.txt"]})

    def test_branch_string(self) -> None:
        """branch is parsed as a plain string."""
        result = config.parse_args(["branch = feature/my-branch"])
        self.assertEqual(result, {"branch": "feature/my-branch"})

    def test_comment_lines_skipped(self) -> None:
        """Lines starting with # are ignored."""
        result = config.parse_args(["# this is a comment", "max_iterations = 5"])
        self.assertEqual(result, {"max_iterations": 5})

    def test_blank_lines_skipped(self) -> None:
        """Blank lines are ignored."""
        result = config.parse_args(["", "  ", "max_iterations = 10"])
        self.assertEqual(result, {"max_iterations": 10})

    def test_lines_without_equals_skipped(self) -> None:
        """Lines without '=' are silently skipped."""
        result = config.parse_args(["some random text", "max_iterations = 5"])
        self.assertEqual(result, {"max_iterations": 5})

    def test_unknown_arg_raises(self) -> None:
        """Unknown argument names raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            config.parse_args(["unknown_arg = value"])
        self.assertIn("unknown_arg", str(ctx.exception))

    def test_invalid_int_raises(self) -> None:
        """Non-integer value for int arg raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            config.parse_args(["max_iterations = not_a_number"])
        self.assertIn("max_iterations", str(ctx.exception))

    def test_multiple_args(self) -> None:
        """Multiple valid argument lines are all parsed."""
        result = config.parse_args([
            "max_iterations = 50",
            "timeout_minutes = 15",
            "extra_files = a.py b.py",
        ])
        self.assertEqual(result, {
            "max_iterations": 50,
            "timeout_minutes": 15,
            "extra_files": ["a.py", "b.py"],
        })

    def test_target_branch_backcompat(self) -> None:
        """target_branch is accepted as backward-compat alias for branch."""
        result = config.parse_args(["target_branch = main"])
        self.assertEqual(result, {"target_branch": "main"})


class TestParseCommand(unittest.TestCase):
    """Tests for config.parse_command."""

    KNOWN_MODES: Set[str] = {"resolve", "design"}

    def test_simple_resolve(self) -> None:
        """Plain 'resolve' gives ('resolve', '')."""
        self.assertEqual(
            config.parse_command("resolve", self.KNOWN_MODES),
            ("resolve", ""),
        )

    def test_resolve_with_model(self) -> None:
        """'resolve-claude-large' gives ('resolve', 'claude-large')."""
        self.assertEqual(
            config.parse_command("resolve-claude-large", self.KNOWN_MODES),
            ("resolve", "claude-large"),
        )

    def test_design_mode(self) -> None:
        """Design mode is recognized."""
        self.assertEqual(
            config.parse_command("design", self.KNOWN_MODES),
            ("design", ""),
        )

    def test_design_with_model(self) -> None:
        """'design-claude-small' gives ('design', 'claude-small')."""
        self.assertEqual(
            config.parse_command("design-claude-small", self.KNOWN_MODES),
            ("design", "claude-small"),
        )

    def test_case_insensitive(self) -> None:
        """Command strings are case-insensitive."""
        self.assertEqual(
            config.parse_command("Resolve-Claude-Large", self.KNOWN_MODES),
            ("resolve", "claude-large"),
        )

    def test_empty_string_raises(self) -> None:
        """Empty command string raises ValueError."""
        with self.assertRaises(ValueError):
            config.parse_command("", self.KNOWN_MODES)

    def test_unknown_mode_raises(self) -> None:
        """Unknown mode raises ValueError mentioning the mode."""
        with self.assertRaises(ValueError) as ctx:
            config.parse_command("unknown", self.KNOWN_MODES)
        self.assertIn("unknown", str(ctx.exception))

    def test_model_with_multiple_dashes(self) -> None:
        """Model aliases with multiple dashes are preserved correctly."""
        # "resolve-claude-opus-3" → mode=resolve, alias=claude-opus-3
        mode, alias = config.parse_command("resolve-claude-opus-3", self.KNOWN_MODES)
        self.assertEqual(mode, "resolve")
        self.assertIn("claude", alias)


class TestParseInvocation(unittest.TestCase):
    """Tests for config.parse_invocation."""

    KNOWN_MODES: Set[str] = {"resolve", "design"}

    def test_simple_slash_agent_resolve(self) -> None:
        """/agent resolve parses to ('resolve', '', {})."""
        mode, alias, args = config.parse_invocation(
            "/agent resolve", self.KNOWN_MODES
        )
        self.assertEqual(mode, "resolve")
        self.assertEqual(alias, "")
        self.assertEqual(args, {})

    def test_dash_syntax(self) -> None:
        """/agent-resolve (dash) parses correctly."""
        mode, alias, args = config.parse_invocation(
            "/agent-resolve", self.KNOWN_MODES
        )
        self.assertEqual(mode, "resolve")

    def test_model_in_command(self) -> None:
        """Model alias embedded in command is parsed out."""
        mode, alias, args = config.parse_invocation(
            "/agent-resolve-claude-large", self.KNOWN_MODES
        )
        self.assertEqual(mode, "resolve")
        self.assertEqual(alias, "claude-large")

    def test_inline_args(self) -> None:
        """Inline args on subsequent lines are parsed."""
        body = "/agent resolve\nmax iterations = 75"
        mode, alias, args = config.parse_invocation(body, self.KNOWN_MODES)
        self.assertEqual(mode, "resolve")
        self.assertEqual(args, {"max_iterations": 75})

    def test_extra_files_arg(self) -> None:
        """extra_files inline arg is parsed as a list."""
        body = "/agent-design-claude-small\nextra_files = a.txt b.txt"
        mode, alias, args = config.parse_invocation(body, self.KNOWN_MODES)
        self.assertEqual(mode, "design")
        self.assertEqual(alias, "claude-small")
        self.assertEqual(args["extra_files"], ["a.txt", "b.txt"])

    def test_custom_prefix(self) -> None:
        """Custom command prefix (e.g. 'dogfood') is respected."""
        mode, alias, args = config.parse_invocation(
            "/dogfood resolve", self.KNOWN_MODES, command_prefix="dogfood"
        )
        self.assertEqual(mode, "resolve")

    def test_timeout_arg(self) -> None:
        """timeout_minutes inline arg is parsed."""
        body = "/agent resolve\ntimeout_minutes = 5"
        _, _, args = config.parse_invocation(body, self.KNOWN_MODES)
        self.assertEqual(args["timeout_minutes"], 5)


class TestDeepMerge(unittest.TestCase):
    """Tests for config.deep_merge."""

    def test_empty_dicts(self) -> None:
        """Merging two empty dicts yields an empty dict."""
        self.assertEqual(config.deep_merge({}, {}), {})

    def test_override_wins_for_scalars(self) -> None:
        """Override values win for scalar keys."""
        result = config.deep_merge({"a": 1}, {"a": 2})
        self.assertEqual(result["a"], 2)

    def test_base_keys_preserved_when_not_overridden(self) -> None:
        """Keys in base that are not in override are preserved."""
        result = config.deep_merge({"a": 1, "b": 2}, {"b": 3})
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 3)

    def test_nested_dict_merged_recursively(self) -> None:
        """Nested dicts are merged recursively."""
        base = {"agent": {"max_iterations": 50, "pr_type": "ready"}}
        override = {"agent": {"max_iterations": 75}}
        result = config.deep_merge(base, override)
        self.assertEqual(result["agent"]["max_iterations"], 75)
        self.assertEqual(result["agent"]["pr_type"], "ready")

    def test_override_scalar_with_dict_replaces(self) -> None:
        """If base has a scalar and override has a dict for the same key, dict wins."""
        result = config.deep_merge({"a": 1}, {"a": {"nested": True}})
        self.assertEqual(result["a"], {"nested": True})

    def test_base_not_mutated(self) -> None:
        """The original base dict is not mutated."""
        base = {"a": {"x": 1}}
        override = {"a": {"y": 2}}
        config.deep_merge(base, override)
        self.assertNotIn("y", base["a"])

    def test_lists_are_not_merged(self) -> None:
        """List values in override replace list values in base (no concat)."""
        base = {"files": ["a.py", "b.py"]}
        override = {"files": ["c.py"]}
        result = config.deep_merge(base, override)
        self.assertEqual(result["files"], ["c.py"])


class TestDetectApiProvider(unittest.TestCase):
    """Tests for config.detect_api_provider."""

    def test_anthropic(self) -> None:
        """Anthropic prefix is detected correctly."""
        self.assertEqual(
            config.detect_api_provider("anthropic/claude-sonnet-4-5"), "anthropic"
        )

    def test_openai(self) -> None:
        """OpenAI prefix is detected correctly."""
        self.assertEqual(
            config.detect_api_provider("openai/gpt-5-nano"), "openai"
        )

    def test_gemini(self) -> None:
        """Gemini prefix is detected correctly."""
        self.assertEqual(
            config.detect_api_provider("gemini/gemini-2.5-flash"), "gemini"
        )

    def test_unknown_provider_raises(self) -> None:
        """Unknown provider raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            config.detect_api_provider("unknown/some-model")
        self.assertIn("unknown/some-model", str(ctx.exception))


class TestResolveConfig(unittest.TestCase):
    """Integration tests for config.resolve_config using temporary config files."""

    MINIMAL_BASE: Dict[str, Any] = {
        "models": {
            "claude-small": {"id": "anthropic/claude-haiku-3-5"},
            "claude-large": {"id": "anthropic/claude-sonnet-4-5"},
        },
        "default_model": "claude-small",
        "modes": {
            "resolve": {
                "action": "pr",
                "default_model": "claude-small",
            },
            "design": {
                "action": "design",
                "default_model": "claude-large",
            },
        },
        "agent": {
            "max_iterations": 50,
            "pr_type": "ready",
            "on_failure": "comment",
            "branch": "main",
        },
    }

    def _write_yaml(self, data: Dict[str, Any]) -> str:
        """Write a YAML config to a temp file and return its path."""
        import yaml
        tf = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        yaml.dump(data, tf)
        tf.close()
        return tf.name

    def setUp(self) -> None:
        """Create temp base config file for each test."""
        self.base_path = self._write_yaml(self.MINIMAL_BASE)
        self.override_path = tempfile.mktemp(suffix=".yaml")  # doesn't exist
        self.addCleanup(os.unlink, self.base_path)

    def test_resolve_defaults(self) -> None:
        """Basic resolve command returns expected defaults."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve"
        )
        self.assertEqual(result["mode"], "resolve")
        self.assertEqual(result["action"], "pr")
        self.assertEqual(result["alias"], "claude-small")
        self.assertEqual(result["model"], "anthropic/claude-haiku-3-5")
        self.assertEqual(result["max_iterations"], 50)
        self.assertEqual(result["pr_type"], "ready")
        self.assertEqual(result["target_branch"], "main")
        self.assertFalse(result["has_override"])

    def test_resolve_with_explicit_model(self) -> None:
        """Explicit model alias overrides the mode default."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve-claude-large"
        )
        self.assertEqual(result["alias"], "claude-large")
        self.assertEqual(result["model"], "anthropic/claude-sonnet-4-5")

    def test_design_mode(self) -> None:
        """Design mode is resolved with its own defaults."""
        result = config.resolve_config(
            self.base_path, self.override_path, "design"
        )
        self.assertEqual(result["mode"], "design")
        self.assertEqual(result["action"], "design")
        self.assertEqual(result["alias"], "claude-large")

    def test_override_config_merged(self) -> None:
        """Override config from target repo is merged in."""
        import yaml
        override_data = {
            "agent": {
                "max_iterations": 75,
            }
        }
        override_path = self._write_yaml(override_data)
        self.addCleanup(os.unlink, override_path)

        result = config.resolve_config(
            self.base_path, override_path, "resolve"
        )
        self.assertEqual(result["max_iterations"], 75)
        self.assertTrue(result["has_override"])

    def test_inline_args_override_iterations(self) -> None:
        """Inline args dict overrides max_iterations."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve",
            args={"max_iterations": 99}
        )
        self.assertEqual(result["max_iterations"], 99)

    def test_timeout_minutes_per_invocation(self) -> None:
        """per-invocation timeout_minutes overrides the default."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve",
            timeout_minutes=30
        )
        self.assertEqual(result["timeout_minutes"], 30)

    def test_default_timeout_when_not_set(self) -> None:
        """Default timeout is used when not specified."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve"
        )
        self.assertEqual(result["timeout_minutes"], config.DEFAULT_TIMEOUT_MINUTES)

    def test_inline_timeout_arg(self) -> None:
        """timeout_minutes in inline args is respected."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve",
            args={"timeout_minutes": 5}
        )
        self.assertEqual(result["timeout_minutes"], 5)

    def test_unknown_mode_raises(self) -> None:
        """Unknown mode raises ValueError."""
        with self.assertRaises(ValueError):
            config.resolve_config(
                self.base_path, self.override_path, "nonexistent-mode"
            )

    def test_unknown_model_alias_raises(self) -> None:
        """Unknown model alias raises KeyError."""
        with self.assertRaises(KeyError):
            config.resolve_config(
                self.base_path, self.override_path, "resolve-no-such-model"
            )

    def test_branch_inline_arg(self) -> None:
        """branch inline arg sets target_branch and marks it explicit."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve",
            args={"branch": "feature/my-branch"}
        )
        self.assertEqual(result["target_branch"], "feature/my-branch")
        self.assertTrue(result["target_branch_explicit"])

    def test_extra_files_additive(self) -> None:
        """extra_files from inline args are appended (additive, no dupes)."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve",
            args={"extra_files": ["new_file.py"]}
        )
        self.assertIn("new_file.py", result.get("extra_files", []))

    def test_graceful_wrapup_defaults(self) -> None:
        """Graceful wrapup settings default to enabled=True, threshold=0.8."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve"
        )
        self.assertTrue(result["graceful_wrapup_enabled"])
        self.assertAlmostEqual(result["graceful_wrapup_threshold"], 0.8)
        # wrapup_iteration = int(50 * 0.8) = 40
        self.assertEqual(result["graceful_wrapup_iteration"], 40)

    def test_assign_issue_default_true(self) -> None:
        """assign_issue defaults to True."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve"
        )
        self.assertTrue(result["assign_issue"])

    def test_assign_pr_default_true(self) -> None:
        """assign_pr defaults to True."""
        result = config.resolve_config(
            self.base_path, self.override_path, "resolve"
        )
        self.assertTrue(result["assign_pr"])

    def test_on_failure_invalid_raises(self) -> None:
        """Invalid on_failure value raises ValueError."""
        import yaml
        override_data = {"agent": {"on_failure": "invalid_value"}}
        override_path = self._write_yaml(override_data)
        self.addCleanup(os.unlink, override_path)

        with self.assertRaises(ValueError) as ctx:
            config.resolve_config(self.base_path, override_path, "resolve")
        self.assertIn("on_failure", str(ctx.exception))


class TestDocstrings(unittest.TestCase):
    """Verify that key public functions have docstrings."""

    def test_normalize_arg_name_has_docstring(self) -> None:
        self.assertIsNotNone(config.normalize_arg_name.__doc__)

    def test_parse_args_has_docstring(self) -> None:
        self.assertIsNotNone(config.parse_args.__doc__)

    def test_parse_command_has_docstring(self) -> None:
        self.assertIsNotNone(config.parse_command.__doc__)

    def test_parse_invocation_has_docstring(self) -> None:
        self.assertIsNotNone(config.parse_invocation.__doc__)

    def test_resolve_config_has_docstring(self) -> None:
        self.assertIsNotNone(config.resolve_config.__doc__)

    def test_deep_merge_has_docstring(self) -> None:
        self.assertIsNotNone(config.deep_merge.__doc__)

    def test_detect_api_provider_has_docstring(self) -> None:
        self.assertIsNotNone(config.detect_api_provider.__doc__)


if __name__ == "__main__":
    unittest.main()
