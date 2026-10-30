"""Inspect minimal event fixtures; this does not evaluate GitHub filters."""

import argparse
import json
from pathlib import Path
import sys


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("event", choices=["push", "pull_request", "workflow_dispatch"])
parser.add_argument("fixture", type=Path)
args = parser.parse_args()
payload = json.loads(args.fixture.read_text())
try:
    if args.event == "pull_request":
        pr = payload["pull_request"]
        selected = {"base": pr["base"]["ref"], "head": pr["head"]["ref"]}
    elif args.event == "push":
        selected = {"ref": payload["ref"], "after": payload["after"]}
    else:
        selected = {"ref": payload["ref"], "run_checks": payload["inputs"]["run_checks"]}
except KeyError as error:
    print(f"Missing required field: {error.args[0]}", file=sys.stderr)
    raise SystemExit(1) from error
print(json.dumps({"event": args.event, **selected}, indent=2))
