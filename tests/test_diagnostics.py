#!/usr/bin/env python3
"""
Tests for diagnostics.py script.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import diagnostics


class TestDiagnostics(unittest.TestCase):
    """Test cases for diagnostics module."""

    def test_collect_diagnostics_returns_string(self):
        """Test that collect_diagnostics returns a string."""
        result = diagnostics.collect_diagnostics()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_diagnostics_contains_system_info(self):
        """Test that diagnostics contains system information."""
        result = diagnostics.collect_diagnostics()
        self.assertIn("SYSTEM DIAGNOSTICS", result)
        self.assertIn("SYSTEM INFORMATION:", result)
        self.assertIn("Platform:", result)
        self.assertIn("Python Version:", result)

    def test_diagnostics_contains_env_vars_section(self):
        """Test that diagnostics contains environment variables section."""
        result = diagnostics.collect_diagnostics()
        self.assertIn("ENVIRONMENT VARIABLES:", result)

    def test_sensitive_data_masking(self):
        """Test that sensitive environment variables are masked."""
        os.environ['E2E_TEST_TOKEN'] = 'secret123456'
        os.environ['E2E_API_KEY'] = 'apikey7890'
        os.environ['E2E_SAFE_VAR'] = 'visible_data'

        try:
            result = diagnostics.collect_diagnostics()

            self.assertIn('E2E_TEST_TOKEN', result)
            self.assertNotIn('secret123456', result)
            self.assertIn('*', result.split('E2E_TEST_TOKEN=')[1].split('\n')[0])

            self.assertIn('E2E_API_KEY', result)
            self.assertNotIn('apikey7890', result)

            self.assertIn('E2E_SAFE_VAR', result)
            self.assertIn('visible_data', result)
        finally:
            del os.environ['E2E_TEST_TOKEN']
            del os.environ['E2E_API_KEY']
            del os.environ['E2E_SAFE_VAR']

    def test_write_diagnostics_creates_file(self):
        """Test that write_diagnostics creates a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, 'test_diagnostics.txt')
            result = diagnostics.write_diagnostics(output_file)

            self.assertEqual(result, output_file)
            self.assertTrue(os.path.exists(output_file))

            with open(output_file, 'r') as f:
                content = f.read()

            self.assertGreater(len(content), 0)
            self.assertIn("SYSTEM DIAGNOSTICS", content)

    def test_relevant_env_vars_captured(self):
        """Test that relevant environment variables are captured."""
        os.environ['E2E_TEST_VAR'] = 'test_value'
        os.environ['GITHUB_ACTION'] = 'test_action'
        os.environ['IRRELEVANT_VAR'] = 'should_not_appear'

        try:
            result = diagnostics.collect_diagnostics()

            self.assertIn('E2E_TEST_VAR', result)
            self.assertIn('GITHUB_ACTION', result)
            self.assertNotIn('IRRELEVANT_VAR', result)
        finally:
            del os.environ['E2E_TEST_VAR']
            del os.environ['GITHUB_ACTION']
            del os.environ['IRRELEVANT_VAR']

    def test_empty_token_masking(self):
        """Test that empty sensitive variables are handled correctly."""
        os.environ['E2E_SECRET'] = ''

        try:
            result = diagnostics.collect_diagnostics()
            self.assertIn('E2E_SECRET', result)
            self.assertIn('(empty)', result)
        finally:
            del os.environ['E2E_SECRET']


if __name__ == '__main__':
    unittest.main()
