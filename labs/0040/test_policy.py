import copy
import json
import unittest
import yaml
from policy import HERE, check_build, check_identity


class CompositionPolicyTests(unittest.TestCase):
    def test_build_only(self):
        check_build(yaml.load((HERE / "build.yml").read_text(), Loader=yaml.BaseLoader))

    def test_push_rejected(self):
        recipe = yaml.load((HERE / "build.yml").read_text(), Loader=yaml.BaseLoader)
        next(s for s in recipe["jobs"]["image"]["steps"] if s.get("id") == "build")["with"]["push"] = "true"
        with self.assertRaisesRegex(ValueError, "registry push"):
            check_build(recipe)

    def test_exact_identity_plan(self):
        check_identity(json.loads((HERE / "identity-plans.json").read_text())["oidc-ok"])

    def test_every_policy_field_matters(self):
        good = json.loads((HERE / "identity-plans.json").read_text())["oidc-ok"]
        for key in good:
            changed = copy.deepcopy(good)
            changed[key] = False if key == "approved" else "unexpected"
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, key):
                check_identity(changed)


if __name__ == "__main__":
    unittest.main()
