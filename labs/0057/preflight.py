"""Check caller files, without simulating setup-node or its cache service."""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--workspace", type=Path, default=Path.cwd())
parser.add_argument("--lockfile", default="package-lock.json")
args = parser.parse_args()
workspace = args.workspace.resolve()
for relative in ("labs/0057/action/action.yml", args.lockfile):
    if not (workspace / relative).is_file():
        raise SystemExit(f"FAIL: caller workspace is missing {relative}")
    print(f"FOUND: {relative}")
print("PASS: caller files exist; setup-node and npm cache were not executed")
