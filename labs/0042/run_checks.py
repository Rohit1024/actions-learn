"""Run the explicit Module 7 host/static checks, never documentation checks.

Expected-negative commands must fail with the selected diagnostic. The unsafe
string experiment intentionally exits zero while showing an incorrect choice.
No action, package install, container, hosted workflow, or API is executed.
"""
import argparse
import datetime
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON = ".venv/bin/python"
POSITIVE = ["labs/0038/selective.yml", "labs/0039/exchange.yml", "labs/0040/build.yml", "labs/0041/release.yml", "labs/0042/pipeline.yml"]


def cases():
    checks = []
    for lesson, filename in [("0037", "test_selection.py"), ("0038", "test_route.py"), ("0039", "test_contract.py"), ("0040", "test_policy.py"), ("0041", "test_effects.py"), ("0042", "test_maintenance.py")]:
        checks.append(([PYTHON, "-m", "unittest", "discover", "-s", f"labs/{lesson}", "-p", filename, "-v"], 0, "OK"))
    checks += [
        ([PYTHON, "labs/0042/check_contracts.py"], 0, "20 exact-pin"),
        ([".tools/bin/actionlint", "-no-color", *POSITIVE], 0, ""),
        ([PYTHON, "labs/0037/selection.py", "labs/0037/accepted.json"], 0, "ADMIT RECORD:"),
        ([PYTHON, "labs/0037/selection.py", "labs/0037/mismatched.json"], 1, "Marketplace repository mismatch"),
    ]
    for name, expected in [("code", "code"), ("docs", "docs"), ("mixed", "code,docs"), ("unrelated", "none"), ("manual", "code,docs")]:
        checks.append(([PYTHON, "labs/0038/route.py", name], 0, f"selected={expected}"))
    checks += [
        ([PYTHON, "labs/0038/route.py", "unrelated", "--bare"], 0, "selected=code,docs"),
        ([PYTHON, "labs/0038/route.py", "code", "--typo"], 1, "missing or invalid output: codes"),
        ([PYTHON, "labs/0038/route.py", "missing"], 1, "missing or invalid output: docs"),
        ([PYTHON, "labs/0039/contract.py"], 0, "PASS:"),
        ([PYTHON, "labs/0039/contract.py", "--skip-install"], 1, "MODULE_NOT_FOUND"),
        ([PYTHON, "labs/0039/contract.py", "--wrong-name"], 1, "artifact name mismatch"),
        ([PYTHON, "labs/0039/contract.py", "--tamper"], 1, "consumer digest mismatch"),
        ([PYTHON, "labs/0040/policy.py", "build"], 0, "image execution unverified"),
        ([PYTHON, "labs/0040/policy.py", "push"], 1, "rejects registry push"),
        ([PYTHON, "labs/0040/policy.py", "oidc-ok"], 0, "no token or cloud authorization verified"),
        ([PYTHON, "labs/0040/policy.py", "oidc-wrong-subject"], 1, "rejected: subject"),
        ([PYTHON, "labs/0040/policy.py", "oidc-no-permission"], 1, "rejected: id_token_permission"),
        ([PYTHON, "labs/0041/effects.py", "release"], 0, "ALLOW PLAN:"),
        ([PYTHON, "labs/0041/effects.py", "fork"], 1, "requires dispatch from main"),
        ([PYTHON, "labs/0041/effects.py", "no-write"], 1, "permissions do not match"),
        ([PYTHON, "labs/0041/effects.py", "untrusted"], 1, "untrusted producer"),
        ([PYTHON, "labs/0041/effects.py", "excess"], 1, "permissions do not match"),
        ([PYTHON, "labs/0041/report.py", "labs/0041/pass.xml"], 0, "total=2 failed=0 skipped=0"),
        ([PYTHON, "labs/0041/report.py", "labs/0041/fail.xml"], 1, "total=2 failed=1 skipped=0"),
        ([PYTHON, "labs/0042/check_contracts.py", "labs/0042/obsolete-input.negative.yml"], 1, "unknown inputs: always-auth"),
        ([PYTHON, "labs/0042/gate.py", "--image", "false", "--node-result", "success", "--image-result", "skipped"], 0, "READY:"),
        ([PYTHON, "labs/0042/gate.py", "--image", "true", "--node-result", "success", "--image-result", "success"], 0, "READY:"),
        ([PYTHON, "labs/0042/gate.py", "--image", "true", "--node-result", "success", "--image-result", "skipped"], 1, "image result is skipped; expected success"),
        ([PYTHON, "labs/0042/gate.py", "--image", "false", "--node-result", "failure", "--image-result", "skipped"], 1, "required node result is failure"),
    ]
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()
    results = []
    for command, expected_code, expected_text in cases():
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        passed = result.returncode == expected_code and expected_text in output
        results.append({"command": shlex.join(command), "expected_exit": expected_code, "actual_exit": result.returncode, "expected_text": expected_text, "passed": passed, "output": output})
        print(f"{'PASS' if passed else 'FAIL'} exit={result.returncode} expected={expected_code}: {shlex.join(command)}")
        if not passed:
            print(output)
    if args.write_receipt:
        receipt = {"checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "scope": "Module 7 host programs and explicit-file workflow/metadata checks only; documentation validation deferred.", "results": results}
        (ROOT / "labs/0042/check-results.json").write_text(json.dumps(receipt, indent=2) + "\n")
    failed = sum(not r["passed"] for r in results)
    print(f"RESULT: {len(results)} expected outcomes; {failed} unexpected failures")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
