import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from diagnose import classify
from plan import audit

base = Path(__file__).parent
plan = json.loads((base / "plan.json").read_text())
ceiling, errors = audit(plan)
assert ceiling == 32 and not errors
assert len(audit(plan, require_ready=True)[1]) == 5
print("expected readiness rejection: five unresolved execution prerequisites")
for name, field, value in [("runner budget", "max_runner_minutes", 31), ("blind third rerun", "actual_runs", 3), ("model overrun", "actual_model_requests", 9), ("unplanned write", "actual_external_writes", 1)]:
    broken = copy.deepcopy(plan)
    broken["budget"][field] = value
    assert audit(broken)[1], name
    print(f"expected rejection: {name}")
events = json.loads((base / "events.json").read_text())
assert len({classify(event)[0] for event in events}) == 8
assert classify({"signal": "new_failure"})[0] == "unknown"
assert classify({"signal": "model_auth_denied"})[1].startswith("stop;")
with tempfile.TemporaryDirectory() as directory:
    declared_usage = copy.deepcopy(plan)
    declared_usage["budget"]["actual_runs"] = 1
    declared_usage["budget"]["actual_model_requests"] = 2
    path = Path(directory) / "synthetic-usage.json"
    path.write_text(json.dumps(declared_usage))
    result = subprocess.run([sys.executable, str(base / "plan.py"), str(path)], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result
    assert "hosted runs=1, model requests=2, writes=0 in this saved declaration" in result.stdout
    print("accepted: synthetic nonzero declarations retained; no actual requests made")
print("PASS: budget overruns blocked; eight boundaries plus unknown classified; hosted runs=0")
