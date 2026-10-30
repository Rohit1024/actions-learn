"""Synthetic usage policy, escaped diagnostics and local recovery journal."""
import argparse
import json
import math
import os
from pathlib import Path
import re
import tempfile


def escape_command(text):
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def evaluate(ledger):
    if (not re.fullmatch(r"[0-9]+", ledger["run_id"])
            or not re.fullmatch(r"[a-f0-9]{40}", ledger["sha"])
            or type(ledger["attempt"]) is not int or ledger["attempt"] < 1):
        raise ValueError("invalid run identity")
    expected = {"linux", "windows"}
    jobs = ledger["jobs"]
    if len(jobs) != 2 or {job["id"] for job in jobs} != expected:
        raise ValueError("missing or duplicate required job")
    for job in jobs:
        if job["result"] not in {"success", "failure", "skipped", "cancelled"}:
            raise ValueError("unknown result")
        for field in ["seconds", "artifact_bytes"]:
            value = job[field]
            if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
                raise ValueError("invalid usage measurement")
    if type(ledger["model_calls"]) is not int or ledger["model_calls"] < 0:
        raise ValueError("invalid model call count")
    usage = {"runner_seconds": sum(job["seconds"] for job in jobs),
             "artifact_bytes": sum(job["artifact_bytes"] for job in jobs),
             "model_calls": ledger["model_calls"]}
    problems = [f"required {job['id']}={job['result']}" for job in jobs if job["result"] != "success"]
    for name, value in usage.items():
        limit = ledger["budget"][name]
        if type(limit) not in {int, float} or not math.isfinite(limit) or limit < 0:
            raise ValueError("invalid budget")
        if value > limit:
            problems.append(f"{name} over budget")
    text = (f"Run {ledger['run_id']} attempt {ledger['attempt']} at {ledger['sha']}\n\n"
            f"Required evidence: {'BLOCKED' if problems else 'PASS'}\n\n"
            f"Runner seconds: {usage['runner_seconds']}; artifact bytes: {usage['artifact_bytes']}; "
            f"model calls: {usage['model_calls']}\n")
    return usage, problems, text


def recovery_demo():
    with tempfile.TemporaryDirectory(prefix="lesson-0036-") as folder:
        root = Path(folder)
        payload = root / "uploaded-marker"
        receipt = root / "receipt"
        payload.write_text("candidate-a\n")
        assert payload.exists() and not receipt.exists()
        print("interrupted model: upload marker exists; receipt missing")
        for _ in range(2):
            # Reconcile the same operation identity before completing its receipt.
            if payload.read_text() != "candidate-a\n":
                raise ValueError("operation identity conflict")
            receipt.write_text("candidate-a complete\n")
        assert payload.read_text() == "candidate-a\n" and receipt.exists()
        print("reconcile twice: one upload marker; matching completed receipt")
    print("temporary journal removed; no real publication or cancellation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["pass", "over-budget", "failed-worker", "recovery"])
    args = parser.parse_args()
    if args.case == "recovery":
        recovery_demo()
        return 0
    ledger = json.loads(Path(__file__).with_name("ledger.json").read_text())
    if args.case == "over-budget":
        ledger["jobs"][1]["seconds"] = 100
    if args.case == "failed-worker":
        ledger["jobs"][1]["result"] = "failure"
    _, problems, summary = evaluate(ledger)
    print(summary, end="")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write(summary)
    for problem in problems:
        print("::error title=Module 6 policy::" + escape_command(problem))
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(main())
