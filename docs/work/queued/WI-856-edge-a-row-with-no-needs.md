+++
id = "WI-856"
title = "A queue-with-edge verdict edges a waiter filed without a needs line"
workstream = "process"
specref = "docs/reviews/wi-855-adjudicate-queue-overlap-2042/001-ADJUDICATE-2d74139.md"
sr_refs = ["SR-220"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-08 from the WI-855 consolidation
verdict's last finding (`001-ADJUDICATE-2d74139.md`, the MINOR on the
machinery). `consolidate.edged_text` returns None for a row whose frontmatter
has no `needs` line, so `handback._enact_plan` refuses the whole verdict when
an edge names such a row as its waiter. An adjudicator must then leave a
correct edge out of its typed block and ask the coordinator to write it by
hand. WI-855 hit this twice: WI-833's edges on WI-828 and WI-832, and WI-848's
on WI-846 (`docs/decisions/wi-855.toml` D-001). Hand-filed rows commonly carry
no `needs` line, so the gap recurs at every census.

LLR-210's detail names `edged_text` as one of the pure transforms the close
writes back; this row widens what it accepts, not what it means.

## Done-when

- `edged_text` gives a row with no `needs` line one, holding just the
  blocker, inserted in the frontmatter (the row's Context and Deliverable stay
  byte-identical). A row with a `needs` line behaves as today, idempotence
  included. A frontmatter it cannot read is still refused.
- Tests: a queue-with-edge close edges a waiter that had no `needs` line; the
  inserted line parses and the rest of the spec is unchanged; an existing
  `needs` line is extended exactly as before.
- LLR-210's detail and its TC say that the transform inserts a missing `needs`
  line, and those rows pass in-lane adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (an adopter's census can
  now edge its hand-filed rows).
