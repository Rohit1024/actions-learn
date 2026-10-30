# Module 7 authoring handoff — 2026-10-30

## Completion and ownership

**MODULE 7 AUTHORING COMPLETE: canonical lessons 0037–0042.** All six existing pages are fully developed reference lessons and marked `lesson_status: authored`. Optional guide `docs/lessons/prebuilt-actions.md` is updated. Boundary pagination remains 0036 → 0037–0042 → 0043. No numbering, shared catalog/count, shared example, dependency, workflow-installation, credential, or infrastructure changes were made by this authoring thread. Other top-level authors/coordinator have simultaneous uncommitted changes; those were preserved. No commits, pushes, hosted execution, new threads, or subagents were used.

The later explicit user requirement supersedes the old teach handoff wording: the six completed lessons have learner prerequisites, labs, predictions, collapsed worked solutions, failures, transfer/retrieval questions, references, vertical diagrams, annotations/admonitions and navigation, but no lesson-creation/thread prompts or authoring handoff directions. Authoring evidence is stored here and in the owned lab receipts.

Written availability and assistant-run checks establish **no learner mastery**. No learner exercise responses were collected. Live teaching can begin with prerequisite predictions rather than treating these pages as completed learning.

## Page inventory

- `docs/lessons/0037-selecting-popular-prebuilt-actions.md`
- `docs/lessons/0038-paths-filter-and-selective-jobs.md`
- `docs/lessons/0039-setup-cache-and-artifact-actions.md`
- `docs/lessons/0040-docker-build-and-cloud-auth-actions.md`
- `docs/lessons/0041-release-pr-and-reporting-actions.md`
- `docs/lessons/0042-compose-maintained-actions-and-manage-updates.md`
- `docs/lessons/prebuilt-actions.md` — module overview, contract map, explicit local commands and integration boundaries.

## Complete lab inventory

All recipes below remain inactive under `labs/`. No new file was installed under `.github/`. All fixture data is synthetic except explicitly dated read-only upstream observations. The dependency module in 0039 is authored locally and copied into a temporary synthetic tree, not installed from a package manager.

### 0037

Action selection policy, synthetic accepted/mismatched decisions, six regression tests, and read-only primary-source receipts for 13 project action pins.

- `labs/0037/accepted.json`
- `labs/0037/mismatched.json`
- `labs/0037/selection.py`
- `labs/0037/test_selection.py`
- `labs/0037/upstream-evidence.json`

### 0038

Actual inactive paths-filter recipe, supplied output cases, constrained literal mapping consumer and four test methods. No path matcher/API/runner emulator.

- `labs/0038/cases.json`
- `labs/0038/route.py`
- `labs/0038/selective.yml`
- `labs/0038/test_route.py`

### 0039

Inactive setup/artifact exchange, real Node build/module-resolution probe, synthetic dependency, local file/name/digest consumers and five test methods.

- `labs/0039/build.cjs`
- `labs/0039/contract.py`
- `labs/0039/exchange.yml`
- `labs/0039/fixture-dependency.cjs`
- `labs/0039/test_contract.py`

### 0040

Inactive Docker build-only recipe, bounded scratch image context, intended-identity fixtures, real recipe/policy checks and four test methods. No JWT/provider emulator.

- `labs/0040/build.yml`
- `labs/0040/identity-plans.json`
- `labs/0040/image/Dockerfile`
- `labs/0040/image/message.txt`
- `labs/0040/policy.py`
- `labs/0040/test_policy.py`

### 0041

Inactive manually acknowledged release-proposal recipe, operation policy used by that recipe, bounded XML report consumer, passing/failing reports and five test methods. No API transport.

- `labs/0041/effect-plans.json`
- `labs/0041/effects.py`
- `labs/0041/fail.xml`
- `labs/0041/pass.xml`
- `labs/0041/release.yml`
- `labs/0041/report.py`
- `labs/0041/test_effects.py`

### 0042

Inactive composed pipeline and actual join program, five-file exact-pin contract checker, real historical obsolete-input fixture, Dependabot proposal, six test methods, explicit check runner and persisted receipts.

- `labs/0042/check-results.json`
- `labs/0042/check_contracts.py`
- `labs/0042/dependabot.example.yml`
- `labs/0042/environment-results.json`
- `labs/0042/gate.py`
- `labs/0042/historical-input-evidence.json`
- `labs/0042/obsolete-input.negative.yml`
- `labs/0042/pipeline.yml`
- `labs/0042/run_checks.py`
- `labs/0042/test_maintenance.py`

