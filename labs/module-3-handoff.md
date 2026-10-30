# Module 3 authoring handoff

> Numbering update: module labels, lesson IDs, paths, and command references in this handoff now use the sequential course layout. Original authoring checks preceded the renumbering; the coordinator records verification at the current paths in NOTES.md.

Completed **2026-10-30** in the shared checkout
`/Users/rohitkharche/.t3/projects/actions-learn`.

## Completion and ownership

All six assigned reference lessons and isolated labs are fully developed. All six
pages now have `lesson_status: authored`. Each page has prerequisites, concrete
outcomes, explanations tied to action/workflow boundaries, runnable local
commands with expected results, a vertical `flowchart TD` Mermaid diagram,
admonitions and code annotations, predictions and collapsed worked solutions,
deliberate failures with diagnosis/repair, transfer and retrieval exercises,
local/hosted evidence limits, an exact-file future teaching prompt, and catalog
pagination. Written availability does not establish learner mastery. No learner
answers, modified learner examples or demonstrated understanding were collected.

Only these six pages, `labs/0013/`–`labs/0018/`, and this handoff were edited by
this authoring thread. Existing shared edits and other modules were preserved.
No shared catalog, notes, Taskfile, example implementation, manifest, lockfile,
validator, workflow registration or guide was changed. No subagents, commits,
pushes, releases, publication, hosted workflows or model execution were used.

Boundary order follows the corrected sequence: **0012 → 0013 → 0014 → 0015 → 0016 → 0017 → 0018 →
0019**. No neighboring page was edited.

## Developed pages

| ID | Page | Main developed behavior |
| --- | --- | --- |
| 0013 | `docs/lessons/0013-docker-action-metadata-and-lifecycle.md` | Named inputs → ordered arguments → exec entrypoint → channels/status → runner output; build/start/run separation and optional pre/post lifecycles |
| 0014 | `docs/lessons/0014-dockerfiles-layers-and-build-context.md` | Context versus runtime workspace, COPY/RUN/image configuration, real optional cache experiment, outside-context failure, base identity/update strategy |
| 0015 | `docs/lessons/0015-container-mounts-ownership-and-output-paths.md` | Independent workspace/command-file mounts, host/container path map, ownership, rootless/VM limits, private and read-only output failures, partial report policy |
| 0016 | `docs/lessons/0016-docker-action-direct-and-image-tests.md` | Two pure-function assertions and one 11-case contract matrix for host/image, missing interpreter fixture, caller outcome/output assertions |
| 0017 | `docs/lessons/0017-container-errors-signals-and-cleanup.md` | Truthful status, staged output, SIGINT/TERM/KILL, exec wrapper, swallowed-status failure, graceful versus forced cleanup, Docker stop versus GitHub cancellation |
| 0018 | `docs/lessons/0018-container-security-and-release-tradeoffs.md` | Inventory versus SBOM/scan, source/base/image identities, pin freshness, bounded measurement harness, packaging comparison, evidence-based unexecuted release plan |

There are **six new lesson diagrams** in these pages. They have **not** been
validated or rendered in this thread; no zero-error diagram/build claim is made.

## Lab file inventory

There are 41 developed lab files, plus this handoff. Lab actions are copied or
extended fixtures; shared `examples/` remain unchanged. Recipes are inactive
outside `.github/workflows/`.

- `labs/0013/action/action.yml`
- `labs/0013/action/Dockerfile`
- `labs/0013/action/entrypoint.py`
- `labs/0013/probe.py`
- `labs/0013/consumer.yml`
- `labs/0014/action/action.yml`
- `labs/0014/action/Dockerfile`
- `labs/0014/action/Dockerfile.bad-context`
- `labs/0014/action/.dockerignore`
- `labs/0014/action/entrypoint.py`
- `labs/0014/action/runtime-policy.txt`
- `labs/0014/outside-only.py`
- `labs/0014/host_probe.py`
- `labs/0014/cache_experiment.py`
- `labs/0015/action/action.yml`
- `labs/0015/action/Dockerfile`
- `labs/0015/action/entrypoint.py`
- `labs/0015/mount_probe.py`
- `labs/0015/consumer.yml`
- `labs/0016/action/action.yml`
- `labs/0016/action/Dockerfile`
- `labs/0016/action/Dockerfile.missing-runtime`
- `labs/0016/action/entrypoint.py`
- `labs/0016/contract.py`
- `labs/0016/consumer.yml`
- `labs/0017/action/action.yml`
- `labs/0017/action/Dockerfile`
- `labs/0017/action/entrypoint.sh`
- `labs/0017/action/worker.py`
- `labs/0017/swallow.py`
- `labs/0017/test_host.py`
- `labs/0017/test_container.py`
- `labs/0017/consumer.yml`
- `labs/0018/action/action.yml`
- `labs/0018/action/Dockerfile`
- `labs/0018/action/entrypoint.py`
- `labs/0018/inventory.py`
- `labs/0018/review.py`
- `labs/0018/test_review.py`
- `labs/0018/measure.py`
- `labs/0018/release-review.md`

