import unittest
from release_demo import ROOT, consume, demo, run_node


class ReleaseTests(unittest.TestCase):
    def test_distribution_matches(self):
        result = run_node([ROOT / "build.cjs", "--check"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_consumer_output(self):
        result, output = consume(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output, "greeting=Hello, Ada!\n")

    def test_invalid_input_publishes_no_output(self):
        result, output = consume(ROOT, "\n")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(output, "")

    def test_temporary_drift_and_repair(self):
        demo()


if __name__ == "__main__":
    unittest.main()
