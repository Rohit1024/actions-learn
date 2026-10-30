# Lab 0055: choose a reusable boundary

Work from the repository root. Run `uv run python scripts/test_actions.py` to
observe four existing adapters with the same greeting contract. Those tests
observe programs, not action metadata or a GitHub runner.

Before reading the worked decisions, choose a boundary for each request:

| Request | Your choice and reason |
| --- | --- |
| Install Node 24 and cache npm downloads | |
| Give several repositories the same setup inputs and installed-version output | |
| Validate a component/channel pair and compute a release key | |
| Ship a Linux-only file scanner with its runtime | |
| Run scan/build on separate runners, then join their evidence | |

For your proposed team action, write the input names, defaults, invalid cases,
output names, failed-exit behavior, caller files, permissions, supported runners,
and the smallest useful test. Identify one maintained component you can reuse.

<details>
<summary>Worked decisions</summary>

1. Reuse `actions/setup-node` at a reviewed commit. It already handles runtime
   acquisition and package-manager cache integration.
2. Compose setup-node in a composite. The caller still checks out files, installs
   dependencies, and runs project-specific tests.
3. Implement a focused Node action only when this policy is repeated across
   callers. For one workflow, an explicit repository command may be enough.
4. Consider Docker when the packaged Linux tooling is needed. Python by itself
   does not make a container necessary. Account for image maintenance and startup.
5. Use a reusable workflow: runner selection, job dependencies, and joins belong
   to a workflow. A composite invocation is one step inside an existing job.

The module develops `component=docs`, `channel=preview` into
`release-key=docs-preview`. It performs no release, upload, or API call, needs no
action token, rejects invalid labels, and writes a named output. Docker's separate
file-inspection example demonstrates a packaging boundary rather than replacing
this small Node operation with a container.
</details>

Failure exercise: propose a custom installer that downloads an unversioned Node
archive and extracts it into a hardcoded system directory. List the cache,
platform, integrity, PATH, and update responsibilities you have taken on. Repair
the design by reusing setup-node; do not execute an installer.

No learner answers have been recorded in this worksheet.
