"""Run the real entrypoint contract on host Python or a separately built image."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

parser = argparse.ArgumentParser()
parser.add_argument("--container", metavar="IMAGE", help="Use an existing built image, not host Python")
parser.add_argument("--wrong-output", action="store_true", help="Mutate a temporary entrypoint to reproduce a guessed path")
args = parser.parse_args()
if args.container and args.wrong_output:
    parser.error("--wrong-output is a host-only deliberate mutation")
here = Path(__file__).resolve().parent
cases = [
    ("valid spaced path", "fixtures/release notes.txt", "1024", "valid", 0, "bytes=11\nlines=2\n", ""),
    ("exact byte limit", "fixtures/release notes.txt", "11", "valid", 0, "bytes=11\nlines=2\n", ""),
    ("oversize", "fixtures/release notes.txt", "10", "valid", 1, "", "exceeds max-bytes"),
    ("empty input", "", "1024", "valid", 1, "", "nonempty relative path"),
    ("escaping path", "../outside.txt", "1024", "valid", 1, "", ""),
    ("bad limit", "fixtures/release notes.txt", "zero", "valid", 1, "", "max-bytes"),
    ("missing file", "missing.txt", "1024", "valid", 1, "", ""),
    ("missing output", "fixtures/release notes.txt", "1024", "missing", 1, "", "GITHUB_OUTPUT"),
    ("output is directory", "fixtures/release notes.txt", "1024", "directory", 1, "", ""),
    ("invalid UTF-8", "binary.dat", "1024", "valid", 1, "", ""),
    ("escaping symlink", "escape.txt", "1024", "valid", 1, "", ""),
]
with TemporaryDirectory(prefix="docker action contract ") as directory:
    scratch = Path(directory)
    workspace = scratch / "workspace"
    workspace.mkdir()
    shutil.copytree(here / "fixtures", workspace / "fixtures")
    (scratch / "outside.txt").write_text("outside\n", encoding="utf-8")
    (workspace / "binary.dat").write_bytes(b"\xff")
    (workspace / "escape.txt").symlink_to("../outside.txt")
    io = scratch / "runner io"
    io.mkdir()
    output = io / "step output.txt"
    entrypoint = here / "action/entrypoint.py"
    if args.wrong_output:
        mutated = scratch / "wrong-entrypoint.py"
        mutated.write_text(entrypoint.read_text(encoding="utf-8").replace(
            'os.environ.get("GITHUB_OUTPUT")',
            'str(Path(os.environ["GITHUB_WORKSPACE"]) / "guessed-output.txt")'), encoding="utf-8")
        entrypoint = mutated
    for label, relative, limit, output_mode, status, records, diagnostic in cases:
        output.write_text("existing=value\n", encoding="utf-8")
        env = os.environ.copy()
        for key in ("GITHUB_WORKSPACE", "GITHUB_OUTPUT"):
            env.pop(key, None)
        if args.container:
            command = ["docker", "run", "--rm", "--network", "none",
                       "--mount", f"type=bind,source={workspace},target=/github/workspace,readonly",
                       "--mount", f"type=bind,source={io},target=/runner-io",
                       "--workdir", "/github/workspace", "-e", "GITHUB_WORKSPACE=/github/workspace"]
            if output_mode != "missing":
                target = "/runner-io" if output_mode == "directory" else "/runner-io/step output.txt"
                command += ["-e", f"GITHUB_OUTPUT={target}"]
            command += [args.container, relative, limit]
        else:
            env["GITHUB_WORKSPACE"] = str(workspace)
            if output_mode != "missing":
                env["GITHUB_OUTPUT"] = str(io if output_mode == "directory" else output)
            command = [sys.executable, str(entrypoint), relative, limit]
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=30)
        actual = output.read_text(encoding="utf-8")
        if (result.returncode != status or actual != "existing=value\n" + records
                or (status == 1 and (not result.stderr or result.stdout))
                or diagnostic not in result.stderr):
            print(f"FAIL: {label}; exit={result.returncode}; runner output={actual!r}", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            raise SystemExit(1)
        print(f"PASS: {label}")
print(f"PASS: {len(cases)} {'container' if args.container else 'host process'} cases; no GitHub runner used")
