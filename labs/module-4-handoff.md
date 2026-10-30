# Module 4 authoring handoff

> Numbering update: module labels, lesson IDs, paths, and command references in this handoff now use the sequential course layout. Original authoring checks preceded the renumbering; the coordinator records verification at the current paths in NOTES.md.

Date: **2026-10-30**. Scope: all six JavaScript/TypeScript reference lessons, IDs **0019–0024**. Status: **complete for integration; no authoring blocker**.

All six pages have `lesson_status: authored`, developed explanations, runnable labs, predictions, collapsed worked solutions, deliberate failures with diagnosis/repair, transfer/retrieval exercises, verification limits, code annotations, admonitions, vertical quoted-label Mermaid diagrams, exact-file teaching prompts, and curriculum-order pagination. The boundary remains **0018 → 0019 → 0020 → 0021 → 0022 → 0023 → 0024 → 0025**.

**Documentation validation is deferred to the coordinator's ONE combined 24-lesson pass after all four modules and shared edits are integrated.** No Markdown, link, Mermaid, or Zensical validation was run in this thread. Neither `task docs:verify` nor `task check` was run. Mermaid render counts and documentation build success are therefore not claimed.

## Developed pages and their contracts

| ID | Existing page expanded in place | Developed lab contract |
| --- | --- | --- |
| 0019 | `docs/lessons/0019-javascript-action-runtime-and-toolkit.md` | Metadata/runtime/input/output boundary; missing required-input validation defect; dependency-free implementation with explicitly unexecuted Toolkit reference |
| 0020 | `docs/lessons/0020-pure-functions-and-node-tests.md` | Pure timing-report policy, real input/output adapter, valid/empty/equality/malformed cases, temporary boundary mutant |
| 0021 | `docs/lessons/0021-typescript-bundling-and-dist-drift.md` | Local strict compiler configuration, shared bundler options, shipping CJS artifact, nonrepairing drift check, safe stale-bundle experiment |
| 0022 | `docs/lessons/0022-output-contracts-and-mocked-github-api.md` | Fake normalized API seam, pagination, empty versus denied data, bounded transient reads, rate-limit failure, malformed/partial results, truthful process outputs |
| 0023 | `docs/lessons/0023-javascript-action-lifecycle-and-state.md` | Setup in local main, saved state, separate post process, ownership checks, partial allocation, missing/lost state, idempotence, cleanup failure |
| 0024 | `docs/lessons/0024-cross-platform-actions-and-versioned-releases.md` | Portable logical-line policy, path models and real host files, missing-binary failure, intended hosted matrix, dependency/release compatibility decisions |

No learner predictions, code, diagnoses, or retrieval answers were supplied. Author-run evidence is not learner mastery. No learning record was created.

## Lab file inventory

All additions are under the assigned `labs/0019/`–`labs/0024/` directories. Temporary exercise directories are removed by the harnesses. This handoff is the only module-wide file added.

### labs/0019/

- `action.yml` — required greeting interface, Node 24, local CJS entrypoint.
- `greet.cjs` — copied greeting rule from the existing shared example, left unchanged there.
- `index.cjs` — validated standard-library adapter.
- `broken.cjs` — intentional missing-validation defect.
- `process.cjs` — reusable Module 4 real-child-process helper with isolated output files and environment cleanup.
- `action.test.cjs` — 8 focused process cases.
- `demo.cjs` — displays captured child status, stdout, stderr, and output bytes.
- `module4-contracts.yml` — inactive workflow calling all six actions after pinned checkout and asserting their runner-consumed outputs.

### labs/0020/

- `action.yml` — JSON durations/budget interface and report output.
- `report.cjs` — explicit-input timing-report function.
- `index.cjs` — JSON/numeric input adapter.
- `report.test.cjs` — 4 function tests.
- `process.test.cjs` — 4 process tests using the 0019 helper.
- `mutation.cjs` — creates a temporary `<=` to `<` mutant, verifies the existing tests reject it, then removes the copy.

### labs/0021/

- `action.yml` — selects `dist/index.cjs` with Node 24.
- `src/index.ts` — isolated extension of the shared TypeScript example.
- `tsconfig.json` — lab-only strict/noEmit compiler configuration.
- `bundle.cjs` — one in-memory esbuild configuration for generation and comparison.
- `build.cjs` — explicit distribution repair/generation command.
- `check-dist.cjs` — compares bytes without writing the shipping artifact.
- `dist/index.cjs` — actually generated shipping artifact; not ignored by the current ignore rules.
- `artifact.test.cjs` — 4 real bundled-process tests.
- `drift-demo.cjs` — temporary source change, passing type check, stale-byte rejection, old consumer behavior, intentional rebuild, and new consumer behavior.

