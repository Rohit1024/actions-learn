"""Inspect one lab source; this is not the gh-aw compiler or its schema."""
import hashlib
import json
from pathlib import Path
import sys

import yaml


def split_source(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("missing closing frontmatter delimiter")
    front, body = "".join(lines[1:end]), "".join(lines[end + 1:])
    # BaseLoader preserves 'on' as a string instead of YAML 1.1's boolean.
    config = yaml.load(front, Loader=yaml.BaseLoader)
    if not isinstance(config, dict) or not body.strip():
        raise ValueError("expected configuration mapping and nonempty instructions")
    return front, body, config


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def inventory(path):
    front, body, config = split_source(path.read_text())
    return {
        "trigger": list(config["on"]),
        "engine": config["engine"],
        "permissions": config["permissions"],
        "github_toolsets": config["tools"]["github"]["toolsets"],
        "github_allowed": config["tools"]["github"]["allowed"],
        "bash_commands": config["tools"]["bash"],
        "network": config["network"],
        "staged": config["safe-outputs"]["staged"],
        "issue_limit": config["safe-outputs"]["create-issue"]["max"],
        "agent_step_timeout_minutes": config["timeout-minutes"],
        "turn_limit": config["max-turns"],
        "lab_frontmatter_sha256": digest(front),
        "lab_body_sha256": digest(body),
        "claim": "source inspected; compile and runtime unverified",
    }


if __name__ == "__main__":
    try:
        target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("repo-report.md")
        print(json.dumps(inventory(target), indent=2))
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        sys.exit(1)
