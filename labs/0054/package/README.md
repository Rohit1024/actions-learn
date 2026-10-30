# Module 9 release-key action candidate

This local teaching package computes a validated label. It performs no release,
upload, network request, GitHub API write, or credential lookup. It is not a
published action. The display name has not been checked for Marketplace uniqueness.

| Input | Default | Accepted value |
| --- | --- | --- |
| `component` | `docs` | ASCII lowercase letter followed by 0–31 lowercase letters, digits, or hyphens; no trimming |
| `channel` | `preview` | Exactly `preview` or `stable` |

Output `release-key` is `${component}-${channel}`, for example `docs-stable`.
Explicit empty, whitespace, newlines, uppercase components, and unknown channels
fail with nonzero status and no success output. Missing/unwritable `GITHUB_OUTPUT`
also fails. Logs are diagnostics; consumers must use the named output.

```yaml
- uses: ./labs/0054/package
  id: key
  with:
    component: docs
    channel: stable
- name: Consume the named output
  env:
    RELEASE_KEY: ${{ steps.key.outputs.release-key }}
  shell: bash
  run: test "$RELEASE_KEY" = docs-stable
```

The local path requires checkout first. For an extracted repository, replace it
with `OWNER/REPOSITORY@REVIEWED_FULL_COMMIT_SHA` after an actual commit exists.
That string is a future template, not an executable reference.

Runtime: `node24`, entrypoint `dist/index.cjs`. The bundle needs no npm install
by the consumer and no external binaries. Linux/macOS/Windows are design targets;
only the authoring host has process-test evidence. Hosted compatibility and remote
download resolution remain unverified. The action itself needs no token. The
example caller needs `contents: read` to check out this public learning repository.
Self-hosted runners need a runner release supporting Node 24 actions.

Source is included under `src/`. Rebuild in the learning checkout using
`node labs/0052/build.cjs --write`, then run its distribution check and tests before
`uv run python labs/0054/prepare.py`. A future standalone maintenance repository
must include its own reviewed, locked development toolchain and equivalent tests;
this snapshot is a runnable consumer package, not a new project scaffold.

SemVer plan: input/output removals, a stricter accepted-input policy, or changed
key spelling require a major release. Backward-compatible additions can be minor;
compatible fixes can be patches. A future consumer should record the full reviewed
commit SHA and release association. Roll back by restoring its last known-good
SHA. Do not silently move an immutable version release to hide a defect.

License: MIT for this original lab package; see LICENSE. This does not relicense
the entire learning repository or third-party tools.

No learner understanding or hosted validation is established by this README.
