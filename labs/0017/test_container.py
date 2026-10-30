"""Opt-in stop/kill checks of an already-built image; always remove our containers."""
from pathlib import Path
import subprocess
import tempfile
import time
import uuid


def docker(*arguments):
    return subprocess.run(["docker", *arguments], capture_output=True, text=True, timeout=30, check=True)


docker("info")
for kind in ("TERM", "KILL"):
    name = f"lesson17-{uuid.uuid4().hex[:12]}"
    with tempfile.TemporaryDirectory(prefix="lesson17-container-") as directory:
        workspace = Path(directory)
        output = workspace / "output"
        output.touch()
        try:
            docker("run", "-d", "--name", name, "--network", "none", "--mount",
                   f"type=bind,source={workspace},target=/work", "--env", "GITHUB_WORKSPACE=/work",
                   "--env", "GITHUB_OUTPUT=/work/output", "actions-learn-0017:local", "wait")
            deadline = time.monotonic() + 10
            while not (workspace / ".lesson17.partial").exists():
                if time.monotonic() >= deadline:
                    raise AssertionError("no staging file: inspect image startup and mount mapping")
                time.sleep(0.05)
            # READY follows handler installation and staging; allow no assumed startup delay.
            if kind == "TERM":
                docker("stop", "--time", "2", name)
            else:
                docker("kill", "--signal", "KILL", name)
            docker("wait", name)
            status = int(docker("inspect", "--format", "{{.State.ExitCode}}", name).stdout.strip())
            assert status == (143 if kind == "TERM" else 137), status
            assert output.read_text() == "" and not (workspace / "result.txt").exists()
            assert (workspace / ".lesson17.partial").exists() == (kind == "KILL")
            print(f"PASS container {kind}: exit={status}; no success output; staging policy observed")
        finally:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True, text=True, timeout=30)
