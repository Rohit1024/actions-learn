# User learning notes and preferences

## Learner profile

- **Author / GitHub handle:** rohit1024.
- **Topic:** GitHub Actions, Docker container actions, JavaScript/TypeScript actions, composite actions, and GitHub Agentic Workflows.
- **Starting proficiency:** not established. Record demonstrated Actions understanding; the requested course scope does not establish programming or Actions mastery.
- **Concrete goal:** develop and debug actions locally to avoid repeated GitHub-runner iteration and unnecessary quota use.

## Teaching preferences

- Prefer maintained pre-built actions for common automation and reduce repeated shell glue. Track dated stars and matched Marketplace creator evidence separately. Create custom actions for missing behavior or a useful team interface.
- Start directly with GitHub Actions: events, workflows, jobs, steps, runners, expressions, inputs, outputs, and dependencies.
- The user explicitly requested deletion of the basic Linux and general programming lessons. Keep supporting YAML, shell, language, Git, or API explanations brief and inside the relevant Actions example.
- Progress toward independent professional orchestration: worker contracts, workflow DAGs, evidence joins, trust boundaries, release gates, diagnostics, usage budgets, and recovery.
- Develop one lesson in each future teaching thread. Read its exact page, the mission, these notes, `docs/lessons/teaching-guide.md`, and prerequisite Actions pages; expand the existing page in place.
- Pause for learner predictions, exercises, and retrieval answers. Written content and placeholders do not establish mastery.
- Make the local loop part of action lessons: direct tests, workflow linting, container checks when needed, selected `act` execution, then targeted GitHub validation.
- Explain process boundaries and input/output contracts with vertical Mermaid diagrams.
- Use runnable workflows and actions, failure experiments, and retrieval questions.
- Completed lessons must contain learner-facing content: keep prerequisites, lab instructions, exercises, and navigation; remove lesson-creation prompts, thread-start blocks, and authoring coordination notes. Keep session and authoring instructions in the teaching guide, these notes, or module handoffs.
- Keep navigation at section roots and catalog lessons within their section, with previous/catalog/next links.
- Use primary documentation for current runtime versions and `gh aw` behavior. Treat `gh aw trial` as hosted execution with runner and possible model usage.

## Active state

- **Current starting point:** lesson 0001, the GitHub Actions execution model. The earlier basic-lesson exercises are superseded by the user's course-scope change.
- **Authored content:** 54 reference lessons in Modules 1–9: 0001–0054, with prerequisites, local labs, explained examples, exercises, and diagrams. There are no starter pages.
- **Placeholders:** six detailed capstone briefs in Module 10: 0055–0060.
- **Roadmap:** 60 consecutive GitHub Actions lessons, 0001–0060, across 10 modules with six lessons each. Follow workflow execution (1), local testing (2), Docker (3), JavaScript/TypeScript (4), composite actions/reusable workflows (5), security (6), pre-built actions (7), agentic workflows (8), create your own action (9), capstone (10). Module order, lesson numbers, filenames, lab paths, and pagination now agree. Checked items track written content, not mastery.
- **Next suggested teaching session:** `/teach 0001`, using the authored `docs/lessons/0001-execution-model.md`. Begin with a prediction; no learner exercise evidence has been collected. The remaining authoring target is Module 10, the production capstone beginning at 0055.
- **History:** the dated handoffs below retain the module/lesson numbers used at the time. The sequential-numbering update at the end supersedes those earlier layouts and identifies the current handoff paths and commands.
- **Learning records:** `learning-records/0001-start-with-github-actions.md` records the user's explicit scope preference. No technical mastery has been demonstrated yet.
- **Environment observation during setup:** Node 24, uv, Task, and act are installed. The Docker command points to Podman, whose socket was unavailable. Host tests do not depend on that daemon.

## Course restructuring handoff — 2026-10-30

