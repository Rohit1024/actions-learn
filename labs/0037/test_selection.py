import copy
import json
import unittest
from selection import HERE, admit


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads((HERE / "upstream-evidence.json").read_text())
        self.decision = json.loads((HERE / "accepted.json").read_text())

    def test_record_is_admissible(self):
        self.assertTrue(admit(self.evidence, self.decision).startswith("ADMIT RECORD:"))

    def test_stars_do_not_repair_identity(self):
        evidence = copy.deepcopy(self.evidence)
        evidence["records"][0]["observation"]["stargazers_count"] = 99999999
        self.decision["listing_repository"] = "lookalike/checkout"
        with self.assertRaisesRegex(ValueError, "repository mismatch"):
            admit(evidence, self.decision)

    def test_mutable_tag_rejected(self):
        self.decision["sha"] = "v7"
        with self.assertRaisesRegex(ValueError, "40-character"):
            admit(self.evidence, self.decision)

    def test_badge_does_not_replace_review(self):
        self.decision["release_review"] = ""
        with self.assertRaisesRegex(ValueError, "release review"):
            admit(self.evidence, self.decision)

    def test_wrong_commit_rejected(self):
        self.decision["sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "upstream tag"):
            admit(self.evidence, self.decision)

    def test_community_requires_exception(self):
        self.decision["repository"] = self.decision["listing_repository"] = "dorny/paths-filter"
        r = next(r for r in self.evidence["records"] if r["repository"] == "dorny/paths-filter")
        self.decision["sha"] = r["resolved_sha"]
        with self.assertRaisesRegex(ValueError, "exception"):
            admit(self.evidence, self.decision)
        self.decision["community_exception"] = "Fixture decision: named filters fit; read-only job; review before activation."
        self.assertIn("ADMIT RECORD", admit(self.evidence, self.decision))


if __name__ == "__main__":
    unittest.main()
