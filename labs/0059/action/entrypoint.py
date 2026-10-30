"""Extend the greeting adapter into bounded, read-only workspace inspection."""

import os
from pathlib import Path
import re
import sys


def inspect(workspace: Path, relative: str, limit: str) -> tuple[int, int]:
    if not relative or Path(relative).is_absolute() or "\n" in relative or "\r" in relative:
        raise ValueError("file must be a nonempty relative path")
    if not re.fullmatch(r"[0-9]{1,7}", limit) or not 1 <= int(limit) <= 1048576:
        raise ValueError("max-bytes must be an integer from 1 through 1048576")
    root = workspace.resolve(strict=True)
    path = (root / relative).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("file must be a regular file inside GITHUB_WORKSPACE")
    with path.open("rb") as source:
        data = source.read(int(limit) + 1)
    if len(data) > int(limit):
        raise ValueError("file exceeds max-bytes")
    text = data.decode("utf-8")
    return len(data), len(text.splitlines())


def main() -> int:
    try:
        if len(sys.argv) != 3:
            raise ValueError("expected file and max-bytes arguments")
        workspace = os.environ.get("GITHUB_WORKSPACE")
        if not workspace:
            raise ValueError("GITHUB_WORKSPACE must be set")
        size, lines = inspect(Path(workspace), sys.argv[1], sys.argv[2])
        output_path = os.environ.get("GITHUB_OUTPUT")
        if not output_path:
            raise ValueError("GITHUB_OUTPUT must be set")
        with Path(output_path).open("a", encoding="utf-8") as output:
            output.write(f"bytes={size}\nlines={lines}\n")
        print(f"Inspected file: {size} bytes, {lines} lines")
        return 0
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
