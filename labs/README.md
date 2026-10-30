# Local learning labs

Modules 1–4 and 9 have authored reference lessons and developed local exercises. Lesson IDs and lab paths follow the consecutive curriculum order below. All commands run from the repository root with the installed project dependencies.

| Module | Lessons and lab directories | Local checks |
| --- | --- | --- |
| 1 · Workflow execution and configuration | `0001`–`0006` | `task lint:module1` and the direct exercises below |
| 2 · Testing locally with Task and act | `0007`–`0012` | `task test:module2` and `task lint:module2` |
| 3 · Docker container actions | `0013`–`0018` | `task test:module3` and `task lint:module3` |
| 4 · JavaScript and TypeScript actions | `0019`–`0024` | `task test:module4` and `task lint:module4` |
| 9 · Create your own GitHub action | `0049`–`0054` | `task test:module9` and `task lint:module9` |

Run `task test:labs` for all Modules 2–4 and 9 host suites and `task lint:labs` for the 23 syntax-valid recipes across Modules 1–4 and 9. These tasks do not run documentation validation, start a container engine, execute hosted workflows, or publish a release. The existing `task test` continues to check the four shared example adapters.

Some diagnostic workflows deliberately fail static analysis. Lint tasks use explicit positive file lists; do not replace them with an all-YAML glob. A syntax-valid workflow can still contain an intentional output-mapping defect, which the execution exercise must detect.

Host checks remain separate from image, mount, act, and GitHub evidence. Podman was stopped/refused connection during authoring, so container execution is deferred in the lessons and handoffs. Toolkit, ShellCheck, and zizmor packages/tools were not installed as part of authoring. Module 4 uses runnable standard-library adapters alongside explicitly unexecuted Toolkit references. Release candidates are local exercises.

The module handoffs record the exact author-run checks, primary source URLs, and outstanding boundaries:

- [Module 2 handoff](module-2-handoff.md)
- [Module 3 handoff](module-3-handoff.md)
- [Module 4 handoff](module-4-handoff.md)
- [Module 9 handoff](module-9-handoff.md)

## Module 1 exercises

Run commands from the repository root using the existing installed dependencies. The six authored lessons live under `docs/lessons/0001-*.md` through `0006-*.md`. These exercises introduce Actions behavior rather than standalone shell or programming lessons.

All workflow recipes here are **inactive**: GitHub only registers workflow files under `.github/workflows/`. Local scripts use temporary files and require no credentials or container daemon.

| Lesson | Host exercise | Expected evidence |
| --- | --- | --- |
| 0001 | `uv run python labs/0001/processes.py` | Two shells share a file but not an export |
| 0002 | `uv run python labs/0002/probe.py` | Real Node adapter writes the expected named result |
| 0003 | `uv run python labs/0003/read_event.py pull_request labs/0003/pull_request.json` | PR base and head from a minimal fixture |
| 0004 | Inspect `0004/module1-conditions.yml`; optional `act` command is in the lesson | Typed flag and failure-status predictions |
| 0005 | `uv run python labs/0005/inspect_output.py` | Log text and output-file records are separate channels |
| 0006 | `uv run python labs/0006/gate.py --worker success --review success` | Required evidence policy returns READY |

Deliberate negative cases exit **1**. Run them separately so their expected failures do not obscure later commands:

```bash
uv run python labs/0002/probe.py --expect 'Hello Ada'
uv run python labs/0003/read_event.py pull_request labs/0003/dispatch.json
uv run python labs/0005/inspect_output.py --stdout-only
uv run python labs/0006/gate.py --worker success --review skipped
```

The fixture reader inspects payloads; it does not simulate trigger filters. The gate applies an evidence policy; it does not simulate scheduling. The output inspector only reads the existing action's single-line contract; it is not a general environment-file parser.

## Check the complete workflow batch

```bash
task lint:module1
task test
task lint:workflows
```

`lint:module1` stages all seven recipes in a temporary `.github/workflows/` directory and exposes the existing example actions through a symlink. It runs the already installed actionlint against the real local action and reusable-workflow interfaces, then removes the staging directory. No recipe is installed into this repository's active workflows.

The reusable caller and callee must retain the names `module1-caller.yml` and `module1-reusable.yml`. To try them on GitHub, use a learning repository containing the relevant `examples/` and `labs/` files, copy the selected recipes into its `.github/workflows/`, and commit them. Manual dispatch requires the workflow to exist on the default branch. The event-selection recipe additionally has real push/PR triggers, so installing it changes automatic execution.

Selected optional `act` commands are provided in the lessons. They need a running Docker-compatible engine and may download runner images or action sources. The reusable-workflow pair is statically checked here; a hosted call remains integration evidence to collect deliberately.

After finishing a documentation authoring batch, run `task docs:verify` once. The checks cover site links, cached Mermaid rendering, and an incremental Zensical build. Host exercises, static linting, local workflow execution, and hosted platform checks establish different claims.
