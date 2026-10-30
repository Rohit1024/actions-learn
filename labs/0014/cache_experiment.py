"""Opt-in real builder experiment in a temporary copy, without editing shared files."""
from pathlib import Path
import shutil
import subprocess
import tempfile

subprocess.run(["docker", "info"], check=True, timeout=30)
source = Path(__file__).parent / "action"
with tempfile.TemporaryDirectory(prefix="lesson14-build-") as directory:
    context = Path(directory) / "action"
    shutil.copytree(source, context, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for label in ("first build", "program-only edit"):
        print(f"EXPERIMENT: {label}", flush=True)
        if label == "program-only edit":
            with (context / "entrypoint.py").open("a", encoding="utf-8") as program:
                program.write("\n# program-only cache experiment\n")
        subprocess.run(["docker", "build", "--tag", "actions-learn-0014:local", str(context)], check=True, timeout=120)
    output = Path(directory) / "output"
    output.touch()
    subprocess.run([
        "docker", "run", "--rm", "--network", "none", "--mount",
        f"type=bind,source={directory},target=/contract", "--env", "GITHUB_OUTPUT=/contract/output",
        "actions-learn-0014:local", "Ada",
    ], check=True, timeout=30)
    assert output.read_text() == "greeting=Hello, Ada!\n"
    print("PASS: edited image runs; inspect builder logs to determine actual cache reuse")
