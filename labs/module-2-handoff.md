# Module 2 authoring handoff — 2026-10-30

**Status: all six assigned reference lessons and their isolated labs are fully developed.** Each page is `lesson_status: authored`; this records available content, not learner mastery. No learner predictions, exercises, or technical explanations were collected, and no learning record was invented.

**Documentation validation is deferred to the coordinator's combined 24-lesson pass.** No Markdown/link/Mermaid validator or Zensical build was executed in this thread. The coordinator should integrate all four modules and shared changes before running the ONE whole-site `task docs:verify`. Six vertical Mermaid diagrams were authored here; their rendering, cache statistics, and error status remain unverified. The site build is NOT RUN.

## Ownership and developed pages

Only these six assigned lesson pages, files under `labs/0007/`–`labs/0012/`, and this handoff were edited by this authoring thread. The checkout already contained unrelated uncommitted work, including shared curriculum changes, which was preserved. No commits, pushes, publishing, hosted workflow runs, model execution, new threads, or subagents were requested or performed.

| ID | Fully developed page | Distinct lab boundary |
| --- | --- | --- |
| 0007 | `docs/lessons/0007-taskfile-shared-command-contract.md` | Shared invocation, preconditions, sequential calls, stale Task cache and tracked-policy repair |
| 0008 | `docs/lessons/0008-workflow-shell-and-security-linting.md` | Expression and local metadata diagnostics, suppressed shell defect, template/source trust boundary |
| 0009 | `docs/lessons/0009-unit-tests-fixtures-and-output-files.md` | Pure function versus real process, deterministic cases/event bridge, exact output bytes, failure status |
| 0010 | `docs/lessons/0010-container-engines-images-and-architecture.md` | Read-only engine map, disposable missing socket, host versus Linux CPU, image/output-mount probe |
| 0011 | `docs/lessons/0011-act-targeted-workflow-smoke-tests.md` | Selected events/job, identical scripts with different composite output mappings, caller assertion |
| 0012 | `docs/lessons/0012-local-hosted-coverage-and-usage-budget.md` | Claim-to-layer evidence plan, false platform proof, stale revision, release gaps, declared usage cap |

All pages include prerequisite links, complete explanations, runnable commands and expected observations, a vertical `flowchart TD` diagram with quoted labels, admonitions, code annotations, predictions, collapsed worked solutions, deliberate failure/diagnosis/repair, transfer and retrieval exercises, local/hosted limits, and an exact-file future teaching prompt. Pagination follows **0006 → 0007–0012 → 0055**, preserving IDs and filenames. Neighboring pages and the catalog remain coordinator-owned.

## Lab inventory

There are 40 developed lab files, plus this handoff. Workflow files remain inactive under `labs/`.

- `labs/0007/Taskfile.yml`
- `labs/0007/check.py`
- `labs/0007/cache_demo.py`
- `labs/0007/input.json`
- `labs/0007/policy.json`
- `labs/0007/module2-command.yml`
- `labs/0008/good.yml`
- `labs/0008/bad-expression.yml`
- `labs/0008/bad-metadata.yml`
- `labs/0008/safe-template.yml`
- `labs/0008/unsafe-template.yml`
- `labs/0008/good.sh`
- `labs/0008/bad.sh`
- `labs/0008/shell_probe.py`
- `labs/0009/greet.cjs`
- `labs/0009/index.cjs`
- `labs/0009/broken.cjs`
- `labs/0009/cases.json`
- `labs/0009/greet.test.cjs`
- `labs/0009/contract.test.cjs`
- `labs/0009/dispatch.json`
- `labs/0009/event_probe.py`
- `labs/0010/environment.py`
- `labs/0010/probe.py`
- `labs/0010/socket_failure.py`
- `labs/0010/Dockerfile`
- `labs/0010/.dockerignore`
- `labs/0010/smoke.py`
- `labs/0011/action/action.yml`
- `labs/0011/action/greet.sh`
- `labs/0011/broken-action/action.yml`
- `labs/0011/broken-action/greet.sh`
- `labs/0011/smoke.yml`
- `labs/0011/broken-smoke.yml`
- `labs/0011/dispatch.json`
- `labs/0011/push.json`
- `labs/0011/direct.py`
- `labs/0012/plan.json`
- `labs/0012/coverage.py`
- `labs/0012/exercise.py`

