"""Record bounded local samples; build and image modes require an existing engine."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("boundary", choices=["host", "build", "image"])
parser.add_argument("--samples", type=int, choices=range(1, 6), default=3)
args = parser.parse_args()
action = Path(__file__).parent / "action"
samples = []
for number in range(args.samples):
    with tempfile.TemporaryDirectory(prefix="lesson18-") as directory:
        output = Path(directory) / "output"
        output.touch()
        environment = os.environ.copy()
        if args.boundary == "build":
            command = ["docker", "build", "--tag", "actions-learn-0018:local", str(action)]
        elif args.boundary == "image":
            command = ["docker", "run", "--rm", "--network", "none", "--mount",
                       f"type=bind,source={directory},target=/measure", "--env", "GITHUB_OUTPUT=/measure/output",
                       "actions-learn-0018:local", "Ada"]
        else:
            environment["GITHUB_OUTPUT"] = str(output)
            command = [sys.executable, str(action / "entrypoint.py"), "Ada"]
        started = time.perf_counter()
        result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=120)
        seconds = time.perf_counter() - started
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)
        if args.boundary != "build":
            assert output.read_text() == "greeting=Hello, Ada!\n"
        samples.append({"sample": number + 1, "seconds": round(seconds, 6)})
print(json.dumps({"boundary": args.boundary, "cache_state": "not reset or controlled", "samples": samples}, indent=2))
