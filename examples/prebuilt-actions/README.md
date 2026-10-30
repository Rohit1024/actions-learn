# Pre-built actions recipes

These are inactive workflow examples. GitHub does not execute YAML under `examples/`; copy a chosen recipe into `.github/workflows/` only when you intend to enable its events and effects.

- `ci.yml`: use `dorny/paths-filter` to select Node and documentation jobs; use maintained setup/cache and artifact actions instead of change-detection, installation, archive, and upload scripts. Manual dispatch runs both branches. A pull request uses path-based selection.
- `container-build.yml`: use Docker's Buildx, metadata, and build actions, then upload an OCI archive. It builds an image without logging into a registry or pushing it.
- `release-please.yml`: propose release PRs and releases using the verified Google publisher's action. This template needs repository write permissions, suitable release configuration, and deliberate activation; it is not executed by adding this examples directory.
- `../own-action-consumer.yml`: call our own `project-setup-action`, a composite action built by composing a pinned setup action without adding shell logic.

Action release tags and upstream commit SHAs were checked on 2026-10-30. See `docs/references/actions-snapshot.json` and the pre-built action guide for the dated popularity and publisher evidence.

Run `task lint:recipes` for static workflow validation and `task test` for the existing application/action contracts. These checks do not prove remote action execution, fork permissions, artifact service behavior, registry identity, or release writes. Use a reviewed GitHub run for those boundaries.

The `run` commands left in the recipes install project dependencies, test the project, or build its output. Setup actions configure tools and caches; they do not substitute for application work. The npm cache stores download data, so `npm ci` still runs.