The greeting implementation in 0009 and scripts in 0011 are isolated copies of the existing examples. All deliberate defects live inside assigned labs. The 0007 cache harness uses temporary copies and an absolute selected Taskfile; it removes its generated result and Task cache with the temporary directory. Other host exercises use temporary output files/directories. The optional image helper retains a local image tag after a future successful build; no image was built here.

## Environment observed

Inspected installed tools rather than installing dependencies:

| Observation | Actual result |
| --- | --- |
| Host | Darwin/arm64 |
| `task --version` | 3.53.1 |
| `node --version` | v24.21.0 |
| `uv --version` | 0.11.24 |
| `act --version` | 0.2.89 |
| `docker --version` | `docker version 6.0.2`; executable is the existing Podman compatibility wrapper |
| `podman --version` | 6.0.2 |
| `.tools/bin/actionlint -version` | v1.7.12, built for darwin/arm64 |
| Executable lookup for ShellCheck and zizmor | Both unavailable; neither installed or invoked |
| `DOCKER_HOST` | Unset |
| `podman machine list --format json` | Exit 0; existing `podman-machine-default`, `Running: false` |
| `docker info` | Exit 125; Podman connection to `127.0.0.1:62183` refused |
| `act --help` | Exit 0; confirmed event/file/job/fixture/platform/list/default-data-file flags used by the lesson |
| `.tools/bin/actionlint -help` | Exit 0; confirmed explicit workflow paths and optional ShellCheck integration |

The engine was not started, configured, replaced, or provisioned. No dependency installation and no `npx` invocation occurred. `uv run --no-sync` reused the existing environment.

## Exact focused checks executed and results

The following are actual executed checks, not a list of suggested future commands. Negative cases are intentional and reported separately from passing evidence.

| Exact command | Actual result |
| --- | --- |
| `task --taskfile labs/0007/Taskfile.yml check` | Exit 0; `PASS: Hello, Ada!` |
| `uv run --no-sync python labs/0007/cache_demo.py` | Final run exit 0; bad cache reused stale `!` after policy changed to `?`; independent comparison failed as intended; fixed source list rebuilt; ordered check passed; missing input failed its precondition as intended |
| `uv run --no-sync python labs/0008/shell_probe.py` | Exit 0; one literal argument, including spaces, `*`, and shell-like text |
| `uv run --no-sync python labs/0008/shell_probe.py --bad` | Expected exit 1; script itself returned 0 while stdout split into five records and expanded `*` to `visible.txt`; probe caught the transport defect |
| `node --test labs/0009/greet.test.cjs labs/0009/contract.test.cjs` | Exit 0; **16 tests passed, 0 failed**: 2 function tests and 14 process tests |
| `env LAB_ADAPTER=broken node --test labs/0009/contract.test.cjs` | Expected exit 1; **14 tests, 7 passed, 7 failed**; swallowed exceptions returned status 0 for invalid input/output failures |
| `uv run --no-sync python labs/0009/event_probe.py labs/0009/dispatch.json` | Exit 0; fixture name `Grace`; stdout `Hello, Grace!\n`; file `greeting=Hello, Grace!\n` |
| `uv run --no-sync python labs/0010/environment.py` | Exit 0 as a diagnostic report; nested machine-list exit 0, nested `docker info` exit 125; final engine state explicitly deferred |
| `uv run --no-sync python labs/0010/probe.py` | Exit 0; `{"machine": "arm64", "system": "Darwin"}`; host process only |
| `uv run --no-sync python labs/0010/socket_failure.py` | Expected exit 1; `[Errno 2] No such file or directory`; no engine API request/image/action execution |
| `uv run --no-sync python labs/0010/smoke.py` | Exit **2**, explicitly DEFERRED at engine preflight; no pull, build, or container run attempted |
| `uv run --no-sync python labs/0011/direct.py` | Exit 0; both good and broken action scripts wrote the correct output; metadata was not executed |
| `uv run --no-sync python labs/0012/coverage.py labs/0012/plan.json` | Exit 0; six honest open/simulated/deferred states; planned ceiling 5 job-minutes; plan consistency only |
| `uv run --no-sync python labs/0012/coverage.py labs/0012/plan.json --require-release` | Expected exit 1; four blockers: host and static not-run, act deferred, actual token permissions not-run |
| `uv run --no-sync python labs/0012/exercise.py` | Exit 0; honest declaration accepted; false local OIDC pass, stale revision, and declared hosted-run overrun rejected |

The passing workflow batch was executed exactly as:

