+++
id = "WI-963"
title = "The trunk mint never mints an amendment row for a row the merged range already settled"
workstream = "process"
sr_refs = ["SR-174", "SR-228"]
specref = "docs/plans/2026-10-03-s11-in-lane-adjudication.md#42-the-re-mint-trap"
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand by the attended coordinator on 2026-10-20, split from WI-810 by
the owner's ruling (coordinator-2026-10-20 D-009); WI-810's remainder is
cancelled. It is the first build after headless leg 06.

**The defect.** When a lane lands, the trunk mint (`intake._routed_amendments`,
called by `intake_after_merge` from the merge slot's post-merge arm and by
`intake.py sweep` after a coordinator's hand landing) diffs the approved and
routed cells of the spine registries across the merge and mints an
`adjudicate:` row for every row whose text moved. It never asks whether the
lane already judged that change. Since in-lane adjudication (WI-849, WI-912),
a lane amends a row, sits it, and re-attests it in its own act; the row's
Status does not change, so the mint sees changed text and files a redundant
row. The coordinator then closes it "as already settled", citing the act.
That has happened 54 times (WI-785 on 2026-10-03 to WI-959 on 2026-10-20;
`git log --grep="already settled"`), each burning a WI id and a close commit,
and the coordinator-cycle skill carries the workaround as a standing landing
step ("close the re-mint citing the act", SKILL section 4 step 3; recipes
section 3).

**The design** is the S11 plan's section 4.2, never built: drop an amendment
record when an act-ledger entry the merged range added re-attests the row
(`acceptance_record.reattested_between` already reads this) AND the row's
changed cells at the merged tree equal their copies in the approved snapshot
(`docs/archive/last_approved/`) at that same tree. The second test keeps the
mint for a row amended again after its act.

Anchor: LLR-153 (the unified trunk-side intake mint) under SR-174 and SR-228.
WI ids stay trunk-minted (revision 33); this row changes which rows the trunk
mint files, not where ids come from.

## Done-when

- An approved row amended in the merged range, re-attested by an act-ledger
  entry the range added, and whose changed cells at the merged tree equal
  their approved-snapshot copies there, yields no amendment row, at the merge
  slot's post-merge arm and at `intake.py sweep` alike (one shared filter).
- A row re-attested in the range and then amended again after its act still
  yields its amendment row.
- An approved row amended with no act in the range still yields its
  amendment row, exactly as today.
- An act ledger or approved snapshot that cannot be read or parsed at either
  side refuses the mint by name, as `reattested_between`'s refusal already
  does; it is never read as "settled", and nothing is skipped silently.
- A regression replays two real landings that minted a redundant row (WI-926's
  landing `08bbb71b6`, which minted WI-952, and WI-956's, which minted
  WI-959) and mints none of their rows, while a fixture amended after its act
  still mints.
- LLR-153's detail (or a new LLR under SR-174, if the in-lane adjudicator
  rules the rule a separate obligation) states the filter, a TC verifies each
  arm, and the set passes in-lane adjudication.
- The coordinator-cycle skill and its recipes drop "close the re-mint citing
  the act" from the landing steps, in the same lane.
- RESYNC_PACK: one entry anchored at a trunk commit; an adopter's trunk mint
  stops filing rows for amendments its lanes already settled. No data
  migrates.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

- **Producer:** the act ledger (`docs/archive/last_approved/acts.toml`) and the
  approved snapshot are written only by the act turn
  (`coordinator_adjudicate.py act`, the snapshot step) and landed with the lane.
- **Consumers:** `intake._routed_amendments` and, through it,
  `intake_after_merge` (the merge slot) and `intake.py sweep`.
- **Ruling:** an absent, unreadable or malformed ledger or snapshot refuses the
  mint by name (fail closed); a row the filter cannot prove settled is minted.
  The filter only ever removes a row it can prove was judged in the range.