## Exact executable checks actually run

Commands below were executed from the repository root using existing installed
dependencies. Intentional nonzero probes are expected negative observations,
not unresolved regressions. The 0013 probes were repeated after improving their
failure diagnostic. Python syntax was rechecked after the final script edit.

| Exact command | Result |
| --- | --- |
| `uv run --no-sync python labs/0013/probe.py` | Exit 0. Program gets `['Ada', 'Hello']`; stdout `Hello, Ada!\n`; stderr empty; output `prior=kept\ngreeting=Hello, Ada!\n`. |
| `uv run --no-sync python labs/0013/probe.py --reverse` | Expected exit 1 from probe. Adapter exits 0 but writes `Ada, Hello!`; probe detects argument-order contract mismatch. |
| `uv run --no-sync python labs/0013/probe.py --name ''` | Expected exit 1 from probe and adapter. Nonempty/single-line diagnostic; prior output record unchanged. |
| `uv run --no-sync python labs/0014/host_probe.py` | Exit 0. Copied program writes exact greeting; explicitly no image/cache claim. |
| `uv run --no-sync python labs/0015/mount_probe.py` | Exit 0. Adapter exit 0; exact greeting/report outputs and report contents. Observed host process/report-owner UID 501. |
| `uv run --no-sync python labs/0015/mount_probe.py --mode missing` | Probe exit 0 verifying intended adapter exit 1. Missing-parent diagnostic, empty output file, report remains as documented. |
| `uv run --no-sync python labs/0016/contract.py host` | Exit 0. Two pure-function assertions and all **11** process cases pass: default, ordinary, trim, Unicode, literal shell-like text, empty, spaces, newline, CR, unset output, missing parent. |
| `uv run --no-sync python labs/0017/test_host.py` | Exit 0. **6 tests pass**: success, ordinary failure, SIGINT→130, SIGTERM→143, SIGKILL→host subprocess -9 with leftover staging, swallowed-status demonstration. |
| `sh -n labs/0017/action/entrypoint.sh` | Exit 0, no diagnostics. Syntax only; image permissions/startup remain untested. |
| `uv run --no-sync python labs/0018/inventory.py` | Exit 0. Base `python:3.14-alpine`; imports `os, pathlib, sys`; no explicit extra package installs; base packages/digest/scan/image timings explicitly uncollected. |
| `uv run --no-sync python labs/0018/test_review.py` | Exit 0. **4 tests pass**: current, age 30 accepted, age 31 rejected, future date rejected. |
| `uv run --no-sync python labs/0018/review.py --reviewed-on 2026-01-01 --as-of 2026-10-30` | Expected exit 1: review age 302 days outside 0..30. No digest or vulnerability assertion. |
| `uv run --no-sync python labs/0018/review.py --reviewed-on 2026-10-30 --as-of 2026-10-30` | Exit 0: age 0 days. Output explicitly limits this to freshness, not scan/release approval. |
| `uv run --no-sync python labs/0018/measure.py host --samples 1` | Exit 0. One raw host subprocess sample emitted and exact output verified. Cache state uncontrolled; no performance comparison or container result claimed. |
| `.tools/bin/actionlint -color labs/0013/consumer.yml labs/0015/consumer.yml labs/0016/consumer.yml labs/0017/consumer.yml` | Exit 0, no diagnostics for **all four** inactive recipes and their known local action interfaces. |

In-memory Python syntax check, executed twice with the final result **19 files,
exit 0**:

