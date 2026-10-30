"""Reproduce stale success and its repair entirely in temporary lab copies."""

from pathlib import Path
import shutil
import subprocess
import tempfile

LAB = Path(__file__).resolve().parent


def run(directory, task, expected=0):
    result = subprocess.run(
        ["task", "--dir", str(directory), "--taskfile", str(directory / "Taskfile.yml"), task],
        capture_output=True, text=True, timeout=20,
    )
    print("$ task " + task)
    print((result.stdout + result.stderr).strip())
    if (result.returncode == 0) != (expected == 0):
        raise AssertionError("unexpected task result: " + str(result.returncode))
    return result


with tempfile.TemporaryDirectory(prefix="module2 task contract ") as directory:
    root = Path(directory)
    for source in ("Taskfile.yml", "check.py", "input.json", "policy.json"):
        shutil.copy2(LAB / source, root / source)
    run(root, "check")
    run(root, "build:bad")
    run(root, "build:bad")
    (root / "policy.json").write_text('{"punctuation": "?"}\n')
    run(root, "build:bad")
    run(root, "verify-result", expected=1)
    run(root, "build:fixed")
    run(root, "verify-result")
    (root / "policy.json").write_text('{"punctuation": "!"}\n')
    run(root, "ordered")
    (root / "input.json").unlink()
    run(root, "check", expected=1)
print("PASS: stale cache detected, policy tracked, missing input explained")
