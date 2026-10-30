# Module 6 authoring handoff

Date: **2026-10-30**. Assignment: **Module 6, canonical IDs 0031–0036**. All six existing pages are fully developed in place with `lesson_status: authored`. The six pages include prerequisites/observable goals, explained Actions examples, vertical `flowchart TD` diagrams, code annotations/admonitions, predictions and collapsed worked solutions, runnable isolated labs, deliberate failures/repairs, transfer/retrieval exercises, verification limits, dated primary references, and Previous/All/Next navigation. Boundary pagination remains **0030 → 0031–0036 → 0037**.

The user's later requirement supersedes the original lesson-prompt instructions: these completed pages contain no lesson-creation/thread prompts, `/teach` blocks, or coordinator/authoring handoff directions. Authoring evidence is stored here. Written availability and assistant-run checks establish **no learner mastery**; no learner predictions, code, or retrieval answers were received.

## Ownership and inventory

Only the six assigned lesson files, `labs/0031/`–`labs/0036/`, and this handoff were edited. No shared notes/catalog/index, guide, Taskfile, workflow registration, dependency manifest/lock, validator, shared example, or other module was edited. No commits, pushes, publication, hosted runs, releases, deployments, credentials, cloud setup, model calls, new threads, or subagents were used.

| Lesson page | Developed lab and purpose |
| --- | --- |
| `docs/lessons/0031-github-token-forks-and-trust-boundaries.md` | `labs/0031/`: declared authority inventory, fork/code provenance decisions, precise-scope diagnosis |
| `docs/lessons/0032-script-injection-artifacts-and-privileged-events.md` | `labs/0032/`: fixed shell injection marker versus safe data transport; bounded data-only ZIP and producer fixtures |
| `docs/lessons/0033-oidc-environments-and-hosted-policy.md` | `labs/0033/`: synthetic ID-bearing claim matching, separate approval input, accepted/rejected contexts |
| `docs/lessons/0034-caches-artifacts-and-reproducibility.md` | `labs/0034/`: broken/fixed cache keys, repeatable bytes, manifest/producer/revision/expiry checks and unsigned-checksum limitation |
| `docs/lessons/0035-sha-pins-semantic-releases-and-provenance.md` | `labs/0035/`: TypeScript source, shipping CJS, non-repairing comparison, real process consumer, synthetic refs and temporary stale candidate |
| `docs/lessons/0036-observability-concurrency-and-usage-budgets.md` | `labs/0036/`: allowlisted ledger report, annotation escaping, summary adapter, budgets, local partial-operation reconciliation |

Complete lab file inventory: **26 files**, plus this handoff.

```text
labs/0031/jobs.json
labs/0031/policy.py
labs/0031/read-only-pr.yml
labs/0031/test_policy.py
labs/0032/boundaries.py
labs/0032/data-only-pr.yml
labs/0032/test_boundaries.py
labs/0033/claims.json
labs/0033/policy-shape.yml
labs/0033/test_trust.py
labs/0033/trust.py
labs/0034/local-reuse.yml
labs/0034/reuse.py
labs/0034/test_reuse.py
labs/0035/action.yml
labs/0035/build.cjs
labs/0035/candidate-consumer.yml
labs/0035/dist/index.cjs
labs/0035/release_demo.py
labs/0035/src/index.ts
labs/0035/test_release.py
labs/0035/tsconfig.json
labs/0036/ledger.json
labs/0036/observable-check.yml
labs/0036/operations.py
labs/0036/test_operations.py
```

All six workflow recipes remain inactive under `labs/`. `policy-shape.yml` declares an OIDC permission/environment as a design specimen but contains no token request, login, or deployment step. Other recipes perform read-only/local behavior. No negative YAML fixtures exist in this module; negative behavior is exercised through synthetic inputs and temporary copies.

## Environment and tools actually inspected

Commands run included `python3 --version`, `node --version`, `.tools/bin/actionlint -version`, `.tools/bin/actionlint -help`, `act --version`, `docker info`, and installed-tool discovery with `command -v` / Python `shutil.which`.

