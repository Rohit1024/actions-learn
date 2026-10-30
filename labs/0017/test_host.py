"""Actual host processes and signals; no Docker or GitHub cancellation claim."""
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parent


class WorkerTests(unittest.TestCase):
    def run_case(self, mode, *, signum=None, broken=False):
        with tempfile.TemporaryDirectory(prefix="lesson17-") as directory:
            workspace = Path(directory)
            output = workspace / "output"
            output.touch()
            # A failed attempt must not erase a prior completed artifact.
            result_file = workspace / "result.txt"
            result_file.write_text("prior completed report\n")
            script = ROOT / "swallow.py" if broken else ROOT / "action/worker.py"
            process = subprocess.Popen(
                [sys.executable, str(script), mode],
                env=dict(os.environ, GITHUB_WORKSPACE=str(workspace), GITHUB_OUTPUT=str(output)),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            try:
                if signum is not None:
                    self.assertTrue(select.select([process.stdout], [], [], 5)[0], "no READY message")
                    self.assertEqual(process.stdout.readline().strip(), "READY: staging file exists")
                    process.send_signal(signum)
                stdout, stderr = process.communicate(timeout=5)
                partial_exists = (workspace / ".lesson17.partial").exists()
                if signum == signal.SIGKILL:
                    self.assertEqual(process.returncode, -signal.SIGKILL)
                    self.assertTrue(partial_exists)
                elif signum is not None:
                    self.assertEqual(process.returncode, 128 + signum, stderr)
                    self.assertIn(signal.Signals(signum).name, stderr)
                    self.assertFalse(partial_exists)
                elif mode == "fail":
                    self.assertEqual(process.returncode, 0 if broken else 1)
                    self.assertIn("deliberate failure", stderr)
                    self.assertFalse(partial_exists)
                else:
                    self.assertEqual(process.returncode, 0, stderr)
                    self.assertEqual(stderr, "")
                    self.assertIn("DONE", stdout)
                    self.assertFalse(partial_exists)
                    self.assertEqual(output.read_text(), "result=result.txt\n")
                    self.assertEqual(result_file.read_text(), "completed local report\n")
                    return
                self.assertEqual(output.read_text(), "")
                self.assertEqual(result_file.read_text(), "prior completed report\n")
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate(timeout=5)

    def test_success(self):
        self.run_case("success")

    def test_failure(self):
        self.run_case("fail")

    def test_sigint(self):
        self.run_case("wait", signum=signal.SIGINT)

    def test_sigterm(self):
        self.run_case("wait", signum=signal.SIGTERM)

    def test_sigkill_leaves_staging(self):
        self.run_case("wait", signum=signal.SIGKILL)

    def test_broken_adapter_falsely_exits_zero(self):
        self.run_case("fail", broken=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
