"""Validate a build-only recipe and a synthetic intended-identity policy.

No Docker API, JWT verifier, token issuer, registry, or cloud SDK is invoked.
The cloud records are assertions supplied by a fixture, not attested claims.
"""
import argparse
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent


def check_build(recipe):
    job = recipe["jobs"]["image"]
    build = next(s for s in job["steps"] if s.get("id") == "build")
    if build["with"].get("push") != "false":
        raise ValueError("build-only policy rejects registry push; design a separate authenticated job")
    if build["with"].get("context") != "labs/0040/image":
        raise ValueError("expected checked-out path context")
    if "type=oci,dest=" not in build["with"].get("outputs", ""):
        raise ValueError("expected an OCI file exporter")
    if any("login-action@" in s.get("uses", "") for s in job["steps"]):
        raise ValueError("build-only recipe must not acquire registry credentials")


def check_identity(plan):
    expected = {
        "event": "workflow_dispatch",
        "ref": "refs/heads/main",
        "environment": "preview",
        "id_token_permission": "write",
        "issuer": "https://token.actions.githubusercontent.com",
        "audience": "sts.amazonaws.com",
        "subject": "repo:example/course:environment:preview",
        "role_scope": "preview-read-only",
        "approved": True,
    }
    for key, value in expected.items():
        if plan.get(key) != value or type(plan.get(key)) is not type(value):
            raise ValueError(f"identity plan rejected: {key}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("build", "push", "oidc-ok", "oidc-wrong-subject", "oidc-no-permission"))
    args = parser.parse_args()
    try:
        if args.case in ("build", "push"):
            recipe = yaml.load((HERE / "build.yml").read_text(), Loader=yaml.BaseLoader)
            if args.case == "push":
                next(s for s in recipe["jobs"]["image"]["steps"] if s.get("id") == "build")["with"]["push"] = "true"
            check_build(recipe)
            print("PASS: build-only recipe policy; image execution unverified")
        else:
            check_identity(json.loads((HERE / "identity-plans.json").read_text())[args.case])
            print("PASS: intended identity plan; no token or cloud authorization verified")
    except ValueError as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
