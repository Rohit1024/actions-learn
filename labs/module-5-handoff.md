# Module 5 authoring handoff — 2026-10-30

Module 5 is complete at the canonical IDs **0025–0030**. Six existing lesson pages were expanded in place and marked `lesson_status: authored` after their explanations and runnable labs were developed. The boundary pagination remains **0024 → 0025–0030 → 0031**. This is written reference availability and assistant verification, not learner mastery; no learner exercise evidence or new learning record is claimed.

The later explicit user requirement was followed: all six authored pages omit lesson-creation instructions, `/teach` blocks, new-thread prompts, and coordinator/authoring handoff directions. Learner prerequisites, predictions, collapsed worked solutions, failure/repair exercises, retrieval, technical verification limits, and Previous Lesson / All Lessons / Next Lesson navigation remain.

**All documentation validation is deferred to the coordinator's ONE combined whole-site `task docs:verify` after all four modules (24 new lessons) and shared integration are complete.** No Markdown checker, link checker, Mermaid renderer, Zensical build, `task docs:verify`, or root `task check` was run in this thread. The six lesson diagrams have not been rendered here; no zero-error documentation claim is made.

## Ownership and complete inventory

Only these six lesson pages, the 42 listed lab files, and this handoff were created/edited by this thread. Shared files, dependencies, existing examples, active workflows, other module files, and unrelated concurrent changes were not edited. No commit, push, release, publication, new thread, subagent, credential change, dependency installation, infrastructure start, or hosted execution occurred.

| Canonical page | Developed content |
| --- | --- |
| `docs/lessons/0025-composite-action-inputs-and-outputs.md` | Public versus private names, explicit input transport, output-file process contract, ID-refactoring diagnosis |
| `docs/lessons/0026-composite-shells-paths-and-portability.md` | Bash/tool requirements, action/workspace/cwd ownership, paths with spaces, real argument observation, OS limits |
| `docs/lessons/0027-untrusted-input-and-shell-quoting.md` | Source versus data, bounded marker demonstration, env/quoted argv, JSON output encoding, exact recovery |
| `docs/lessons/0028-composite-script-tests-and-workflow-wiring.md` | Complementary process/static/caller checks, identical scripts behind an empty public mapping, selected act scope |
| `docs/lessons/0029-reusable-workflows-and-permission-interfaces.md` | Typed inputs/domain bounds, explicit fixture-secret mapping, token ceiling, full output chain, static negative cases and gap |
| `docs/lessons/0030-compose-step-and-job-orchestration.md` | Setup composite, explicit build/test commands, reusable workers, unique artifacts, fan-out/fan-in, required evidence gate |

Complete lab inventory, relative to the repository root:

```text
labs/0025/action/action.yml
labs/0025/action/report.sh
labs/0025/consumer.yml
labs/0025/test_contract.py

labs/0026/action/action.yml
labs/0026/action/inspect.sh
labs/0026/action/inspect.cjs
labs/0026/fixtures/input with spaces.txt
labs/0026/consumer.yml
labs/0026/paths.py

labs/0027/action/action.yml
labs/0027/action/accept.sh
labs/0027/action/accept.cjs
labs/0027/consumer.yml
labs/0027/transport.py

labs/0028/action/action.yml
labs/0028/action/report.sh
labs/0028/broken-action/action.yml
labs/0028/broken-action/report.sh
labs/0028/smoke.yml
labs/0028/broken-smoke.yml
labs/0028/direct.py

labs/0029/fixtures/checks.json
labs/0029/worker.cjs
labs/0029/worker.test.cjs
labs/0029/module5-reusable.yml
labs/0029/module5-caller.yml
labs/0029/lint_module.py
labs/0029/negative/missing-label.yml
labs/0029/negative/missing-secret.yml
labs/0029/negative/wrong-boolean.yml
labs/0029/negative/wrong-number.yml

labs/0030/setup/action.yml
labs/0030/domain.cjs
labs/0030/domain.test.cjs
labs/0030/build.cjs
labs/0030/emit.cjs
labs/0030/gate.cjs
labs/0030/gate.test.cjs
labs/0030/exercise.py
labs/0030/module5-worker.yml
labs/0030/module5-orchestrator.yml

labs/module-5-handoff.md
```

All reusable caller/callee YAML is isolated under owned labs. `lint_module.py` explicitly stages nine recipes into a disposable repository, preserving exact reusable-workflow basenames and symlinking only labs 0025–0030 for local action lookup. It calls actionlint with an explicit file list. Its temporary `.github/workflows/` never belongs to this checkout, and no active workflow was registered.

## Installed environment actually inspected