Inventory: **37 lab/source/fixture/receipt files**, plus this handoff and the seven lesson/guide files listed above. Python bytecode caches, if present, are generated local cache files and not authored source artifacts.

## Actually executed focused checks

The final reproducible entrypoint was:

```bash
.venv/bin/python labs/0042/run_checks.py --write-receipt
```

It exited **0**: **39 expected outcomes; 0 unexpected failures**. This includes **30 passing unittest methods** (6 + 4 + 5 + 4 + 5 + 6), five explicit positive workflow actionlint targets and 20 exact-pin input contracts. Standalone negative commands are expected exits, not failing positive checks. The unsafe bare-string example intentionally exits 0 while producing the wrong selection. The full output/exit/expected-text receipt is `labs/0042/check-results.json`. Its scope is host and static workflow/metadata checking only.

The same six test modules, offline metadata checker and explicit actionlint list were also run directly earlier. After changing the historical-input negative fixture from an invented unknown name to the verified historical `always-auth` input, the final runner re-executed all checks with the final executable files. No source/code changes followed that successful run; only the environment receipt and this handoff were added.

### Exact final commands and results

| Command | Expected / actual exit | Result |
| --- | --- | --- |
| `.venv/bin/python -m unittest discover -s labs/0037 -p test_selection.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python -m unittest discover -s labs/0038 -p test_route.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python -m unittest discover -s labs/0039 -p test_contract.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python -m unittest discover -s labs/0040 -p test_policy.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python -m unittest discover -s labs/0041 -p test_effects.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python -m unittest discover -s labs/0042 -p test_maintenance.py -v` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0042/check_contracts.py` | 0 / 0 | Expected outcome observed |
| `.tools/bin/actionlint -no-color labs/0038/selective.yml labs/0039/exchange.yml labs/0040/build.yml labs/0041/release.yml labs/0042/pipeline.yml` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0037/selection.py labs/0037/accepted.json` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0037/selection.py labs/0037/mismatched.json` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py code` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py docs` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py mixed` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py unrelated` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py manual` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py unrelated --bare` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py code --typo` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0038/route.py missing` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0039/contract.py` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0039/contract.py --skip-install` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0039/contract.py --wrong-name` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0039/contract.py --tamper` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0040/policy.py build` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0040/policy.py push` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0040/policy.py oidc-ok` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0040/policy.py oidc-wrong-subject` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0040/policy.py oidc-no-permission` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0041/effects.py release` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0041/effects.py fork` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0041/effects.py no-write` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0041/effects.py untrusted` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0041/effects.py excess` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0041/report.py labs/0041/pass.xml` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0041/report.py labs/0041/fail.xml` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0042/check_contracts.py labs/0042/obsolete-input.negative.yml` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0042/gate.py --image false --node-result success --image-result skipped` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0042/gate.py --image true --node-result success --image-result success` | 0 / 0 | Expected outcome observed |
| `.venv/bin/python labs/0042/gate.py --image true --node-result success --image-result skipped` | 1 / 1 | Expected outcome observed |
| `.venv/bin/python labs/0042/gate.py --image false --node-result failure --image-result skipped` | 1 / 1 | Expected outcome observed |

### Positive workflow list

```bash
.tools/bin/actionlint -no-color \
  labs/0038/selective.yml \
  labs/0039/exchange.yml \
  labs/0040/build.yml \
  labs/0041/release.yml \
  labs/0042/pipeline.yml
```

Actionlint exited 0 with no diagnostics. `labs/0042/obsolete-input.negative.yml` was never included in a positive lint glob/list. `dependabot.example.yml` is configuration, not a workflow-lint target. The obsolete-input failure was asserted by the exact-pin metadata consumer, not represented as an observed GitHub runtime failure.

### Expected negative interpretations

