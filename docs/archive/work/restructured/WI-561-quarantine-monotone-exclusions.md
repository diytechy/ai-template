+++
id = "WI-561"
title = "The quarantine spares what is monotone or record: the id watermark, docs/reviews, docs/log.d (OI-76 / plan 2.6)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Restructured into WI-581.

## Context

Commissioned by `OI-76`'s ruling (plan section 2.6, findings N and the
zero-rounds hole). The bar-inert revert took `docs/id-watermark` back with
the product diff (`IF 174 -> 173`) — a mark only ever rises, so the
reverted tree could never pass registry-integrity and the run stopped on
the very artifact built to be inert. The same revert deleted the lane's
review evidence: `WI-540` is the one merged row on trunk with zero round
files, and its disposition adjudicator judged a close whose review it could
not read.

## Done-when

1. `dispatch._refresh_or_quarantine`'s revert excludes `docs/id-watermark`
   (and anything else monotone by contract): a minted id is burned whether
   or not its row survives, and the reverted tree passes
   registry-integrity.
2. The revert preserves `docs/reviews/` and `docs/log.d/` as record paths,
   the way it already preserves the handback report — evidence of what
   happened survives the reverting of what was done.
3. Tests drive both exclusions on a scaffold quarantine.
