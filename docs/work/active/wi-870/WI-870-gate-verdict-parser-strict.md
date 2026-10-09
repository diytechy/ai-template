+++
id = "WI-870"
title = "The merge gate reads a review round's VERDICT line strictly, as filing does"
workstream = "process"
specref = "project-trajectory/scripts/score_reviews.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 6
+++

## Context

Found by WI-852's builder on 2026-10-08 while fixing the final-gate review's filing finding, and probed directly. The verdict gate reads review round files through `score_reviews.parse_verdict` (via `round_entries`), and that parser is lax on lines the gate counts:
- `VERDICT: APPROVED findings=0` reads as APPROVE;
- `VERDICT: APPROVE findings=0.5` reads as APPROVE with 0 findings;
- a `CHANGES-REQUESTED` line followed by an `APPROVE` line reads as APPROVE (the last line wins; two lines are not refused);
- a `NEEDS-HUMAN` line is silently ignored.

WI-852's second full-lane review found the same class in the shared per-line reader itself: `kitlib.sitting`'s token reader collapses duplicate fields into a dictionary and keeps the last, so `VERDICT: APPROVE findings=7 findings=0` reads as zero findings. WI-852 refused it at the attended filing boundary only and left the shared reader unchanged.

WI-852 made the attended filing boundary strict through `kitlib.sitting`'s per-physical-line reader (WI-841's "one verdict parser"), but left the gate unchanged because its scope was render-only. A round file is agent-written repository content, so this is in scope under the review threat model (PROCESS.md §6).

## Done-when

- The gate's reader of a review round's verdict is the same strict per-line reader the filing boundary uses (one parser, not a second one): a VERDICT label outside the enum, a missing or non-integer count, or more than one VERDICT line makes the round unreadable, which the gate treats as no verdict (fail closed), never as APPROVE.
- The shared per-line reader refuses a duplicated field on a machine line, for every consumer (adjudication verdicts included), and the filing boundary's local duplicate check is removed in favour of it.
- Tests, red first, for each of the four probes above against the gate's reading, and for a duplicated field.
- Existing committed round files in this repo still read as before (a migration check over `docs/reviews/`); any that do not are listed for the owner rather than rewritten.
- The spine carries the change (Terra authors; an independent adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script changes).