```bash
uv run --no-sync python - <<'PY'
from pathlib import Path
paths = [p for n in range(13, 19) for p in Path(f'labs/{n:04}').rglob('*.py')]
for path in paths:
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
print(f'Compiled {len(paths)} lab Python files in memory; no image-execution claim')
PY
```

Generated `__pycache__` directories from these tests were removed only beneath
owned `labs/0013/`–`labs/0018/` directories. No installed package state was changed.

Environment inspections actually run:

- `command -v docker podman python3 uv act`: existing Docker wrapper, Podman,
  Python, uv and act found; no installation performed.
- `uv run --no-sync python --version`: Python **3.14.6**.
- `.tools/bin/actionlint -version`: **v1.7.12**, installed local binary.
- `act --version`: **0.2.89**.
- `docker stop --help`: installed compatibility command documents `--time`;
  the opt-in container stop fixture uses `--time 2`.
- `podman machine list`: existing `podman-machine-default`, applehv, not started
  by this thread. Listing is not evidence of engine readiness.
- `docker info`: final standalone command exits **125**. Output identifies the
  Podman compatibility boundary on darwin/arm64, version **6.0.2**, and reports:

```text
Cannot connect to Podman. Please verify your connection to the Linux system using `podman system connection list`, or try `podman machine init` and `podman machine start` to manage a new Linux VM
Error: unable to connect to Podman socket: failed to connect: dial tcp 127.0.0.1:62183: connect: connection refused
```

The suggested setup commands in that diagnostic were **not** executed. No VM,
socket configuration or daemon was provisioned/started.

## Deferred checks and precise limits

**Documentation validation is deferred to the coordinator's ONE combined
24-lesson pass, after all four authoring modules and shared edits are ready.**
This thread ran no Markdown/link checks, Mermaid validation, Zensical build,
`task docs:verify`, `task check`, or alternative custom documentation validator.
Do not treat the unvalidated diagrams or site as passed. Coordinator should run
`task docs:verify` once at the requested combined boundary.

All Docker builds, pulls and container runs remain deferred because `docker info`
failed before the relevant boundary. In particular, these developed fixtures
have not produced image evidence:

- `labs/0014/cache_experiment.py`: two real builds, cache-log interpretation,
  program edit and run; bad-context Dockerfile failure is also unexecuted.
- `labs/0015/mount_probe.py --container` and its `private`, `read-only`, `missing`
  modes: actual mounts, VM sharing, image ownership and read-only access.
- `labs/0016/contract.py image`: all 11 image cases; the deliberately
  missing-runtime image build/start failure is also unexecuted.
- `labs/0017/test_container.py`: engine stop/kill, PID-boundary behavior,
  container exit 143/137 and forced-cleanup limits.
- `labs/0018/measure.py build` / `image`: build/run timing samples, image size
  observations, base/image resolution and scan/SBOM collection.
- All `act` caller executions. No hosted dispatch, cancellation or policy test
  ran. Lint success is not runner ingestion/output-mapping evidence.

No base registry digest or final image digest was collected. The labs keep the
starter's readable mutable `python:3.14-alpine` tag and label it as a teaching
reference. No image pin, finding count, architecture compatibility or release
readiness was invented. The release worksheet intentionally preserves missing
evidence. The single host timing smoke sample is not a cold-start measurement.

## Primary sources checked

All sources below were opened/checked on **2026-10-30** through current primary
GitHub, Docker, Python or act maintainer material. GitHub sources come from the
curated library; Docker/Python detail pages follow those official references.
New direct URLs are proposed for the shared source index below. No community
post was used to override primary contracts.