Executed `node --version`, `.venv/bin/python --version`, `.tools/bin/actionlint -version`, `.tools/bin/actionlint -help`, `act --version`, `act --help`, `uname -sm`, and `bash --version | head -n 1`:

- Host: Darwin arm64.
- Node: v24.21.0; installed Python: 3.14.6.
- actionlint: v1.7.12, built with go1.26.10 for darwin/arm64.
- act: 0.2.89; confirmed selection, empty data-file, image and architecture flags from actual help.
- Bash: GNU 5.3.20(1)-release.
- `command -v docker podman bash shellcheck` located the first three and returned 1 because ShellCheck was absent. No ShellCheck installation or standalone analysis occurred. Actionlint's clean result must not be represented as a ShellCheck pass.

Executed `docker info` separately: **exit 125**, Podman 6.0.2 on darwin/arm64 reported `dial tcp 127.0.0.1:62183: connect: connection refused`. Executed `podman machine list`: existing `podman-machine-default`, applehv, last up two weeks earlier. No machine was started or provisioned. Engine-backed act execution remains unavailable.

## Focused checks actually executed

Commands below were run from the repository root. Several were batched with `&&`; these are the exact individual subcommands, with independent results retained. No command in this section runs documentation validation.

```bash
.venv/bin/python labs/0025/test_contract.py
.venv/bin/python labs/0026/paths.py
.venv/bin/python labs/0027/transport.py
.venv/bin/python labs/0028/direct.py
node --test labs/0029/worker.test.cjs labs/0030/domain.test.cjs labs/0030/gate.test.cjs
.venv/bin/python labs/0030/exercise.py
```

Results:

- 0025: **3 unittest methods pass** (five valid-name cases, six invalid-name cases, missing-output-path case). Real Bash status, stdout/stderr, preserved prior output records, Unicode/literal command-shaped input, and output paths with spaces are checked.
- 0026: harness exit **0**; relative script lookup and unquoted action-root lookup fail as expected; repaired invocation receives one exact caller-owned path and writes `lines=2`. Action root, workspace and unrelated cwd are separate temporary directories with spaces.
- 0027: harness exit **0**; the one fixed generated-source payload creates `marker.txt` inside its temporary cwd; the harness verifies its bytes then deletes it. Four repaired env/quoted-argv cases exactly round-trip through JSON with marker absent; three invalid labels fail without corrupting prior output. No arbitrary input reaches the unsafe demonstration.
- 0028: both actual report scripts pass direct invocation. Output explicitly states public mapping was **NOT executed**. This is intentional evidence that adapter checks miss the metadata defect.
- Combined Node command: **12 tests pass**, zero failures/skips: three typed-worker tests, two domain tests, seven gate-policy tests. Variants include invalid boolean transport, numeric/type/bounds errors, missing fixture token, strict failures, unsuccessful worker statuses, absent/stale/extra/malformed/wrong-schema/wrong-kind/false evidence.
- Default 0030 harness: exit **0**, both statuses success, readiness log and `ready=true` output, exact synthetic bundle bytes, plan-only log. It runs actual project processes sequentially and uses temporary directories, rather than emulating GitHub parallel scheduling or artifact services.

Executed expected-blocked scenarios through this exact asserting wrapper:

```python
import subprocess
for case in ['fail-test', 'missing-test', 'skipped-test', 'stale-test']:
    result = subprocess.run(['.venv/bin/python', 'labs/0030/exercise.py', '--case', case], text=True, capture_output=True, timeout=20)
    print(f'{case}: exit={result.returncode}')
    print(result.stdout, end='')
    assert result.returncode == 1 and 'BLOCKED:' in result.stdout, result.stderr
```

The wrapper exited **0**. Each child exited **1**, published no readiness, and reported respectively:

```text
fail-test: test result must be success (got failure)
missing-test: test evidence must contain exactly test.json
skipped-test: test result must be success (got skipped)
stale-test: test evidence does not match required candidate/schema/pass
```

`fail-test` intentionally fails evidence emission after a passing domain command; it is a required-branch failure experiment, not a claim that the domain tests failed. The positive harness rerun recreates fresh matching evidence; negative outputs are not silently accepted as positive tests.

Executed static checks:

```bash
.tools/bin/actionlint -no-color labs/0025/consumer.yml labs/0026/consumer.yml labs/0027/consumer.yml labs/0028/smoke.yml labs/0028/broken-smoke.yml
.venv/bin/python labs/0029/lint_module.py
.venv/bin/python labs/0029/lint_module.py --negative missing-label
.venv/bin/python labs/0029/lint_module.py --negative missing-secret
.venv/bin/python labs/0029/lint_module.py --negative wrong-boolean
.venv/bin/python labs/0029/lint_module.py --negative wrong-number
```