- **Actual work:** removed the 12 standalone foundation lessons, their catalog, and their two local labs. Updated the mission, home page, curriculum, README, Actions prerequisites, lesson prompts, teaching guide, reference annotations, and teach skill to begin directly with Actions.
- **Learner evidence:** the user asked to delete the basic Linux/programming lessons and structure the course around GitHub Actions. This is a scope preference, not evidence of completed technical exercises.
- **Checks executed:** `task docs:verify` passed: 61 Markdown pages, 454 local links, and 61 diagrams (3 rendered, 58 cached), 0 errors; incremental Zensical build succeeded. Verified 48 consecutive Actions lesson IDs across 8 modules, with 2 starters and 46 placeholders. No removed-track IDs, paths, or lab directories remain in the course sources. Deleted lesson HTML and sitemap entries are absent; lesson 0001 is generated. `git diff --check` passed for tracked changes.
- **Skill validation:** the generic skill-creator validator rejects the existing `argument-hint` and `disable-model-invocation` extension fields. A temporary copy containing its recognized fields passed; the two extensions and explicit-only invocation policy were checked separately and preserved in the actual skill.
- **Checks deferred:** action tests, workflow linting, containers, and hosted execution; action and workflow implementations were not changed.
- **Open questions:** learner proficiency in specific Actions topics is still unknown; assess it through the requested Actions lesson's examples.
- **Next lesson:** 0001, then 0002 for local feedback. Keep the remaining lesson IDs and Actions module sequence stable.

## GitHub repository and Pages setup — 2026-10-30

- **Repository:** `https://github.com/Rohit1024/actions-learn`; published the workspace and README to `main`. The user explicitly authorized changing the repository from private to public for Pages.
- **Repository metadata:** description explains the 48-lesson Actions course, custom actions, local testing, and agentic workflows; homepage is `https://rohit1024.github.io/actions-learn/`.
- **Pages:** enabled with the GitHub Actions build source and HTTPS enforcement. Documentation workflow run `41018410694`, attempt 2, deployed successfully to `https://rohit1024.github.io/actions-learn/`.
- **CI finding:** hosted Ubuntu rejected Puppeteer's downloaded Chrome sandbox. The checks workflow now selects `/usr/bin/google-chrome`, the installed browser covered by Ubuntu's AppArmor policy. This setting is scoped to the `task check` step; the local validator stays unchanged.
- **Verification:** `task check` passed locally, including action tests, workflow linting, 454 documentation links, 61 diagrams, and the site build. All 61 diagrams also passed a forced render. Hosted contract-check run `41019013890` passed with the runner's Chrome. The public home page, curriculum, first lesson, logo, stylesheet, and JavaScript asset returned HTTP 200. The remote README matches the local file; repository metadata confirms public visibility, the description, homepage, and enabled Pages.

## Pre-built and custom-action modules — 2026-10-30

- **User preference:** add popular pre-built actions, including dorny/paths-filter, to reduce shell scripting; emphasize verified publishers for important tasks and include a dedicated module for creating our own actions.
- **Work:** added modules 2 and 4, with 12 lesson briefs, two module guides, three inactive pre-built workflow recipes, a shell-free project setup composite, and its inactive consumer recipe. Existing lesson URLs remain stable; pagination follows module order.
- **Evidence sources:** 29-repository snapshot records current stars, non-archived status, last pushes, repository releases, and matched Marketplace badges. Community and unknown badge cases are labeled explicitly. The chart ranks only the curated shortlist.
- **Learning record:** `learning-records/0002-prefer-prebuilt-actions-and-create-focused-actions.md` records this scope preference, without claiming technical mastery.
- **Verification:** active workflows and all four inactive workflow recipes passed actionlint, including the new local composite's metadata. Type checking, distribution consistency, 3 JavaScript tests, and 4 process-adapter tests passed. Documentation verification passed: 76 Markdown pages, 602 local links, and 76 diagrams (18 rendered, 58 cached), 0 errors; incremental build succeeded. Verified 60 lesson IDs, 10 modules, all pagination in module order, and 29 sorted snapshot records with 20 observed creator badges. All 10 remote recipe references have full commit pins, and their configured input names match metadata fetched at those exact commits. The teach skill compatibility check preserved its existing invocation metadata.
- **Deferred execution:** the Docker-compatible daemon is unavailable; container and act execution were not run. The inactive recipes have not executed remote setup, cache/artifact services, a container build, or release writes. Existing application/adapter tests remain the local behavior evidence.
- **Publication:** commit `ec9b546` passed hosted contract checks (`41023169449`) and the documentation deployment (`41023169353`). Both module guides, the ranked catalog, its JSON snapshot, the chart, and the final new lesson are publicly accessible with expected content. The repository description now reflects 60 lessons and pre-built action reuse.

