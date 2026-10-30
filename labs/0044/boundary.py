"""A normalized capability exercise, not the gh-aw authorization implementation."""
import json
from pathlib import Path
import sys


def authorize(policy, request):
    if request["tool"] not in policy["tools"]:
        return "tool unavailable"
    if request["domain"] not in policy["domains"]:
        return "network destination denied"
    if request["permission"] not in policy["permissions"]:
        return "token permission denied"
    if request["credential"] not in policy["credential_roles"]:
        return "credential role unavailable"
    if request["operation"] != "read":
        return "direct mutation forbidden by this reporting design"
    return "allow"


def audit(policy):
    problems = []
    if set(policy["tools"]) != {"get_file_contents"}:
        problems.append("report requires only get_file_contents")
    if set(policy["domains"]) != {"api.github.com"}:
        problems.append("unexpected data-service destination")
    if set(policy["permissions"]) != {"contents:read"}:
        problems.append("unexpected repository authority")
    if set(policy["credential_roles"]) != {"repository-reader"}:
        problems.append("unexpected credential role")
    return problems


if __name__ == "__main__":
    policy = json.loads(Path(sys.argv[1]).read_text())
    problems = audit(policy)
    if problems:
        for problem in problems:
            print(f"REJECT: {problem}", file=sys.stderr)
        sys.exit(1)
    for request in policy["requests"]:
        actual = authorize(policy, request)
        if actual != request["expected"]:
            raise SystemExit(f"unexpected decision: {request['id']}: {actual}")
        print(f"{request['id']}: {actual}")
    print("PASS: declared capability decisions match; no service contacted")