- Host: macOS/darwin ARM64.
- Python **3.14.5**; Node **24.21.0**.
- Existing installed TypeScript **7.0.2**, esbuild **0.28.2**, read with `node -p 'JSON.stringify({typescript:require("typescript/package.json").version,esbuild:require("esbuild/package.json").version})'`.
- actionlint **1.7.12**, local `.tools/bin/actionlint`; help confirmed explicit file arguments.
- act **0.2.89**, `/opt/homebrew/bin/act`; version only, no workflow listing/execution.
- Bash `/opt/homebrew/bin/bash`; the injection experiment runs this installed interpreter with only a basic PATH and synthetic TITLE in its subprocess environment.
- Docker-compatible command `/Users/rohitkharche/.local/bin/docker` reports Podman **6.0.2**. Standalone `docker info` returned **125**: `unable to connect to Podman socket ... dial tcp 127.0.0.1:62183: connect: connection refused`. An earlier combined discovery command exposed the same failure. No VM/daemon was started and no container/act execution attempted.
- ShellCheck and zizmor: **not installed/on PATH**. Their optional analysis was not run or installed. Passing actionlint does not imply either ran.
- No dependency installs, `npx`, credential inspection, identity minting, infrastructure provisioning, or secret values were required.

## Focused executed checks and actual results

All commands below start at the repository root. No command in this section invokes documentation validation.

### Host suites

```bash
python3 -B -m unittest discover -s labs/0031 -p 'test_*.py' -v
python3 -B -m unittest discover -s labs/0032 -p 'test_*.py' -v
python3 -B -m unittest discover -s labs/0033 -p 'test_*.py' -v
python3 -B -m unittest discover -s labs/0034 -p 'test_*.py' -v
python3 -B -m unittest discover -s labs/0035 -p 'test_*.py' -v
python3 -B -m unittest discover -s labs/0036 -p 'test_*.py' -v
```

All exited **0**: respectively **9, 7, 7, 4, 4, 7** methods, **38 total**. There are additional subcases for identity fields, paths/schemas, every cache input, manifest failure modes, and each budget/result axis; 38 is the test-method count rather than an inflated assertion count. Expected exceptions and inner failed comparisons are asserted by passing suites.

```bash
node labs/0035/build.cjs
node labs/0035/build.cjs --check
node node_modules/typescript/bin/tsc --project labs/0035/tsconfig.json
```

The initial build generated only the owned `dist/index.cjs`. Final distribution comparison prints `PASS: distribution matches current source and builder`, exit **0**; final TypeScript check exits **0** with no diagnostics. After adding the local TypeScript configuration and copying it into temporary candidates, the 0035 suite, comparison, and type check were rerun and passed. These are the final configured-state results.

The real consumer processes run the shipping CJS from an unrelated temporary working directory, with explicit synthetic inputs/output path and no inherited credential environment. Valid input returns `greeting=Hello, Ada!`; invalid newline input exits **1** and publishes no success output.

### Six positive workflow recipes

Executed as one explicit-file command after the YAML repair:

```bash
.tools/bin/actionlint labs/0031/read-only-pr.yml labs/0032/data-only-pr.yml labs/0033/policy-shape.yml labs/0034/local-reuse.yml labs/0035/candidate-consumer.yml labs/0036/observable-check.yml
```

Final result: **exit 0, no diagnostics**. Local action metadata is available for the 0035 consumer. This is static syntax/expression/interface evidence only; it does not establish runner output mapping, permissions, identity issuance, environment enforcement, cancellation, hosted services, or OS parity.

### CLI examples and expected negative exits

The following exact command argument vectors were executed by a bounded Python subprocess harness (`capture_output=True`, 30-second per-child timeout), checking each exit against the declared expectation. This covers **17 CLI examples**, **nine expected nonzero denials** and eight successful decisions/demos.

