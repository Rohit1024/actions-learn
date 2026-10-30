"""Optional compile only. No dispatch, agent invocation, install, or root writes.

Exit 2 means a prerequisite or flag is unavailable. Compilation is performed in
an isolated temporary repository underneath this lab, then removed. Only an
explicit --emit copies actual compiler lock files into labs/0045/generated/.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent


def run(args, **kwargs):
    return subprocess.run(args, text=True, capture_output=True, timeout=120, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    options = parser.parse_args()
    if not shutil.which("gh"):
        print("UNVERIFIED: gh unavailable", file=sys.stderr)
        return 2
    help_result = run(["gh", "aw", "compile", "--help"])
    if help_result.returncode:
        print(help_result.stdout + help_result.stderr, file=sys.stderr, end="")
        print("UNVERIFIED: gh-aw compile help unavailable; compiler not invoked", file=sys.stderr)
        return 2
    flags = ["--strict", "--output" if options.emit else "--no-emit"]
    if any(flag not in help_result.stdout + help_result.stderr for flag in flags):
        print("UNVERIFIED: required flags absent from installed help", file=sys.stderr)
        return 2
    version = run(["gh", "aw", "version"])
    if version.returncode:
        print("UNVERIFIED: cannot record compiler version", file=sys.stderr)
        return 2
    print(version.stdout.strip())
    with tempfile.TemporaryDirectory(prefix="compile-", dir=BASE) as directory:
        scratch = Path(directory)
        # Prevent repository discovery from reaching the course's .github tree.
        initialized = run(["git", "init", "--quiet", str(scratch)])
        if initialized.returncode:
            print(initialized.stderr, file=sys.stderr)
            return 2
        source = scratch / ".github/workflows/repo-report.md"
        source.parent.mkdir(parents=True)
        shutil.copyfile(BASE.parent / "0043/repo-report.md", source)
        command = ["gh", "aw", "compile", str(source), "--strict"]
        command += ["--output", str(scratch / "out")] if options.emit else ["--no-emit"]
        result = run(command, cwd=scratch)
        print(result.stdout, end="")
        print(result.stderr, file=sys.stderr, end="")
        if result.returncode:
            print("UNVERIFIED: compile failed; retain the diagnostic category", file=sys.stderr)
            return 1
        if options.emit:
            locks = sorted((scratch / "out").rglob("*.lock.yml"))
            if not locks:
                print("UNVERIFIED: compiler emitted no lock in requested directory", file=sys.stderr)
                return 1
            destination = BASE / "generated"
            destination.mkdir(exist_ok=True)
            for lock in locks:
                relative = lock.relative_to(scratch / "out")
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(lock, target)
                print(f"actual compiler output: {target.relative_to(BASE.parent.parent)}")
            (destination / "compiler-version.txt").write_text(version.stdout + version.stderr)
        print("PASS: compilation only; no engine or workflow dispatched")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired:
        print("UNVERIFIED: local command exceeded 120 seconds", file=sys.stderr)
        sys.exit(2)
