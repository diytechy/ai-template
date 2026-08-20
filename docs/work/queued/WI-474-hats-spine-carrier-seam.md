+++
id = "WI-474"
title = "Declare or re-partition the hats -> spine_carrier seam: the one live strict-architecture ERROR (repo review 2026-08-19 H-03)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Verified 2026-08-19 on this tree: `check_trajectory.py --strict` reports
exactly one ERROR — `cross-component import scripts/hats (CMP-008) ->
scripts/spine_carrier (CMP-006) has no declared IF-### seam`. `hats.py` imports
and consumes `spine_carrier`; the LLR registry assigns the carrier to CMP-006
and hats to CMP-008; no queued or partial WI and no pending open item named
this edge before this row. `docs/status.md` has carried it anonymously as "the
`trajectory` gating red" — this row is that red's owner.

Two honest resolutions, per the review: (a) declare the consuming IF row
(owned by the carrier's design row, LLR-168's side) and cite the contract test
that pins the consumed surface — the precedent is the `gen_arch_map` straddle,
whose single import edge stays policed via IF-117 (see `components.toml`'s
CMP-006 notes); or (b) correct the component assignments if the partition is
wrong. Either way the exit condition is the same: the strict trajectory run
reports zero errors, and the fix is a declaration or a re-partition — never a
suppression. Do not leave the strict job advisory after correction.

Interacts with: WI-472 re-points IF-117's `req_refs` in the same registry
(adjacent rows, no ordering constraint); the wi455 lane owns the broader
interface-contract rework — this row deliberately stays a single-edge fix so
the one hard error does not wait on that program.
