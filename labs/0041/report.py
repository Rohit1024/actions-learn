"""Consume a bounded synthetic JUnit file as data; no GitHub check is created."""
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent


def summarize(path):
    raw = path.read_bytes()
    if len(raw) > 16_384 or b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("report exceeds fixture policy")
    root = ET.fromstring(raw)
    if root.tag != "testsuite":
        raise ValueError("fixture requires a testsuite root")
    cases = root.findall("testcase")
    if not cases or len(cases) > 20:
        raise ValueError("fixture requires 1..20 test cases")
    failed = sum(c.find("failure") is not None or c.find("error") is not None for c in cases)
    skipped = sum(c.find("skipped") is not None for c in cases)
    return len(cases), failed, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        total, failed, skipped = summarize(args.path)
        print(f"REPORT DATA: total={total} failed={failed} skipped={skipped}; no check published")
        return 1 if failed else 0
    except (ValueError, ET.ParseError) as error:
        print(f"BLOCKED: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
