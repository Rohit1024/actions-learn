from pathlib import Path

from inspect_lock import inspect

base = Path(__file__).parent
data, problems = inspect(base / "illustrative.lock.yml")
assert not problems
assert data["jobs"]["agent"]["needs"] == "prepare"
assert data["jobs"]["safe_outputs"]["needs"] == "agent"
_, problems = inspect(base / "fixtures/unsafe.lock.yml")
assert any("unpinned remote reference" in problem for problem in problems)
assert any("broad or write authority" in problem for problem in problems)
assert any("missing explicit job deadline" in problem for problem in problems)
print("PASS: schematic dependency chain inspected; unsafe authority, pin and deadline rejected")
