"""Check review freshness independently of whether a dependency reference is pinned."""
import argparse
from datetime import date


def check_freshness(reviewed_on: date, as_of: date, max_age_days: int = 30) -> int:
    age = (as_of - reviewed_on).days
    if max_age_days < 0 or age < 0 or age > max_age_days:
        raise ValueError(f"dependency review age={age} days is outside 0..{max_age_days}")
    return age


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-on", required=True, type=date.fromisoformat)
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    args = parser.parse_args()
    try:
        age = check_freshness(args.reviewed_on, args.as_of)
    except ValueError as error:
        print(f"FAIL: {error}")
        return 1
    print(f"PASS: review age={age} days; freshness only, no scan or release approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
