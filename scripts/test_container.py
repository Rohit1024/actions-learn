#!/usr/bin/env python3
"""Exercise the built Linux image's entrypoint and mounted output file."""

from pathlib import Path
import subprocess
import tempfile
import unittest


class ContainerContractTests(unittest.TestCase):
    def test_image_input_and_output_contract(self):
        for name, succeeds in [("Ada", True), ("$(exit 99)", True), ("", False), ("Ada\nother=x", False)]:
            with self.subTest(name=name), tempfile.TemporaryDirectory(prefix="container-contract-") as directory:
                output = Path(directory) / "output"
                output.touch()
                result = subprocess.run([
                    "docker", "run", "--rm", "--mount", f"type=bind,source={directory},target=/github-test",
                    "--env", "GITHUB_OUTPUT=/github-test/output", "actions-learn-greet:local", name,
                ], capture_output=True, text=True, timeout=120)
                if succeeds:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(output.read_text(), f"greeting=Hello, {name}!\n")
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("nonempty, single-line", result.stderr)
                    self.assertEqual(output.read_text(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
