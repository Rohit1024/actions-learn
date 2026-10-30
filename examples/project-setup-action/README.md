# Our own project setup action

This composite action turns an existing setup action into a repository-specific interface with declared inputs and an installed-version output. It contains no shell script.

The caller must check out a project containing the lockfile named by `cache-dependency-path`. The action configures Node and its npm download cache. The caller then runs its dependency installation and tests; a cache hit does not supply an installed `node_modules` directory.

See `examples/own-action-consumer.yml` and `docs/lessons/create-your-own-action.md`. The Docker, JavaScript, TypeScript, and script-based composite examples remain available for behavior that needs custom implementation.

For a standalone release, put this `action.yml` at the root of an action repository, add its README and license, and test a real consumer pinned to the reviewed release commit. The published course repository contains multiple examples; it is not itself a single-action Marketplace package.
