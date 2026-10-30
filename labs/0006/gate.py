"""Apply this lab's evidence policy; this does not simulate job scheduling."""

import argparse
import sys


parser = argparse.ArgumentParser(description=__doc__)
states = ["success", "failure", "skipped", "cancelled"]
parser.add_argument("--worker", choices=states, default="success")
parser.add_argument("--review", choices=states, default="success")
args = parser.parse_args()
if args.worker != "success" or args.review != "success":
    print(f"BLOCKED: worker={args.worker}, review={args.review}", file=sys.stderr)
    raise SystemExit(1)
print("READY: required worker and review evidence succeeded")