### labs/0022/

- `action.yml` — explicitly fixture-only interface; no token input.
- `fixtures/scenarios.json` — two-page, empty, denied, rate, primary-rate, transient, unavailable, partial, malformed, and cycle response scripts.
- `fake-client.cjs` — exact method/URL request checks and injected clock/sleep; cannot perform network I/O.
- `report.cjs` — normalized response policy, page/attempt/time budgets, shape checks, issue-versus-PR filtering.
- `adapter.cjs` — all-pages-before-output adapter plus a deliberately broken catch path.
- `index.cjs` — normal fixture-only entrypoint.
- `broken.cjs` — deliberate failure-as-empty-success entrypoint.
- `demo.cjs` — captured process evidence for a selected fixture.
- `report.test.cjs` — 10 tests covering function/client and real-process contracts, including output append and absent output path.

### labs/0023/

- `action.yml` — local main/post hooks; setup intentionally lives in main because local actions do not support `runs.pre`.
- `resource.cjs` — allocation/state persistence, immediate rollback on state-write failure, owned-directory cleanup.
- `index.cjs` — main work and success output only after completion.
- `cleanup.cjs` — separate cleanup entrypoint with visible failure status.
- `lifecycle.cjs` — narrow state-forwarding harness; success, main-failure, partial-setup, missing-state, lost-state, cleanup-failure.
- `lifecycle.test.cjs` — 8 tests, including repeated cleanup and refusal of outside/unowned/symlink targets.

### labs/0024/

- `action.yml` — required workspace-relative file, logical line-count output.
- `lines.cjs` — native path containment and LF/CRLF/CR line policy, with injectable POSIX/Windows lexical models.
- `index.cjs` — realpath containment, UTF-8 read, named result, truthful error handling.
- `broken.cjs` — intentional `wc` dependency.
- `fixtures/report with spaces-रोहित.txt` — two-line Unicode/space-path fixture.
- `portable.test.cjs` — 8 tests, including real CRLF, escaping filesystem link, and unavailable external binary.
- `module4-platforms.yml` — inactive Ubuntu/macOS/Windows matrix recipe; no hosted execution occurred.
- `release-plan.json` — candidate version and compatibility questions, explicitly unexecuted matrix/publication; no invented commit SHA.

## Installed tools reused

Observed host: **darwin/arm64**, Node **v24.21.0**. Installed TypeScript reports **7.0.2**; esbuild reports **0.28.2**. Local actionlint reports **v1.7.12**, built with Go 1.26.10 for darwin/arm64.

`require.resolve` confirmed both `@actions/core` and `@actions/github` are **absent**. Nothing was installed. Toolkit code on the pages is explicitly reference-only; dependency-free adapters provide the runnable comparison. Root package manifests, locks, examples, scripts, validators, active workflows, Taskfile, source index, notes, and other modules were not edited by this thread.

## Exact final executable checks and results

Run from the repository root. These checks were executed after all six labs existed; the final consolidated run used the following commands, in this order:

```bash
node --test labs/0019/action.test.cjs labs/0020/report.test.cjs labs/0020/process.test.cjs labs/0021/artifact.test.cjs labs/0022/report.test.cjs labs/0023/lifecycle.test.cjs labs/0024/portable.test.cjs
node node_modules/typescript/bin/tsc --project labs/0021/tsconfig.json
node labs/0021/check-dist.cjs
node labs/0020/mutation.cjs
node labs/0021/drift-demo.cjs
.tools/bin/actionlint -color labs/0019/module4-contracts.yml labs/0024/module4-platforms.yml
```

Results:

- **46 tests passed, 0 failed, 0 skipped/cancelled/todo**, final test-run duration approximately 0.78 seconds. Breakdown: 0019 = 8; 0020 = 8; 0021 = 4; 0022 = 10; 0023 = 8; 0024 = 8.
- TypeScript: **exit 0, no diagnostics**.
- Distribution comparison: **exit 0**, `PASS: labs/0021/dist/index.cjs matches source.`
- Mutation experiment: **outer exit 0**, `PASS: exact-budget assertion rejected the <= to < mutant (test exit 1).` The inner test failure is deliberate and asserted.
- Drift experiment: **outer exit 0**; inner compiler exit 0; inner stale check exit 1 with shipping bytes unchanged; consumer initially `Hello, Ada!`; explicit build and comparison exit 0; consumer then `Welcome, Ada!`. Maintained source/dist remained unchanged by the experiment.
- actionlint: **exit 0, no diagnostics**, both inactive recipes checked, with local action references covering all six interfaces.

