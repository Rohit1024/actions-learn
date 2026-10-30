---
name: teach
description: Teach GitHub Actions step by step using this workspace’s mission, curriculum, runnable local labs, and learning records.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

# Teaching Workspace

Guide the user through multi-session learning grounded in the workspace state.

## Workspace State

- `docs/mission.md`: The guiding compass and user goals. Ground all teaching here. See [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `docs/lessons/`: Sequential lessons (`NNNN-<slug>.md`). Maintained in `docs/lessons/index.md`.
- `docs/lessons/teaching-guide.md`: The GitHub Actions teaching contract, placeholder expansion rules, and handoff format for separate threads. Read it before developing a lesson.
- `docs/cheatsheet/`: Compressed commands, annotations, and quick references.
- `docs/debugging/`: Diagnostic playbooks with failure sequence diagrams.
- `docs/interview/`: Senior technical and system design question bank.
- `docs/references/`: Official sources (`resources.md`), glossary (`glossary.md`), and reference index (`index.md`). For updates, see [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md) and [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).
- `learning-records/`: ADR-style records of demonstrated user understanding (`NNNN-<slug>.md`). See [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `NOTES.md`: Scratchpad for learner profile and working notes.

## Core Rules

1. **Ground in Mission**: Align every lesson with `docs/mission.md`. If unclear, interview the user first.
2. **High-Trust Knowledge**: Source facts from `docs/references/resources.md`. Verify facts before explaining.
3. **Storage Strength**: Build retention through active recall, desirable difficulty, and hands-on exercises.
4. **Local Feedback**: Use `Taskfile.yml` and `docs/cheatsheet/local-testing.md`. Prefer direct tests and actionlint, then container/act checks when that boundary changes. Explain which remaining contracts require GitHub.
5. **Agentic Boundaries**: Local `gh aw compile --no-emit --strict` validates a specification. `gh aw trial` and `gh aw run` use GitHub infrastructure and may consume model usage; distinguish these from local tests.
6. **Evidence**: Curriculum checkboxes track written lessons. Record mastery only after learner evidence. The starter glossary is reference vocabulary, not a record of demonstrated understanding.
7. **Teaching Scope**: Start directly with GitHub Actions at lesson 0001. Prefer maintained pre-built actions for standard platform operations, using the dated action catalog for publisher and popularity evidence. Create custom actions when a reusable interface or domain behavior requires them. Keep explanations grounded in workflows and custom actions; introduce YAML, shell, language, or API details only when the current example needs them. Check linked Actions prerequisites and actual learner evidence. The learner has excluded standalone Linux and general programming lessons.
8. **Interactive Pace**: Teach one small concept at a time. Ask for predictions, pause for exercises, and give the learner a chance to answer before revealing solutions.

## Authoring Lessons

1. **Resolve the Existing Page**: Lessons 0001–0060 use `docs/lessons/NNNN-<slug>.md`, starting with `0001-execution-model.md`. Follow the catalog's module order and previous/next links, or the user's exact path, and expand an existing placeholder in place instead of creating a duplicate lesson.
2. **Catalog and Status Updates**: Keep planned lessons unchecked with `lesson_status: placeholder`. Use `starter` for introductory drafts and `authored` after developing the full reference lesson. Check off written lessons in the curriculum; update counts and learner notes. These states do not establish mastery.
3. **Sidebar Rule**: Expose only top-level section roots in `zensical.toml` `nav` (e.g. `{ "Lessons" = ["lessons/index.md"] }`). Keep individual lessons cataloged inside `docs/lessons/index.md`.
4. **Bottom Pagination**: Include navigation linking `Previous Lesson | All Lessons (index.md) | Next Lesson`. Update the previous lesson's "Next" link when adding a lesson.
5. **Visual Diagrams**: Include vertical Mermaid diagrams in every lesson and debugging guide.
6. **Zensical Styling**: Use admonitions (`!!! note`, `!!! tip`), code annotations, and copy buttons.
7. **Future-Thread Handoff**: Read mission, NOTES, the teaching guide, and prerequisite pages at the start of a thread. At handoff, persist actual work, learner evidence, executed/deferred checks, open questions, and the next lesson in NOTES and justified learning records. The prompt on each lesson page identifies its exact target file.

## Authoring Reference & Debugging Guides

- Cheatsheets: `docs/cheatsheet/`
- Debugging Playbooks: `docs/debugging/` (include failure sequence diagrams)
- Interview Questions: `docs/interview/`
- Catalog all guides in their section `index.md` with bottom pagination tables.

## Mermaid Standards & Verification

### Layout Standards
- **Orientation**: Default to `flowchart TD` (top-to-bottom).
- **Subgraphs**: Stack parallel architectures vertically (`SubA ~~~ SubB`) to maintain readable node widths.
- **Quoted Labels**: Quote node labels with special characters (e.g., `Node["Item (Details)"]`).

### Verification Steps
Run automated verification before completing your turn:

1. Validate Mermaid diagrams (must report 0 errors). Successful renders are cached by diagram content and tool versions; unchanged diagrams do not start Node or a browser:
   ```bash
   uv run python .agents/skills/teach/scripts/validate_mermaid.py
   ```
   For a focused edit, append the changed Markdown paths to that command. Use `--force` to re-render every selected diagram when changing validator/dependency configuration or investigating a rendering problem. Never install dependencies or invoke `npx` during validation; use the project's locked local dependencies installed at setup.
2. Check links with `uv run python scripts/check_docs.py`, and run `task test` / `task lint:workflows` when executable action or workflow code changes. Link checking still covers the whole site so incoming links to renamed or removed headings are checked.
3. Validate the documentation build once after all edits, using the incremental build:
   ```bash
   uv run zensical build
   ```
   In this project, `task docs:verify` runs the three documentation checks together. Use `task docs:build:clean` for a clean publishing check; routine edits do not need a clean rebuild or action/container tests unless their code changed.
4. Report completion summary:
   - Number of Mermaid diagrams checked, newly rendered, and reused from cache (0 errors).
   - Zensical build status.
