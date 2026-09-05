+++
id = "WI-583"
title = "The consolidation adjudicator: the consolidate brief, the digest-guarded census, the multi-row close into restructured"
workstream = "process"
needs = ["WI-579", "WI-570"]
specref = ""
buildtier = "strong"
priority = 5
safety_class = "ordinary"
+++

## Deliverable

Plan §1 built in full, as a hand commit series out of band. The `consolidate`
brief (`prompts/adjudicate-consolidate.template.md`,
`adjudicate_brief.VERDICT_GRAMMAR["consolidate"]`, `consolidate_values`), the
digest-guarded census that mints it (`scripts/consolidate.py`, new; the mint arm
`intake.mint_consolidation`), the typed `Digests` column in all four schema
homes, and the close that absorbs several queued rows into one successor
(`handback._consolidation_close` + `consolidate.archive_absorbed`).
`adjudicate-conflict` is RETIRED with its prompt key and catalogue row, per
Done-when 1's "otherwise retire it": it had a template and a grammar and never a
mint, an assembler or a reader for its `needs=` field.

ONE DEVIATION STANDS, and the second was closed at rework. The absorbed rows'
move to `restructured/` runs at the MINT and not in the close, because its
Deliverable names an id `intake._mint` allocates one commit later and because
`_supersedes_refusal` would otherwise make the mint refuse its own successor —
the close still performs every guard and every non-minting outcome Done-when 3
asks for, and two adversarial rounds confirmed that argument true. The census
IS now called from `dispatch._admit` (it was inert at first close, when that
module was another lane's); wiring it also exposed a defect neither reviewer
found — a minted row whose SpecRef did not resolve could never be claimed and
wedged the frontier — which is why the SpecRef is an existence probe.

AMENDED AT REWORK (2026-09-04), after two independent hostile rounds returned
11 and 9 findings, all of which held: the close's six all-or-nothing holes, the
unimplemented Done-when quoting plan §1.5 promised, the parser's type and
uniqueness gaps and the CRLF-fragile text transforms are all closed, each with
a mutation-verified test. The account is the second section of
`docs/log.d/WI-583-consolidation-adjudicator.md`.

Evidence: `tests/test_consolidate.py` (the decision half — digests, the two new
pre-filter signals, clusters, the three guards, the typed verdict block, the
text transforms), `tests/test_consolidate_close.py` (the arc on a real
repository: mint over three queued rows, brief, verdict, close, merge, mint —
three rows in `restructured/` naming the successor, the successor superseding
all three, the census silent afterwards), plus the new cases in
`tests/test_adjudicate_brief.py`, `tests/test_intake.py` and
`tests/test_wi_convert.py`. `RESYNC_PACK.md` carries the adopter entry and
`docs/enforcement-audit.md` the two rows for what now enforces this.

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). A NEW row: it absorbs nothing and quotes nothing; its spec of record is plan §1.

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