| Actually executed command | Exit | Observed result |
| --- | --- | --- |
| `python3 -B labs/0031/policy.py fork-read` | 0 | Supplied job meets teaching policy |
| `python3 -B labs/0031/policy.py fork-write` | 1 | Untrusted code receives authority |
| `python3 -B labs/0031/policy.py target-head` | 1 | Privileged event does not trust fork head |
| `python3 -B labs/0031/policy.py trusted-comment` | 0 | Reviewed synthetic reporter meets minimal scope rule |
| `python3 -B labs/0031/policy.py missing-scope` | 1 | Missing `issues:write`; unrelated `contents:read` exceeds operation contract |
| `python3 -B labs/0033/trust.py allowed` | 0 | Synthetic claim selection and approval match |
| `python3 -B labs/0033/trust.py wrong-audience` | 1 | `claim aud mismatch` |
| `python3 -B labs/0033/trust.py fork` | 1 | Subject/repository-ID mismatches |
| `python3 -B labs/0033/trust.py expired` | 1 | Outside fictional validity window |
| `python3 -B labs/0033/trust.py unapproved` | 1 | Approval not observed in simulation |
| `python3 -B labs/0036/operations.py pass` | 0 | Fictional run 360, 75 runner seconds, 3072 bytes, zero calls |
| `python3 -B labs/0036/operations.py over-budget` | 1 | 130 seconds; blocked, escaped fixed-title error annotation |
| `python3 -B labs/0036/operations.py failed-worker` | 1 | Required windows failure blocks evidence |
| `python3 -B labs/0036/operations.py recovery` | 0 | Missing receipt observed, repeated matching reconciliation, temporary journal removed |
| `python3 -B labs/0032/boundaries.py` | 0 | Unsafe marker created; safe data preserved with marker absent; accepted 3/3 data report |
| `python3 -B labs/0034/reuse.py` | 0 | Stale broken key, fixed miss, tamper/wrong producer/expiry rejected, unsigned forgery limitation demonstrated |
| `python3 -B labs/0035/release_demo.py` | 0 | Synthetic alias movement; inner stale comparison 1; old executable observed; explicit repair and new executable observed |

The final 0035 suite reran its same temporary drift/repair demo after configuration copying was added, with the same expected output. Source/dist in the maintained candidate remain unchanged by the demo. All-`a`/all-`b` commit labels and integer run IDs are fictional.

A separate bounded process adapter used a `TemporaryDirectory`, supplied its file as `GITHUB_STEP_SUMMARY`, launched `python3 -B labs/0036/operations.py pass`, and asserted exit **0**, exact stdout/file equality, and absence of `SYNTHETIC-SECRET` from output. It printed `summary process adapter: stdout equals appended file; private fixture field absent`. The file was deleted with the directory. The page's `mktemp`/`cat`/`rm` snippet documents the equivalent learner path; that exact shell snippet was not separately run.

### Unexpected failures found and repaired

1. The first six-file actionlint invocation exited **1** because a YAML plain scalar contained `Policy step outcome: %s` at `labs/0036/observable-check.yml:25`. Converted that `run` value to a block scalar; the full six-file invocation then passed. No negative fixture was accidentally included.
2. The initial command `node node_modules/typescript/bin/tsc --noEmit --strict --target es2022 --module commonjs --types node labs/0035/src/index.ts` exited **1**, TS5112, because the installed TypeScript sees a root config while explicit files are supplied. Read installed help with `node node_modules/typescript/bin/tsc --help --all | rg -A 3 'ignoreConfig|--project'`. Added the owned `labs/0035/tsconfig.json` and changed the page to the successful explicit `--project` command. No root configuration was altered.

No unresolved executable failure remains. Expected denied policies, rejected artifact inputs, and the inner stale-bundle failure remain deliberate examples.

## Verified primary sources

All URLs below were opened/read through the web tool on **2026-10-30**, using the curated library and linked official material. No failed primary fetch remained. Installed help/version and focused execution supplied the tool-specific evidence above. These are dated source observations; future lessons should recheck evolving platform/tool features.

| Verified URL | Use in Module 6 |
| --- | --- |
| https://docs.github.com/en/actions/reference/security/secure-use | Token exposure, input transport, untrusted execution, current action dependency locking guidance |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | Requested permissions, omitted scopes, effective fork calculation and settings exception |
| https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows | Fork admission; current default-branch target-event context; workflow_run authority/conclusion |
| https://docs.github.com/en/actions/concepts/security/openid-connect | Issuer/provider/resource identity chain |
| https://docs.github.com/en/actions/reference/security/oidc | Current immutable ID-bearing subject format, legacy behavior, claims and request permission |
| https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments | Environment rules/configuration and plan/visibility boundaries |
| https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching | Reuse versus produced results and trust concerns |
| https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | Exact/prefix keys, cache scope, current cache-mode and low-trust restrictions |
| https://github.com/actions/cache | Maintained cache action interface |
| https://github.com/actions/upload-artifact | IDs/digests, missing-file and retention inputs, replacement identity |
| https://github.com/actions/download-artifact | Artifact ID/run/repository/destination and current version-specific digest policy |
| https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles | Current generated actions.lock model, transitive action coverage and reusable-call exclusion |
| https://docs.github.com/en/actions/how-tos/create-and-publish-actions/release-and-maintain-actions | Shipped executable files and action release maintenance |
| https://docs.github.com/en/actions/how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases | Immutable release-linked references and separate moving aliases |
| https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | Authenticated build provenance and consumer policy boundary |
| https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline | Bundles and trusted roots required by offline attestation verification |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands | Annotation data, summaries, file channels |
| https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency | Current default single pending and optional queue max semantics |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation | Condition reevaluation, process termination and recovery limits |
| https://esbuild.github.io/api/ | Installed builder options and in-memory comparison |
| https://esbuild.github.io/content-types/#typescript | Transpilation versus semantic type checking |
| https://nektosact.com/not_supported.html | Permissions/OIDC/environment/concurrency/summary/cancellation limits |
| https://github.com/rhysd/actionlint/blob/main/docs/usage.md | Explicit-file static checks and optional analyzers |

