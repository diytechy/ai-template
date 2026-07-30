+++
id = "WI-280"
title = "Bounded core decomposition — characterize state transitions, introduce typed session/route value objects, isolate pure decisions from Git/subprocess effects, and split gen_trajectory.py into parse/graph/view-model/render modules; the module-size ratchet (WI-279-adjacent) is the growth sensor while this is deferred; subsumes the retired WI-082 (bootstrap.py main() decomposition) as a concrete first slice; Modules owned (named so docs/dupes-allow can charge blocks here and tests/test_dupes_census_audit.py can verify it): gen_trajectory.py's graph/view-model/render layer and bootstrap.py's main(). RE-SPECIFIED 2026-07-29 (owner ruling): the train half of the original scope — agent_dispatch.py's disposition arms and the typed train objects — was DELETED whole at concurrency-restructure Phase 5, so it left this row's scope as removal, not decomposition; measured sizes at the re-spec: gen_trajectory.py 4574 / bootstrap.py 1919 / agent_loop.py 2836 lines (whether agent_loop joins the owned set is the claimer's first design call)."
workstream = "scripts"
needs = ["~WI-226"]
specref = "docs/repo-review-2026-07-22.md#h-2--core-module-and-function-complexity-remains-beyond-maintainable-review-scale"
buildtier = "strong"
safety_class = "ordinary"
order = 277
+++
