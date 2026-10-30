# User learning notes and preferences

## Learner profile

- **Author / GitHub handle:** rohit1024.
- **Topic:** GitHub Actions, Docker container actions, JavaScript/TypeScript actions, composite actions, and GitHub Agentic Workflows.
- **Starting proficiency:** not established. Record demonstrated Actions understanding; the requested course scope does not establish programming or Actions mastery.
- **Concrete goal:** develop and debug actions locally to avoid repeated GitHub-runner iteration and unnecessary quota use.

## Teaching preferences

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
- **Placeholders:** 46 detailed Actions lesson briefs, 0003–0048.
- **Roadmap:** 48 GitHub Actions lessons across 8 modules. Checked items track written content, not mastery.
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

## Project map

- `docs/mission.md`: goals and constraints.
- `docs/lessons/index.md`: the 48-lesson GitHub Actions curriculum and publication status.
- `docs/lessons/teaching-guide.md`: teaching scope, lesson development, and handoff rules.
- `docs/cheatsheet/local-testing.md`: the local-testing workflow and environment setup.
- `examples/`: executable Docker, JavaScript, TypeScript, composite, and agentic examples.
- `Taskfile.yml`: shared local and CI command contract.
- `learning-records/`: learner evidence and explicit course preferences.