## Module 1 batch authoring — 2026-10-30

- **User request:** author every lesson in Module 1 together and run Markdown/documentation validation after the complete batch, rather than per lesson. This explicitly overrides the usual one-page authoring pace for this session; live teaching still pauses for learner answers.
- **Actual work:** expanded 0001–0006 in place to `lesson_status: authored`. Added prerequisites, explained examples, predictions, collapsed solutions, failure diagnosis, transfer/retrieval exercises, vertical execution diagrams, verification limits, and exact-file teaching prompts. Preserved module-order pagination through 0006 → 0049 and section-root sidebar navigation.
- **Runnable material:** `labs/0001/`–`labs/0006/` contain process, adapter, event-payload, output-channel, and evidence-gate exercises plus seven inactive workflow recipes. `task lint:module1` stages and checks the recipes together, including the local reusable-workflow caller/callee interface, without installing active workflows.
- **Course state:** six authored lessons, zero starters, 54 placeholders, 60 total lessons across 10 modules. Updated the curriculum, home page, README, and trusted source list.
- **Learner evidence:** the user requested batch authoring. No predictions, code, failure explanations, or retrieval answers were supplied by the learner; no technical mastery record is justified.
- **Checks executed after the full content batch:** one `task docs:verify` passed: 76 Markdown pages, 611 local links, and 76 Mermaid diagrams (6 newly rendered, 70 reused from cache), 0 errors; one incremental Zensical build succeeded with no issues. All seven inactive Module 1 workflows passed `task lint:module1`, including local action and reusable-call metadata. All 28 host lab cases passed their expected outcomes, including deliberate failures and every one of the 16 evidence-gate state pairs. `task test` passed TypeScript checking, distribution consistency, three JavaScript tests, and four process-adapter test methods; `task lint:workflows` passed for active workflows. Confirmed 60 lesson pages with six authored, zero starter, and 54 placeholder statuses, six checked curriculum items, and a vertical diagram plus exact-file prompt on each Module 1 page. `git diff --check` passed. No per-lesson Markdown validation or build was run.
- **Deferred integration:** no GitHub dispatch, container execution, or model call is part of this authoring batch. Actual event admission, hosted output processing, permissions, scheduler/cancellation behavior, and the reusable hosted call remain integration boundaries.
- **Next step (updated by the module ordering below):** teach 0001 interactively, or author Module 2 beginning at 0007 if requested. Keep remaining pages unchecked until authored and keep technical proficiency unknown until demonstrated.

## Module ordering update — 2026-10-30

