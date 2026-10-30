"""Only check the copied program; image construction is a separate check."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

with tempfile.TemporaryDirectory(prefix="lesson14-") as directory:
    output = Path(directory) / "output"
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "action/entrypoint.py"), "Ada"],
        env=dict(os.environ, GITHUB_OUTPUT=str(output)),
        capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 0, result.stderr
    assert output.read_text() == "greeting=Hello, Ada!\n"
    print("PASS: copied program; no image or build-cache claim")
