+++
id = "WI-280"
title = "Bounded core decomposition — characterize state transitions, introduce typed session/train/route value objects, isolate pure decisions from Git/subprocess effects, and split gen_trajectory.py into parse/graph/view-model/render modules; the module-size ratchet (WI-279-adjacent) is the growth sensor while this is deferred; subsumes the retired WI-082 (bootstrap.py main() decomposition) as a concrete first slice; Modules owned (named so docs/dupes-allow can charge blocks here and tests/test_dupes_census_audit.py can verify it): agent_dispatch.py's train disposition arms and gen_trajectory.py's graph/render layer."
workstream = "scripts"
needs = ["~WI-226"]
specref = "docs/repo-review-2026-07-22.md#h-2--core-module-and-function-complexity-remains-beyond-maintainable-review-scale"
buildtier = "strong"
safety_class = "ordinary"
order = 277
+++
