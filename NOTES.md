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
- Keep navigation at section roots and catalog lessons within their section, with previous/catalog/next links.
- Use primary documentation for current runtime versions and `gh aw` behavior. Treat `gh aw trial` as hosted execution with runner and possible model usage.

## Active state

- **Current starting point:** lesson 0001, the GitHub Actions execution model. The earlier basic-lesson exercises are superseded by the user's course-scope change.
- **Starter content:** 0001 execution model and 0002 local feedback loop; both have prompts for fuller guided sessions.
- **Placeholders:** 58 detailed Actions lesson briefs, 0003–0060.
- **Roadmap:** 60 GitHub Actions lessons across 10 modules; follow catalog order, including new lessons 0049–0054 after 0006 and 0055–0060 after 0012. Checked items track written content, not mastery.
- **Next suggested session:** `/teach 0001`, using `docs/lessons/0001-execution-model.md`. Begin with an event becoming a workflow run, jobs, steps, and runner processes.
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

## Project map

- `docs/mission.md`: goals and constraints.
- `docs/lessons/index.md`: the 60-lesson GitHub Actions curriculum and publication status.
- `docs/lessons/teaching-guide.md`: teaching scope, lesson development, and handoff rules.
- `docs/cheatsheet/local-testing.md`: the local-testing workflow and environment setup.
- `examples/`: executable Docker, JavaScript, TypeScript, composite, and agentic examples.
- `Taskfile.yml`: shared local and CI command contract.
- `learning-records/`: learner evidence and explicit course preferences.
