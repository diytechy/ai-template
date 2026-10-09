+++
id = "WI-865"
title = "The coordinator's adjudication entry point rules a contested or repeated review finding"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 8
needs = ["WI-860"]
+++

## Deliverable

The coordinator's adjudication entry point carries a `dispute` brief class on the shared composition, binding, verdict and telemetry path (`coordinator_adjudicate.py adjudicate --brief dispute`). Its brief holds each contested finding and the builder's or coordinator's position verbatim (a strict TOML findings file: `range` plus `[[finding]]` tables of exactly `id`, `held_by`, `finding`, `position`), the lane range's git facts, and the review threat model by link to PROCESS.md §6. One strict per-line parser (`kitlib/dispute.py`) accepts only a verdict ruling each requested finding once as FIX, DISMISS (`out-of-scope`, `refuted` or `not-worth-cost`, with a reason) or ESCALATE, and refuses anything unruled, duplicate, unrequested or malformed; an accepted dispute verdict authorizes no approval act. The class and grammar are built once for WI-811's loop sitting to reuse. The session-protocol skill routes a contested or third-round finding to the dispute sitting before another build round (WI-848 relocates the route). The dispute brief joins `FINDING_JUDGING_BRIEFS`, and `dispute` joins this repo's `retain_for`. Rows: SR-233, LLR-311 and TC-332 re-attested (the dispute brief joins the finding-judging set); SR-234, LLR-315 approved (verdict 001); LLR-314, TC-334 approved (verdict 002, after the exact-key tests were added in the lane); IF-290 Drafted. Codex 6.1 Sol: the fresh full-lane review SOUND (`bf3498ec`, at medium; `docs/reviews/wi-865-coordinator-rules-dispute/sol-review-full.md`). Decisions: `docs/decisions/wi-865.toml` (D-001, D-002).

## Context

Filed by hand by the coordinator on 2026-10-08 at the owner's direction, splitting the coordinator path out of WI-811 (which absorbed it from the cancelled WI-861 the same day). The owner's ruling ([log.d/2026-10-08-owner-ruling-review-threat-model.md](../../../log.d/2026-10-08-owner-ruling-review-threat-model.md)), rule 2: it is the adjudicator's job to make the call on a contested or repeated finding, not the coordinator's by sending every finding back to the builder; its call is final (OI-103 Q3), and a high-risk finding goes to the owner. WI-811 keeps the loop's RESOLVE, a step inside the in-lane sitting WI-809 builds, so it waits behind WI-809; this coordinator path needs neither WI-809 nor WI-805 and should not wait for them. WI-846's lane recorded the gap twice (docs/decisions/wi-846.toml D-006, D-007).

## Done-when

- The coordinator's adjudication entry point (`coordinator_adjudicate.py adjudicate`) carries a dispute brief class: the brief holds each finding as the reviewer wrote it, the builder's or coordinator's position, the lane range it concerns, and the review threat model WI-860 states (by link); the verdict rules each finding FIX, DISMISS (out of scope, refuted, or not worth its cost, with the reason) or ESCALATE (high risk, to the owner), and is validated like the other classes. The class and its verdict grammar are built once, here, for WI-811's loop sitting to reuse.
- The coordinator's in-lane cycle routes to it: a finding the builder or coordinator contests, and any finding class reaching its third review round, goes to the dispute sitting before another build round; the ruling's path is recorded in the lane's decisions record, and a dismissed finding is not re-raised to the builder.
- The coordinator-cycle skill (WI-848, if landed) states the route in place of rules 2 and 3's interim procedure.
- The spine carries the obligation (Terra authors it; an independent adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped brief template is added).

## Adjudication follow-ups, answered in this lane

The first sitting (`docs/reviews/wi-865-coordinator-rules-dispute/001-ADJUDICATE-48c33dd.md`) blessed and re-anchored SR-233, LLR-311 and TC-332, approved SR-234 and LLR-315, and returned LLR-314 and TC-334 on one clause: no test drove a finding's exact-four-keys rule. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), it is answered here: a finding with an extra key and a finding missing each of `id`, `held_by`, `finding` and `position` refuse the brief by name (`f309fb31`; red with each check weakened), and TC-334's Method and Expected name them. LLR-314's Detail now states the newline handling exactly (every leading and trailing newline character is removed; spaces and interior lines are kept). The re-sit judges LLR-314 and TC-334 for first approval.
