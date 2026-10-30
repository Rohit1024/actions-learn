"""One observable behavior matrix; choose host process or an already-built image."""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("boundary", choices=["host", "image"])
parser.add_argument("--image", default="actions-learn-0016:local")
args = parser.parse_args()
entrypoint = Path(__file__).parent / "action/entrypoint.py"
if args.boundary == "host":
    spec = importlib.util.spec_from_file_location("greeting_action", entrypoint)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.greet(" Ada ") == "Hello, Ada!"
    try:
        module.greet("")
    except ValueError:
        pass
    else:
        raise AssertionError("pure function accepted empty input")

# label, argv, expected greeting (None = failure), output-path mode
cases = [
    ("default", [], "Hello, World!", "normal"),
    ("ordinary", ["Ada"], "Hello, Ada!", "normal"),
    ("trim", [" Ada "], "Hello, Ada!", "normal"),
    ("unicode", ["Zoë"], "Hello, Zoë!", "normal"),
    ("literal", ["$(exit 99)"], "Hello, $(exit 99)!", "normal"),
    ("empty", [""], None, "normal"),
    ("spaces", ["   "], None, "normal"),
    ("newline", ["Ada\nother=injected"], None, "normal"),
    ("carriage-return", ["Ada\rX"], None, "normal"),
    ("unset-output", ["Ada"], None, "unset"),
    ("missing-parent", ["Ada"], None, "missing"),
]
for label, values, greeting, path_mode in cases:
    with tempfile.TemporaryDirectory(prefix="lesson16 spaces ") as directory:
        output = Path(directory) / "output"
        output.write_text("prior=kept\n", encoding="utf-8")
        if args.boundary == "host":
            command = [sys.executable, str(entrypoint), *values]
            environment = dict(os.environ)
            environment.pop("GITHUB_OUTPUT", None)
            if path_mode != "unset":
                environment["GITHUB_OUTPUT"] = str(Path(directory) / "missing/output" if path_mode == "missing" else output)
        else:
            command = ["docker", "run", "--rm", "--network", "none", "--mount", f"type=bind,source={directory},target=/contract"]
            if path_mode != "unset":
                destination = "/contract/missing/output" if path_mode == "missing" else "/contract/output"
                command += ["--env", f"GITHUB_OUTPUT={destination}"]
            command += [args.image, *values]
            environment = os.environ.copy()
        result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=30)
        if greeting is not None:
            assert result.returncode == 0, (label, result.stderr)
            assert result.stderr == "", (label, result.stderr)
            assert result.stdout == greeting + "\n", (label, result.stdout)
            assert output.read_text() == f"prior=kept\ngreeting={greeting}\n", label
        else:
            assert result.returncode == 1, (label, result.returncode, result.stderr)
            assert result.stdout == "" and result.stderr, label
            assert output.read_text() == "prior=kept\n", label
            if path_mode == "normal":
                assert "nonempty, single-line" in result.stderr, label
            elif path_mode == "unset":
                assert "GITHUB_OUTPUT must be set" in result.stderr, label
        print(f"PASS {args.boundary}: {label}")
print(f"PASS: {len(cases)} process cases at the {args.boundary} boundary")
