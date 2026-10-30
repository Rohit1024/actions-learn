"""Run the real JavaScript action adapter against a temporary output file."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--name", default="Ada")
parser.add_argument("--expect", default="Hello, Ada!")
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
with TemporaryDirectory(prefix="actions-0002-") as directory:
    output = Path(directory) / "output.txt"
    output.touch()
    result = subprocess.run(
        ["node", str(root / "examples/javascript-action/index.cjs")],
        env={**os.environ, "INPUT_NAME": args.name, "GITHUB_OUTPUT": str(output)},
        capture_output=True, text=True,
    )
    actual = output.read_text()
    expected = f"greeting={args.expect}\n"
    print(f"exit={result.returncode}; output={actual!r}")
    if result.returncode != 0 or actual != expected:
        print(f"FAIL: expected exit=0 and output={expected!r}", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        raise SystemExit(1)
    print("PASS: real adapter wrote the expected named output")
