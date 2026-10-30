"""Tiny command shared by the human and CI; no GitHub or container dependency."""

import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        name = json.loads(Path("input.json").read_text())["name"]
        punctuation = json.loads(Path("policy.json").read_text())["punctuation"]
        if not isinstance(name, str) or not name.strip() or "\n" in name or "\r" in name:
            raise ValueError("name must be a nonempty single line")
        if punctuation not in ("!", "?"):
            raise ValueError("punctuation must be ! or ?")
        expected = {"greeting": "Hello, " + name.strip() + punctuation}
        if args.write:
            Path("result.json").write_text(json.dumps(expected) + "\n")
            print("BUILT: " + expected["greeting"])
        elif args.verify:
            actual = json.loads(Path("result.json").read_text())
            if actual != expected:
                raise ValueError("stale result: actual=" + repr(actual) + "; expected=" + repr(expected))
            print("PASS: generated result matches current input and policy")
        else:
            print("PASS: " + expected["greeting"])
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