- **User preference:** move local testing to Module 2. The user clarified that pre-built actions should come before security, making pre-built actions Module 7 and security Module 8; agentic workflows and the capstone remain Modules 9 and 10.
- **Actual work:** reordered the curriculum, README module table, home/curriculum/teaching-guide diagrams, module guides, boundary lesson pagination, prerequisites, and the Module 1 teaching handoff. Current lesson IDs, paths, and publication statuses are preserved. The catalog remains at 60 lessons in 10 modules: six authored and 54 placeholders.
- **Current next step:** author local-testing lesson 0007 when requested; teach 0001 interactively if starting the course. The earlier batch-authoring handoff's proposed next lesson 0049 is superseded by this ordering update.
- **Learner evidence:** this is an explicit sequencing preference; no technical mastery is established.
- **Checks executed after the complete documentation batch:** one `task docs:verify` passed: 76 Markdown pages, 614 local links, and 76 Mermaid diagrams (3 newly rendered, 73 reused from cache), 0 errors; incremental Zensical build succeeded with no issues. Verified all 10 module titles/numbers, the exact 60-lesson sequence, unchanged publication statuses, and every previous/next lesson transition. `git diff --check` passed. Workflow/action implementation tests were not repeated because this ordering update changed documentation only.

## Modules 2–5 dedicated authoring threads — 2026-10-30

- **User request:** create a dedicated thread for each of Modules 2, 3, 4, and 5, author all six lessons in each, then run Markdown validation after the complete 24-lesson batch, with no per-lesson validation.
- **Coordination:** four top-level threads share the existing checkout and have disjoint lesson/lab ownership. Only the coordinating thread updates shared curriculum checkboxes/counts, README, home page, source index, and these notes after completed work is collected. No authored status or learner mastery is inferred from a launched thread.
- **Module 2:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:0caaa745-3180-4fbf-80e4-d471e00410d9:teach-modules-2-5-batch-20261030-v1:0> — lessons 0007–0012; handoff `labs/module-2-handoff.md`.
- **Module 3:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:0caaa745-3180-4fbf-80e4-d471e00410d9:teach-modules-2-5-batch-20261030-v1:1> — lessons 0055–0060; handoff `labs/module-3-handoff.md`.
- **Module 4:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:0caaa745-3180-4fbf-80e4-d471e00410d9:teach-modules-2-5-batch-20261030-v1:2> — lessons 0013–0018; handoff `labs/module-4-handoff.md`.
- **Module 5:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:0caaa745-3180-4fbf-80e4-d471e00410d9:teach-modules-2-5-batch-20261030-v1:3> — lessons 0019–0024; handoff `labs/module-5-handoff.md`.
- **Validation barrier:** every authoring thread deferred link, Mermaid, and site-build validation. After all four threads finish, the coordinator integrates shared status/source updates, runs relevant executable checks, then runs one whole-site `task docs:verify`. Launch-time course counts were six authored and 54 placeholders; confirmed integration now brings the course to 30 authored and 30 placeholders.
- **Current state:** complete. All four module handoffs and final thread results were collected; all 24 requested lessons and isolated labs are authored. Shared curriculum/status/source updates, the lab index, and module-specific host/lint commands are integrated. Course totals are 30 authored lessons, zero starters, and 30 placeholders. No authoring blocker or technical learner mastery is claimed.
- **Module 2 evidence:** authored 0007–0012 and 40 isolated lab files; 16 function/process tests, five positive workflow lint checks, Task/cache and host exercises passed. Deliberate negative cases failed as expected. Both act event listings succeeded but no workflow execution occurred. Image/act runtime is deferred because Podman is stopped/refuses connection; ShellCheck and zizmor are absent. Details and exact primary URLs are in `labs/module-2-handoff.md`.
- **Module 3 evidence:** authored 0055–0060, isolated labs, a local release candidate, and its module guide; metadata probe (5 cases), Node suite (7 tests), Docker host contract (11 cases), TypeScript/distribution/package checks, and five inactive consumer lint checks passed. Image/act execution is deferred because Podman refused connection. Details are in `labs/module-3-handoff.md`.
- **Module 4 evidence:** authored 0013–0018 and 41 isolated lab files; 11 host process cases, six interruption tests, four review tests, positive/negative probes, shell syntax, all 19 Python source compilations, and four inactive consumer lint checks passed. Image/build/cache/mount/stop/act, digest/scan, and hosted evidence remain deferred because Podman refused connection. Details are in `labs/module-4-handoff.md`.
- **Module 5 evidence:** authored 0019–0024 and isolated labs; 46 focused tests, TypeScript/distribution checks, mutation/drift experiments, and two inactive recipe lint checks passed. Toolkit packages are absent; runnable dependency-free adapters and clearly unexecuted Toolkit reference excerpts are used. Details are in `labs/module-5-handoff.md`.
- **Shared integration:** `task test:labs` runs Module 2–5 host suites, while `task lint:labs` selects 23 syntax-valid recipes across Modules 1–5. Expected-negative workflow fixtures are excluded from positive lint lists. Narrowed the Module 1 staging linter to `0001`–`0006` recipes so new Module 2 Taskfiles and diagnostic YAML are not accidentally included. Existing four-adapter tests and active workflows retain their separate commands.
- **Coordinator checks:** `task test:labs` passed all Module 2–5 host contracts, including the 16/7/46-test Node suites, 11-case Docker host contracts in each of Modules 3 and 4, six interruption tests, four review tests, metadata/packaging probes, type checks, and the asserted mutation/drift failures. `task lint:labs` passed all 23 syntax-valid recipes. `task test` passed TypeScript, distribution consistency, three shared JavaScript tests and four adapter test methods; `task lint:workflows` and `task lint:recipes` passed. Verified all 60 catalog IDs, publication states/checkmarks, and previous/next links. `git diff --check` passed. Logs are under `.tools/teach-modules-2-5-*-checks.log`.
- **One combined documentation pass:** after all 24 lessons and shared edits were complete, `task docs:verify` passed 76 Markdown pages and 654 local links with 0 errors; validated 76 Mermaid diagrams (24 newly rendered, 52 reused from cache), 0 errors; one incremental Zensical build succeeded with no issues. No per-lesson or per-module documentation validator/build was run.
- **Remaining verification boundaries:** container/image/build/cache/mount/stop/act execution remains deferred because the existing Podman engine refused connection; no VM was started. ShellCheck/zizmor and Toolkit packages were absent and were not installed. Real GitHub authorization, output/lifecycle processing, hosted OS matrices, remote API behavior, scans/digests, release/Marketplace writes, and model runs remain explicitly unexecuted. Documentation success does not establish those contracts.
- **Next authoring target:** Module 6, starting at `docs/lessons/0025-composite-action-inputs-and-outputs.md`; live teaching still starts with learner predictions and records only demonstrated understanding.
- **Learner evidence:** the request establishes an authoring/workflow preference; no technical mastery is demonstrated.

