+++
id = "WI-583"
title = "The consolidation adjudicator: the consolidate brief, the digest-guarded census, the multi-row close into restructured"
workstream = "process"
needs = ["WI-579", "WI-570"]
specref = "docs/plans/2026-09-02-backlog-restructure-and-consolidation.md#1-the-consolidation-adjudicator"
buildtier = "strong"
priority = 5
safety_class = "ordinary"
+++

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). (No rows absorbed — a new row.) The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

Builds plan §1 in full — read §1.1 through §1.5 and §1.7 before starting; the
plan is the spec of record and this Context does not restate it. The
`restructured` terminal state (§1.6) and list-valued `supersedes` (§1.5) are
ALREADY on trunk (the out-of-band commits of 2026-09-02); build on them.

**Edges.** `WI-579` first: consolidation is always review-owed under the
`when-minting` dial that row ships, and the gate must know how to ask.
`WI-570` first: it types the `[open_item]` table inside `parse_dispositions` /
`_mint_shape_refusal`, the same functions this row extends for
`absorbs=` / list `supersedes` refusals — two lanes in those functions would
conflict.

## Done-when

1. `consolidate` is a fifth routed brief: `prompts/adjudicate-consolidate.template.md`
   (the conflict template's three questions plus the CONSOLIDATE exit and the
   `{prior}` slot; the `conflict` key stays in `KIT_PROMPTS` only if something
   still names it — otherwise retire it and its catalogue row in this change),
   `adjudicate_brief.consolidate_values` (all-or-nothing, §1.4),
   `VERDICT_GRAMMAR["consolidate"]` with `needs=` and `absorbs=` fields.
2. The census trigger (§1.3) in `dispatch`: idle station, no adjudication
   queued or active, queued rows only, the pre-filter plus the two new
   signals, the queue+spine digest pair, the archived-digest refusal,
   `priority = 9`, typed `adjudicates` and `digests` cells.
3. The close (§1.5) in `handback.close_adjudication`: absorbed rows still
   `queued` or the close refuses by name; each moves to
   `archive/work/restructured/` with the one-line Deliverable; QUEUE-WITH-EDGE
   writes the hard `needs` edge; RETURN-TO-DRAFT moves `queued/ -> draft/`
   with the finding quoted into Context.
4. The successor's Context carries the verdict's scope prose then the absorbed
   rows' Done-when blocks quoted under their old ids.
5. Plan §4's census acceptance on a scaffold: five rows, two overlapping pairs
   → exactly one consolidate row; same queue again → nothing; after its close
   absorbed two rows → nothing.
6. `RESYNC_PACK.md` entry; `docs/enforcement-audit.md` row; full suite green.
