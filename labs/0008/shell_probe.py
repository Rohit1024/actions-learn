"""Observe argument transport, even when a static diagnostic is suppressed."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--bad", action="store_true")
args = parser.parse_args()
script = Path(__file__).resolve().parent / ("bad.sh" if args.bad else "good.sh")
env = os.environ.copy()
env["TITLE"] = "two words * $(printf injected)"
with tempfile.TemporaryDirectory(prefix="module2 shell ") as directory:
    Path(directory, "visible.txt").write_text("fixture\n")
    result = subprocess.run(["bash", str(script)], cwd=directory, env=env,
                            capture_output=True, text=True, timeout=10)
expected = "<" + env["TITLE"] + ">\n"
print("exit=" + str(result.returncode) + "; stdout=" + repr(result.stdout))
if result.returncode != 0 or result.stdout != expected:
    print("FAIL: expected one literal argument; quote the variable", file=sys.stderr)
    sys.exit(1)
print("PASS: spaces, glob, and shell-like text stayed in one data argument")
