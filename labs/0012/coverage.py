"""Audit a small evidence declaration; does not execute checks or attest their truth."""

import argparse
import json
from pathlib import Path
import sys

PLATFORM_CLAIMS = {"actual-token-permissions", "oidc-federation", "environment-approval"}
LAYERS = {"host", "static", "container", "act", "github"}


def audit(plan, release=False):
    problems = []
    claims = plan["claims"]
    if not claims:
        problems.append("no verification claims declared")
    ids = [claim["id"] for claim in claims]
    if len(ids) != len(set(ids)):
        problems.append("duplicate claim IDs")
    for claim in claims:
        evidence = claim["evidence"]
        layer, status = evidence["layer"], evidence["status"]
        minimum = claim["minimum_layer"]
        if layer not in LAYERS or minimum not in LAYERS:
            problems.append(claim["id"] + ": unknown evidence layer")
        if status not in {"pass", "fail", "not-run", "deferred", "simulated"}:
            problems.append(claim["id"] + ": unknown evidence status")
        if claim["id"] in PLATFORM_CLAIMS and minimum != "github":
            problems.append(claim["id"] + ": platform contract requires GitHub evidence")
        if status == "pass":
            if layer != minimum:
                problems.append(claim["id"] + ": passing evidence uses the wrong observing layer")
            if claim["id"] in PLATFORM_CLAIMS and layer != "github":
                problems.append(claim["id"] + ": local success cannot prove platform policy")
            if evidence.get("revision") != plan["revision"]:
                problems.append(claim["id"] + ": passing evidence must match the current revision")
            if not evidence.get("reference"):
                problems.append(claim["id"] + ": passing evidence needs a log or run reference")
        if release and claim["required_for"] in {"local-candidate", "platform-release"} and status != "pass":
            problems.append(claim["id"] + ": required evidence is " + status)
    budget = plan["budget"]
    for actual, maximum in (("actual_hosted_runs", "max_hosted_runs_per_revision"),
                            ("actual_model_calls", "max_model_calls"),
                            ("actual_external_writes", "max_external_writes")):
        if budget[actual] < 0 or budget[maximum] < 0 or budget[actual] > budget[maximum]:
            problems.append(actual + ": outside the declared budget")
    for field in ("planned_jobs", "job_timeout_minutes", "matrix_size"):
        if not isinstance(budget[field], int) or isinstance(budget[field], bool) or budget[field] <= 0:
            problems.append(field + ": must be a positive integer")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-release", action="store_true")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text())
        problems = audit(plan, args.require_release)
        for claim in plan["claims"]:
            evidence = claim["evidence"]
            print(claim["id"] + ": " + evidence["status"] + " via " + evidence["layer"])
        budget = plan["budget"]
        ceiling = budget["planned_jobs"] * budget["matrix_size"] * budget["job_timeout_minutes"]
        print("planned execution ceiling=" + str(ceiling) + " job-minutes (not a billing quote)")
        if problems:
            for problem in problems:
                print("BLOCKED: " + problem, file=sys.stderr)
            return 1
        print("PLAN CONSISTENT: declarations accepted; unexecuted checks remain unverified")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("BLOCKED: malformed plan: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
