import copy
import json
import tempfile
import unittest
from pathlib import Path
from effects import HERE, authorize
from report import summarize


class EffectsTests(unittest.TestCase):
    def setUp(self):
        self.plans = json.loads((HERE / "effect-plans.json").read_text())

    def test_release_plan(self):
        self.assertIn("no API", authorize(self.plans["release"]))

    def test_bad_plans(self):
        for name in ("fork", "no-write", "untrusted", "excess"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                authorize(self.plans[name])

    def test_approval_must_be_boolean(self):
        plan = copy.deepcopy(self.plans["release"])
        plan["approved"] = "false"
        with self.assertRaisesRegex(ValueError, "acknowledged"):
            authorize(plan)

    def test_report_counts(self):
        self.assertEqual(summarize(HERE / "pass.xml"), (2, 0, 0))
        self.assertEqual(summarize(HERE / "fail.xml"), (2, 1, 0))

    def test_empty_report_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "empty.xml"
            path.write_text("<testsuite/>")
            with self.assertRaisesRegex(ValueError, "1..20"):
                summarize(path)


if __name__ == "__main__":
    unittest.main()
