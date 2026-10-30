"""Observe two shell processes sharing files, without emulating a runner."""

import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


with TemporaryDirectory(prefix="actions-0001-") as directory:
    environment = dict(os.environ)
    environment.pop("LESSON_NAME", None)
    subprocess.run(
        ["bash", "-eu", "-c", 'export LESSON_NAME=Ada; printf "%s\\n" "$LESSON_NAME" > name.txt'],
        cwd=directory, env=environment, check=True,
    )
    result = subprocess.run(
        ["bash", "-eu", "-c", 'printf "environment=%s\\n" "${LESSON_NAME:-unset}"; cat name.txt'],
        cwd=directory, env=environment, check=True, capture_output=True, text=True,
    )
    assert result.stdout == "environment=unset\nAda\n", result.stdout
    assert (Path(directory) / "name.txt").read_text() == "Ada\n"
    print(result.stdout, end="")
    print("PASS: the file survived; the exported variable did not cross processes")