- 0037 mismatch: exact publisher/repository mismatch blocks despite a correct-looking pin or popularity.
- 0038 `--bare`: deliberately wrong `selected=code,docs` for supplied false/false strings, exit 0. `--typo` and missing output exit 1 with the named lost field. These supplied results do not execute dorny or its picomatch rules.
- 0039 skip materialization: real Node exits with `MODULE_NOT_FOUND`; a synthetic download-cache marker does not populate the required module. Name mismatch and tampered local result also block. This is not an npm/cache/artifact implementation.
- 0040 push mutation: the real local build-only policy rejects the scope expansion; no registry 401 or cloud denial was generated. Wrong subject and missing token-request permission fail the intended-identity policy only.
- 0041 fork, read-only, untrusted-producer and excess-permission plans block; the report fixture with one failed case exits 1 and reports that no check was published.
- 0042 historical `always-auth` field is absent from exact current metadata and fails input checking; required image skip and required Node failure fail the actual workflow gate.

## Environment and tool inspection

Exact recorded environment commands/results are in `labs/0042/environment-results.json`:

- `node --version` — exit 0: v24.21.0.
- `.venv/bin/python --version` — exit 0: Python 3.14.6.
- `uv --version` — exit 0: uv 0.11.24 (5e04460c0 2026-06-23 aarch64-apple-darwin).
- `.tools/bin/actionlint -version` — exit 0: v1.7.12.
- `act --version` — exit 0: act version 0.2.89.
- `docker info` — exit 125: OS: darwin/arm64.
- `zsh -c 'command -v shellcheck'` — exit 1: not found on PATH.
- `zsh -c 'command -v zizmor'` — exit 1: not found on PATH.

`docker info` exits **125**: Docker is a Podman-compatible command on darwin/arm64 (Podman 6.0.2/libkrun); connection to `127.0.0.1:62183` was refused. No machine/VM was started. Therefore no container build, Buildx image export, image runtime, act workflow execution, cache backend or Docker mount test was attempted. `act` is installed but its version/help is not execution evidence. ShellCheck and zizmor are absent and were not installed; actionlint success is not a security-audit pass.

Installed help actually inspected: `.tools/bin/actionlint -help` documents explicit file arguments, `-no-color`, and the optional ShellCheck integration; `act --help | head -n 45` shows job/workflow/event/architecture selection and listing flags. These were read-only help checks. Existing PyYAML 6.0.3 was imported with `.venv/bin/python`; no dependencies, lockfiles or manifests were installed/changed.

## Verified primary sources and date

All checks below were made on **2026-10-30** using read-only public primary URLs. `labs/0037/upstream-evidence.json` records per-URL outcomes, repository observations (including dated stars/archive/activity), resolved tags, exact-pin metadata input/default/output/runtime summaries, Marketplace matching and release metadata. All 13 project tags resolved to their preserved full SHAs; metadata and release metadata were retrieved. No latest-version claim is inferred merely because a preserved tag was verified. The shared snapshot/catalog was left unchanged.

### Per-pin receipts

