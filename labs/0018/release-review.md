# Docker action release review worksheet

This is an unexecuted release plan. Populate evidence after real checks; a filled
date or unchanged digest cannot substitute for them. No registry push is needed
to complete the local exercises.

| Decision | Evidence to collect | Current lab state |
| --- | --- | --- |
| Consumer contract | Inputs, output, Linux runner and supported architectures | Starter greeting contract; image untested |
| Action source | Reviewed commit and exact source files | Working tree only; no release |
| Base source | Official Images entry, upstream source, chosen tag | `python:3.14-alpine`; mutable teaching base |
| Base identity | Registry index digest plus selected platform manifest digest | Not resolved; do not invent a value |
| Built identity | Image ID for local tests, pushed digest if later published | Not collected |
| Dependencies | Base OS/interpreter SBOM and added dependencies | Python standard-library imports only inventoried |
| Vulnerability evidence | Tool/version, database time, target digest, platform, full findings | Not run |
| Finding decisions | Exposure, fixed version, mitigation, owner, expiry | No findings assessed |
| Behavior | Direct process matrix, image/mount tests, caller output mapping | See module handoff for actual local checks |
| Interruption | Graceful stop, forced kill, partial-result policy | Host evidence only; see lesson 0017 |
| Performance | Machine, engine, platform, cache state, raw build/run samples | No image samples collected |
| Updates | Named owner, review every 30 days and on relevant advisories | Proposed policy; no owner assigned |
| Rollback | Prior tested action commit and matching image digest | Not selected |
| Release decision | Reviewer, accepted risks, unresolved hosted checks | Deferred; no publication authorized |

For a registry-backed action, review both the action commit and the image digest.
For a Dockerfile-backed action, review the base digest and every build input.
Measure cold starts on a disposable clean runner instead of deleting shared
engine caches. Compare the same workload with a Node implementation before
claiming a packaging speed improvement.
