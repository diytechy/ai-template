+++
id = "WI-861"
title = "The adjudicator rules on a contested or repeated review finding"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 8
needs = ["WI-860"]
+++

## Deliverable

CANCELLED, folded into WI-811 (owner, 2026-10-08): WI-811, filed 2026-10-04 from WI-788's approved design note, already carries the dispute resolution this row asked for (the builder disputes a finding, the adjudicator rules uphold, dismiss or advice, and its call is final). WI-811's Done-when gains this row's new parts: the coordinator entry point's dispute class, the third-round trigger, the recorded and not re-raised dismissal, the threat model as a dismissal reason and the owner escalation, with a `needs` edge on WI-860.

## Context

Filed by hand by the coordinator on 2026-10-08 from the owner's ruling
([log.d/2026-10-08-owner-ruling-review-threat-model.md](../../../log.d/2026-10-08-owner-ruling-review-threat-model.md)),
rule 2: it is the adjudicator's job to make the call on a contested or
repeated finding, not the coordinator's by sending every finding back to the
builder; its call is final (OI-103 Q3) and a high-risk finding goes to the
owner. Today the coordinator entry point (`coordinator_adjudicate.py
adjudicate`) has no brief class for it: WI-846 recorded the gap twice
(docs/decisions/wi-846.toml D-006, D-007). WI-853 (every finding is a clause
the rework plan must cover) meets this row: a finding the adjudicator
dismisses is covered by its dismissal verdict.

## Done-when

- The adjudication route carries a dispute brief class: the brief holds the
  finding as the reviewer wrote it, the builder's or coordinator's position,
  the lane range it concerns, and the review threat model WI-860 states; the
  verdict rules each finding FIX, DISMISS (out of scope, refuted, or not
  worth its cost, with the reason) or ESCALATE (high risk, to the owner), and
  is validated like the other classes.
- The in-lane cycle routes to it: a finding the builder or coordinator
  contests, and any finding class reaching its third round, goes to the
  dispute sitting before another build round; the verdict's path is recorded
  in the lane's decisions record, and a dismissed finding is not re-raised to
  the builder.
- The spine carries the obligation (Terra authors it; an independent
  adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).
