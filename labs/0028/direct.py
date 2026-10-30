"""Identical adapters pass while only a runner can consume the public mapping."""
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parent
with TemporaryDirectory(prefix="module5 direct ") as directory:
    for name in ["action", "broken-action"]:
        output = Path(directory) / f"{name} output"
        output.touch()
        result = subprocess.run(["bash", str(root / name / "report.sh")], env=dict(os.environ, REPORT_NAME="Ada", GITHUB_OUTPUT=str(output)), capture_output=True, text=True, timeout=5)
        assert result.returncode == 0 and output.read_text() == "summary=Ready, Ada!\n", result.stderr
        print(f"{name}: PASS direct adapter; public mapping NOT executed")
