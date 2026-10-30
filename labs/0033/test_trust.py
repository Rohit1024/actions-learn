import json
from pathlib import Path
import unittest
from trust import POLICY, decide

CLAIMS = json.loads(Path(__file__).with_name("claims.json").read_text())


class TrustTests(unittest.TestCase):
    def test_matching_selection(self):
        self.assertEqual(decide(CLAIMS, True), [])

    def test_every_identity_condition(self):
        for key in POLICY:
            with self.subTest(key=key):
                self.assertIn(f"claim {key} mismatch", decide(dict(CLAIMS, **{key: "wrong"}), True))

    def test_missing_claim(self):
        claims = dict(CLAIMS)
        del claims["repository_id"]
        self.assertTrue(decide(claims, True))

    def test_approval_separate(self):
        self.assertEqual(decide(CLAIMS, False), ["approval not observed in simulation"])

    def test_validity_boundaries(self):
        self.assertEqual(decide(CLAIMS, True, 1000), [])
        for now in [999, 1300]:
            with self.subTest(now=now):
                self.assertIn("outside validity window", decide(CLAIMS, True, now))

    def test_same_environment_wrong_branch(self):
        self.assertIn("claim ref mismatch", decide(dict(CLAIMS, ref="refs/heads/topic"), True))

    def test_legacy_subject_requires_explicit_policy_migration(self):
        self.assertIn("claim sub mismatch", decide(dict(CLAIMS, sub="repo:example/lesson:environment:staging"), True))


if __name__ == "__main__":
    unittest.main()