| Checked URL | Claims grounded |
| --- | --- |
| https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax | Docker runtime, image/args/env/entrypoint, required-input limitation, separate pre/post containers and conditions |
| https://docs.github.com/en/actions/tutorials/use-containerized-services/create-a-docker-container-action | Linux/Docker runner requirements, build/run lifecycle, explicit arguments and outputs |
| https://docs.github.com/en/actions/reference/workflows-and-actions/dockerfile-support | Root-user requirement, workspace mount/cwd, absolute entrypoints, metadata overrides and CMD/args |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands | UTF-8 command files, GITHUB_OUTPUT and action-scoped GITHUB_STATE |
| https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#steps-context | outcome versus conclusion with continue-on-error |
| https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes | Status 0 versus nonzero and action outcomes |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation | Runner entry-process signaling and timed escalation; distinct from docker stop |
| https://docs.github.com/en/actions/reference/security/secure-use | Least privilege, untrusted input, full commit pins and moved tags |
| https://docs.docker.com/build/concepts/context/ | Final build argument, available files and dockerignore |
| https://docs.docker.com/reference/dockerfile/ | COPY context restrictions, exec/shell forms, ENTRYPOINT/CMD interaction and signal boundary |
| https://docs.docker.com/build/cache/invalidation/ | COPY/cache keys and mtime exclusion |
| https://docs.docker.com/engine/storage/bind-mounts/ | Host/container views, engine-host paths, obscured image content and readonly |
| https://docs.docker.com/build/building/best-practices/ | Base choice, dependency ordering, digest pins and update tradeoffs |
| https://docs.docker.com/build/building/secrets/ | Build args/ENV are unsuitable secret transport; secret mounts |
| https://docs.docker.com/reference/cli/docker/container/stop/ | Main-process stop signal, grace period and kill escalation |
| https://docs.docker.com/reference/cli/docker/image/inspect/ | Image metadata and format inspection |
| https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/ | Registry index/manifest/platform details when Buildx is already available |
| https://docs.docker.com/scout/explore/analysis/ | SBOM/advisory relationship and changing assessment of unchanged image bytes |
| https://docs.docker.com/reference/cli/docker/scout/cves/ | local:// target, severity filters and explicit exit-code option |
| https://raw.githubusercontent.com/docker-library/official-images/master/library/python | Listed Python 3.14-alpine tag, architecture entries and upstream source pointer; no resolved image-digest claim |
| https://github.com/docker-library/python/blob/01dcc3d31fcd879f9af36e097bd96328a457f4bd/3.14/alpine3.24/Dockerfile | Source for the variant pointed to by the checked Official Images entry; source SHA is not an image digest |
| https://docs.python.org/3.14/library/signal.html | Catchable handlers, execution limitations and uncatchable SIGKILL |
| https://nektosact.com/not_supported.html | Local emulation does not establish real GitHub policy/services |

## Proposed shared integration, for coordinator only

No shared integration is necessary to run these labs directly. Optional named
Taskfile targets can make them easier to discover without expanding default
container/hosted cost:

- `test:module3`: run the successful 0013 probe, 0014 host probe, 0015 correct and
  missing host probes, 0016 host contract, 0017 host suite, 0018 review suite.
  Keep expected-nonzero CLI demonstrations outside a generic success-only task
  unless their nonzero status and exact output are explicitly asserted.
- `lint:module3`: use the exact four-recipe actionlint command above. These
  recipes have unique local action paths and do not need reusable-workflow
  staging or registration under `.github/`.
- If adding `test:module3:container`, keep it opt-in with an explicit `docker
  info` precondition. Build the matching `actions-learn-0014:local` through
  `actions-learn-0018:local` tags before their scripts. Never silently create or
  start an engine and do not fold scanners/registry writes into host tests.

Source-index additions proposed for `docs/references/resources.md`: GitHub's
Dockerfile support and exit-code references; Docker build context, Dockerfile,
cache invalidation, bind mounts, best practices, build secrets, stop, inspect,
Buildx imagetools and Scout pages; Official Images Python/source entry; Python
signal documentation. All exact checked URLs are listed above. Recheck runtime
or digest details when updating examples rather than freezing this date as a
permanent currentness claim.

Coordinator owns six curriculum checkboxes, authored counts, NOTES, and any
shared Taskfile/source-index integration. Do not change mastery records: no
technical learner evidence was collected. Next catalog lesson is **0019**.

## Unresolved issues

No known host-code regression remains. Deferred engine-dependent behavior and
unvalidated documentation are the outstanding evidence gaps, not reasons to
leave this module waiting for approval or live learner answers. The action's
fixed staging name is intentionally scoped to one isolated workspace; parallel
writers need unique paths. The artifact/output commit gap and unavailable
cleanup after forced kill are taught explicitly rather than claimed solved.

After this handoff and all file edits are saved, send the requested
`MODULE 4 AUTHORING COMPLETE` notification to the existing coordinator thread;
then end the authoring turn without further edits.
