"""Teaching policy for supplied job descriptions; never obtains a token."""
import argparse
import json
from pathlib import Path

OPERATIONS = {"test": {}, "checkout": {"contents": "read"},
              "comment": {"issues": "write"}, "release": {"contents": "write"}}
LEVEL = {"none": 0, "read": 1, "write": 2}


def assess(job):
    reasons = []
    permissions = job["permissions"]
    if job["operation"] not in OPERATIONS:
        return ["unknown operation"]
    if any(v not in LEVEL for v in permissions.values()):
        return ["unknown permission level"]
    trusted = (job["code_origin"] == "reviewed-base"
               and job["event"] in {"push", "workflow_dispatch", "pull_request_target"})
    if not trusted and (any(v == "write" for v in permissions.values())
                        or job["secret_names"]):
        reasons.append("untrusted code receives authority")
    required = OPERATIONS[job["operation"]]
    for scope, need in required.items():
        if LEVEL.get(permissions.get(scope, "none"), -1) < LEVEL[need]:
            reasons.append(f"missing {scope}:{need}")
    if any(LEVEL[value] > LEVEL.get(required.get(scope, "none"), 0)
           for scope, value in permissions.items()):
        reasons.append("permission exceeds operation contract")
    if job["secret_names"]:
        reasons.append("this operation needs no named secret")
    return reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["fork-read", "fork-write", "target-head", "trusted-comment", "missing-scope"])
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name("jobs.json").read_text())
    reasons = assess(cases[args.case])
    print(("DENY: " + "; ".join(reasons)) if reasons else "ALLOW: supplied job meets the teaching policy")
    print("SIMULATION: no GitHub token, settings, or API authorization observed")
    return bool(reasons)


if __name__ == "__main__":
    raise SystemExit(main())
