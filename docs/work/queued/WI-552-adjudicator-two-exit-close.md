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

## Done-when

1. An adjudication row whose session recorded a verdict CLOSES mechanically:
   its `## Dispositions` successor drafts are minted into `queued/` (ids from
   the watermark, `spec_move.py` for every move), the row archives terminal,
   and the dispatcher no longer resumes it.
2. The human-owed exit exists: the close can mint an OPEN ITEM row into
   `docs/requirements/open-items.toml` — id from the watermark's OI space,
   `status = "pending"`, `gen_open_items.py` regenerated in the same commit —
   so the question reaches the owner surface with no human prose required.
3. The refusal invariant: a PARTIAL or CANCELLED disposition that names
   neither a queued successor nor a minted OI id is REFUSED at the close — no
   third exit, nothing silent.
4. A minted successor carrying `supersedes` re-points, or loudly reports, the
   `needs` edges of the row it supersedes — the `WI-541` strand class (its
   `needs` waited on a terminal row) becomes unrepresentable or at least
   visible at mint time.
5. Tests drive all four on a scaffold, and the ADJUDICATE brief's contract
   text matches what the machinery now actually does.
