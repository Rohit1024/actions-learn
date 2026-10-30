"""Exercise dishonest coverage and budget declarations in temporary copies."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

lab = Path(__file__).resolve().parent
original = json.loads((lab / "plan.json").read_text())
with tempfile.TemporaryDirectory(prefix="module2 evidence ") as directory:
    root = Path(directory)
    for scenario in ("honest", "false-oidc", "stale-evidence", "over-budget"):
        plan = json.loads(json.dumps(original))
        if scenario == "false-oidc":
            plan["claims"][4]["evidence"].update(status="pass", revision=plan["revision"], reference="fake-local-token.json")
        elif scenario == "stale-evidence":
            plan["claims"][0]["evidence"].update(status="pass", revision="old-revision", reference="old-local.log")
        elif scenario == "over-budget":
            plan["budget"]["actual_hosted_runs"] = 2
        path = root / (scenario + ".json")
        path.write_text(json.dumps(plan))
        result = subprocess.run([sys.executable, str(lab / "coverage.py"), str(path)],
                                capture_output=True, text=True, timeout=10)
        if (result.returncode == 0) != (scenario == "honest"):
            raise AssertionError(scenario + ": " + result.stdout + result.stderr)
        print(scenario + ": " + ("PLAN CONSISTENT" if result.returncode == 0 else "BLOCKED as expected"))
        if result.returncode:
            print(result.stderr.strip())
print("PASS: false platform coverage, stale evidence, and budget overrun rejected")
