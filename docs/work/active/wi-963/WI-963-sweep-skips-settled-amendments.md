+++
id = "WI-963"
title = "The trunk mint never mints an amendment row for a row the merged range already settled"
workstream = "process"
sr_refs = ["SR-178"]
specref = "docs/plans/2026-10-03-s11-in-lane-adjudication.md#42-the-re-mint-trap"
needs = []
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 5
+++

## Context

Filed by hand by the attended coordinator on 2026-10-20, split from WI-810 by
the owner's ruling (coordinator-2026-10-20 D-009); WI-810's remainder is
cancelled. It is the first build after headless leg 06.

**The defect.** When a lane lands, the trunk mint (`intake._routed_amendments`,
called by `intake_after_merge` from the merge slot's post-merge arm and by
`intake.py sweep` after a coordinator's hand landing) diffs the approved and
routed cells of the spine registries across the merge and mints an
`adjudicate:` row for every row whose text moved. It never asks whether the
lane already judged that change. Since in-lane adjudication (WI-849, WI-912),
a lane amends a row, sits it, and re-attests it in its own act; the row's
Status does not change, so the mint sees changed text and files a redundant
row. The coordinator then closes it "as already settled", citing the act.
That has happened 54 times (WI-785 on 2026-10-03 to WI-959 on 2026-10-20;
`git log --grep="already settled"`), each burning a WI id and a close commit,
and the coordinator-cycle skill carries the workaround as a standing landing
step ("close the re-mint citing the act", SKILL section 4 step 3; recipes
section 3).

**The design** is the S11 plan's section 4.2, never built: drop an amendment
record when an act-ledger entry the merged range added re-attests the row
(`acceptance_record.reattested_between` already reads this) AND the row's
changed cells at the merged tree equal their copies in the approved snapshot
(`docs/archive/last_approved/`) at that same tree. The second test keeps the
mint for a row amended again after its act. The comparison is the row's whole
approved (and routed traced) cell set against its snapshot copy, not only the
cells the range's net diff reports: a cell edited after the act and then
restored to its pre-range value is absent from the net diff yet differs from
the snapshot, and must still mint (coordinator-2026-10-20 D-013).

Anchor: SR-178 ("text that has moved away from its acceptance record is
reported"): a row re-attested in the range has not moved away from its
record, so routing it again reports nothing. LLR-153 (the unified trunk-side
intake mint) stays the code-home LLR.
WI ids stay trunk-minted (revision 33); this row changes which rows the trunk
mint files, not where ids come from.

## Deliverables and order

Four pieces, landing in this order within the one lane:

1. **The filter** (one shared filter for the merge slot and `intake.py
   sweep`), its regressions, and its LLR/TC rows passed through in-lane
   adjudication. It lands first: everything below describes or depends on it.
2. **The shared-walk clarification** (the comment above `AMENDMENT_CSVS` and
   LLR-158's detail). It could land alone as text, but it states that the mint
   drops re-attested rows, which is false until the filter lands, so it rides
   with the filter rather than preceding it.
3. **The workaround's removal** from the coordinator-cycle skill and its
   recipes. It lands after the filter and its regressions pass: removing the
   "close the re-mint citing the act" step before the mint stops filing those
   rows would leave every landing with an unclosed redundant row.
4. **The RESYNC_PACK entry**, last, anchored at the trunk commit that carries
   the filter, since it describes the landed behaviour to adopters.

They stay one row because pieces 2 to 4 are each true only once piece 1 has
landed, and splitting them would file three rows whose only content is
following piece 1 (the coordinator's answer to S1 at critique round 1).

## Done-when

- An approved row amended in the merged range, re-attested by an act-ledger
  entry the range added, and whose changed cells at the merged tree equal
  their approved-snapshot copies there, yields no amendment row, at the merge
  slot's post-merge arm and at `intake.py sweep` alike (one shared filter).
- A row re-attested in the range and then amended again after its act still
  yields its amendment row.
- An approved row amended with no act in the range still yields its
  amendment row, exactly as today.
- An ABSENT act ledger reads as no acts, as `_ledger_acts` already reads it
  (a fresh adopter has none before its first signing), so nothing is
  filtered and the mint runs exactly as today; the filter is consulted only
  when the range carries amendment records. A ledger or snapshot copy that is
  present but cannot be read or parsed refuses the mint by name, as
  `reattested_between`'s refusal already does. A row the ledger re-attests
  whose snapshot copy is missing is not proven settled, so it is minted,
  never skipped.
- A row re-attested in the range, then edited after its act and restored to
  its pre-range text in one cell, still mints (the whole-row comparison).
- A regression replays two real landings that minted a redundant row (WI-926's
  landing `08bbb71b6`, which minted WI-952, and WI-956's, which minted
  WI-959) and mints none of their rows, while a fixture amended after its act
  still mints.
- LLR-153's detail (or a new LLR under SR-178, if the in-lane adjudicator
  rules the rule a separate obligation) states the filter, a TC verifies each
  arm, and the set passes in-lane adjudication.
- The shared-walk invariant is restated where it lives: the comment above
  `AMENDMENT_CSVS` (`acceptance_record.py`) and LLR-158's detail say the
  pre-commit warn (`staged_spine_findings`) and the mint read one walk, and
  that the mint additionally drops rows the merged range re-attested; the
  warn itself is unchanged (it fires before any act).
- The coordinator-cycle skill and its recipes drop "close the re-mint citing
  the act" from the landing steps, in the same lane, after the filter and its
  regressions pass (Deliverables and order).
- RESYNC_PACK: one entry anchored at a trunk commit; an adopter's trunk mint
  stops filing rows for amendments its lanes already settled. No data
  migrates.
- Coverage bound: the promise reaches the ledgers, snapshot copies and ranges
  that supported workflows and the kit's own routes produce (the act turn, an
  owner's signing act, a lane landing through the merge slot, `intake.py
  sweep` over a landed range), as `project-trajectory/PROCESS.md` §6 "Review
  threat model" bounds a spec's promise. A hand-edited act ledger or snapshot
  copy, hand-chosen name aliases (a row id or registry path in another case
  or spelling) and sub-second timing windows are outside it.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

The act ledger and the approved snapshot gain one new authority: suppressing
an adjudication row the mint would otherwise file. The guard follows
`project-trajectory/PROCESS.md` §3, "When a guard is owed" (both carriers are
files on disk, read at a git revision).

- **Producer:** the act ledger (`docs/archive/last_approved/acts.toml`) and the
  approved snapshot are written by
  `project-trajectory/scripts/baseline_snapshot.py` `copy_live` (IF-123; the
  ledger entry's shape is IF-220), reached through
  `project-trajectory/scripts/intake.py snapshot` by the act turn
  (`project-trajectory/scripts/coordinator_adjudicate.py act`) and by the
  owner's own signing acts, and land with the lane or the owner's commit.
  Every consumer below reads them at a git revision, never from the working
  tree. Failed-write shapes:
  - *Structured error:* `copy_live` refuses (drift outside the act's write
    set, an unknown id, a malformed existing ledger) before any copy and
    writes nothing; there is nothing to commit.
  - *Failed call or timeout* (a crashed or killed act turn): the registry
    copies are written before the ledger entry is appended, so an
    interrupted act leaves either no change or copies with no new ledger
    entry. Nothing reaches a consumer unless that working tree is committed;
    if it is, the range adds no act for those rows and they mint.
  - *Partial file:* a truncated ledger does not parse, and the mint refuses
    by name; a truncated or partial snapshot copy either does not parse (the
    mint refuses by name), or lacks the row or no longer equals its cells
    (the row mints).
- **Consumers newly given the authority, by path:**
  - `project-trajectory/scripts/intake.py`: the filter's one home in
    `_routed_amendments` (or a helper it alone calls), through
    `_amendment_drafts` and `intake_after_merge`, reached by
    `project-trajectory/scripts/integrate.py` (`integrate_one`'s post-merge
    arm, in the held merge slot) and by `intake.py sweep` (`_cmd_sweep`, a
    range sweep after a hand landing).
  - `project-trajectory/scripts/acceptance_record.py`, the intermediary the
    filter reads through: `_ledger_acts` / `_added_acts` /
    `reattested_between` for the ledger at each revision, and the row read of
    a snapshot copy at the after revision. Two existing behaviours there
    collapse a failure into absence: `_ledger_acts` reads any failed `git
    show` (`kitlib` `git_out` returns None on any failure) as an absent
    ledger, and `_spine_rows_at` reads an unparseable carrier as no rows. For
    this filter both collapse toward minting, never toward suppression, but
    the ruling below requires a present but unparseable snapshot copy to
    refuse by name, so the filter reads the copy through a read that tells an
    unparseable copy from an absent one.
- **Unchanged readers, under their established contracts:**
  `acceptance_record.staged_spine_findings` (the pre-commit warn, which keeps
  reading the unfiltered walk); the merge rung's act reads
  (`acceptance_record.lane_acted_set`, `reattest_scope_refusal`,
  `held_reattest_refusal`, reached from `integrate.py`); and the snapshot's
  other readers (`adjudicate_act.py`, `adjudicate_brief.py`,
  `assumption_rules.py`, `check_trajectory.py`, `gen_open_items.py`,
  `hats.py`, `pending.py`, `record_observation.py`, `spine_rules.py`,
  `trace.py`, `trunk_step.py`, all under `project-trajectory/scripts/`). Their
  contracts are IF-123 and IF-220 in `docs/requirements/interfaces.toml`;
  this row redefines neither.
- **Ruling** (coordinator-2026-10-20 D-020, for the owner to confirm or
  overrule): an absent ledger is no acts, so nothing is filtered; a present
  but unreadable or malformed ledger or snapshot copy refuses the mint by name
  (fail closed); a row the filter cannot prove settled, a missing snapshot
  copy included, is minted. The filter only ever removes a row it can prove
  was judged in the range.
- **What the suppression binds to:** the row's identity (its id in its
  registry); act-ledger entries added in the requested range, that is,
  entries whose `seq` the ledger at the range's `before` revision does not
  hold, for the `before`/`after` the merge slot or the sweep was given; and
  the row's whole approved and routed traced cell set at the range's `after`
  tree, compared with the row's copy in the snapshot at that same tree.
  Nothing outside that range or that tree can suppress a row.
- **A refusal on each route:** at the merge slot's post-merge arm the merge
  has already landed, so the refusal says the mint was refused (not that
  nothing was merged) and mints no row; once the named carrier is fixed in a
  reviewed commit, the recovery is `intake.py sweep --before --after` over the
  same range. At `intake.py sweep` the refusal ends the sweep with no row
  minted, as its other refusals do.

## Critique dispositions

Scope critique round 1 (Codex Sol, 2026-10-21; CHANGES-REQUESTED,
findings=4):

- F1 (MAJOR, S4 frontmatter): adopted — "planmode = \"single\"". The row has a
  `## Trust` section, touches two script families (`intake.py`,
  `acceptance_record.py`) and promises behaviour over an input space; it adds
  a code path, so the deletion exception does not apply.
- F2 (MAJOR, S2 `## Trust`): adopted — "The guard follows
  `project-trajectory/PROCESS.md` §3, \"When a guard is owed\""; the Producer
  states each failed-write shape ("*Structured error:* ...", "*Failed call or
  timeout* ...", "*Partial file:* ..."); "Consumers newly given the
  authority, by path" lists the `intake.py` / `integrate.py` routes and the
  `acceptance_record.py` intermediary; "Unchanged readers, under their
  established contracts" links IF-123 and IF-220; "What the suppression binds
  to: the row's identity ...; act-ledger entries added in the requested range
  ...; and the row's whole approved and routed traced cell set at the range's
  `after` tree"; and "A refusal on each route" gives each consumer's failed
  outcome. D-020's ruling text is unchanged.
- F3 (MINOR, S1 Done-when): adopted — "## Deliverables and order": the filter
  with its regressions and spine rows lands first, the workaround's removal
  "lands after the filter and its regressions pass", and "They stay one row
  because pieces 2 to 4 are each true only once piece 1 has landed".
- F4 (MINOR, S3 Done-when/Trust): adopted — "Coverage bound: the promise
  reaches the ledgers, snapshot copies and ranges that supported workflows and
  the kit's own routes produce ... A hand-edited act ledger or snapshot copy,
  hand-chosen name aliases ... and sub-second timing windows are outside it."
