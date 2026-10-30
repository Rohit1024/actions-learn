import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

base = Path(__file__).parent
good = json.loads((base / "valid.json").read_text())
cases = []


def case(name, mutate):
    candidate = copy.deepcopy(good)
    mutate(candidate)
    cases.append((name, candidate))


case("count", lambda x: x["proposals"].append(copy.deepcopy(x["proposals"][0])))
case("unsupported", lambda x: x["proposals"][0].update(type="merge_pull_request"))
case("oversized UTF-8", lambda x: x["proposals"][0].update(body="é" * 513))
case("path traversal", lambda x: x["proposals"][0].update(citations=["../outside.md"]))
case("direct write bypass", lambda x: x["policy"].update(direct_write_tools=["shell-api-write"]))
case("staging disabled", lambda x: x["policy"].update(staged=False))
with tempfile.TemporaryDirectory() as directory:
    for name, candidate in cases:
        path = Path(directory) / "proposal.json"
        path.write_text(json.dumps(candidate))
        result = subprocess.run([sys.executable, str(base / "review.py"), str(path)], capture_output=True, text=True, timeout=10)
        assert result.returncode == 1, (name, result)
        assert result.stdout == "", (name, "partial preview escaped")
        print(f"expected rejection: {name}; no partial preview")
print("PASS: six output-policy failures rejected; publications=0")
