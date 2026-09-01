+++
id = "WI-552"
title = "The adjudicator's two exits: adjudication-row close, successor mint, OI mint with refusal invariant (OI-70)"
specref = "docs/requirements/open-items.toml#OI-70"
workstream = "process"
sr_refs = ["SR-144"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

`OI-70` RULED 2026-08-31 (record `docs/log.d/2026-08-31-owner-rulings-oi70-71-72.md`,
compiled into `docs/log.md`): partial is the only stop, every closure produces
a handback, and the adjudicator judging that handback has exactly two exits —
a QUEUED successor WI where the work continues by another route, and/or a
minted OPEN ITEM where the answer is human-owed. Mixed outcomes are permitted;
`deferred/` is never an adjudicator destination unless what it places there is
a replacement.

What exists: `handback.close_partial` writes the immutable report (`LLR-144`),
`intake._close_drafts` mints exactly one disposition row per report
(`LLR-161`), and ADJUDICATE sessions draft successors (`WI-550` drafted
`WI-551`). What is missing (decision 21 of
`docs/decisions-for-review-2026-08-31.md` carries the live evidence): the
ADJUDICATE brief promises "the machinery mints your draft at this row's own
close" and NOTHING performs that close — the dispatcher resumes a finished
adjudication row in a cycle until a supervisor closes it by hand.

RE-SCOPED by `OI-73`, RULED 2026-08-31 (record
`docs/log.d/2026-08-31-owner-ruling-oi73.md`), same-day refinement of OI-70's
exits: a successor is MANDATORY at every partial/cancelled close (the
OI-alone exit is retired); a minted OI becomes a typed hard dependency of the
successor rather than a standalone exit; the mint REPLACES the superseded
row's inbound hard `needs` edges; and `OI-###` ids become valid hard tokens
in `needs`, satisfied when the row leaves `pending`. Done-when 2–4 below are
amended and 5–6 added accordingly.

## Done-when

1. An adjudication row whose session recorded a verdict CLOSES mechanically:
   its `## Dispositions` successor drafts are minted into `queued/` (ids from
   the watermark, `spec_move.py` for every move), the row archives terminal,
   and the dispatcher no longer resumes it.
2. The human-owed arm exists: the close can mint an OPEN ITEM row into
   `docs/requirements/open-items.toml` — id from the watermark's OI space,
   `status = "pending"`, `gen_open_items.py` regenerated in the same commit —
   and the minted id lands in the queued successor's `needs`, so the ruling
   gates the successor's readiness instead of relying on adjudicator
   restraint (OI-73).
3. The refusal invariant (as tightened by OI-73): a PARTIAL or CANCELLED
   disposition that queues NO successor is REFUSED at the close — an OI alone
   no longer discharges it; no third exit, nothing silent.
4. The mint REPLACES the inbound hard `needs` edges of the row the successor
   supersedes (`supersedes` is the carrier) — the `WI-541` strand class (its
   `needs` waited on a terminal row) becomes unrepresentable, not merely
   visible (OI-73's replacement-not-report arm).
5. Typed OI edges: an `OI-###` id is a valid HARD token in `needs` —
   existence validated through the spine carrier and the id-watermark's OI
   space, readiness satisfied when the row leaves `pending` (a new waiting
   reason in the scheduler), the template grammar and PROCESS_OPTIONS
   dependency prose widened TOLERANTLY so bare WI ids keep meaning what they
   mean and no downstream registry migrates.
6. The validator net: `dead_dependency_findings` extends to `partial`
   predecessors, so a strand minted outside this path is reported rather than
   silent.
7. Tests drive all six on a scaffold, and the ADJUDICATE brief's contract
   text matches what the machinery now actually does.
