<img src="docs/assets/github-actions-logo.svg" width="64" height="64" alt="GitHub Actions learning badge">

# Learn GitHub Actions

Learn to design, build, test, secure, and operate GitHub Actions through **60 lessons across 10 modules**. Start with workflow execution and local testing, build custom actions, then study maintained pre-built actions, security, and production orchestration. Test locally before spending hosted runner minutes.

**[Learning site](https://rohit1024.github.io/actions-learn/)** · **[Curriculum](docs/lessons/index.md)** · **[First lesson](docs/lessons/0001-execution-model.md)** · **[Local testing guide](docs/cheatsheet/local-testing.md)**

## What the course covers

| Module | Lessons | Focus |
| --- | --- | --- |
| Workflow execution and configuration | 0001–0006 | Events, runners, jobs, steps, expressions, outputs, and dependencies |
| Local testing | 0007–0012 | Task, actionlint, fixtures, container checks, and selected `act` runs |
| Create your own GitHub action | 0055–0060 | Choose a runtime, define action metadata, test a consumer, and prepare a release |
| Docker container actions | 0013–0018 | Metadata, images, entrypoints, mounts, failure handling, and releases |
| JavaScript and TypeScript actions | 0019–0024 | Node, the Actions Toolkit, tests, bundling, and versioning |
| Composite actions and reusable workflows | 0025–0030 | Reuse boundaries, input/output contracts, and workflow composition |
| Popular pre-built actions | 0049–0054 | Select maintained actions, verify publishers, and replace repeated shell glue |
| Security, reliability, and releases | 0031–0036 | Token permissions, OIDC, provenance, artifacts, and diagnostics |
| GitHub Agentic Workflows | 0037–0042 | Compilation, engines, tool boundaries, constrained outputs, and evaluation |
| Production capstone | 0043–0048 | Verified workers, orchestration, release gates, and an operating playbook |

Follow the module order above; lesson IDs preserve existing URLs. Modules 1–5 contain 30 authored reference lessons with [local labs](labs/README.md); the remaining 30 pages in Modules 6–10 are detailed teaching briefs for future sessions. There are no starter pages. Written lesson status and demonstrated learner understanding are tracked separately. Supporting syntax is explained within the relevant Actions example.

Explore the [pre-built action module](docs/lessons/prebuilt-actions.md), [29-action catalog with dated stars and publisher evidence](docs/references/prebuilt-actions.md), and [create-your-own-action module](docs/lessons/create-your-own-action.md).

## Start locally

Install **uv, Node.js 24, Go, and Task v3** using the [setup guide](docs/cheatsheet/local-testing.md#install-the-host-tools), then run:

```bash
git clone https://github.com/Rohit1024/actions-learn.git
cd actions-learn
task setup
task check
task docs:serve
```

`task setup` installs the locked dependencies and local tooling. `task check` validates action behavior, workflow syntax, TypeScript bundle consistency, documentation links, diagrams, and the site build. `task docs:serve` prints the local site URL.

## Choose a local check

| Command | Purpose |
| --- | --- |
| `task test` | Test all four action adapters directly on the host |
| `task lint:workflows` | Check active workflow syntax and expressions with actionlint |
| `task lint:recipes` | Check inactive workflow recipes and their local composite action interface |
| `task lint:module1` | Check all seven inactive Module 1 workflows and local reusable-call interfaces |
| `task lint:labs` | Check all 23 syntax-valid workflow recipes across Modules 1–5 |
| `task test:labs` | Run the Module 2–5 host lab suites, without documentation or container execution |
| `task docs:verify` | Check documentation links and diagrams, then build the site |
| `task actions:build` | Rebuild the TypeScript action's committed distribution file |
| `task test:container` | Build and test the Docker action's image and output mount |
| `task act:smoke` | Run the dedicated workflow smoke job locally |
| `task agentic:check` | Compile the agentic example without executing an agent |

Container checks need a running Docker-compatible engine; the selected workflow smoke run also needs `act`. Agentic compilation needs the GitHub CLI and `gh aw` extension. See the [local testing guide](docs/cheatsheet/local-testing.md) for setup and the remaining checks that need GitHub.

## Navigate the workspace

- [Mission](docs/mission.md)
- [60-lesson GitHub Actions curriculum](docs/lessons/index.md)
- [Start with the GitHub Actions execution model](docs/lessons/0001-execution-model.md)
- [Teaching and thread handoff guide](docs/lessons/teaching-guide.md)
- [Runnable action labs](docs/lessons/action-labs.md)
- [GitHub Agentic Workflows lab](docs/lessons/agentic-workflows.md)
- [Debugging guide](docs/debugging/index.md)

In an agent workspace that supports the bundled teach skill, start with `/teach 0001`. Each lesson provides an exact file target and a prompt for its guided session, including predictions, a local experiment, a failure to diagnose, and retrieval questions.

## Site publishing and CI

The site is built with [Zensical](https://zensical.org/). Its GitHub Pages deployment URL is **https://rohit1024.github.io/actions-learn/**. Pages must be supported by the repository's visibility and account plan. Enable **Settings → Pages → Source: GitHub Actions** for the repository; pushes affecting site content on `main` or `master` then run the deployment workflow.

- [Documentation workflow](.github/workflows/docs.yml): validate links, build the site, and deploy the Pages artifact from the main branch. Pull requests build without deploying.
- [Contract checks](.github/workflows/checks.yml): run the shared local checks for relevant action, tooling, and workflow changes.
- [Action smoke workflow](.github/workflows/actions-smoke.yml): manually exercise the action runtimes on GitHub.

Generated files under `site/`, installed dependencies, and local credentials are excluded from version control. `zensical.toml` defines the site URL and navigation.

The agentic example stays under `examples/agentic/`; local compilation does not register it as an active workflow or run a model. `gh aw trial` and `gh aw run` use GitHub infrastructure.