No new remote action pin was invented or independently audited. Recipes reuse the existing course checkout pin `3d3c42e5aac5ba805825da76410c181273ba90b1`; all new action behavior is local under the assigned labs. Current `actions/cache`/artifact interfaces are explanatory references, not newly installed or hosted-executed action dependencies. `gh actions-lock` was neither installed nor executed.

## Deferred boundaries and unresolved questions

- **All documentation validation is deferred to the coordinator's ONE combined whole-site pass after all four modules and shared integration are complete.** This thread ran no Markdown, local-link, Mermaid, or Zensical validator/build, per lesson or at module completion, and no root `task check`/`task docs:verify`. Mermaid checked/rendered/cache counts and Zensical success are **not available**, not a claimed zero-error result.
- Real GitHub event admission, fork settings, credential withholding/downgrades, effective API permissions, caller/callee propagation, self-hosted isolation, and runner output mapping remain unverified.
- OIDC fixtures are claim-selection tests, not a JWT verifier. Issuer keys/signatures, actual subject configuration, environment approvals/protection rules, provider claim mapping, cloud-role/resource policy, accepted/denied federation, and credential lifetime remain unverified. No real token/credential was read, printed, or minted.
- Actual hosted cache tokens/scopes/modes, cache poisoning defenses, artifact upload/download/retention/service digest behavior, signed provenance, dependency lockfile enforcement, and real release protections remain unobserved. Matching unsigned fixture metadata does not authenticate a producer.
- Container/image and act execution remain unavailable because the existing Podman socket refuses connection. No engine, OS matrix, service, runner cancellation, annotation rendering, or summary-rendering success is claimed from host tests/lint.
- The ledger's Linux/Windows names, durations, byte counts, and budgets are synthetic. Actual runner billing/storage/model usage and monetary pricing were not measured or asserted. Hosted/model usage from this task: zero.
- The recovery journal models partial work using temporary files. It does not reproduce distributed locking, actual service writes, process signal escalation, or GitHub cancellation.
- No technical learner proficiency is known; future teaching should collect actual reasoning and results. No learning record was fabricated.
- Authoring blockers: **none**. Deferred engine/platform evidence is intentional and does not block reference availability. Documentation validation remains pending by explicit instruction.

## Optional coordinator-owned integration proposals

1. Add `test:module6` invoking the six explicit unittest discovery commands above, plus `node node_modules/typescript/bin/tsc --project labs/0035/tsconfig.json` and `node labs/0035/build.cjs --check`. Keep build repair separate from a check task. These use existing installed dependencies and no daemon.
2. Add `lint:module6` containing exactly the six positive workflow paths above; keep `action.yml` out of the workflow-file argument list. Add both to aggregate lab commands if desired. No root commands were edited here.
3. Add the official OIDC reference, environment configuration, dependency caching reference, workflow dependency lockfile, and artifact-attestation URLs to the shared source index with the dated observations above.
4. During shared consistency review, reconcile older categorical SHA-pin advice with the current lockfile option, older assumed OIDC name-only subjects with actual subject configuration, and older concurrency prose with the optional larger queue. The new pages explain these boundaries; no existing page outside 0031–0036 was changed here.
5. Update Module 6 catalog checkboxes and overall counts only when all four assigned modules are complete, then run the single combined `task docs:verify`. Retain six capstone placeholders and no mastery claim. No count/catalog update was performed by this thread.

Next curriculum boundary: **0037**, `docs/lessons/0037-selecting-popular-prebuilt-actions.md`. Authoring completion will be sent to the coordinator after this final file edit; no further edits follow that notification.
