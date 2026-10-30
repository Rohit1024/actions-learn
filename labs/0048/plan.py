"""Audit a declared trial budget. Executes no workflow, API or model request."""
import argparse
import json
from pathlib import Path
import sys


def audit(plan, require_ready=False):
    errors = []
    budget = plan["budget"]
    if any(type(value) is not int or value < 0 for value in budget.values()):
        return 0, ["budget values must be nonnegative integers"]
    jobs = plan["planned_job_deadlines_minutes"]
    if not jobs or any(type(value) is not int or value <= 0 for value in jobs.values()):
        return 0, ["job deadlines must be positive integers"]
    ceiling = sum(jobs.values()) * budget["planned_runs"]
    if budget["planned_runs"] > budget["max_runs"]:
        errors.append("planned runs exceed run allowance")
    if ceiling > budget["max_runner_minutes"]:
        errors.append("planned job-minutes exceed allowance")
    for actual, limit in [("actual_runs", "max_runs"), ("actual_model_requests", "max_model_requests"), ("actual_external_writes", "max_external_writes")]:
        if budget[actual] > budget[limit]:
            errors.append(f"{actual} exceeds {limit}")
    if plan["staged"] is not True or budget["max_external_writes"] != 0:
        errors.append("report trial requires staged outputs and zero external-write allowance")
    if require_ready:
        for key in ["compiler_verified", "generated_workflow_reviewed", "authentication_verified", "provider_budget_enforced", "execution_authorized"]:
            if plan[key] is not True:
                errors.append(f"not ready: {key}")
    return ceiling, errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text())
        ceiling, errors = audit(plan, args.require_ready)
        if errors:
            for error in errors:
                print("BLOCKED: " + error, file=sys.stderr)
            sys.exit(1)
        print(f"planned execution ceiling={ceiling} job-minutes; not a billing quote")
        budget = plan["budget"]
        print(f"PLAN CONSISTENT: hosted runs={budget['actual_runs']}, "
              f"model requests={budget['actual_model_requests']}, "
              f"writes={budget['actual_external_writes']} in this saved declaration")
        print("Readiness remains unverified; this program cannot dispatch")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"BLOCKED: invalid plan: {error}", file=sys.stderr)
        sys.exit(1)