- The explicit five-file lint command: exit **0**, no diagnostics.
- Positive staging helper: exit **0**, nine explicit recipes pass, including both real local reusable caller/callee pairs. Syntactically valid `broken-smoke.yml` stays in this list on purpose: only the caller's runtime assertion detects the empty output.
- Missing label and missing secret: underlying actionlint exits **1** with required-field diagnostics; wrappers exit **0** after asserting those expected failures.
- Wrong number `two`: underlying actionlint exits **1** with a number-assignment diagnostic; wrapper exits **0**.
- Wrong boolean text: underlying actionlint **1.7.12 exits 0**. Wrapper prints `STATIC GAP` and exits **0** only after confirming this observed limitation. The independent worker process rejects invalid `STRICT` text. This is not claimed as hosted acceptance; documented reusable input typing still applies.
- Negative interface fixtures are never globbed into the positive lint command.

Executed syntax checks:

```bash
bash -n labs/0025/action/report.sh labs/0026/action/inspect.sh labs/0027/action/accept.sh labs/0028/action/report.sh labs/0028/broken-action/report.sh
```

Exit **0** for all five scripts. Executed this Python source compilation (no `.pyc` writes):

```python
from pathlib import Path
for number in range(25, 31):
    for file in sorted((Path('labs') / f'{number:04}').rglob('*.py')):
        compile(file.read_text(), str(file), 'exec')
        print(f'Python source compiled: {file}')
```

All **six Python sources compiled**. This checks executable source syntax and is not a Markdown/documentation check.

Also executed a temporary Python process probe that launched these exact child argv arrays with isolated output files and five-second timeouts:

- `['bash', 'labs/0025/action/report.sh']` with `REPORT_NAME=Ada`: exit 0, stdout `report rendered`, exact summary record.
- Same argv with `REPORT_NAME` containing actual LF followed by `ready=true`: exit 1, single-line diagnostic, empty output file.
- `['node', 'labs/0029/worker.cjs']` with `LABEL=preview`, `STRICT=true`, `MAX_ITEMS=2`, the fixture constant and output path: exit 0, exact `checked:2:strict` stdout/summary record.
- Same worker with `MAX_ITEMS=1`: exit 1, fixture-bound diagnostic, empty output file.

Executed act selection only:

```bash
act workflow_dispatch -W labs/0028/smoke.yml -j smoke -l --container-architecture linux/amd64 --env-file /dev/null --secret-file /dev/null --var-file /dev/null --input-file /dev/null
```

Exit **0** after completion. It lists one `smoke` job for `Module 5 public report smoke` and warns that no valid Docker connection exists. **No steps, action metadata, or container were executed.** The good and broken runtime smoke commands in lesson 0028 are instructions with expected results, not successful author executions.

## Failures encountered and resolved, versus retained gaps

The first positive staging lint failed on two real draft errors: unquoted YAML scalar text containing `PLAN ONLY:` and `runner.temp` used in a job-level env mapping. Fixed the plan command to a block scalar and moved `runner.temp` references to step environment mappings. Positive nine-file lint passed afterward.

The initial boolean-negative wrapper expected a static rejection and itself exited 1 because actionlint accepted the value. A second expression-text variant was also accepted. The final fixture uses literal `not-a-boolean`; the helper and lesson explicitly record this pinned-tool gap instead of weakening the boolean domain contract or pretending hosted execution succeeded. Missing-field and wrong-number rejection behavior remains intact.

Unresolved implementation blockers: **none**. Deferred execution and documentation boundaries below remain explicit limitations, not green checks.

## Primary sources verified on 2026-10-30

Started from `docs/references/resources.md` and linked official/maintainer material. These URLs returned readable primary content through the web tool; pin metadata was checked rather than copying only version comments from historical notes:

