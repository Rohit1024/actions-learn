"""Offline literal uses/with contract check against exact-pin metadata receipts.

Checks only the named files, literal remote pins and declared input keys. This
is not a workflow linter, expression interpreter, runtime test, or code audit.
"""
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ["labs/0038/selective.yml", "labs/0039/exchange.yml", "labs/0040/build.yml", "labs/0041/release.yml", "labs/0042/pipeline.yml"]


def inspect(path, evidence):
    document = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
    count = 0
    for job in document["jobs"].values():
        for step in job.get("steps", []):
            if "uses" not in step:
                continue
            match = re.fullmatch(r"([^@]+)@([0-9a-f]{40})", step["uses"])
            if not match:
                raise ValueError(f"{path.name}: expected full remote commit pin")
            repo, sha = match.groups()
            record = next((r for r in evidence["records"] if r["repository"] == repo and r.get("resolved_sha") == sha and r.get("pin_matches")), None)
            if not record or not record.get("metadata"):
                raise ValueError(f"{path.name}: no exact-pin metadata receipt for {repo}")
            inputs = record["metadata"]["inputs"]
            supplied = step.get("with", {})
            unknown = set(supplied) - set(inputs)
            if unknown:
                raise ValueError(f"{path.name}: {repo} unknown inputs: {', '.join(sorted(unknown))}")
            for key, properties in inputs.items():
                if properties.get("required") is True and "default" not in properties and key not in supplied:
                    raise ValueError(f"{path.name}: {repo} missing required input: {key}")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    evidence = json.loads((ROOT / "labs/0037/upstream-evidence.json").read_text())
    paths = args.files or [ROOT / path for path in POSITIVE]
    try:
        count = sum(inspect(path, evidence) for path in paths)
        print(f"PASS: {len(paths)} explicit recipes; {count} exact-pin action input contracts")
    except ValueError as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
