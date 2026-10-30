"""Copy code and data to different roots with spaces; use an unrelated cwd."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

source = Path(__file__).resolve().parent
with TemporaryDirectory(prefix="module5 paths ") as directory:
    root = Path(directory)
    action = root / "downloaded action"
    workspace = root / "caller workspace"
    cwd = root / "unrelated working directory"
    shutil.copytree(source / "action", action)
    workspace.mkdir()
    cwd.mkdir()
    fixture = workspace / "input with spaces.txt"
    shutil.copyfile(source / "fixtures/input with spaces.txt", fixture)
    output = root / "output file"
    output.touch()
    env = dict(os.environ, ACTION_DIR=str(action), GITHUB_OUTPUT=str(output))
    broken = subprocess.run(["bash", "inspect.sh", str(fixture)], cwd=cwd, env=env, capture_output=True, text=True, timeout=5)
    assert broken.returncode != 0 and output.read_text() == ""
    print("relative script: EXPECTED FAILURE (inspect.sh absent from cwd)")
    split = subprocess.run(["bash", "-c", 'bash $ACTION_DIR/inspect.sh "$1"', "path-probe", str(fixture)], cwd=cwd, env=env, capture_output=True, text=True, timeout=5)
    assert split.returncode != 0 and output.read_text() == ""
    print("unquoted action path: EXPECTED FAILURE (space splits script path)")
    fixed = subprocess.run(["bash", str(action / "inspect.sh"), str(fixture)], cwd=cwd, env=env, capture_output=True, text=True, timeout=5)
    assert fixed.returncode == 0, fixed.stderr
    assert json.loads(fixed.stdout) == {"argument": str(fixture), "lines": 2}
    assert output.read_text() == "lines=2\n"
    print("quoted action path + workspace file: PASS (one argument, lines=2)")
