"""Bridge a minimal dispatch fixture to the adapter; not a trigger emulator."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("fixture", type=Path)
args = parser.parse_args()
try:
    payload = json.loads(args.fixture.read_text(encoding="utf-8"))
    inputs = payload["inputs"]
    if not isinstance(inputs, dict):
        raise ValueError("dispatch inputs must be an object")
    name = inputs.get("name")
    if name is not None and not isinstance(name, str):
        raise ValueError("name must be text when supplied")
    env = os.environ.copy()
    env.pop("INPUT_NAME", None)
    if name is not None:
        env["INPUT_NAME"] = name
    with tempfile.TemporaryDirectory(prefix="module2 event output ") as directory:
        output = Path(directory) / "output.txt"
        output.write_text("", encoding="utf-8")
        env["GITHUB_OUTPUT"] = str(output)
        env["GITHUB_EVENT_NAME"] = "workflow_dispatch"
        env["GITHUB_EVENT_PATH"] = str(args.fixture.resolve())
        result = subprocess.run(["node", str(Path(__file__).with_name("index.cjs"))], env=env,
                                capture_output=True, text=True, timeout=10)
        print("fixture inputs.name=" + repr(name))
        print("exit=" + str(result.returncode) + "; stdout=" + repr(result.stdout)
              + "; output=" + repr(output.read_text(encoding="utf-8")))
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)
except (OSError, ValueError, KeyError, TypeError) as error:
    print("FAIL: malformed dispatch fixture: " + str(error), file=sys.stderr)
    sys.exit(1)
