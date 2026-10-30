"""Offline action-admission policy, using recorded evidence and a review decision.

This program verifies record consistency. It does not audit an action's code or
assert that a human review took place merely because a fixture says so.
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def admit(evidence, decision):
    repo = decision["repository"]
    record = next((r for r in evidence["records"] if r["repository"] == repo), None)
    if record is None:
        raise ValueError("no evidence for exact owner/repository")
    if decision["listing_repository"] != repo:
        raise ValueError("Marketplace repository mismatch")
    sha = decision["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("use a full 40-character commit pin")
    if not record.get("pin_matches") or record.get("resolved_sha") != sha:
        raise ValueError("pin does not match observed upstream tag")
    if not record.get("metadata"):
        raise ValueError("exact-pin metadata unavailable")
    if record.get("observation", {}).get("archived") is not False:
        raise ValueError("maintenance status requires review")
    if not decision.get("task_fit") or not decision.get("release_review"):
        raise ValueError("task fit and release review must be explicit")
    if record.get("publisher", {}).get("status") != "verified creator observed":
        if not decision.get("community_exception"):
            raise ValueError("publisher unconfirmed/community: document an exception")
    return f"ADMIT RECORD: {repo}@{sha}; code audit and hosted execution remain separate"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decision", type=Path)
    args = parser.parse_args()
    try:
        evidence = json.loads((HERE / "upstream-evidence.json").read_text())
        print(admit(evidence, json.loads(args.decision.read_text())))
    except (ValueError, KeyError) as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
