+++
id = "WI-552"
title = "The adjudicator's two exits: adjudication-row close, successor mint, OI mint with refusal invariant (OI-70)"
specref = ""
workstream = "process"
sr_refs = ["SR-144"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Shipped all seven Done-when arms of OI-70 (as refined by OI-73). The
adjudicator's exits are now mechanical:

1. **Mechanical adjudication-row close** — `handback.close_adjudication` moves a
   DONE adjudication row to `complete/` (inserting a `## Deliverable`, clearing
   `specref`, preserving `## Context`/`## Dispositions`), wired into
   `dispatch._advance` (via `_close_done_adjudication`). The C6 resume-forever
   loop OI-70 measured is closed; the agent self-close path still short-circuits.
2. **OI-mint arm (exit B, typed)** — a `## Dispositions` draft may carry
   `open_item`; `intake._mint_open_item` appends a `pending` OI (id from
   `next_oi_id`, the watermark OI space) and `_inject_open_item` lands its id in
   the successor's `needs`; `open-items.html` regenerates in the mint commit.
3. **Refusal invariant** — a `disposition`-brief close that queues no successor
   is refused, at both `close_adjudication` and `intake._disposition_drafts`.
4. **Inbound-edge replacement** — `intake._replace_inbound_edges` re-points a
   superseded row's hard `needs` edges to the successor at the mint (the WI-541
   strand becomes unrepresentable).
5. **Typed OI edges** — `kitlib.spine.split_pred_edges` is the one home for the
   widened grammar; `schedule` resolves an `OI-###` hard edge as satisfied when
   the row leaves `pending` (new `waiting:open-item-pending` reason, threaded
   through `evaluate`/`frontier`/`simulate` and every caller);
   `check_trajectory.validate` resolves it against the open-items registry;
   template CSV + PROCESS_OPTIONS prose widened tolerantly (bare WI ids
   unchanged).
6. **Validator net** — `dead_dependency_findings` extends to `partial`
   predecessors.
7. **Contract text** — the ADJUDICATE disposition brief matches the machinery
   (mandatory successor, `open_item`, machine-performed close).

Tests cover every arm (`test_intake`, `test_handback`, `test_dispatch`,
`test_schedule`, `test_trajectory`). Smoke tier green within budget; full
unfiltered suite green (close commit). No spine rows minted/re-statused.

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
