"""Review a local proposal envelope. Not the gh-aw safe-output wire schema.

There is deliberately no publisher, credential reader or HTTP client.
"""
import json
from pathlib import Path, PurePosixPath
import sys


def review(envelope):
    policy = envelope["policy"]
    errors = []
    if policy["staged"] is not True:
        errors.append("this lab requires staging")
    if policy["direct_write_tools"]:
        errors.append("direct write path bypasses handler staging")
    proposals = envelope["proposals"]
    if len(proposals) > policy["max_operations"]:
        errors.append("operation count exceeds policy")
    for item in proposals:
        if item.get("type") != "create_issue":
            errors.append("unsupported operation")
        title, body = item.get("title", ""), item.get("body", "")
        if not title.strip() or len(title) > 80 or "\n" in title or "\r" in title:
            errors.append("title must be one nonempty line, at most 80 characters")
        if not body.strip() or len(body.encode()) > policy["max_body_bytes"]:
            errors.append("body exceeds byte limit or is empty")
        citations = item.get("citations", [])
        if not citations:
            errors.append("missing citation")
        for citation in citations:
            path = PurePosixPath(citation)
            if path.is_absolute() or ".." in path.parts or citation not in policy["known_paths"]:
                errors.append("citation outside fixture inventory")
    return errors


if __name__ == "__main__":
    try:
        envelope = json.loads(Path(sys.argv[1]).read_text())
        errors = review(envelope)
        if errors:
            for error in errors:
                print(f"REJECT: {error}", file=sys.stderr)
            sys.exit(1)
        # Validate the entire batch before producing even a local preview.
        for item in envelope["proposals"]:
            print(f"STAGED PREVIEW: [learning] {item['title']}")
            print(item["body"])
        print(f"ACCEPT: {len(envelope['proposals'])} staged proposal(s); publications=0")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"REJECT: invalid lab envelope: {error}", file=sys.stderr)
        sys.exit(1)
