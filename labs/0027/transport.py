"""Fixed harmless payload only: marker writes stay inside a temporary directory."""
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

action = Path(__file__).resolve().parent / "action"
payload = '$(printf injected > marker.txt)'
with TemporaryDirectory(prefix="module5 literal ") as directory:
    cwd = Path(directory)
    marker = cwd / "marker.txt"
    # Intentionally generate shell source from this one fixed synthetic string.
    source = 'printf "%s\\n" "' + payload + '"'
    broken = subprocess.run(["bash", "-c", source], cwd=cwd, capture_output=True, text=True, timeout=5)
    assert broken.returncode == 0 and marker.read_text() == "injected"
    print("generated shell source: marker CREATED (expected unsafe demonstration)")
    marker.unlink()
    cases = [payload, 'Ada "quotes" $HOME `literal` * ; --flag %s रोहित', 'line one\nready=true', '-n']
    for index, label in enumerate(cases):
        output = cwd / f"output {index}"
        output.touch()
        env = dict(os.environ, ACTION_DIR=str(action), RAW_LABEL=label, GITHUB_OUTPUT=str(output))
        result = subprocess.run(["bash", str(action / "accept.sh")], cwd=cwd, env=env, capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, result.stderr
        record = output.read_text()
        assert len(record.splitlines()) == 1 and record.startswith("label-json=")
        assert json.loads(record.removeprefix("label-json=").rstrip("\n")) == label
        assert not marker.exists()
        assert result.stdout == "label accepted\n" and result.stderr == ""
    print("env + quoted argv: PASS (4 exact round trips; marker absent)")
    for label in ["", " ", "x" * 161]:
        output = cwd / "invalid output"
        output.write_text("prior=kept\n")
        env = dict(os.environ, ACTION_DIR=str(action), RAW_LABEL=label, GITHUB_OUTPUT=str(output))
        result = subprocess.run(["bash", str(action / "accept.sh")], cwd=cwd, env=env, capture_output=True, text=True, timeout=5)
        assert result.returncode == 1 and "label must be" in result.stderr
        assert output.read_text() == "prior=kept\n"
    print("invalid labels: PASS (3 rejected; prior output preserved)")