The distribution was initially generated with:

```bash
node labs/0021/build.cjs
```

Result: **exit 0**, `Built labs/0021/dist/index.cjs.` An initial drift-demo implementation tried `require.resolve('typescript/bin/tsc')`, which failed with **ERR_PACKAGE_PATH_NOT_EXPORTED** under the installed TypeScript package. It was repaired to invoke the existing compiler by its explicit project-local filesystem path. The final drift experiment above passed after that repair; no dependency change was needed.

Earlier focused runs also passed: 20 tests for 0019–0021; 17 tests for 0022–0023 before the additional output-path case; and 7 initial 0024 tests before the filesystem-link case. Final counts above supersede those smaller runs. Individual actionlint invocations for the platform recipe and then both recipes also exited 0.

Tool observations were obtained with `node --version`, `node node_modules/typescript/bin/tsc --version`, `.tools/bin/actionlint -version`, a `require.resolve` probe for esbuild/Toolkit packages, and:

```bash
node -p 'JSON.stringify({platform:process.platform,arch:process.arch,node:process.version,esbuild:require("esbuild").version})'
```

Result: `{"platform":"darwin","arch":"arm64","node":"v24.21.0","esbuild":"0.28.2"}`. `git check-ignore labs/0021/dist/index.cjs` returned exit 1 with no matching ignore rule. Scoped file inventory/status reads confirmed the six pages and assigned lab additions; unrelated uncommitted work was preserved.

## Demonstration commands actually executed

The display helpers exit 0 after printing their child's result. The child status, outputs, and resource absence are asserted by the suites above.

| Exact command | Observed result |
| --- | --- |
| `node labs/0019/demo.cjs` | Child 0; `Hello, Ada!` log and `greeting=Hello, Ada!` output |
| `node labs/0019/demo.cjs --broken --missing` | Deliberate child 0; malformed `greeting=Hello, !` exposes absent runtime validation |
| `node labs/0019/demo.cjs --missing` | Child 1; single-line validation diagnostic; no output |
| `node labs/0022/demo.cjs pages` | Child 0; 2 requests, no waits; 2 issues; newline title safely JSON-escaped |
| `node labs/0022/demo.cjs denied` | Child 1; `API status 403`; no output |
| `node labs/0022/demo.cjs transient` | Child 0; 2 requests; fake waits `[250]`; count 1 |
| `node labs/0022/demo.cjs denied --broken` | Deliberate child 0; false empty-success report |
| `node labs/0022/demo.cjs partial` | Child 1 after exhausted page-two 503; no partial output |
| `node labs/0023/lifecycle.cjs success` | Main/post/repeat 0; resource removed; combined 0 |
| `node labs/0023/lifecycle.cjs main-failure` | Main 1/post 0; no output; resource removed; combined 1 |
| `node labs/0023/lifecycle.cjs partial-setup` | Main 1/post 0 after state persisted; resource removed; combined 1 |
| `node labs/0023/lifecycle.cjs missing-state` | No main; post 0; safe no-op |
| `node labs/0023/lifecycle.cjs lost-state` | Deliberately omitted state; resource remains before harness teardown, proving the leak |
| `node labs/0023/lifecycle.cjs cleanup-failure` | Main 0/post 1; resource remains before teardown; combined 1 |

Also executed exactly:

```bash
node -e "const p=require('./labs/0024/release-plan.json'); console.log(p.candidate, p.hostedMatrixExecuted, p.publication)"
```

Result: `v1.1.0 false plan only; no tags, pushes, releases, or Marketplace writes`.

## Deferred checks and explicit boundaries

