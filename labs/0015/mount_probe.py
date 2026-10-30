"""Host path checks or opt-in actual image/mount checks; temporary files only."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--container", action="store_true")
parser.add_argument("--mode", choices=["correct", "private", "read-only", "missing"], default="correct")
args = parser.parse_args()
if not args.container and args.mode in ("private", "read-only"):
    parser.error("private and read-only need --container to observe that boundary")
with tempfile.TemporaryDirectory(prefix="lesson15 spaces ") as directory:
    root = Path(directory)
    workspace, commands = root / "workspace", root / "commands"
    workspace.mkdir()
    commands.mkdir()
    (workspace / "name.txt").write_text("Ada\n", encoding="utf-8")
    output = commands / "output"
    output.touch()
    if args.container:
        destination = "/tmp/private-output" if args.mode == "private" else "/commands/output"
        if args.mode == "missing":
            destination = "/commands/missing/output"
        access = ",readonly" if args.mode == "read-only" else ""
        command = [
            "docker", "run", "--rm", "--network", "none",
            "--mount", f"type=bind,source={workspace},target=/work",
            "--mount", f"type=bind,source={commands},target=/commands{access}",
            "--workdir", "/work", "--env", "GITHUB_WORKSPACE=/work",
            "--env", f"GITHUB_OUTPUT={destination}", "actions-learn-0015:local",
        ]
        environment = os.environ.copy()
    else:
        destination = str(commands / "missing/output") if args.mode == "missing" else str(output)
        command = [sys.executable, str(Path(__file__).parent / "action/entrypoint.py")]
        environment = dict(os.environ, GITHUB_WORKSPACE=str(workspace), GITHUB_OUTPUT=destination)
    result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=30)
    print(f"mode={args.mode}; exit={result.returncode}")
    print(f"stdout={result.stdout!r}; stderr={result.stderr!r}")
    print(f"host output={output.read_text()!r}")
    report = workspace / "report.txt"
    assert report.exists(), "program never reached the workspace; inspect startup/mount errors"
    assert report.read_text() == "Hello, Ada!\n"
    print(f"host report owner uid={report.stat().st_uid}; content={report.read_text()!r}")
    if args.mode == "correct":
        assert result.returncode == 0, result.stderr
        assert output.read_text() == "greeting=Hello, Ada!\nreport=report.txt\n"
    elif args.mode == "private":
        assert result.returncode == 0, result.stderr
        assert output.read_text() == "", "private output should not reach the host mount"
    else:
        assert result.returncode == 1, result.stderr
        assert result.stderr and output.read_text() == ""
    print("PASS: observed the selected path boundary (including intended failure)")
