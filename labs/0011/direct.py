"""The two scripts pass the same direct test despite different metadata."""

import os
from pathlib import Path
import subprocess
import tempfile

lab = Path(__file__).resolve().parent
for variant in ("action", "broken-action"):
    with tempfile.TemporaryDirectory(prefix="module2 direct output ") as directory:
        output = Path(directory) / "output with spaces.txt"
        output.write_text("", encoding="utf-8")
        env = os.environ.copy()
        env.update(GREETING_NAME="Ada", GITHUB_OUTPUT=str(output))
        result = subprocess.run(["bash", str(lab / variant / "greet.sh")],
                                env=env, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or output.read_text() != "greeting=Hello, Ada!\n":
            raise AssertionError(variant + ": " + result.stderr)
        print(variant + ": PASS script output; metadata was not executed")
