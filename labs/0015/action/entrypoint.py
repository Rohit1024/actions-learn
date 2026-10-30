"""Treat workspace and command-file paths as two independent contracts."""
import os
from pathlib import Path
import sys


def main() -> int:
    try:
        workspace_value = os.environ.get("GITHUB_WORKSPACE")
        output_value = os.environ.get("GITHUB_OUTPUT")
        if not workspace_value or not output_value:
            raise ValueError("GITHUB_WORKSPACE and GITHUB_OUTPUT must be set")
        workspace = Path(workspace_value)
        name = (workspace / "name.txt").read_text(encoding="utf-8").strip()
        if not name or "\n" in name or "\r" in name:
            raise ValueError("name.txt must contain one nonempty name")
        greeting = f"Hello, {name}!"
        (workspace / "report.txt").write_text(greeting + "\n", encoding="utf-8")
        with Path(output_value).open("a", encoding="utf-8") as output:
            output.write(f"greeting={greeting}\nreport=report.txt\n")
        print(f"uid={os.geteuid()}; workspace={workspace}; report=report.txt")
        return 0
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
