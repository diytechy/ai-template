# 001 — ADJUDICATE (independent) — WI-568 disposition of the WI-508 close

Close under judgement: lane `wi508-architectural-remap` closed **WI-508** as
`partial` (reason "OI-71 RULED (c)"), range `ff29fef8f9..6ba2711078`, split
`keep=[] discard=[]` decided-by-adjudicator, suggested tier `strong`.

## Basis (read, not trusted)

- The range **is already on trunk** (`git merge-base --is-ancestor 6ba2711078 HEAD`
  → yes; it arrived via the sanctioned manual partial-close that WI-555 merged at
  `77270030`). This is the special case OI-71 named — the reviewed content stays
  on trunk and a successor re-seals it, rather than a HELD branch being
  cherry-picked at merge.
- **Live reviewed spine content, confirmed on trunk:** `LLR-203`/`LLR-204`
  `Approved`; `TC-199`/`TC-200` `Drafted` with `verifies = ["LLR-203"]` /
  `["LLR-204"]` (the direct `SR-163` target removed at round 013) and `Expected`
  scoped to the LLR arm. This is the governing round-10 APPROVE state
  (`b8d57e9f`), not an over-claim.
- **The three round-019 MAJORs are all externally discharged:** the two
  `trace.py --approve modified` renderer defects → `WI-554`
  (`docs/archive/work/complete/WI-554-approval-brief-defects.md`, complete); the
  `SR-163` shape → `OI-72` ruled 2026-08-31 and owned by re-scoped `WI-543`
  (`docs/archive/work/complete/WI-543-sr163-verification-tc.md`, complete —
  ships the tolerant reference cell + four-class checker + direct TC).
- **Snapshot degradation risk (the round-3/4 BLOCKER, the hand-rewritten
  `last_approved` bytes) is null:** OI-71 decision 9 measured `intake.py snapshot`
  reproducing the lane's snapshot byte-identical from live state. The current
  snapshot carries `LLR-203`/`LLR-204` `Approved` (matching live); its `TC-199`
  `verifies` still reads `["SR-163","LLR-203"]`, which is normal drift on a
  `Drafted` (unapproved) row, not a laundered attestation.
- **No inbound hard `needs` edge points at WI-508** (grep of queued/active), so the
  supersede re-point strands nothing.

## Findings

- [MINOR] The claimed outcome **PARTIAL is correct** -> the program delivered slices 1–5 in full (SR-163 decomposed, the two-axis blind derivation, the eighteen-family alignment survey, `WI-519`/`WI-520`/`WI-521` filed, `OI-64` raised-and-ruled, the ratchet debt re-owned) and blessed-then-reviewed the four slice-1 rows, but `SR-163`'s full file→requirement join was honestly unscheduled at close and the lane never landed a clean confirming reviewer round on current trunk (round 019 stalled with three MAJORs). It is neither `complete` (a genuine arm was owed) nor a half-close; PARTIAL matches the owner's OI-71 (c) ruling -> keep the outcome PARTIAL; the byte-identical spec moves to `complete/` and the report stays on record as its claim -> @owner
- [MINOR] The `keep=[] / discard=[]` split, punted to the adjudicator, **is honest — resolved KEEP-all** -> the entire range is already merged to trunk via the sanctioned manual partial-close, the reviewed spine content passed the governing round-10 APPROVE and is the honest final state, and the one historical hazard (the round-3/4 snapshot laundering) was measured (OI-71 decision 9) byte-identical to a clean `intake.py snapshot` regeneration, so nothing shippable is quietly left on trunk that should be reverted -> no commit reversion; the successor RE-SEALS the snapshot by regenerating it at its own approval commit rather than trusting the branch bytes -> @owner
- [MINOR] A successor is drafted and it is **not owner-owed** -> every ruling this thread needed is already made (OI-71 the close path, OI-72 the SR-163 shape) and both discharging lanes (`WI-543`, `WI-554`) are complete, so no new owner ruling gates the remaining confirm-and-reseal work; adding an `open_item` would gate the successor against a ruling that does not exist -> mint the successor with no `open_item`, `planmode = single` (a reseal, not a design fork) -> @owner

## Disposition reasoning

The successor's substantive predecessors (`WI-543` SR-163 verification, `WI-554`
renderer defects) are already complete and the reviewed spine content is already
on trunk, so the honest remaining scope is thin: draw the one clean reviewer
round the lane never got on the current tree — the "fresh reviewer round on a
refreshed tree" the report itself lists under *Not delivered* — confirm the four
rows stand in their reviewed state, and regenerate `docs/archive/last_approved`
via `intake.py snapshot` at the successor's own approval commit (never copied
from the branch's snapshot bytes, per OI-71 (c)). It inherits OI-72's SR-163
ruling. `buildtier = quick`: no build and no design remain — the mechanism,
derivation, consolidations, and SR-163 verification all landed elsewhere; this is
confirm-and-reseal, and if the round surfaces something that is what the round is
for.

## Dispositions

```toml
title = "WI-508 spine reseal: one clean reviewer round on current trunk, regenerate last_approved at the approval commit"
workstream = "process"
buildtier = "quick"
safety_class = "spine"
priority = 2
supersedes = "WI-508"
planmode = "single"
```

OUTCOME: PARTIAL successors=1
