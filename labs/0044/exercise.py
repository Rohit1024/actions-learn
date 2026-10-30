import copy
import json
from pathlib import Path

from boundary import audit, authorize

policy = json.loads(Path(__file__).with_name("policy.json").read_text())
assert not audit(policy)
for field, value, expected in [
    ("tool", "create_issue", "tool unavailable"),
    ("domain", "upload.invalid", "network destination denied"),
    ("permission", "contents:write", "token permission denied"),
    ("credential", "model-provider", "credential role unavailable"),
    ("operation", "write", "direct mutation forbidden by this reporting design"),
]:
    request = copy.deepcopy(policy["requests"][0])
    request[field] = value
    assert authorize(policy, request) == expected
    print(f"expected denial: {expected}")
broad = json.loads(Path(__file__).with_name("overbroad.json").read_text())
assert len(audit(broad)) == 4
print("PASS: five independent denials and four overbroad grants detected")