## Canonical module order and sequential numbering — 2026-10-30

- **User request:** correct the numbering jumps and use this exact module order. This explicitly supersedes the earlier decision to keep lesson IDs/URLs stable while moving modules.

| Module | Topic | Consecutive lessons |
| --- | --- | --- |
| 1 | Workflow execution and configuration | 0001–0006 |
| 2 | Testing locally with Task and act | 0007–0012 |
| 3 | Docker container actions | 0013–0018 |
| 4 | JavaScript and TypeScript actions | 0019–0024 |
| 5 | Composite actions and reusable workflows | 0025–0030 |
| 6 | Security, reliability, and releases | 0031–0036 |
| 7 | Popular pre-built actions: replace shell glue | 0037–0042 |
| 8 | GitHub Agentic Workflows | 0043–0048 |
| 9 | Create your own GitHub action | 0049–0054 |
| 10 | Production capstone | 0055–0060 |

- **Actual changes:** renumbered pre-built lessons 0049–0054 → 0037–0042, agentic lessons 0037–0042 → 0043–0048, custom-action lessons/labs 0055–0060 → 0049–0054, and capstone lessons 0043–0048 → 0055–0060. Updated filenames, frontmatter, titles, teaching prompts, lesson links, pagination, prerequisites, course diagrams, module guides, README, and lab commands. Authored/placeholder states are preserved.
- **Current lab commands:** `test:module2` / `lint:module2` cover local testing; `test:module3` / `lint:module3` cover Docker; `test:module4` / `lint:module4` cover Node; `test:module9` / `lint:module9` cover custom-action creation. Aggregate `task test:labs` and `task lint:labs` follow that order. Current handoffs are `labs/module-2-handoff.md`, `labs/module-3-handoff.md`, `labs/module-4-handoff.md`, and `labs/module-9-handoff.md`; their identifiers/path references were normalized with an explicit migration note. Original thread receipts and execution history above remain historical.
- **Checks completed:** `task test:labs` passed at the new paths and in module order 2 → 3 → 4 → 9; `task lint:labs` passed all 23 syntax-valid recipes, including the renamed Node workflows and custom-action consumers. Shared action tests, active workflow lint, and existing recipe lint also passed. Verified the exact requested 10-module order, 60 consecutive lesson filenames/titles/frontmatter/catalog IDs, all previous/next links, no forward prerequisites, no obsolete lesson filename references in docs/labs, moved lab directories, and preserved 30 authored/30 placeholder states. `git diff --check` passed.
- **Final documentation batch:** after all renumbering edits, one `task docs:verify` passed: 76 Markdown pages, 658 local links, and 76 Mermaid diagrams (3 newly rendered, 73 reused from cache), 0 errors. One incremental Zensical build succeeded with no issues. All 60 canonical lesson pages are generated; all 24 obsolete lesson routes and their sitemap entries are absent. Current-path checks are logged under `.tools/sequential-numbering-*-checks.log`; the old/new lesson manifest is `.tools/lesson-renumbering-20261030.json`.
- **Learner evidence:** the user specified course sequencing and numbering. No technical mastery is inferred. The next authoring target remains lesson 0025 in Module 5.