- **All documentation validation is deferred to the coordinator's combined 24-lesson pass.** Six new vertical diagrams exist, but no diagram render or error count is claimed. Link checking, Markdown/site checks, and Zensical build were not run.
- No `task check`, global `task test`, or global `task lint:workflows` was run. Shared executable implementations did not change; the new lab suites and scoped recipe lint are the executable evidence.
- No Docker/Podman/act execution was attempted. These Node labs changed no container boundary. The previously recorded unavailable container engine in NOTES was not re-probed, so this handoff makes no new engine-availability claim and provisions no infrastructure.
- No real API requests, token authorization checks, GitHub workflow dispatches, release writes, model calls, commits, pushes, or publication occurred. Read-only primary-source browsing was performed.
- The API seam is explicitly normalized (`nextUrl` is not GitHub's response-body field). Production Octokit integration, error-shape adaptation, request cancellation/timeouts, API-version selection, Enterprise base-URL configuration, and permissions remain separate integration work.
- The lifecycle harness models one single-line state record and an explicit main-or-post failure policy. It does not evaluate runner conditions or prove job-end scheduling, cancellation behavior, pre-hooks, state isolation between actual runner action instances, or the runner's final conclusion presentation.
- Runtime tests were executed only on macOS ARM64. POSIX/Windows path-model checks are not hosted Windows or Linux filesystem/runner evidence. The matrix remains explicitly unexecuted.
- The release plan's candidate `v1.1.0` requires a prior-contract review; changed line-count semantics or runner prerequisites could require a breaking major. No fixed version or SHA is fabricated as a published release.

## Primary sources checked on 2026-10-30

Sources were selected from the curated library and official deep links from its Actions, Toolkit, Node, TypeScript, esbuild, Git, and security references. These were current read-only checks; no package installation instructions from upstream were executed.

| URL checked | Used to verify |
| --- | --- |
| https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax | Node 24, main entrypoint, input transport, lack of automatic required-input rejection, pre/post hooks and conditions, unsupported local pre |
| https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands | UTF-8 environment files, outputs, private lifecycle state and STATE_ transport |
| https://docs.github.com/en/actions/tutorials/create-actions/create-a-javascript-action | Node action packaging, Toolkit responsibilities, cross-OS external-binary concerns |
| https://raw.githubusercontent.com/actions/toolkit/main/packages/core/README.md | Input/output/state/failure helper interfaces |
| https://raw.githubusercontent.com/actions/toolkit/main/packages/core/src/core.ts | getInput normalization/trim/required behavior; setFailed versus error; file-output and state helpers |
| https://raw.githubusercontent.com/actions/toolkit/main/packages/github/README.md | getOctokit, event context, REST client and paginate reference |
| https://nodejs.org/docs/latest-v24.x/api/test.html | Built-in test runner and assertions on the Node 24 documentation line |
| https://nodejs.org/api/path.html | Host versus explicit POSIX/Windows path models; existing stable APIs also exercised with installed Node 24 |
| https://www.typescriptlang.org/docs/handbook/intro.html | TypeScript static-checking role and source/runtime distinction |
| https://esbuild.github.io/api/ | In-memory Node-targeted bundling options and output-file API |
| https://esbuild.github.io/content-types/#typescript | TypeScript syntax transformation does not perform type checking |
| https://github.com/actions/typescript-action | Maintained committed-distribution and authoring/release patterns |
| https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api | Link-based REST pagination versus the lab's normalized seam |
| https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api | Retry-After/quota-reset/backoff guidance, access failures, safe bounded retries |
| https://docs.github.com/en/rest/issues/issues#list-repository-issues | Issue-list endpoint also includes pull requests |
| https://docs.github.com/en/actions/how-tos/create-and-publish-actions/release-and-maintain-actions | Shipping dependencies and semantically versioned releases/aliases |
| https://docs.github.com/en/actions/how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases | Immutable release tags versus moving compatibility aliases |
| https://docs.github.com/en/actions/reference/security/secure-use | Reviewed full commit pins and dependency/input trust boundaries |
| https://git-scm.com/book/en/v2/Git-Basics-Tagging | Tags identify selected revisions; ordinary tags alone are not a hosted immutability policy |

The browser fetch failed for `https://github.com/actions/toolkit/tree/main/packages/core`; its official raw README/source URLs above were successfully read instead. It also rejected the attempted `/manage-releases` documentation path and the versioned Node path-page URL; the correct official release-maintenance and stable path-reference URLs above were successfully read. No fact relies on the failed fetches.

## Coordinator-owned integration proposals

Do not treat this handoff as shared-file edits; none were made here.

1. Mark the six Module 4 entries authored/checked and update global authored/placeholder counts, learner notes, and course summary only after integrating all modules. Preserve the published paths and catalog-order boundary.
2. Optionally add `test:module4` with the exact six-command final check sequence above. Keep `node labs/0021/build.cjs` as an explicit repair command, never before a drift check in verification. A separate `lint:module4` can use the existing `ACTIONLINT` variable with the two recipe paths.
3. Add precise official deep links to the shared source index if desired: Toolkit core/GitHub references, Node path documentation, REST pagination/best practices/issues listing, and action release/immutable-tag guidance. Existing curated TypeScript/esbuild/Node-test links already cover the rest.
4. Run the ONE whole-site `task docs:verify` only when the coordinator confirms all four modules and shared integration are complete. No per-module documentation verification was performed.

Next live teaching session: assess actual prerequisites, start 0019 if Module 4 is desired, and record only demonstrated learner understanding. Next curriculum page after this module: `docs/lessons/0025-composite-action-inputs-and-outputs.md`.
