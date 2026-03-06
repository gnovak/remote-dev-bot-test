"""Comprehensive unit tests for .remote-dev-bot/lib/feedback.py.

Tests cover:
- InstallProblem dataclass: construction, from_exception factory
- InstallReport dataclass: add_problem, has_problems, to_dict, to_json
- Formatting helpers: format_issue_title, format_issue_body, format_metoo_comment
- format_summary_issue_body: multi-problem summary formatting
- get_environment_info: returns dict with expected keys
- get_consent_prompt: returns a non-empty consent string
- report_problems: dry_run mode, problem-count limits, return structure
"""

import json
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

# Allow importing from .remote-dev-bot/lib
sys.path.insert(0, str(Path(__file__).parent.parent / ".remote-dev-bot" / "lib"))

import feedback
from feedback import (
    DEFAULT_REPO,
    MAX_ISSUES_PER_INSTALL,
    InstallProblem,
    InstallReport,
    _append_conversation_summary,
    format_issue_body,
    format_issue_title,
    format_metoo_comment,
    format_summary_issue_body,
    get_consent_prompt,
    get_environment_info,
    report_problems,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_problem(
    step: str = "1.1",
    title: str = "Test Step",
    result: str = "fail",
    expected: str = "Expected X",
    actual: str = "Actual Y",
    workaround: Optional[str] = None,
    suggested_fix: Optional[str] = None,
) -> InstallProblem:
    """Factory for test InstallProblem instances."""
    return InstallProblem(
        step=step,
        title=title,
        result=result,
        expected=expected,
        actual=actual,
        workaround=workaround,
        suggested_fix=suggested_fix,
    )


# ---------------------------------------------------------------------------
# InstallProblem tests
# ---------------------------------------------------------------------------

class TestInstallProblem(unittest.TestCase):
    """Tests for the InstallProblem dataclass."""

    def test_basic_construction(self) -> None:
        """Fields are stored correctly."""
        p = _make_problem()
        self.assertEqual(p.step, "1.1")
        self.assertEqual(p.title, "Test Step")
        self.assertEqual(p.result, "fail")
        self.assertEqual(p.expected, "Expected X")
        self.assertEqual(p.actual, "Actual Y")
        self.assertIsNone(p.workaround)
        self.assertIsNone(p.suggested_fix)

    def test_optional_fields_set(self) -> None:
        """Optional workaround and suggested_fix fields are stored when provided."""
        p = _make_problem(workaround="Did Z instead", suggested_fix="Update step N")
        self.assertEqual(p.workaround, "Did Z instead")
        self.assertEqual(p.suggested_fix, "Update step N")

    def test_from_exception_factory(self) -> None:
        """from_exception creates a problem with result='fail' and exception details."""
        exc = ValueError("something went wrong")
        p = InstallProblem.from_exception(
            step="2.3",
            title="Some Step",
            exc=exc,
            expected="Should have worked",
        )
        self.assertEqual(p.step, "2.3")
        self.assertEqual(p.title, "Some Step")
        self.assertEqual(p.result, "fail")
        self.assertIn("ValueError", p.actual)
        self.assertIn("something went wrong", p.actual)

    def test_from_exception_with_workaround(self) -> None:
        """from_exception preserves optional workaround field."""
        exc = RuntimeError("oops")
        p = InstallProblem.from_exception(
            step="3.0",
            title="Another Step",
            exc=exc,
            expected="Works",
            workaround="Manually edited file",
        )
        self.assertEqual(p.workaround, "Manually edited file")


# ---------------------------------------------------------------------------
# InstallReport tests
# ---------------------------------------------------------------------------

class TestInstallReport(unittest.TestCase):
    """Tests for the InstallReport dataclass."""

    def test_default_construction(self) -> None:
        """Default construction auto-populates environment fields."""
        report = InstallReport()
        self.assertIsInstance(report.os_info, str)
        self.assertIsInstance(report.shell, str)
        self.assertIsInstance(report.python_version, str)
        self.assertEqual(report.problems, [])
        self.assertIsNone(report.conversation_summary)

    def test_has_problems_empty(self) -> None:
        """has_problems() returns False when no problems exist."""
        report = InstallReport()
        self.assertFalse(report.has_problems())

    def test_has_problems_after_add(self) -> None:
        """has_problems() returns True after a problem is added."""
        report = InstallReport()
        report.add_problem(
            step="1.0", title="T", result="fail",
            expected="E", actual="A"
        )
        self.assertTrue(report.has_problems())

    def test_add_problem_stores_correctly(self) -> None:
        """add_problem appends a correctly constructed InstallProblem."""
        report = InstallReport()
        report.add_problem(
            step="2.1", title="Enable Actions",
            result="fail", expected="X", actual="Y",
            workaround="W", suggested_fix="SF",
        )
        self.assertEqual(len(report.problems), 1)
        p = report.problems[0]
        self.assertEqual(p.step, "2.1")
        self.assertEqual(p.workaround, "W")

    def test_set_conversation_summary(self) -> None:
        """set_conversation_summary stores the summary."""
        report = InstallReport()
        report.set_conversation_summary("All went well except step 3")
        self.assertEqual(report.conversation_summary, "All went well except step 3")

    def test_to_dict_structure(self) -> None:
        """to_dict() returns expected keys."""
        report = InstallReport()
        report.add_problem(
            step="1.1", title="T", result="fail", expected="E", actual="A"
        )
        d = report.to_dict()
        self.assertIn("os", d)
        self.assertIn("shell", d)
        self.assertIn("python", d)
        self.assertIn("problems", d)
        self.assertEqual(len(d["problems"]), 1)
        self.assertEqual(d["problems"][0]["step"], "1.1")

    def test_to_json_valid(self) -> None:
        """to_json() returns valid JSON."""
        report = InstallReport()
        json_str = report.to_json()
        parsed = json.loads(json_str)
        self.assertIn("os", parsed)

    def test_multiple_problems(self) -> None:
        """Multiple problems are stored in order."""
        report = InstallReport()
        for i in range(3):
            report.add_problem(
                step=str(i), title=f"Step {i}",
                result="fail", expected="E", actual="A"
            )
        self.assertEqual(len(report.problems), 3)


# ---------------------------------------------------------------------------
# Formatting helpers tests
# ---------------------------------------------------------------------------

class TestFormatIssueTitle(unittest.TestCase):
    """Tests for feedback.format_issue_title."""

    def test_title_includes_step_and_title(self) -> None:
        """Issue title includes both step number and step title."""
        p = _make_problem(step="2.1", title="Enable Actions Permissions")
        title = format_issue_title(p)
        self.assertIn("2.1", title)
        self.assertIn("Enable Actions Permissions", title)

    def test_title_is_string(self) -> None:
        """Return value is a string."""
        p = _make_problem()
        self.assertIsInstance(format_issue_title(p), str)


class TestFormatIssueBody(unittest.TestCase):
    """Tests for feedback.format_issue_body."""

    ENV_INFO: Dict[str, str] = {
        "os": "Linux-5.15",
        "shell": "/bin/bash",
        "python": "3.12.0",
    }

    def test_body_contains_env_info(self) -> None:
        """Body includes OS, shell, and Python version."""
        p = _make_problem()
        body = format_issue_body(p, self.ENV_INFO)
        self.assertIn("Linux-5.15", body)
        self.assertIn("/bin/bash", body)
        self.assertIn("3.12.0", body)

    def test_body_contains_expected_and_actual(self) -> None:
        """Body includes expected and actual behaviour."""
        p = _make_problem(expected="It should work", actual="It blew up")
        body = format_issue_body(p, self.ENV_INFO)
        self.assertIn("It should work", body)
        self.assertIn("It blew up", body)

    def test_workaround_included_when_present(self) -> None:
        """Workaround section is included when the field is set."""
        p = _make_problem(workaround="Ran manually")
        body = format_issue_body(p, self.ENV_INFO)
        self.assertIn("Ran manually", body)

    def test_workaround_absent_when_none(self) -> None:
        """Workaround section is absent when the field is None."""
        p = _make_problem()
        body = format_issue_body(p, self.ENV_INFO)
        self.assertNotIn("Workaround", body)

    def test_suggested_fix_included_when_present(self) -> None:
        """Suggested fix section is included when set."""
        p = _make_problem(suggested_fix="Update the runbook")
        body = format_issue_body(p, self.ENV_INFO)
        self.assertIn("Update the runbook", body)

    def test_suggested_fix_absent_when_none(self) -> None:
        """Suggested fix section is absent when None."""
        p = _make_problem()
        body = format_issue_body(p, self.ENV_INFO)
        self.assertNotIn("Suggested fix", body)


class TestFormatMetooComment(unittest.TestCase):
    """Tests for feedback.format_metoo_comment."""

    ENV_INFO: Dict[str, str] = {
        "os": "macOS-14.0",
        "shell": "/bin/zsh",
        "python": "3.11.5",
    }

    def test_comment_includes_me_too(self) -> None:
        """Comment starts with or contains 'Me too'."""
        p = _make_problem()
        comment = format_metoo_comment(p, self.ENV_INFO)
        self.assertIn("Me too", comment)

    def test_comment_includes_env(self) -> None:
        """Comment includes OS and shell info."""
        p = _make_problem()
        comment = format_metoo_comment(p, self.ENV_INFO)
        self.assertIn("macOS-14.0", comment)

    def test_comment_includes_actual(self) -> None:
        """Comment describes what actually happened."""
        p = _make_problem(actual="Access denied")
        comment = format_metoo_comment(p, self.ENV_INFO)
        self.assertIn("Access denied", comment)

    def test_workaround_in_comment_when_present(self) -> None:
        """Workaround is included in comment when set."""
        p = _make_problem(workaround="Skipped that step")
        comment = format_metoo_comment(p, self.ENV_INFO)
        self.assertIn("Skipped that step", comment)


class TestFormatSummaryIssueBody(unittest.TestCase):
    """Tests for feedback.format_summary_issue_body."""

    def _make_report_with_n_problems(self, n: int) -> InstallReport:
        report = InstallReport()
        for i in range(n):
            report.add_problem(
                step=str(i), title=f"Step {i}",
                result="fail", expected="E", actual=f"Error {i}"
            )
        return report

    def test_body_mentions_problem_count(self) -> None:
        """Summary body mentions the number of problems."""
        report = self._make_report_with_n_problems(4)
        body = format_summary_issue_body(report)
        self.assertIn("4", body)

    def test_body_lists_all_steps(self) -> None:
        """Summary body includes info for each individual problem."""
        report = self._make_report_with_n_problems(3)
        body = format_summary_issue_body(report)
        for i in range(3):
            self.assertIn(f"Error {i}", body)

    def test_conversation_summary_appended(self) -> None:
        """Conversation summary is appended when set."""
        report = self._make_report_with_n_problems(2)
        report.set_conversation_summary("Long session summary here")
        body = format_summary_issue_body(report)
        self.assertIn("Long session summary here", body)


class TestAppendConversationSummary(unittest.TestCase):
    """Tests for feedback._append_conversation_summary."""

    def test_appends_when_summary_set(self) -> None:
        """Summary text is appended to the body."""
        report = InstallReport()
        report.set_conversation_summary("My summary")
        result = _append_conversation_summary("Base body.\n", report)
        self.assertIn("My summary", result)
        self.assertIn("Base body.", result)

    def test_unchanged_when_no_summary(self) -> None:
        """Body is returned unchanged when no summary is set."""
        report = InstallReport()
        result = _append_conversation_summary("Base body.\n", report)
        self.assertEqual(result, "Base body.\n")


class TestGetEnvironmentInfo(unittest.TestCase):
    """Tests for feedback.get_environment_info."""

    def test_returns_dict_with_required_keys(self) -> None:
        """Returns a dict with 'os', 'shell', and 'python' keys."""
        info = get_environment_info()
        self.assertIn("os", info)
        self.assertIn("shell", info)
        self.assertIn("python", info)

    def test_values_are_strings(self) -> None:
        """All values in the dict are strings."""
        info = get_environment_info()
        for key, val in info.items():
            self.assertIsInstance(val, str, f"Key '{key}' should be a string")


class TestGetConsentPrompt(unittest.TestCase):
    """Tests for feedback.get_consent_prompt."""

    def test_prompt_is_nonempty_string(self) -> None:
        """Consent prompt is a non-empty string."""
        report = InstallReport()
        report.add_problem("1.0", "T", "fail", "E", "A")
        prompt = get_consent_prompt(report)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_prompt_mentions_problem_count(self) -> None:
        """Prompt mentions the number of problems."""
        report = InstallReport()
        report.add_problem("1.0", "T", "fail", "E", "A")
        report.add_problem("1.1", "U", "fail", "E", "A")
        prompt = get_consent_prompt(report)
        self.assertIn("2", prompt)

    def test_prompt_mentions_github(self) -> None:
        """Prompt mentions GitHub (so user knows where data goes)."""
        report = InstallReport()
        report.add_problem("1.0", "T", "fail", "E", "A")
        prompt = get_consent_prompt(report)
        self.assertIn("GitHub", prompt)

    def test_prompt_singular_problem(self) -> None:
        """Prompt uses singular 'problem' for a single problem."""
        report = InstallReport()
        report.add_problem("1.0", "T", "fail", "E", "A")
        prompt = get_consent_prompt(report)
        # Should say "1 problem" not "1 problems"
        self.assertNotIn("1 problems", prompt)


class TestReportProblems(unittest.TestCase):
    """Tests for feedback.report_problems — using dry_run=True to avoid side effects."""

    def _make_report(self, n: int = 1) -> InstallReport:
        """Create an InstallReport with n problems."""
        report = InstallReport()
        for i in range(n):
            report.add_problem(
                step=str(i), title=f"Step {i}",
                result="fail", expected="E", actual=f"Error {i}"
            )
        return report

    def test_no_problems_returns_empty_result(self) -> None:
        """Empty report returns all-empty lists."""
        report = InstallReport()
        result = report_problems(report, dry_run=True)
        self.assertEqual(result["filed"], [])
        self.assertEqual(result["commented"], [])
        self.assertEqual(result["skipped"], [])
        self.assertEqual(result["errors"], [])

    def test_dry_run_does_not_call_subprocess(self) -> None:
        """dry_run=True does not actually call subprocess.run."""
        report = self._make_report(1)
        with patch("feedback.find_matching_issue", return_value=None):
            result = report_problems(report, dry_run=True)
        # In dry run, filed should contain the dry-run entry
        self.assertEqual(len(result["filed"]), 1)
        self.assertTrue(result["filed"][0].get("dry_run"))

    def test_dry_run_returns_filed_entries(self) -> None:
        """dry_run returns filed entry with title and body."""
        report = self._make_report(1)
        with patch("feedback.find_matching_issue", return_value=None):
            result = report_problems(report, dry_run=True)
        entry = result["filed"][0]
        self.assertIn("title", entry)
        self.assertIn("body", entry)

    def test_exceeds_limit_files_summary(self) -> None:
        """When problems exceed MAX_ISSUES_PER_INSTALL, a single summary is filed."""
        n = MAX_ISSUES_PER_INSTALL + 1
        report = self._make_report(n)
        result = report_problems(report, dry_run=True)
        # Should file exactly one summary issue
        self.assertEqual(len(result["filed"]), 1)
        self.assertIn("Multiple problems", result["filed"][0]["title"])

    def test_existing_issue_gets_comment(self) -> None:
        """If an existing issue is found, a 'me too' comment is added (dry_run)."""
        report = self._make_report(1)
        fake_issue = {"number": 42, "url": "https://github.com/x/y/issues/42"}
        with patch("feedback.find_matching_issue", return_value=fake_issue):
            result = report_problems(report, dry_run=True)
        self.assertEqual(len(result["commented"]), 1)
        self.assertEqual(len(result["filed"]), 0)

    def test_result_keys_present(self) -> None:
        """Return dict always has all four expected keys."""
        report = self._make_report(0)
        result = report_problems(report, dry_run=True)
        for key in ("filed", "commented", "skipped", "errors"):
            self.assertIn(key, result)


class TestModuleConstants(unittest.TestCase):
    """Verify module-level constants have expected values/types."""

    def test_default_repo_is_string(self) -> None:
        self.assertIsInstance(DEFAULT_REPO, str)

    def test_max_issues_is_positive_int(self) -> None:
        self.assertIsInstance(MAX_ISSUES_PER_INSTALL, int)
        self.assertGreater(MAX_ISSUES_PER_INSTALL, 0)


if __name__ == "__main__":
    unittest.main()
