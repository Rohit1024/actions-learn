"""Claim-selection exercise, NOT a JWT verifier or provider policy."""
import argparse
import json
from pathlib import Path

POLICY = {
    "iss": "https://token.actions.githubusercontent.com", "aud": "urn:lesson:deploy",
    "sub": "repo:example@100/lesson@200:environment:staging",
    "repository_id": "200", "repository_owner_id": "100", "environment": "staging",
    "ref": "refs/heads/main", "event_name": "workflow_dispatch",
}


def decide(claims, approved, now=1100):
    reasons = [f"claim {key} mismatch" for key, expected in POLICY.items()
               if claims.get(key) != expected]
    if (type(claims.get("nbf")) is not int or type(claims.get("exp")) is not int
            or not claims["nbf"] <= now < claims["exp"]):
        reasons.append("outside validity window")
    if approved is not True:
        reasons.append("approval not observed in simulation")
    return reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["allowed", "wrong-audience", "fork", "expired", "unapproved"])
    args = parser.parse_args()
    claims = json.loads(Path(__file__).with_name("claims.json").read_text())
    if args.case == "wrong-audience":
        claims["aud"] = "urn:other"
    if args.case == "fork":
        claims["sub"] = "repo:external@300/fork@400:pull_request"
        claims["repository_id"] = "400"
    reasons = decide(claims, args.case != "unapproved", 1400 if args.case == "expired" else 1100)
    print("DENY: " + "; ".join(reasons) if reasons else "ALLOW: synthetic claim selection and approval match")
    print("NOT VERIFIED: signature, issuer keys, real approval, federation, resource authorization")
    return bool(reasons)


if __name__ == "__main__":
    raise SystemExit(main())
