+++
id = "WI-474"
title = "Declare or re-partition the hats -> spine_carrier seam: the one live strict-architecture ERROR (repo review 2026-08-19 H-03)"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Deliverable

Resolved by path (a): the `scripts/hats` → `scripts/spine_carrier` edge is
declared as IF-133 in `docs/requirements/interfaces.toml`, following the
IF-118/119/120/122 carrier-consumption shape (owner LLR-166, carried_by
IF-102, req_refs SR-147, component CMP-008, status Drafted). The partition
was checked and found correct — hats belongs to the round machinery, the
carrier to the registry tier — so no membership was retagged and nothing
was suppressed. The consumed surface (`load_needs`/`resolve`/
`NEED_CARRIERS`/`stem`/`folded`) had no consumer-side contract test, so two
were added to `tests/test_hats.py` and both were driven negative under a
simulated direct-`tomllib` read: an unreadable needs registry must refuse
rather than audit as zero needs, and the legacy `.md` carrier must still
reach the worksheet. `hats.py` gained its `Contracts: IF-133` docstring
line per the established convention. The watermark rose IF 132 → 133 and
the approval snapshot was re-taken, so live and `last_approved` are
byte-identical. `check_trajectory --strict` now exits 0 with zero errors;
the residual warnings are the undeclared hats→plan_briefs Provides seam and
the uncited-seam count, both named and left to the wi455 lane.

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
