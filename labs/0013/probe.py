"""Execute argv transport directly; this does not evaluate action.yml."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--name", default="Ada")
parser.add_argument("--salutation", default="Hello")
parser.add_argument("--reverse", action="store_true")
args = parser.parse_args()
values = [args.name, args.salutation]
if args.reverse:
    values.reverse()
with tempfile.TemporaryDirectory(prefix="lesson13-") as directory:
    output = Path(directory) / "output"
    output.write_text("prior=kept\n", encoding="utf-8")
    environment = dict(os.environ, GITHUB_OUTPUT=str(output), INPUT_NAME="Ignored")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "action/entrypoint.py"), *values],
        env=environment, capture_output=True, text=True, timeout=5,
    )
    actual = output.read_text(encoding="utf-8")
    print(f"argv={values!r}; exit={result.returncode}")
    print(f"stdout={result.stdout!r}; stderr={result.stderr!r}")
    print(f"output={actual!r}")
    expected = f"prior=kept\ngreeting={args.salutation.strip()}, {args.name.strip()}!\n"
    if result.returncode or actual != expected:
        print("FAIL: expected successful execution with the documented name, salutation order")
        raise SystemExit(1)
    print("PASS: argv order, append protocol, and process status")
