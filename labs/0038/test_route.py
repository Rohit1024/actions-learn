import json
import unittest
from route import HERE, load_recipe, route


class RoutingTests(unittest.TestCase):
    def test_table(self):
        cases = json.loads((HERE / "cases.json").read_text())
        for name, expected in {"code": ["code"], "docs": ["docs"], "mixed": ["code", "docs"], "unrelated": [], "manual": ["code", "docs"]}.items():
            with self.subTest(name=name):
                self.assertEqual(route(load_recipe(), cases[name]), expected)

    def test_missing_is_not_false(self):
        with self.assertRaisesRegex(ValueError, "missing or invalid"):
            route(load_recipe(), {"event": "pull_request", "step_outputs": {}})

    def test_typo_in_actual_mapping(self):
        recipe = load_recipe()
        recipe["jobs"]["changes"]["outputs"]["code"] = "${{ steps.filter.outputs.codes }}"
        with self.assertRaisesRegex(ValueError, "codes"):
            route(recipe, {"event": "pull_request", "step_outputs": {"code": "true", "docs": "false"}})

    def test_unsafe_policy_demonstrates_regression(self):
        fixture = {"event": "pull_request", "step_outputs": {"code": "false", "docs": "false"}}
        self.assertEqual(route(load_recipe(), fixture, bare=True), ["code", "docs"])
        self.assertEqual(route(load_recipe(), fixture), [])


if __name__ == "__main__":
    unittest.main()