```bash
.tools/bin/actionlint -no-color labs/0007/module2-command.yml labs/0008/good.yml labs/0008/safe-template.yml labs/0011/smoke.yml labs/0011/broken-smoke.yml
```

Result: **exit 0, five workflows, no diagnostics**. The broken composite mapping is intentionally not inferable from arbitrary shell output publication; this clean result is part of the lesson, not proof that the broken caller works.

The workflow-negative checks were:

```bash
.tools/bin/actionlint -no-color labs/0008/bad-expression.yml labs/0008/bad-metadata.yml
.tools/bin/actionlint -no-color labs/0008/unsafe-template.yml
```

Both commands returned **1** as intended. The first reported undefined `githb` at `11:20` and unsupported input `recipient` at `14:11`. The second reported potentially untrusted PR-title interpolation at `12:33`. The installed actionlint itself detects that template-injection pattern; ShellCheck/zizmor coverage must not be inferred from it.

An earlier exploratory invocation also combined the 0007 good workflow, 0008 good/safe workflows, and `unsafe-template.yml`; it returned 1 solely for the same unsafe-template diagnostic. The positive-only five-workflow command above establishes the passing static evidence separately.

These two exact act discovery commands were executed:

```bash
act workflow_dispatch -W labs/0011/smoke.yml -j smoke -l --container-architecture linux/amd64 --env-file /dev/null --secret-file /dev/null --var-file /dev/null --input-file /dev/null
act push -W labs/0011/smoke.yml -j smoke -l --container-architecture linux/amd64 --env-file /dev/null --secret-file /dev/null --var-file /dev/null --input-file /dev/null
```

Both returned **0** and listed the single `smoke` job. Both also warned: `Couldn't get a valid docker connection: no DOCKER_HOST and an invalid container socket ''`. Listing is not execution. No good/broken dispatch or push workflow step was run under act.

### Implementation correction during the checks

The initial `cache_demo.py` run returned 1 because it combined `--dir <temporary-directory>` with the relative `--taskfile Taskfile.yml`. Task resolved the repository Taskfile and attempted its root `check`; that attempt stopped at the `lint:workflows` missing-tool precondition before any documentation operation. The harness was corrected to select the temporary Taskfile by **absolute path**, then rerun successfully. No Markdown/link/Mermaid validator or Zensical build ran. The final harness and all lesson commands explicitly select the lab Taskfile to avoid this ambiguity.

## Deferred and intentionally excluded checks

- **Documentation:** no `task docs:verify`, `docs:check`, `docs:diagrams`, `docs:build`, direct Markdown/link/Mermaid checker, or Zensical build was run. The coordinator owns the one combined 24-lesson validation pass. No render/cache success or zero-error count is claimed.
- **Containers:** image build, Linux entrypoint/CPU, and mounted output assertions remain deferred because the existing Podman VM is stopped and its connection is refused. The helper's preflight result is evidence only of that boundary.
- **Act runtime:** the good/broken mapping executions and push/dispatch assertions remain deferred. Only job listing, direct scripts, and static caller checks have actual results.
- **Optional analyzers:** ShellCheck and zizmor are absent. Their current primary documentation was checked, and optional installed-tool commands are supplied; no analyzer success is claimed.
- **Hosted platform:** token enforcement, OIDC federation, environments, concurrency/cancellation, hosted artifacts/caches, and intended OS matrices were not exercised. No workflow was installed or dispatched.
- **Agentic execution:** neither compilation nor `gh aw trial`/`run` was executed. Lessons distinguish later local specification validation from hosted runner/model use. This authoring task used zero hosted workflow runs and zero model calls.
- **Shared suites:** no broad `task test` or `task lint:workflows` was needed beyond the focused tests and explicit consumers. The accidental root Task selection above never advanced beyond its first lint precondition. No shared executable implementation was changed.

## Primary sources checked on 2026-10-30

Started from `docs/references/resources.md`, then followed current primary subpages. Installed help and executed reproductions were used to confirm supported syntax in the actual local versions. The latest web Task/Node pages may describe newer releases; examples use the supported subset observed on Task 3.53.1 and Node 24.21.0.

