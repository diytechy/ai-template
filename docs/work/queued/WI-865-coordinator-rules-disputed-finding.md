+++
id = "WI-865"
title = "The coordinator's adjudication entry point rules a contested or repeated review finding"
workstream = "process"
specref = "docs/log.d/2026-10-08-owner-ruling-review-threat-model.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 8
needs = ["WI-860"]
+++

## Context

Filed by hand by the coordinator on 2026-10-08 at the owner's direction, splitting the coordinator path out of WI-811 (which absorbed it from the cancelled WI-861 the same day). The owner's ruling ([log.d/2026-10-08-owner-ruling-review-threat-model.md](../../log.d/2026-10-08-owner-ruling-review-threat-model.md)), rule 2: it is the adjudicator's job to make the call on a contested or repeated finding, not the coordinator's by sending every finding back to the builder; its call is final (OI-103 Q3), and a high-risk finding goes to the owner. WI-811 keeps the loop's RESOLVE, a step inside the in-lane sitting WI-809 builds, so it waits behind WI-809; this coordinator path needs neither WI-809 nor WI-805 and should not wait for them. WI-846's lane recorded the gap twice (docs/decisions/wi-846.toml D-006, D-007).

## Done-when

- The coordinator's adjudication entry point (`coordinator_adjudicate.py adjudicate`) carries a dispute brief class: the brief holds each finding as the reviewer wrote it, the builder's or coordinator's position, the lane range it concerns, and the review threat model WI-860 states (by link); the verdict rules each finding FIX, DISMISS (out of scope, refuted, or not worth its cost, with the reason) or ESCALATE (high risk, to the owner), and is validated like the other classes. The class and its verdict grammar are built once, here, for WI-811's loop sitting to reuse.
- The coordinator's in-lane cycle routes to it: a finding the builder or coordinator contests, and any finding class reaching its third review round, goes to the dispute sitting before another build round; the ruling's path is recorded in the lane's decisions record, and a dismissed finding is not re-raised to the builder.
- The coordinator-cycle skill (WI-848, if landed) states the route in place of rules 2 and 3's interim procedure.
- The spine carries the obligation (Terra authors it; an independent adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped brief template is added).
