"""Inspect an actual adapter output file, without parsing it as shell code."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--stdout-only", action="store_true", help="Demonstrate the broken channel")
parser.add_argument("--name", default="Ada")
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
with TemporaryDirectory(prefix="actions-0005-") as directory:
    output = Path(directory) / "output.txt"
    output.touch()
    command = (
        ["node", "-e", 'console.log("greeting=Hello, Ada!")']
        if args.stdout_only else ["node", str(root / "examples/javascript-action/index.cjs")]
    )
    result = subprocess.run(
        command, env={**os.environ, "INPUT_NAME": args.name, "GITHUB_OUTPUT": str(output)},
        capture_output=True, text=True,
    )
    raw = output.read_text()
    print(f"exit={result.returncode}; stdout={result.stdout!r}; output_file={raw!r}")
    if result.returncode:
        print(result.stderr, file=sys.stderr, end="")
        raise SystemExit(result.returncode)
    # This adapter promises a single-line value; this is not a general runner parser.
    lines = raw.splitlines()
    if len(lines) != 1 or not lines[0].startswith("greeting="):
        print("FAIL: missing single-line greeting output", file=sys.stderr)
        raise SystemExit(1)
    print("named greeting:", lines[0].partition("=")[2])
