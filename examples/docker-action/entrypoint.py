#!/usr/bin/env python3
"""Keep the action's program executable with either host Python or a container."""

import os
from pathlib import Path
import sys


def greet(name: str) -> str:
    if "\r" in name or "\n" in name or not name.strip():
        raise ValueError("name must be a nonempty, single-line string")
    return f"Hello, {name.strip()}!"


def main() -> int:
    try:
        greeting = greet(sys.argv[1] if len(sys.argv) > 1 else "World")
        output_path = os.environ.get("GITHUB_OUTPUT")
        if not output_path:
            raise ValueError("GITHUB_OUTPUT must be set")
        with Path(output_path).open("a", encoding="utf-8") as output:
            output.write(f"greeting={greeting}\n")
        print(greeting)
        return 0
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
