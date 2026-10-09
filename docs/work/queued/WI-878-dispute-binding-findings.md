+++
id = "WI-878"
title = "A dispute sitting's binding records the findings file it ruled, and the coverage gate reads exactly that file"
workstream = "process"
sr_refs = ["SR-236"]
specref = "project-trajectory/scripts/plan_coverage.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-09 (overnight leg 02) from WI-853's dispute sitting `docs/reviews/wi-853-findings-gate-in-rework/006-ADJUDICATE-349bb13.md`, which ruled Sol's last-gate finding DISMISS not-worth-cost for WI-853 and named this follow-up (`docs/decisions/wi-853.toml` D-006).

`plan_coverage.py` lets an `F#` exclusion that cites an accepted dispute DISMISS resolve the finding only when the ruled finding is shown to be the excluded one. Nothing records which findings file a dispute verdict ruled: the `.requested` binding beside the verdict holds only the brief class, the requested ids and the outcome. So the gate reads every findings file beside the verdict whose ids match the requested ids, and requires all of them to record the excluded finding's text. That fails closed: when two dispute rounds in one lane reuse finding ids (F1, F2) for different findings, a valid cited dismissal is refused (reproduced by Sol at `9cbf1a59`, exit 1). Until this lands, a lane's dispute findings use ids unique within the lane, or the plan excludes the finding with an uncited reason.

## Done-when

- The sitting's binding (written by the entry point at reservation, out of the adjudicator's reach) records the findings file the dispute brief was composed over, and the coverage gate reads exactly that file to show correspondence; it no longer scans sibling files.
- A binding without that record (every dispute bound before this change) fails closed, as today.
- Tests, red first: two dispute rounds in one lane reusing ids, each dismissal cited for its own round's finding, both pass; a citation of round 1's verdict for round 2's same-id finding still refuses; the existing correspondence and refusal cases still hold.
- The rows the change makes untrue are amended in the lane and judged in one combined sitting: SR-232/LLR-310 (the binding), SR-234/LLR-315 (the dispute grammar and brief), LLR-069/TC-069 (the gate), and IF-290's contract.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (shipped scripts change).
