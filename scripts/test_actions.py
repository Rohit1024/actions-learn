#!/usr/bin/env python3
"""Test actual action processes without a runner, network, or container daemon."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
    "javascript": ["node", "examples/javascript-action/index.cjs"],
    "typescript": ["node", "examples/typescript-action/dist/index.cjs"],
    "docker-program": [sys.executable, "examples/docker-action/entrypoint.py"],
    "composite-script": ["bash", "examples/composite-action/greet.sh"],
}


class ActionContractTests(unittest.TestCase):
    def run_adapter(self, adapter, name, *, output_available=True, existing=""):
        with tempfile.TemporaryDirectory(prefix="action contract ") as directory:
            output = Path(directory) / "output with spaces.txt"
            output.write_text(existing, encoding="utf-8")
            env = os.environ.copy()
            for key in ("INPUT_NAME", "GREETING_NAME", "GITHUB_OUTPUT"):
                env.pop(key, None)
            if output_available:
                env["GITHUB_OUTPUT"] = str(output)
            command = ADAPTERS[adapter].copy()
            if name is not None:
                if adapter == "docker-program":
                    command.append(name)
                else:
                    env["GREETING_NAME" if adapter == "composite-script" else "INPUT_NAME"] = name
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=20)
            return result, output.read_text(encoding="utf-8")

    def test_successful_inputs_publish_the_same_contract(self):
        cases = [(None, "World"), ("Ada", "Ada"), ("  Ada  ", "Ada"), ("रोहित", "रोहित"),
                 ("$(exit 99); `exit 88`", "$(exit 99); `exit 88`"), ("a=b", "a=b")]
        for adapter in ADAPTERS:
            for name, expected in cases:
                with self.subTest(adapter=adapter, name=name):
                    result, output = self.run_adapter(adapter, name)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(output, f"greeting=Hello, {expected}!\n")
                    self.assertEqual(result.stdout, f"Hello, {expected}!\n")

    def test_invalid_inputs_fail_without_publishing_success(self):
        for adapter in ADAPTERS:
            for name in ("", "   ", "Ada\nother=injected", "Ada\rother=injected"):
                with self.subTest(adapter=adapter, name=name):
                    result, output = self.run_adapter(adapter, name)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("nonempty, single-line", result.stderr)
                    self.assertEqual(output, "")

    def test_output_is_appended_without_destroying_prior_step_values(self):
        for adapter in ADAPTERS:
            with self.subTest(adapter=adapter):
                result, output = self.run_adapter(adapter, "Ada", existing="existing=value\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, "existing=value\ngreeting=Hello, Ada!\n")

    def test_missing_output_contract_fails(self):
        for adapter in ADAPTERS:
            with self.subTest(adapter=adapter):
                result, output = self.run_adapter(adapter, "Ada", output_available=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("GITHUB_OUTPUT", result.stderr)
                self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
