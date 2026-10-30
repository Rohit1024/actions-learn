"""Two explicit argv values; no shell interpretation or implicit INPUT lookup."""

import os
from pathlib import Path
import sys


def single_line(value: str, label: str) -> str:
    if not value.strip() or "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be a nonempty, single-line string")
    return value.strip()


def main() -> int:
    try:
        if len(sys.argv) > 3:
            raise ValueError("expected at most two arguments: name, salutation")
        name = single_line(sys.argv[1] if len(sys.argv) > 1 else "World", "name")
        salutation = single_line(sys.argv[2] if len(sys.argv) > 2 else "Hello", "salutation")
        greeting = f"{salutation}, {name}!"
        destination = os.environ.get("GITHUB_OUTPUT")
        if not destination:
            raise ValueError("GITHUB_OUTPUT must be set")
        with Path(destination).open("a", encoding="utf-8") as output:
            output.write(f"greeting={greeting}\n")
        print(greeting)
        return 0
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
