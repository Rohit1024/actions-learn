"""Real source mutations and a small evidence-claim exercise, with no engine."""
from pathlib import Path

from inventory import digest, split_source

source = Path(__file__).with_name("repo-report.md").read_text()
front, body, config = split_source(source)
changed_front, changed_body, _ = split_source(source.replace("Repository learning report", "Repository evidence report"))
assert digest(front) == digest(changed_front)
assert digest(body) != digest(changed_body)
print("body edit: lab frontmatter digest unchanged; body digest changed")

changed_front, _, changed_config = split_source(source.replace("max: 1", "max: 2"))
assert digest(front) != digest(changed_front)
assert changed_config["safe-outputs"]["create-issue"]["max"] == "2"
print("output-limit edit: lab frontmatter digest changed")

try:
    split_source(source.replace("---", "", 1))
except ValueError as error:
    assert str(error) == "missing opening frontmatter delimiter"
    print(f"expected rejection: {error}")
else:
    raise AssertionError("malformed source accepted")

# A tiny teaching ledger, not gh-aw's own evidence format or hash algorithm.
observed = {"source-inspection": {"configuration-read"}, "compile": {"specification-valid"}}
assert "tests-passed" not in observed["compile"]
assert "agent-read-files" not in observed["source-inspection"]
print("PASS: source edits distinguished; invented runtime claims rejected")
