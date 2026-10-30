"""Build/run one probe image and check a mounted output path; no credentials."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--platform", choices=("linux/amd64", "linux/arm64"), default="linux/amd64")
args = parser.parse_args()
lab = Path(__file__).resolve().parent


def run(command):
    return subprocess.run(command, check=True, text=True, capture_output=True, timeout=120)


try:
    info = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=15)
    if info.returncode:
        print(info.stderr.strip(), file=sys.stderr)
        print("DEFERRED: engine unavailable; no image build or container run attempted", file=sys.stderr)
        sys.exit(2)
    image = "actions-learn-module2-probe:" + args.platform.split("/")[1]
    run(["docker", "build", "--platform", args.platform, "--tag", image, str(lab)])
    with tempfile.TemporaryDirectory(prefix="module2 mount with spaces ") as directory:
        output = Path(directory) / "runner output.txt"
        output.write_text("existing=value\n", encoding="utf-8")
        # The mount and filename are argv elements, never shell source.
        result = run([
            "docker", "run", "--rm", "--platform", args.platform,
            "--volume", directory + ":/runner", "--env", "GITHUB_OUTPUT=/runner/runner output.txt",
            image,
        ])
        print(result.stdout.strip())
        expected_machine = "x86_64" if args.platform == "linux/amd64" else "aarch64"
        expected = "existing=value\nplatform=Linux/" + expected_machine + "\n"
        actual = output.read_text(encoding="utf-8")
        if actual != expected:
            raise ValueError("unexpected mounted output: " + repr(actual))
        print("PASS: Linux process ran at selected architecture and appended to host-visible output")
except (OSError, ValueError, subprocess.SubprocessError) as error:
    print("FAIL: " + str(error), file=sys.stderr)
    if isinstance(error, subprocess.CalledProcessError):
        print((error.stdout or "") + (error.stderr or ""), file=sys.stderr)
    sys.exit(1)