- [Composite action tutorial](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action) — step reuse, explicit input mapping and action path.
- [Action metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax) — composite input environment exception, explicit shell, output `value`, input validation caveat.
- [Workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands) — environment/output files and single-line/multiline boundary.
- [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) — private/caller scopes, workspace, context availability and runner.temp placement.
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — workflow_call types and declarations, jobs, permissions and dependencies.
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) — direct workflow placement, calls, typed inputs, named secrets, output mappings and last-completing matrix output semantics; required secret declaration is distinct from a nonempty valid value.
- [Reusable workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) — caller keywords, token permission ceiling, caller context/environment and checkout behavior.
- [Secure use](https://docs.github.com/en/actions/reference/security/secure-use) — intermediate env data transport and minimum permissions.
- [Artifact tutorial](https://docs.github.com/en/actions/tutorials/store-and-share-data) — named file exchange across jobs.
- [Pinned checkout metadata](https://raw.githubusercontent.com/actions/checkout/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml) — checkout inputs; existing catalog pin, v7.0.1.
- [Pinned setup-node metadata](https://raw.githubusercontent.com/actions/setup-node/949feb2413d6458794dcd2491c4babbbce0c15c1/action.yml) — node-version, output and package-manager-cache; existing catalog pin, v7.1.0.
- [Pinned upload-artifact metadata](https://raw.githubusercontent.com/actions/upload-artifact/cf430e030ddbb5b0abf93d22962f4752f3646cd9/action.yml) and [README](https://raw.githubusercontent.com/actions/upload-artifact/cf430e030ddbb5b0abf93d22962f4752f3646cd9/README.md) — existing catalog pin, v7.0.2; path/name/missing-file/retention behavior and unique artifact identities.
- [Pinned download-artifact metadata](https://raw.githubusercontent.com/actions/download-artifact/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml) and [README](https://raw.githubusercontent.com/actions/download-artifact/9000827ccba6bdab643e8b6fd33ac0654aef8333/README.md) — existing catalog pin, v8.0.2; exact-name destination semantics.
- [actionlint 1.7.12 checks](https://github.com/rhysd/actionlint/blob/v1.7.12/docs/checks.md) — workflow-call checks and static scope, supplemented by actual installed behavior above.
- [act usage](https://nektosact.com/usage/index.html) and [unsupported behavior](https://nektosact.com/not_supported.html) — selection and gaps such as ignored job permissions/timeouts, cancellation and environments.
- [Node 24 test runner](https://nodejs.org/docs/latest-v24.x/api/test.html) — built-in test invocation; fetched latest-v24 documentation identifies 24.22.2, while actual test runtime remains installed **24.21.0**. No upgrade was performed.

Failed web fetches, not counted as verified sources:

- `https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/store-and-share-data-from-a-workflow` was inaccessible; used the verified current artifact tutorial URL above instead.
- `https://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html` and `https://www.gnu.org/software/bash/manual/bash.html#Double-Quotes` timed out. No claim of a successful Bash manual lookup; the shell behavior is reproduced directly in the bounded lab and supported by GitHub's verified secure-use pattern.
- `https://nodejs.org/docs/latest-v24.x/api/child_process.html` was inaccessible. No new behavior was asserted solely from this failed fetch; actual child processes and their results were exercised locally.

## Deferred boundaries and integration proposals

- **All documentation validation remains deferred** to the coordinator's single combined pass. No diagram-render count or build/link success is available from this thread.
- Engine-backed good/broken composite metadata execution remains deferred because the actual Podman socket refuses connection. Job listing and direct adapter tests do not prove runner mappings.
- Hosted typed-input resolution, actual GitHub output processing, secret presence/values/masking, private-repository access and token permission enforcement remain unexecuted. The public fixture constant proves no authorization.
- Real setup-node acquisition, hosted artifact upload/download, caller/callee scheduling, cancellation, environments and OS parity remain unexecuted. The host harness is sequential, and Linux containers would not establish macOS/Windows runner parity anyway.
- `preview-1` evidence is synthetic consistency data, not a commit identity, attestation or release authorization. The independent test branch does not consume the generated bundle. Both limits are explained in 0030.
- ShellCheck is absent and was not installed. No security-linter pass is claimed.

Optional coordinator-owned changes, **proposed only**:

1. Add `test:module5` to Taskfile using the six positive host commands listed above; optionally add an asserting wrapper for the four expected-blocked pipeline cases. Add it to `test:labs` in canonical module order. Do not add expected-failure commands directly to an all-positive `&&` chain without asserting their expected statuses.
2. Add `lint:module5` as `.venv/bin/python labs/0029/lint_module.py` (or equivalent existing locked `uv run --no-sync python` convention), then integrate it into `lint:labs`. Keep the four diagnostic files separate; `wrong-boolean` is a documented static gap, not a failing positive workflow.
3. Update shared catalog checkboxes/counts only after collecting all four module completions, targeting the authorized 54 authored / 6 placeholders total. No counts were changed here.
4. The source library already includes the core metadata, reuse, security and action repositories. Optionally add the current artifact tutorial, reusable-configuration reference and pinned metadata URLs above when integrating the source index. Do not cite the timed-out Bash pages as verified.
5. Add this module's lab inventory and focused commands to shared guides if desired. No extra guide was assigned or created here.

No learner mastery was established. Live teaching can begin at 0001 or the requested lesson after checking actual prerequisite evidence; this authoring batch does not advance that learner state.
