"""Project policy for intended repository effects, with no API transport."""
import argparse
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = {
    "release-pr": {"contents": "write", "issues": "write", "pull-requests": "write"},
    "generated-pr": {"contents": "write", "pull-requests": "write"},
    "test-check": {"checks": "write", "contents": "read"},
}


def authorize(plan):
    operation = plan["operation"]
    if operation not in REQUIRED:
        raise ValueError("unknown operation")
    if plan.get("event") != "workflow_dispatch" or plan.get("ref") != "refs/heads/main":
        raise ValueError("write policy requires dispatch from main")
    if plan.get("approved") is not True:
        raise ValueError("intended write effect has not been acknowledged")
    if plan.get("producer") != "reviewed-main":
        raise ValueError("untrusted producer cannot supply privileged executable content")
    if plan.get("permissions") != REQUIRED[operation]:
        raise ValueError("permissions do not match the selected effect")
    return f"ALLOW PLAN: {operation}; no API operation performed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", choices=("release", "fork", "no-write", "untrusted", "excess"))
    parser.add_argument("--env", action="store_true")
    args = parser.parse_args()
    try:
        if args.env:
            plan = {"operation": "release-pr", "event": os.environ.get("EVENT_NAME"), "ref": os.environ.get("REF_NAME"), "approved": os.environ.get("ACKNOWLEDGE") == "true", "producer": "reviewed-main", "permissions": REQUIRED["release-pr"]}
        elif args.case:
            plan = json.loads((HERE / "effect-plans.json").read_text())[args.case]
        else:
            parser.error("choose a fixture case or --env")
        print(authorize(plan))
    except (ValueError, KeyError) as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