## Modules 5–8 dedicated authoring threads — 2026-10-30

- **User request:** create one dedicated `$teach` thread for each of Modules 5, 6, 7, and 8; author all six lessons in each; run Markdown validation only after the whole 24-lesson batch, not on individual lessons.
- **Canonical scope:** Module 5 composite/reusable workflows 0025–0030; Module 6 security/reliability/releases 0031–0036; Module 7 pre-built actions 0037–0042; Module 8 agentic workflows 0043–0048. Keep the corrected consecutive numbering and existing module order.
- **Module 5:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:712b5ab7-a148-4fcb-8bfa-a78f32a67de3:teach-modules-5-8-batch-20261030-v1:0> — lessons 0025–0030; handoff `labs/module-5-handoff.md`.
- **Module 6:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:712b5ab7-a148-4fcb-8bfa-a78f32a67de3:teach-modules-5-8-batch-20261030-v1:1> — lessons 0031–0036; handoff `labs/module-6-handoff.md`.
- **Module 7:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:712b5ab7-a148-4fcb-8bfa-a78f32a67de3:teach-modules-5-8-batch-20261030-v1:2> — lessons 0037–0042; handoff `labs/module-7-handoff.md`.
- **Module 8:** <t3-thread://v2/40e022a1-9b9d-4296-82b4-a3deba1bb57d/thread:mcp:712b5ab7-a148-4fcb-8bfa-a78f32a67de3:teach-modules-5-8-batch-20261030-v1:3> — lessons 0043–0048; handoff `labs/module-8-handoff.md`.
- **Ownership:** each thread owns its six lesson pages, isolated `labs/<lesson-id>/` paths, and one module handoff. Module 7 may update `docs/lessons/prebuilt-actions.md`; Module 8 may update `docs/lessons/agentic-workflows.md`. Shared catalog/counts, notes, README, source index, Taskfile, existing examples, active workflows, validators, and dependencies remain coordinator-owned.
- **Completion and validation:** each thread must save its handoff after all file edits and focused executable checks, then notify this coordinator with `MODULE N AUTHORING COMPLETE`. This resumes integration automatically. All four threads defer every Markdown/link/Mermaid/Zensical validator and `task check`; the coordinator will run one whole-site `task docs:verify` after all 24 pages and shared integration are complete.
- **Current state:** complete authoring and shared integration. All four final handoffs/results were collected: 24 new lessons (0025–0048), 137 isolated lab/source/fixture/receipt files (42/26/37/32 for Modules 5/6/7/8), and the two assigned module guides. Course totals are 54 authored lessons (Modules 1–9), zero starters, and six capstone placeholders (Module 10). Catalog checkboxes, home/README counts, local-testing guide, lab index, source index, and shared Taskfile commands are updated. All 54 authored pages omit creation/thread prompts and coordinator directions. No learner mastery is claimed.
- **Coordinator executable checks:** `task test:labs` passed Modules 2–9 in canonical order; `task lint:labs` passed 44 explicit workflow/schematic recipes across Modules 1–9. Module 7 asserted all 39 expected outcomes with zero unexpected failures, including 30 test methods and 20 exact-pin input contracts; Module 8 ran 13 host commands without an agent. Shared four-adapter tests/type/distribution checks, active workflow lint, and existing example recipe lint also passed. Verified all 60 sequential filenames/frontmatter/titles, the exact ten-module order, 54 checked/6 unchecked entries, boundary pagination, 137 new lab files, and removal of creation prompts. Logs are under `.tools/teach-modules-5-8-*-checks.log` and `.tools/teach-modules-5-8-*-workflows.log`.
- **Final documentation validation:** the ONE combined `task docs:verify`, run only after all four final handoffs and shared edits, passed on its first invocation: 76 Markdown pages, 664 local links, and 76 Mermaid diagrams (26 newly rendered, 50 reused from cache), zero errors. The single incremental Zensical build found no issues and finished in 1.33 seconds. Log: `.tools/teach-modules-5-8-docs.log`. No individual lesson or module documentation check ran. All 54 generated authored lesson pages omit the removed creation/thread headings and prompts; `git diff --check` passed. Remaining authoring target: Module 10, lessons 0055–0060.
- **Latest user correction:** remove lesson-creation and thread prompts from completed lessons. The coordinator removed 30 prompt blocks from existing authored pages (0001–0024 and 0049–0054), retained learner prerequisites, and removed six obsolete documentation-scheduling admonitions and teacher-recording instructions. The teaching guide, teach skill, README, home page, and curriculum now direct session setup to the teaching guide. All four running module threads received this correction before completion. Validation remains deferred to the combined final pass.
- **Cleanup checks:** confirmed the 30 lessons retain their prerequisite headings, every non-prompt fenced example/diagram, and exact pagination. `git diff --check` passed. The skill's supported frontmatter/body passed the generic skill validator in a temporary copy; its existing explicit-invocation extension fields were preserved. No Markdown/link/Mermaid/Zensical validation or site build ran for this cleanup.
- **Execution boundaries:** no hosted workflow dispatch, cloud/release write, `gh aw trial`/`run`, model call, credential change, dependency installation, or infrastructure provisioning is requested. Local compilation and synthetic fixtures must be reported separately from actual agent/platform behavior.
- **Learner evidence:** this is an authoring/workflow preference, not demonstrated technical mastery.

## Project map

- `docs/mission.md`: goals and constraints.
- `docs/lessons/index.md`: the 60-lesson GitHub Actions curriculum and publication status.
- `docs/lessons/teaching-guide.md`: teaching scope, lesson development, and handoff rules.
- `docs/cheatsheet/local-testing.md`: the local-testing workflow and environment setup.
- `examples/`: executable Docker, JavaScript, TypeScript, composite, and agentic examples.
- `Taskfile.yml`: shared local and CI command contract.
- `learning-records/`: learner evidence and explicit course preferences.
