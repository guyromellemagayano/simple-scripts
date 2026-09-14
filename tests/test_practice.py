"""Regression tests for selection, grading, and failure reporting."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import practice


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "tooling").symlink_to(practice.ROOT / "tooling", target_is_directory=True)
        self.base = self.root / "challenges/ttl-store"
        self.base.mkdir(parents=True)
        self.fixture = self.base / "cases.json"
        self.write_cases([
            {"name": "example", "suite": "examples", "config": {}, "operations": [
                {"op": "get", "args": ["key"], "expect": "starter"}]},
            {"name": "assessment", "suite": "assessment", "config": {}, "operations": [
                {"op": "get", "args": ["key"], "expect": "assessment"}]},
        ])
        self.source = self.base / "python/starter/exercise.py"
        self.source.parent.mkdir(parents=True)
        self.source.write_text(
            "class TTLStore:\n"
            "    def __init__(self, clock): pass\n"
            "    def get(self, key): return 'starter'\n")
        reference = self.base / "python/solution/exercise.py"
        reference.parent.mkdir(parents=True)
        reference.write_text("raise AssertionError('Reference must not be loaded')\n")

    def tearDown(self):
        self.directory.cleanup()

    def write_cases(self, cases):
        self.fixture.write_text(json.dumps({"cases": cases}))

    def run_selected(self, suite="examples", structure=False):
        with mock.patch.object(practice, "ROOT", self.root):
            return practice.run_assessment("ttl-store", "python", "starter", suite,
                                           structure=structure, capture=True)

    def test_selected_starter_runs_without_loading_reference(self):
        result = self.run_selected()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_suite_includes_assessment_failures(self):
        self.assertEqual(self.run_selected("examples").returncode, 0)
        result = self.run_selected("full")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("assessment", result.stderr)

    def test_missing_starter_does_not_fall_back_to_existing_reference(self):
        self.source.unlink()
        with self.assertRaisesRegex(RuntimeError, "Selected implementation is missing"):
            self.run_selected()

    def test_boolean_cannot_pass_as_an_integer(self):
        self.source.write_text(
            "class TTLStore:\n"
            "    def __init__(self, clock): pass\n"
            "    def get(self, key): return True\n")
        self.write_cases([{"name": "strict types", "suite": "examples", "config": {},
                           "operations": [{"op": "get", "args": ["key"], "expect": 1}]}])
        self.assertNotEqual(self.run_selected().returncode, 0)

    def test_unimplemented_starter_reports_failure_but_loads(self):
        self.source.write_text(
            "class TTLStore:\n"
            "    def __init__(self, clock): raise NotImplementedError('Not implemented')\n"
            "    def get(self, key): raise NotImplementedError('Not implemented')\n")
        self.assertEqual(self.run_selected(structure=True).returncode, 0)
        result = self.run_selected()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Not implemented", result.stderr)

    def test_structure_requires_public_methods(self):
        self.source.write_text("class TTLStore: pass\n")
        result = self.run_selected(structure=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing public method", result.stderr)

    def test_empty_selection_is_an_error(self):
        self.write_cases([])
        result = self.run_selected()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No assessment cases selected", result.stderr)

    def test_cli_defaults_to_starter_and_full_assessment(self):
        captured = {}
        original_run = practice.run_assessment

        def capture_run(*args, **kwargs):
            result = original_run(*args, **kwargs, capture=True)
            captured["output"] = result.stderr
            return result

        with mock.patch.object(practice, "ROOT", self.root), \
                mock.patch.object(practice, "run_assessment", side_effect=capture_run), \
                contextlib.redirect_stdout(io.StringIO()):
            result = practice.main(["test", "ttl-store", "--language", "python"])
        self.assertEqual(result, 1)
        self.assertIn("assessment", captured["output"])
        self.assertNotIn("Reference must not be loaded", captured["output"])

    def test_missing_runtime_has_actionable_error(self):
        with mock.patch("practice.shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Required runtime 'node'.*PATH"):
                practice.require_runtime("node")

    @unittest.skipUnless(os.name == "posix", "Process groups are POSIX-specific")
    def test_timeout_stops_the_assessment_process_group(self):
        process = mock.Mock(pid=12345)
        process.communicate.side_effect = [
            subprocess.TimeoutExpired(["node"], 120), ("", ""),
        ]
        with mock.patch("practice.subprocess.Popen", return_value=process), \
                mock.patch("practice.os.killpg") as kill_group:
            with self.assertRaisesRegex(RuntimeError, "timed out after 120s"):
                practice.run_process(["node"], capture=True)
        kill_group.assert_called_once_with(process.pid, practice.signal.SIGKILL)
        self.assertEqual(process.communicate.call_count, 2)

    def test_list_works_from_another_directory_without_language_runtimes(self):
        env = os.environ.copy()
        env["PATH"] = ""
        result = subprocess.run([sys.executable, str(practice.ROOT / "practice.py"), "list"],
                                cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("06. notification-dispatcher", result.stdout)
        self.assertIn("javascript, typescript, go, php", result.stdout)

    def test_unknown_challenge_is_rejected_before_execution(self):
        result = subprocess.run([sys.executable, str(practice.ROOT / "practice.py"),
                                 "test", "../solution", "--language", "python"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
