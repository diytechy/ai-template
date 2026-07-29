+++
id = "WI-231"
title = "Integrator regenerates generated artifacts on conflict + WI-keyed registry union merge (2026-07-18 field finding 2)"
workstream = "unattended"
sr_refs = ["SR-063"]
needs = ["~WI-226"]
buildtier = "strong"
safety_class = "high-risk"
order = 228
+++

## Deliverable

On a composition conflict integrate_train now routes through _compose_train, which resolves the conflicts the harness OWNS and continues composition, parking only otherwise. Slice A: a path in the module-level GENERATED_ARTIFACTS set (PROJECT_STATE.html and docs/okf fully generated; docs/architecture.md and docs/status.md block-generated, each keyed to its check.py --check step) resolves by taking OURS wholesale or, for a block file, stripping only in-block conflict hunks (parking if a conflict escapes into hand-authored prose) then re-running the sibling generators IN the integrate worktree via _regenerate_generated. Slice B: a work-items.csv conflict resolves by a WI-ID-keyed 3-way row union (_union_registry/_merge_wi_rows/_ordered_wi_rows) read from the merge index stages - a row changed on one side takes that side, a both-sides edit parks, header from the merged result and rows in base-then-additions order. A distinct integration-regenerated event journals the auto-resolved paths and a run-summary counter tallies it. Regressions: two dashboard-regenerating trains integrate without parking (--check green on the merged tree), disjoint registry rows union, a same-row collision and a mixed generated+source conflict still park, plus block-conflict and row-union units. No C901 baseline change (integrate_train stays 16; new helpers under 10).