| Checked URL | Fact used |
| --- | --- |
| https://taskfile.dev/docs/guide/ | Current guide organization and shared command features |
| https://taskfile.dev/docs/guide/dependencies | Concurrent dependencies versus sequential task calls |
| https://taskfile.dev/docs/guide/conditional-execution | Failed preconditions and the fact dependencies precede that task's preconditions |
| https://taskfile.dev/docs/guide/up-to-date | Source fingerprints, generated files, configuration inputs, and stale-result reasoning |
| https://github.com/rhysd/actionlint/blob/main/docs/checks.md | Workflow expressions, known local interfaces, and untrusted interpolation checks |
| https://github.com/rhysd/actionlint/blob/main/docs/usage.md | Explicit workflow file selection and optional shell integration |
| https://www.shellcheck.net/wiki/SC2086 | Word splitting and glob expansion on unquoted values |
| https://docs.zizmor.sh/audits/#template-injection | Workflow source/data trust boundary and env-based repair |
| https://docs.zizmor.sh/usage/ | Offline analysis mode and coverage limits |
| https://docs.github.com/en/actions/reference/security/secure-use | Untrusted event data and safe transport into shell commands |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands | Environment/output-file protocol and single-line versus multiline results |
| https://nodejs.org/api/test.html | Current generic Node test docs inspected before selecting the supported major |
| https://nodejs.org/docs/latest-v24.x/api/test.html | Node 24 built-in test runner used by this workspace |
| https://nektosact.com/usage/index.html | Event, workflow, job, payload, and configuration selection |
| https://nektosact.com/usage/runners.html | Explicit runner-image mapping and incomplete hosted-image parity |
| https://nektosact.com/usage/custom_engine.html | Docker-compatible API and `DOCKER_HOST` selection |
| https://nektosact.com/not_supported.html | Ignored permissions/environment/concurrency/timeout behavior and OIDC limitations |
| https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax | Composite public-output expression mapping |
| https://docs.github.com/en/actions/tutorials/use-containerized-services/create-a-docker-container-action | Docker action packaging, Linux requirement, and image/entrypoint boundaries |
| https://github.com/docker-library/official-images/blob/master/library/python | Current `3.14-slim` tag and listed amd64/arm64 variants; no local pull/build claim |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | Actual hosted job timeout declaration |
| https://docs.github.com/en/actions/concepts/billing-and-usage | Usage depends on actual runner/account policy; no guessed rates |
| https://github.github.com/gh-aw/setup/cli/ | Specification compilation versus hosted trial/run distinction |

A supplementary attempt to open `https://nektosact.com/not_supported/docker_context.html` returned a web-tool access error. No lesson claim depends on that failed lookup; the successfully checked custom-engine and unsupported-functionality pages supply the needed limits.

## Coordinator integration proposals — not applied here

1. Mark Module 2 IDs 0007–0012 as authored in the shared catalog and recompute combined counts with the other module handoffs. Preserve 0006 → 0007–0012 → 0055 navigation. Update shared NOTES without implying learner mastery.
2. No shared Taskfile change is required to use the explicit lab commands. If named integration is wanted, add `test:module2` for the cache harness, good shell probe, combined 16 Node tests, event bridge, direct composite scripts, and evidence exercise. Add `lint:module2` using the exact positive-only five-workflow command above. Do **not** glob every lab YAML: expected-negative diagnostic fixtures intentionally fail. Keep image/act checks optional and engine-gated.
3. If future CI should exercise labs, include `labs/**` in the relevant shared workflow path filters and invoke the selected lab contracts. Do not copy the unsafe or deliberately broken recipes into active workflows. No `.github/` edits were made here.
4. The curated source index already has the main tool/GitHub sources. Optional additions are Task's current split subpages, SC2086, zizmor audit/usage pages, the Node 24-specific test reference, Python's official-image manifest, and GitHub billing/usage. The URLs and check date above are ready for the coordinator's source-index update.
5. Keep root `task check` out of parallel authoring steps because it includes docs validation. Run the ONE `task docs:verify` only after every module and shared edit is integrated. Container/act deferral must remain visible even if the documentation pass succeeds.

## Unresolved issues and next session

No authoring blocker remains. Outstanding verification boundaries are the stopped engine, absent optional analyzers, unexecuted platform/model paths, and coordinator-owned documentation validation. The teaching audit intentionally does not authenticate evidence references, prevent dispatches, enforce monetary limits, or implement a generic deployment gate; its limits are explained in lesson 0012. Its sample release flag covers local-candidate/platform-release scopes, leaving deployment scopes explicit.

Continue in catalog order to **0055**, `docs/lessons/0055-reuse-compose-or-create-an-action.md`, for Module 3. A live session can begin earlier if the learner's predictions reveal prerequisite gaps. Persist only actual learner evidence when that session occurs.
