"""Deterministic cache invalidation and unsigned manifest experiments."""
import hashlib
import json


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(source, lock, tool):
    return json.dumps({"source": source, "lock": lock, "tool": tool},
                      sort_keys=True, separators=(",", ":")).encode() + b"\n"


def key(source, lock, tool, policy, os_name="linux", arch="x64"):
    inputs = [source, lock, tool, policy, os_name, arch]
    return "lab-v2-" + digest(json.dumps(inputs, separators=(",", ":")).encode())


def verify(data, manifest, observed, expected, now):
    if observed != expected:
        raise ValueError("producer context mismatch")
    if set(manifest) != {"sha256", "source", "expires_at"}:
        raise ValueError("invalid manifest schema")
    if manifest["source"] != expected["sha"]:
        raise ValueError("source revision mismatch")
    if type(manifest["expires_at"]) is not int or now >= manifest["expires_at"]:
        raise ValueError("artifact expired under lab policy")
    if manifest["sha256"] != digest(data):
        raise ValueError("content digest mismatch")
    return True


def demo():
    source, lock, tool = "report-v1", "deps-v1", "builder-v1"
    first = build(source, lock, tool)
    second = build(source, lock, tool)
    assert first == second
    print("clean rebuild: identical bytes")
    # Broken key omits the tool; its hit returns the old result after an update.
    broken_cache = {digest(lock.encode()): first}
    stale = broken_cache[digest(lock.encode())]
    assert stale != build(source, lock, "builder-v2")
    print("broken key: stale hit after builder changed")
    assert key(source, lock, tool, "policy-v1") != key(source, lock, "builder-v2", "policy-v1")
    print("fixed key: miss after builder changed; rebuild required")
    producer = {"repository": "example/lesson", "run_id": 340, "sha": "a" * 40}
    manifest = {"sha256": digest(first), "source": producer["sha"], "expires_at": 200}
    assert verify(first, manifest, producer, producer, 100)
    for label, data, observed, now in [
        ("tamper", first + b"changed", producer, 100),
        ("wrong producer", first, dict(producer, run_id=341), 100),
        ("retention", first, producer, 200),
    ]:
        try:
            verify(data, manifest, observed, producer, now)
        except ValueError as error:
            print(f"{label}: rejected ({error})")
        else:
            raise AssertionError("negative case accepted")
    # A checksum delivered by an attacker with the bytes is not authenticity.
    forged = dict(manifest, sha256=digest(b"attacker bytes"))
    assert verify(b"attacker bytes", forged, producer, producer, 100)
    print("unsigned manifest: matching checksum alone cannot authenticate a producer")


if __name__ == "__main__":
    demo()
