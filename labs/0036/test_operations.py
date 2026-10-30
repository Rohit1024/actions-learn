import copy
import json
from pathlib import Path
import unittest
from operations import escape_command, evaluate, recovery_demo

LEDGER = json.loads(Path(__file__).with_name("ledger.json").read_text())


class OperationsTests(unittest.TestCase):
    def test_usage_is_sum_not_wall_clock(self):
        usage, problems, _ = evaluate(LEDGER)
        self.assertEqual(usage["runner_seconds"], 75)
        self.assertEqual(problems, [])

    def test_allowlist_omits_private_payload(self):
        self.assertNotIn("SYNTHETIC-SECRET", evaluate(LEDGER)[2])

    def test_every_budget_axis(self):
        for axis in LEDGER["budget"]:
            changed = copy.deepcopy(LEDGER)
            changed["budget"][axis] = 0
            if axis == "model_calls":
                changed["model_calls"] = 1
            with self.subTest(axis=axis):
                self.assertIn(f"{axis} over budget", evaluate(changed)[1])

    def test_non_success_blocks(self):
        for result in ["failure", "skipped", "cancelled"]:
            changed = copy.deepcopy(LEDGER)
            changed["jobs"][1]["result"] = result
            with self.subTest(result=result):
                self.assertIn(f"required windows={result}", evaluate(changed)[1])

    def test_missing_evidence_and_invalid_measurement(self):
        changed = copy.deepcopy(LEDGER)
        changed["jobs"].pop()
        with self.assertRaisesRegex(ValueError, "required job"):
            evaluate(changed)
        changed = copy.deepcopy(LEDGER)
        changed["jobs"][0]["seconds"] = float("nan")
        with self.assertRaisesRegex(ValueError, "measurement"):
            evaluate(changed)

    def test_annotation_data_escaping(self):
        self.assertEqual(escape_command("50%\n::error::fake\r"), "50%25%0A::error::fake%0D")

    def test_repeatable_recovery(self):
        recovery_demo()


if __name__ == "__main__":
    unittest.main()
