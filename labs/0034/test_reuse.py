import unittest
from reuse import build, digest, key, verify


class ReuseTests(unittest.TestCase):
    def test_every_input_invalidates_key(self):
        values = ["source", "lock", "tool", "policy", "linux", "x64"]
        for index in range(len(values)):
            changed = values.copy()
            changed[index] += "-changed"
            with self.subTest(index=index):
                self.assertNotEqual(key(*values), key(*changed))

    def test_clean_rebuild(self):
        self.assertEqual(build("s", "l", "t"), build("s", "l", "t"))

    def test_distinct_inputs_change_bytes(self):
        self.assertNotEqual(build("s", "l", "t"), build("s", "l", "t2"))

    def test_manifest_rejects_tamper_producer_revision_expiry(self):
        data = b"report"
        producer = {"sha": "a" * 40, "run_id": 340}
        manifest = {"sha256": digest(data), "source": producer["sha"], "expires_at": 200}
        self.assertTrue(verify(data, manifest, producer, producer, 100))
        cases = [(data + b"x", manifest, producer, 100),
                 (data, manifest, dict(producer, run_id=341), 100),
                 (data, dict(manifest, source="b" * 40), producer, 100),
                 (data, manifest, producer, 200)]
        for content, record, observed, now in cases:
            with self.subTest(record=record, now=now), self.assertRaises(ValueError):
                verify(content, record, observed, producer, now)


if __name__ == "__main__":
    unittest.main()
