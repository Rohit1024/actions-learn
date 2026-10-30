import json
import unittest
from check_contracts import ROOT, POSITIVE, inspect
from gate import require_evidence


class MaintenanceTests(unittest.TestCase):
    def test_exact_metadata_contracts(self):
        evidence = json.loads((ROOT / "labs/0037/upstream-evidence.json").read_text())
        for filename in POSITIVE:
            with self.subTest(filename=filename):
                self.assertGreater(inspect(ROOT / filename, evidence), 0)

    def test_unknown_input_rejected(self):
        evidence = json.loads((ROOT / "labs/0037/upstream-evidence.json").read_text())
        with self.assertRaisesRegex(ValueError, "always-auth"):
            inspect(ROOT / "labs/0042/obsolete-input.negative.yml", evidence)

    def test_optional_skip_is_explicit(self):
        self.assertIn("READY", require_evidence("false", "success", "skipped"))
        self.assertIn("READY", require_evidence("true", "success", "success"))

    def test_required_failure_missing_skip_cancel(self):
        for state in ("failure", "skipped", "cancelled", ""):
            with self.subTest(state=state), self.assertRaises(ValueError):
                require_evidence("true", "success", state)

    def test_node_always_required(self):
        with self.assertRaisesRegex(ValueError, "node"):
            require_evidence("false", "failure", "skipped")

    def test_string_false_is_parsed_explicitly(self):
        with self.assertRaisesRegex(ValueError, "true or false"):
            require_evidence("yes", "success", "skipped")


if __name__ == "__main__":
    unittest.main()