| Repository | Preserved tag / commit | Metadata runtime | Publisher observation |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` / `3d3c42e5aac5ba805825da76410c181273ba90b1` | `node24` | verified creator observed |
| `actions/cache` | `v6.1.0` / `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` | `node24` | verified creator observed |
| `docker/build-push-action` | `v7.4.0` / `c3c9e263c25d99ce0380d002d59b67737d91b0dc` | `node24` | verified creator observed |
| `actions/setup-node` | `v7.1.0` / `949feb2413d6458794dcd2491c4babbbce0c15c1` | `node24` | verified creator observed |
| `actions/upload-artifact` | `v7.0.2` / `cf430e030ddbb5b0abf93d22962f4752f3646cd9` | `node24` | verified creator observed |
| `dorny/paths-filter` | `v4.0.3` / `ceb8a2b8f2d89434be7ff52d3de7ec3738c5cc9d` | `node24` | no badge observed |
| `peter-evans/create-pull-request` | `v8.1.1` / `5f6978faf089d4d20b00c7766989d076bb2fc7f1` | `node24` | no badge observed |
| `googleapis/release-please-action` | `v5.0.0` / `45996ed1f6d02564a971a2fa1b5860e934307cf7` | `node24` | verified creator observed |
| `actions/download-artifact` | `v8.0.2` / `9000827ccba6bdab643e8b6fd33ac0654aef8333` | `node24` | verified creator observed |
| `docker/login-action` | `v4.7.0` / `81c6f93d4bc991e510b342a00b419b3bb4efc5c6` | `node24` | verified creator observed |
| `docker/setup-buildx-action` | `v4.4.1` / `f87e5991a6d7451dcb8d9637bfbc97413f497069` | `node24` | verified creator observed |
| `docker/metadata-action` | `v6.2.0` / `dc802804100637a589fabce1cb79ff13a1411302` | `node24` | verified creator observed |
| `astral-sh/setup-uv` | `v10.3.3` / `68559e99cc807c1eb7e9238fd43a15bba460eec2` | `node24` | verified creator observed |

### Exact upstream URLs checked

**actions/checkout**

- https://api.github.com/repos/actions/checkout/git/ref/tags/v7.0.1
- https://raw.githubusercontent.com/actions/checkout/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml
- https://api.github.com/repos/actions/checkout
- https://github.com/marketplace/actions/checkout
- https://api.github.com/repos/actions/checkout/releases/tags/v7.0.1

**actions/cache**

- https://api.github.com/repos/actions/cache/git/ref/tags/v6.1.0
- https://raw.githubusercontent.com/actions/cache/55cc8345863c7cc4c66a329aec7e433d2d1c52a9/action.yml
- https://api.github.com/repos/actions/cache
- https://github.com/marketplace/actions/cache
- https://api.github.com/repos/actions/cache/releases/tags/v6.1.0

**docker/build-push-action**

- https://api.github.com/repos/docker/build-push-action/git/ref/tags/v7.4.0
- https://raw.githubusercontent.com/docker/build-push-action/c3c9e263c25d99ce0380d002d59b67737d91b0dc/action.yml
- https://api.github.com/repos/docker/build-push-action
- https://github.com/marketplace/actions/build-and-push-docker-images
- https://api.github.com/repos/docker/build-push-action/releases/tags/v7.4.0

**actions/setup-node**

- https://api.github.com/repos/actions/setup-node/git/ref/tags/v7.1.0
- https://raw.githubusercontent.com/actions/setup-node/949feb2413d6458794dcd2491c4babbbce0c15c1/action.yml
- https://api.github.com/repos/actions/setup-node
- https://github.com/marketplace/actions/setup-node-js-environment
- https://api.github.com/repos/actions/setup-node/releases/tags/v7.1.0

**actions/upload-artifact**

- https://api.github.com/repos/actions/upload-artifact/git/ref/tags/v7.0.2
- https://raw.githubusercontent.com/actions/upload-artifact/cf430e030ddbb5b0abf93d22962f4752f3646cd9/action.yml
- https://api.github.com/repos/actions/upload-artifact
- https://github.com/marketplace/actions/upload-a-build-artifact
- https://api.github.com/repos/actions/upload-artifact/releases/tags/v7.0.2

**dorny/paths-filter**

- https://api.github.com/repos/dorny/paths-filter/git/ref/tags/v4.0.3
- https://raw.githubusercontent.com/dorny/paths-filter/ceb8a2b8f2d89434be7ff52d3de7ec3738c5cc9d/action.yml
- https://api.github.com/repos/dorny/paths-filter
- https://github.com/marketplace/actions/paths-changes-filter
- https://api.github.com/repos/dorny/paths-filter/releases/tags/v4.0.3

**peter-evans/create-pull-request**

- https://api.github.com/repos/peter-evans/create-pull-request/git/ref/tags/v8.1.1
- https://raw.githubusercontent.com/peter-evans/create-pull-request/5f6978faf089d4d20b00c7766989d076bb2fc7f1/action.yml
- https://api.github.com/repos/peter-evans/create-pull-request
- https://github.com/marketplace/actions/create-pull-request
- https://api.github.com/repos/peter-evans/create-pull-request/releases/tags/v8.1.1

**googleapis/release-please-action**

- https://api.github.com/repos/googleapis/release-please-action/git/ref/tags/v5.0.0
- https://raw.githubusercontent.com/googleapis/release-please-action/45996ed1f6d02564a971a2fa1b5860e934307cf7/action.yml
- https://api.github.com/repos/googleapis/release-please-action
- https://github.com/marketplace/actions/release-please-action
- https://api.github.com/repos/googleapis/release-please-action/releases/tags/v5.0.0

**actions/download-artifact**

- https://api.github.com/repos/actions/download-artifact/git/ref/tags/v8.0.2
- https://raw.githubusercontent.com/actions/download-artifact/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml
- https://api.github.com/repos/actions/download-artifact
- https://github.com/marketplace/actions/download-a-build-artifact
- https://api.github.com/repos/actions/download-artifact/releases/tags/v8.0.2

**docker/login-action**

- https://api.github.com/repos/docker/login-action/git/ref/tags/v4.7.0
- https://raw.githubusercontent.com/docker/login-action/81c6f93d4bc991e510b342a00b419b3bb4efc5c6/action.yml
- https://api.github.com/repos/docker/login-action
- https://github.com/marketplace/actions/docker-login
- https://api.github.com/repos/docker/login-action/releases/tags/v4.7.0

**docker/setup-buildx-action**

- https://api.github.com/repos/docker/setup-buildx-action/git/ref/tags/v4.4.1
- https://raw.githubusercontent.com/docker/setup-buildx-action/f87e5991a6d7451dcb8d9637bfbc97413f497069/action.yml
- https://api.github.com/repos/docker/setup-buildx-action
- https://github.com/marketplace/actions/docker-setup-buildx
- https://api.github.com/repos/docker/setup-buildx-action/releases/tags/v4.4.1

**docker/metadata-action**

- https://api.github.com/repos/docker/metadata-action/git/ref/tags/v6.2.0
- https://raw.githubusercontent.com/docker/metadata-action/dc802804100637a589fabce1cb79ff13a1411302/action.yml
- https://api.github.com/repos/docker/metadata-action
- https://github.com/marketplace/actions/docker-metadata-action
- https://api.github.com/repos/docker/metadata-action/releases/tags/v6.2.0

**astral-sh/setup-uv**

- https://api.github.com/repos/astral-sh/setup-uv/git/ref/tags/v10.3.3
- https://raw.githubusercontent.com/astral-sh/setup-uv/68559e99cc807c1eb7e9238fd43a15bba460eec2/action.yml
- https://api.github.com/repos/astral-sh/setup-uv
- https://github.com/marketplace/actions/astral-sh-setup-uv
- https://api.github.com/repos/astral-sh/setup-uv/releases/tags/v10.3.3

### Additional primary documentation read

- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions
- https://docs.github.com/en/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/actions/reference/workflows-and-actions/expressions
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs
- https://raw.githubusercontent.com/dorny/paths-filter/ceb8a2b8f2d89434be7ff52d3de7ec3738c5cc9d/README.md
- https://raw.githubusercontent.com/actions/setup-node/949feb2413d6458794dcd2491c4babbbce0c15c1/README.md
- https://raw.githubusercontent.com/actions/cache/55cc8345863c7cc4c66a329aec7e433d2d1c52a9/README.md
- https://raw.githubusercontent.com/actions/upload-artifact/cf430e030ddbb5b0abf93d22962f4752f3646cd9/README.md
- https://raw.githubusercontent.com/actions/download-artifact/9000827ccba6bdab643e8b6fd33ac0654aef8333/README.md
- https://raw.githubusercontent.com/docker/setup-buildx-action/f87e5991a6d7451dcb8d9637bfbc97413f497069/README.md
- https://raw.githubusercontent.com/docker/metadata-action/dc802804100637a589fabce1cb79ff13a1411302/README.md
- https://raw.githubusercontent.com/docker/build-push-action/c3c9e263c25d99ce0380d002d59b67737d91b0dc/README.md
- https://raw.githubusercontent.com/docker/login-action/81c6f93d4bc991e510b342a00b419b3bb4efc5c6/README.md
- https://docs.docker.com/build/ci/github-actions/cache/
- https://docs.github.com/en/actions/concepts/security/openid-connect
- https://github.com/aws-actions/configure-aws-credentials
- https://github.com/Azure/login
- https://github.com/google-github-actions/auth
- https://raw.githubusercontent.com/googleapis/release-please-action/45996ed1f6d02564a971a2fa1b5860e934307cf7/README.md
- https://raw.githubusercontent.com/peter-evans/create-pull-request/5f6978faf089d4d20b00c7766989d076bb2fc7f1/README.md
- https://github.com/dorny/test-reporter
- https://github.com/codecov/codecov-action
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions
- https://raw.githubusercontent.com/actions/setup-node/v4.0.0/action.yml
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts

### Failed and recovered source checks

- Initial exact-pin Release Please `action.yml` retrieval hit an SSL handshake timeout. The receipt preserves the failed attempt and a successful metadata retry; the final metadata checker accepts its declared inputs.
- A first Marketplace heuristic looked for literal `Verified creator`, which missed the current `verified-owner` markup. It was not treated as proof that vendor listings were unverified. Matching badge markup plus the exact repository recovered observations. Google and Astral needed the listing embedded `externalUsesPathPrefix` because absolute-URL-only matching was inconclusive. Those methods and retries are recorded, and their latest observations are verified-creator observed.
- The guessed GitHub store/share-data URL (`https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/store-and-share-data`) was inaccessible through web fetch. It is not cited as verified support. The pinned upload/download metadata/README and official artifact-download page provide the used contract evidence instead.
- Historical setup-node `v4.0.0` metadata declares `always-auth`; the current preserved pin does not. `labs/0042/historical-input-evidence.json` saves the actual old field/runtime observation. No historical runtime was executed.

## Technical details for shared integration

- The release lesson follows current GitHub platform guidance for `GITHUB_TOKEN`-created/updated PR `opened`, `synchronize` and `reopened` events: approval-required CI runs can be created. Some upstream READMEs still summarize the older broad no-recursion rule. Do not replace the lesson with the stale blanket statement that token-created PRs can never have CI. The trigger documentation also retains dispatch exceptions and general prevention of other recursive token events.
- The exact download-artifact pin declares `digest-mismatch` and defaults it to `error`. The new exchange recipe states it explicitly. Older guidance that digest mismatch always only warns does not describe this pin.
- Paths-filter has dynamic filter-name outputs not fully enumerated in metadata. The local contract checker validates literal input names and pins, not those dynamic outputs. The independent routing consumer reads the actual two mapping expressions with supplied outputs.
- The release recipe uses `skip-github-release: true` but may still write release PRs when activated. It is not a dry run. No activation/write occurred.
- Dependabot proposal demonstrates the documented active-workflow scan scope; inactive `labs/` and `examples/` maintenance is explicitly inventoried rather than promised automatically.

## Deferred boundaries and unresolved issues

**All documentation validation is deferred to the coordinator’s ONE combined whole-site pass after all four modules and shared integration are complete.** No Markdown/link/Mermaid/Zensical validator, docs build, `task check`, or `task docs:verify` ran in this thread. Diagram counts/render success and site-build/link status are therefore **not established here**, not reported as zero-error passes.

Remote action execution, actual step→job output processing, PR changed-file API/matcher behavior, Git history edge cases, runtime acquisition, real dependency installation, hosted cache/artifact service behavior, effective GitHub authorization, fork policy, token-triggered CI/approvals, OIDC issuance/signature/provider policy, environment approval, registry access, publish/release/PR/check/coverage writes, hosted cancellation and OS parity all remain unexecuted. No cloud/API write, registry push, deployment, release, model call or credential change was made.

No authoring blocker remains. These are explicit integration limits, not failed host tests. The narrow XML reader is a synthetic fixture consumer, not a production general-purpose JUnit/security implementation. Selection record admission verifies fields/consistency and cannot establish that a claimed human code review took place.

## Optional shared changes for the coordinator

- Update catalog checkboxes/counts/notes only after all four assignments are collected, preserving 0037–0042 and 0036/0043 boundaries. Add the 37 lab files and this module to the shared lab index as appropriate.
- Add a focused Module 7 check entry using `.venv/bin/python labs/0042/run_checks.py` (without `--write-receipt` in CI), or integrate its six unittest commands plus the offline checker into `test:module7`. The runner deliberately asserts standalone negative outcomes and invokes only the explicit five-file workflow lint list; it contains no documentation task.
- If maintaining separate lint tasks, use exactly the five positive paths shown above for `lint:module7`; exclude `obsolete-input.negative.yml` and `dependabot.example.yml`. Do not glob the entire module.
- Expand the shared primary source index with current token-trigger exceptions, exact download-artifact digest behavior, PR/report/coverage references, vendor auth sources and Dependabot active-workflow scope. Keep publisher/star evidence separate and leave the historical shared snapshot untouched unless a separately authorized refresh is wanted.
- The optional module guide is already updated in its assigned file. The shared teaching prompt cleanup is coordinator-owned and was not duplicated in other authors’ pages.

Next learner-facing lesson after this module: **0043**, GitHub Agentic Workflows. Learner proficiency remains unknown.
