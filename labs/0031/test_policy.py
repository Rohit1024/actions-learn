import copy
import json
from pathlib import Path
import unittest
from policy import assess

CASES = json.loads(Path(__file__).with_name("jobs.json").read_text())


class PolicyTests(unittest.TestCase):
    def test_fork_read(self):
        self.assertEqual(assess(CASES["fork-read"]), [])

    def test_fork_write(self):
        self.assertIn("untrusted code receives authority", assess(CASES["fork-write"]))

    def test_target_does_not_trust_head(self):
        self.assertTrue(assess(CASES["target-head"]))

    def test_trusted_comment(self):
        self.assertEqual(assess(CASES["trusted-comment"]), [])

    def test_missing_scope(self):
        self.assertIn("missing issues:write", assess(CASES["missing-scope"]))

    def test_extra_authority(self):
        job = copy.deepcopy(CASES["trusted-comment"])
        job["permissions"]["contents"] = "write"
        self.assertIn("permission exceeds operation contract", assess(job))

    def test_no_secret_transport(self):
        job = copy.deepcopy(CASES["fork-read"])
        job["secret_names"] = ["SYNTHETIC_NOT_A_CREDENTIAL"]
        self.assertIn("untrusted code receives authority", assess(job))

    def test_identity_permission_is_authority(self):
        job = copy.deepcopy(CASES["fork-read"])
        job["permissions"]["id-token"] = "write"
        self.assertTrue(assess(job))

    def test_unknown_operation_fails_closed(self):
        job = copy.deepcopy(CASES["fork-read"])
        job["operation"] = "anything"
        self.assertEqual(assess(job), ["unknown operation"])


if __name__ == "__main__":
    unittest.main()
