# Proposed v1.0.0 — local candidate, unreleased

Compute `release-key` from validated `component` and `channel` inputs using a
self-contained Node 24 bundle. Default example: `docs-preview`.

Compatibility: key spelling and accepted input set constitute the v1 interface.
The action makes no API calls and requests no token. Caller checkout is separate.
Host tests and source/distribution comparison can establish local readiness.
GitHub runner execution, the intended OS matrix, immutable remote reference
resolution, and Marketplace name eligibility require future evidence.

Before release, record the exact candidate commit, source/distribution test
results, consumer run URL and head SHA, reviewed dependency pins, supported
runner matrix, and any known limitations. Replace this proposed note with
observed evidence; do not describe deferred checks as passed.

Future operator exercise: extract this single-action package to a dedicated
repository, add locked build/test tooling, check the license and display name,
review the candidate commit, run a bounded consumer check against its full SHA,
then deliberately create a versioned release. Marketplace listing is optional
and requires the publication prerequisites and agreement. Do not perform any
of those remote operations as part of this local lab.

Recovery: retain the previous known-good full SHA in consumer history. A fixed
release gets a new version and commit. Consider a movable major alias only under
a documented update policy and compatible repository release protections.
