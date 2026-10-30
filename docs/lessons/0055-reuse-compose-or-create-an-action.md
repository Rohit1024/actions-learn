---
icon: lucide/book-open
lesson_id: "0055"
lesson_status: authored
---

# 0055 · Decide when to reuse, compose, or create your own action

!!! note "Authored reference lesson"
    This starts Module 3's complete creation path. Predict each decision before opening its worked explanation. The lesson and assistant-run checks establish available material, not learner mastery.

## Prerequisites and goal

Read [0012 · Local and hosted coverage](0012-local-hosted-coverage-and-usage-budget.md) and the [module guide](create-your-own-action.md). Recall [0001's execution boundaries](0001-execution-model.md): a workflow owns jobs, a job selects a runner, and a step either runs a command or calls an action. If a repeated step sequence needs a second runner, the reuse boundary has changed.

By the end, you should be able to choose a maintained action, a composite, a Node action, a Docker action, or a reusable workflow for a concrete request. Your evidence is a written caller contract and an explanation of the cheapest check that can observe it. All commands on this page run from the repository root with the [existing host tools](../cheatsheet/local-testing.md).

## Begin with a caller requirement

An **action** is a reusable unit invoked by a job step. Creating one introduces a public interface and a maintenance obligation: callers depend on its names, defaults, outputs, failure behavior, and runtime files. A short script that only one workflow uses can remain an explicit project command. Wrapping it becomes useful when several callers need a stable policy or reusable behavior.

Before implementing anything, write one sentence describing the caller's need. For example: “Every repository should select Node 24, restore npm's download cache using its lockfile, and receive the installed version.” Runtime installation is already maintained by `actions/setup-node`; our own contribution can be the narrower team interface. GitHub's [building-block guide](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions) explains how callers reference actions.

The [dated catalog](../references/prebuilt-actions.md) is a discovery aid. Check task fit and upstream input/output metadata before choosing a component. Popularity is dated evidence, and a verified creator badge identifies the publisher; neither establishes that the code meets your contract. This module reuses the existing reviewed full commit references instead of silently updating them.

```mermaid
flowchart TD
    Need["Write the caller requirement and observable result"] --> Existing{"Does a maintained action satisfy it?"}
    Existing -->|"Yes"| Reuse["Reuse its reviewed interface"]
    Existing -->|"Needs a team policy"| Boundary{"Must the reusable unit own jobs or runners?"}
    Boundary -->|"Yes"| Workflow["Use a reusable workflow"]
    Boundary -->|"No"| Behavior{"Is new domain behavior required?"}
    Behavior -->|"No"| Composite["Compose existing actions inside one job step"]
    Behavior -->|"Yes"| Runtime["Choose Node or a justified Linux container runtime"]
    Reuse --> Contract["Document caller inputs, outputs, errors, and test limits"]
    Workflow --> Contract
    Composite --> Contract
    Runtime --> Contract
```

!!! tip "Prediction"
    A team asks for checkout, setup, build, and test on Ubuntu plus a separate Windows job. Can one composite action choose both runners? What would its caller have to own?

??? tip "Worked prediction"
    Each composite invocation runs inside one existing job. The caller can invoke it separately in an OS matrix, or a reusable workflow can own the jobs and matrix. A composite's metadata cannot create an independent Windows job. Choose a reusable workflow when the reusable contract includes that orchestration.

## Choose the boundary deliberately

| Need | First useful choice | Responsibility you still own |
| --- | --- | --- |
| Install Node and cache npm downloads | Maintained `actions/setup-node` | Reviewed inputs, lockfile, dependency installation, and tests |
| Standardize setup inputs across repositories | Composite around setup-node | Public defaults and mappings; dependency updates |
| Validate a repeated component/channel naming policy | Small Node action | Domain validation, process adapter, packaged JavaScript |
| Ship a specific Linux scanner and runtime together | Docker action | Base image, tool versions, image startup, mount and process tests |
| Reuse runner selection, job dependencies, and evidence joins | Reusable workflow | Job-level inputs, permissions, outputs, and orchestration |

A **composite** packages steps in the caller's job. A **reusable workflow** is called at the job level and can contain multiple jobs. GitHub's [comparison in the composite tutorial](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action#composite-actions-and-reusable-workflows) describes these distinct scopes. An action does not declare its own trigger or job-level token permissions.

A **Node action** executes JavaScript selected by metadata. TypeScript can author that implementation, but the consumer runs JavaScript. A **Docker action** packages a Linux process in an image; the runner still supplies arguments, workspace mounts, output files, and status handling. Python existing on the host is not by itself a reason to introduce a container. Use one when consistent Linux tooling or dependencies justify its cost.

## Inspect the existing examples before adding code

Open `examples/project-setup-action/action.yml`. Its useful team interface is two inputs, `node-version` and `cache-dependency-path`, and the `node-version` output. Internally, it calls setup-node. The caller still owns checkout and project commands:

```yaml title="Existing caller excerpt; complete recipe: examples/own-action-consumer.yml"
- uses: ./examples/project-setup-action # (1)!
  id: project
  with:
    node-version: '24'
    cache-dependency-path: package-lock.json
- run: npm ci # (2)!
- run: npm test
```

1. This path resolves from the checked-out workspace. The complete recipe runs checkout first; the excerpt is not a complete workflow.
2. Restoring npm download data does not install `node_modules` or execute the project's dependency installation. Keeping this command in the caller makes project behavior visible.

Now run the existing four-adapter comparison:

```bash
uv run python scripts/test_actions.py
```

Expected: four test methods report `ok`, followed by `OK`. Their subcases exercise the JavaScript, bundled TypeScript, Python entrypoint, and composite script directly. They verify equivalent greeting output, invalid inputs, append behavior, and missing-output errors. They do not invoke setup-node or execute Docker metadata.

**Prediction:** if all four implementations produce `greeting=Hello, Ada!`, have you proved that four custom runtimes are needed?

??? tip "Worked interpretation"
    Equivalent results expose packaging choices, not a requirement for four implementations. Choose the cheapest maintainable boundary that satisfies actual runtime and portability needs. The Node function is enough for this tiny transformation; the other examples teach interfaces and test layers.

## Lab: write the decision record

Use `labs/0055/decision-record.md`. Its five requests cover reuse, composition, domain policy, Linux tooling, and jobs. Write your decisions before opening its collapsed answer. Then define this proposed action:

> Given a component such as `docs` and a channel such as `preview`, compute `release-key=docs-preview`. Do not upload or publish anything.

Record input names and accepted strings, defaults, invalid cases, output name, exit behavior, caller files, runner assumptions, and required token permissions. Explain whether this is shared policy or merely one caller's command. Later lessons implement that small policy so the public contract can be tested independently of release operations.

??? tip "Worked contract"
    Use `component=docs` and `channel=preview` as defaults. Accept a lowercase ASCII component starting with a letter, at most 32 characters, with remaining characters limited to letters, digits, and hyphens. Accept only `preview` or `stable` for channel. Publish `release-key` after all validation succeeds. Reject empty strings, whitespace, newlines, unknown channels, and malformed labels with nonzero status and no success output. The action needs no token and no caller files. A consumer using a local path needs checkout. A Node implementation can be tested with pure cases plus a real process and temporary output file.

## Break the design, then repair its responsibility

Propose a custom installer that downloads “latest Node,” extracts it into a hardcoded system directory, and assumes every runner has the same architecture. Do not run it. Identify who now maintains integrity checks, platform selection, PATH updates, caching, and new releases.

**Observable design failure:** your proposed installer cannot satisfy the declared cross-repository setup contract without adding responsibilities already owned by setup-node. A successful download on your laptop would not resolve the other cases.

??? tip "Diagnosis and repair"
    Trace the requirement to the existing action's metadata, rather than debugging an installer implementation. Replace installation logic with a reviewed setup-node call. Add a composite only if the narrower team defaults and output mapping are valuable. In 0057, the actual failure becomes a missing caller lockfile; adding an installer fallback would conceal that error instead of fixing the file boundary.

## Transfer and retrieval

A release pipeline needs a Linux scanner, a Windows compatibility check, and a final job that rejects missing evidence. Choose the workflow-level unit and the possible action-level units inside it. State one reason each unit should remain separate.

Answer without reopening the table:

1. What missing requirement justifies a new implementation?
2. When is a composite too small a boundary?
3. Which behavior must remain stable if you replace a Node implementation with Docker?
4. What did the four-adapter host check leave untested?

??? tip "Worked transfer and retrieval"
    A reusable workflow can own runner selection, both jobs, dependencies, and the final gate. The Linux scanner can be a Docker action when its toolchain requires packaging; the Windows check may reuse a maintained action and explicit project commands. A naming policy can remain a small Node action. New code is justified by unmet domain behavior or runtime needs. Public input/output names, accepted values, defaults, failures, and documented platforms remain the compatibility contract. Host tests do not evaluate action metadata, remote downloads, GitHub scheduling, or token policy.

## Verification limits and next lesson

The decision record is a design artifact. The adapter tests give actual process evidence for existing examples; neither establishes that a chosen remote action executed successfully. A reviewed, bounded GitHub consumer remains necessary for platform services and intended runner compatibility. No hosted or model execution is part of this authoring work.

Primary references were checked on **2026-10-30**; exact URLs and executed checks are recorded in `labs/module-3-handoff.md`. Continue to [0056](0056-own-action-metadata-and-contracts.md) to turn the chosen boundary into metadata and executable assertions. In a guided session, record the learner's decisions and explanations only after they supply them.

## Start this lesson in a new thread

```text
/teach 0055

Use docs/lessons/0055-reuse-compose-or-create-an-action.md and
labs/0055/decision-record.md. Read docs/mission.md, NOTES.md,
docs/lessons/teaching-guide.md, the module guide, and lesson 0012.
Ask me to choose each reuse boundary and write the release-key contract.
Pause before worked answers. Explain the limits of the four-adapter check.
Record demonstrated understanding only; hand off to lesson 0056.
```

| Previous Lesson | All Lessons | Next Lesson |
| --- | --- | --- |
| [0012 · Local and hosted coverage](0012-local-hosted-coverage-and-usage-budget.md) | [Curriculum](index.md) | [0056 · Action metadata and contracts](0056-own-action-metadata-and-contracts.md) |
