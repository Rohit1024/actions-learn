"""Real shell adapter tests; no Actions expression evaluation."""
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

SCRIPT = Path(__file__).parent / "action/report.sh"


class ReportContract(unittest.TestCase):
    def run_report(self, value, prior="", output=True):
        with TemporaryDirectory(prefix="module5 output ") as directory:
            path = Path(directory) / "output with spaces"
            path.write_text(prior)
            env = dict(os.environ)
            env.pop("REPORT_NAME", None)
            env.pop("GITHUB_OUTPUT", None)
            if value is not None:
                env["REPORT_NAME"] = value
            if output:
                env["GITHUB_OUTPUT"] = str(path)
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True, timeout=5)
            return result, path.read_text()

    def test_valid_names_and_append(self):
        for name in ["Ada", "Ada Lovelace", "रोहित", "$(exit 99)", "a=b"]:
            with self.subTest(name=name):
                result, data = self.run_report(name, "prior=kept\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(data, f"prior=kept\nsummary=Ready, {name}!\n")
                self.assertEqual(result.stdout, "report rendered\n")

    def test_invalid_does_not_publish(self):
        for name in [None, "", "  ", "Ada\nready=true", "Ada\rnext=x", "x" * 161]:
            with self.subTest(name=name):
                result, data = self.run_report(name, "prior=kept\n")
                self.assertEqual(result.returncode, 1)
                self.assertIn("name must be", result.stderr)
                self.assertEqual(data, "prior=kept\n")
                self.assertEqual(result.stdout, "")

    def test_missing_output(self):
        result, data = self.run_report("Ada", output=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("GITHUB_OUTPUT must be set", result.stderr)
        self.assertEqual(data, "")


if __name__ == "__main__":
    unittest.main()
