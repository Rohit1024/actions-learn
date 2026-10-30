"""Read literal step-output mappings and apply this lab's job-selection policy.

Fixtures supply action outputs; this is neither a path matcher nor an Actions
expression engine. Only the two documented mapping expressions are accepted.
"""
import argparse
import json
import re
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent


def route(recipe, fixture, bare=False):
    mappings = recipe["jobs"]["changes"]["outputs"]
    if fixture["event"] == "workflow_dispatch":
        return ["code", "docs"]
    if fixture["event"] != "pull_request":
        raise ValueError("unsupported fixture event")
    selected = []
    for name in ("code", "docs"):
        match = re.fullmatch(r"\$\{\{ steps\.filter\.outputs\.([a-z]+) \}\}", mappings[name])
        if not match:
            raise ValueError("unsupported mapping expression")
        value = fixture["step_outputs"].get(match[1])
        if value not in ("true", "false"):
            raise ValueError(f"missing or invalid output: {match[1]}")
        if (bool(value) if bare else value == "true"):
            selected.append(name)
    return selected


def load_recipe(path=HERE / "selective.yml"):
    return yaml.load(path.read_text(), Loader=yaml.BaseLoader)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("code", "docs", "mixed", "unrelated", "manual", "missing"))
    parser.add_argument("--bare", action="store_true", help="deliberately unsafe nonempty-string policy")
    parser.add_argument("--typo", action="store_true", help="mutate the mapping in memory to codes")
    args = parser.parse_args()
    recipe = load_recipe()
    if args.typo:
        recipe["jobs"]["changes"]["outputs"]["code"] = "${{ steps.filter.outputs.codes }}"
    fixture = json.loads((HERE / "cases.json").read_text())[args.case]
    try:
        print("selected=" + (",".join(route(recipe, fixture, args.bare)) or "none"))
    except ValueError as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
