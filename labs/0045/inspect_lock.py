"""Conservative reporting-lab review rules; not a full Actions security audit."""
from pathlib import Path
import re
import sys

import yaml


def inspect(path):
    data = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
    problems = []
    if "workflow_dispatch" not in data.get("on", {}) or len(data.get("on", {})) != 1:
        problems.append("expected manual dispatch only")
    scopes = [("workflow", data.get("permissions"))]
    for name, job in data.get("jobs", {}).items():
        scopes.append((name, job.get("permissions", data.get("permissions"))))
        if not job.get("timeout-minutes"):
            problems.append(f"{name}: missing explicit job deadline")
        for step in job.get("steps", []):
            ref = step.get("uses", "")
            if ref and not ref.startswith("./") and not re.fullmatch(r"[^@]+@[0-9a-fA-F]{40}", ref):
                problems.append(f"{name}: unpinned remote reference {ref}")
    for name, permission in scopes:
        if not isinstance(permission, dict) or any(value != "read" for value in permission.values()):
            problems.append(f"{name}: broad or write authority")
    return data, problems


if __name__ == "__main__":
    path = Path(sys.argv[1])
    try:
        data, problems = inspect(path)
        if problems:
            for problem in problems:
                print(f"REJECT: {problem}", file=sys.stderr)
            sys.exit(1)
        print("jobs=" + ",".join(data["jobs"]))
        print("PASS: reporting-lab static rules; inspect scripts, dependencies and runtime separately")
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as error:
        print(f"REJECT: cannot inspect workflow: {error}", file=sys.stderr)
        sys.exit(1)
