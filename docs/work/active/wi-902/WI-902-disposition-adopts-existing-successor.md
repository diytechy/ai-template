+++
id = "WI-902"
title = "A disposition can name an already-filed successor instead of drafting a duplicate"
workstream = "process"
sr_refs = ["SR-220"]
specref = "project-trajectory/scripts/handback.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 (overnight leg 01, decision D-022 in
`docs/decisions/coordinator-2026-10-10.toml`), from WI-894's disposition
verdict (`docs/reviews/wi-894/001-ADJUDICATE-3cd530b.md`, its second
finding). WI-828 closed partial after its successors (WI-892, WI-893) and its
open item (OI-113) were filed by hand. The sitting ruled PARTIAL and drafted
no successor, because a draft would mint a duplicate of WI-893. Two guards
then refuse the outcome the verdict reached:
`handback.close_adjudication`'s `owes_successor` guard refuses the mechanical
close (WI-894 was closed by hand), and `intake.py sweep` refuses the merge of
an early-close adjudication row whose `## Dispositions` is empty (OI-70/OI-73,
"no third exit"). No draft key names an existing queued row:
`intake._DRAFT_KEYS` mints a new row only.

## Trust

Written before the claim, answering the scope critique's S2 (coordinator
2026-10-11 D-005, for the owner to confirm or overrule). Naming an existing
row as the successor gives the adjudicator's text authority over the close
and the sweep, so this section states the carrier, its producer, its
consumers and a ruling per consumer, under `project-trajectory/PROCESS.md`
§3, "When a guard is owed". This row has one landable deliverable.

**The carrier.** An *adoption* is a block in the disposition row's own
`## Dispositions` section, beside or instead of drafts (the section the
drafts already live in, never the verdict file): a fenced TOML block holding
exactly one key, `adopts = "WI-NNN"`. A block with `adopts` and any other
key, or a value that is not one well-formed WI id, is a parse refusal, as a
malformed draft is today. The verdict's machine line
(`OUTCOME: ... successors=N`) is unchanged: the verdict reader checks only
that `successors=` is present, and this row adds no count comparison.

**Producer and write route.** The adjudicator writes the block in the
sitting's own spec in the lane, as it writes drafts
(`adjudicate-disposition.template.md` gains the adoption form), and commits
it with the verdict. Failed writes: a failed call, a timeout and a
structured error from the CLI all end the sitting with exit 1 (no valid
verdict), and the loop's `adjudication_owed` holds the close as today. Any
output the failed sitting already wrote (a partial block or section in the
lane's spec, committed or not) is never closed on: the close runs only after
a sitting that exited 0, and the coordinator reverts a failed sitting's
writes before the re-sit. A malformed block, or a half-written section (a
git-committed file cannot be read half-written, only malformed), is a parse
refusal at every consumer below except the historical absorption reader,
which keeps its own rule (its bullet). No consumer repairs or guesses a block.

**What the authority binds to.** An adoption names only the successor. The
row it disposes is never read from the adjudicator's text: it is read from
the disposition row's title, the immutable event token `_mint` dedups on
(the row's `specref` is cleared at the close). Both minted forms carry a
terminal path whose file name leads with the disposed row's id: a
report-backed close's title names the close report (`<wi>-<branch>`), and a
report-less cancellation's (`intake._close_drafts`, "the cancellation
recorded at") names the cancelled spec (`WI-NNN-<slug>.md`). One function,
shared by the close and the sweep, resolves that id; a title whose token is
absent or does not resolve to exactly one WI id refuses at both, never
guessed. An adoption is accepted only while the named row exists open on
trunk's registry (`queued/`, `active/` or `draft/`) and its `supersedes`
cell names that disposed row, read at each consumer's read, not trusted from
the time the adjudicator wrote it.

**Absent, unreadable and failed inputs.** At the close and the sweep: an
adopted id naming no open row refuses ("names no open row"); an adopted row
whose spec cannot be read or parsed refuses with a distinct reason ("cannot
read"); a registry that cannot be loaded refuses. No case falls back to
minting or to accepting. The sweep today skips a merged adjudication spec it
cannot read or whose front matter does not parse; this row makes that a
sweep refusal (the merge stands, exit 1), because a skipped early close is a
close that vanishes without a successor. An absent `## Dispositions`
section keeps today's rule at every consumer: the close and the sweep refuse
it for a row that owes a successor, and the scheduler and gate read it as
nothing drafted.

**Consumers and rulings** (found by grep over `project-trajectory/scripts`
for `Dispositions`, `owes_successor`, `_DRAFT_KEYS`, `parse_dispositions`
and `adjudication_review_owed`):

- **The close** (`handback._archive_one_adjudication_row`, through
  `close_adjudication`): `owes_successor` is discharged by a draft or by an
  accepted adoption. An adoption naming a missing, closed or
  non-superseding row refuses the close with the reason, as the guard
  refuses an empty section today. A consolidation row's close
  (`_consolidation_close`) refuses an adoption: its absorbs reconcile
  against drafts' `supersedes` only.
- **The sweep** (`intake._disposition_drafts`, from `intake_after_merge` for
  the merge slot and `intake.py sweep`): the same acceptance rule, read
  against trunk; an accepted adoption mints nothing and discharges the
  empty-section refusal; a refused one refuses the sweep as today (the merge
  stands and nothing is minted, exit 1). OI-73's "no third exit" holds: an
  adoption is the successor exit, a queued successor, not a third one.
- **The mint** (`intake._mint` and `_draft_refusal`): an adoption block is
  never a draft and is never minted; `_DRAFT_KEYS` does not gain `adopts`.
- **The review scheduler and the merge gate** (`agent_loop.dispositions_drafted`
  and `integrate._verdict_owed`, both through
  `agent_policy.adjudication_review_owed`): these read the block's shape
  only, never the adopted row; a well-formed adoption owes no spine review
  (it mints and amends nothing), and acceptance stays the close's and the
  sweep's. A malformed section or an unreadable spec keeps today's
  fail-toward-review rule.
- **The historical absorption reader**
  (`project-trajectory/scripts/consolidate.py:_enacted_supersedes`, read
  through `enacted_absorbs`, `judged_absorbed` and
  `consolidation_successors` by the census's `_seed_pairs` and `clusters`,
  and by `project-trajectory/scripts/adjudicate_brief.py:_prior_lines`):
  unchanged. It reads only a `consolidate` outcome's drafts' `supersedes`,
  and an adoption carries no `supersedes`, so an adoption never counts as an
  absorption. It keeps its draft-only rule for bad input: an absent
  section enacted nothing, and a block that does not parse is skipped (the
  close and the mint refuse a malformed verdict, so no absorption rode on
  one); since a consolidation close refuses an adoption (above), no
  consolidation verdict on trunk carries one.
- **The successor sweep for Done-when verdicts** (`intake._successor_drafts`):
  unchanged; a SUCCESSOR Done-when verdict still needs a draft.

## Done-when

- A disposition verdict can discharge the successor obligation by naming an
  existing queued row that carries `supersedes` of the closed row; the
  mechanical close and the sweep accept it, and still refuse an early close
  that names neither a draft nor such a row.
- The scope of OI-73's "no third exit" is kept: naming an existing successor
  is the same exit (a successor is queued), not a third one.
- Tests: an early close naming an existing superseding row closes and
  sweeps; one naming a row without `supersedes`, or a missing row, refuses;
  a drafted successor is unchanged.
- The rows the change makes untrue (LLR-312's chain, and the sweep's row)
  state it and pass adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (shipped scripts change).
