+++
id = "WI-572"
title = "The approval act is the adjudicator's, on trunk: lanes author Drafted rows, a first-approval adjudication flips and snapshots them"
workstream = "process"
needs = ["WI-571"]
specref = ""
buildtier = "strong"
priority = 5
safety_class = "ordinary"
+++

## Deliverable

The approval act on a spine row — the `Status` flip into `Approved`/`Founded`
and the `docs/archive/last_approved/` copy that anchors it — is now the
adjudicator's, on the serial trunk side. A worker lane authors `Drafted` rows
and amends cell text; nothing else changed about what a lane may do.

1. **Lanes cannot approve.** The merge slot REFUSES a work branch whose spine
   delta flips a `Status`, mints a row born claiming approval, or writes the
   snapshot directory — by name, listing each row, its registry and every file
   touched — each worded by what the branch DID to it — with the remedy.
   Construction-first: `staged_approval_acts` reports the set
   `staged_spine_amendments` exempts MINUS the de-approvals (a withdrawal
   blesses nothing, and `staged_drafted_rows` raises the re-approval it owes
   instead), off one shared two-tree walk (`_spine_row_sides`), so no second
   detector entered. The judgement is
   `acceptance_record.lane_approval_refusal`; `integrate._approval_act_refusal`
   is the rung. Verified against the record: the reader reproduces the
   pre-ruling census exactly — the four flips at `580df781` and the
   born-`Approved` rows of WI-483, WI-500, WI-501, WI-507.
2. **A first-approval adjudication arm exists.** Trigger (a2) mints ONE
   `brief = "first-approval"` row per merge over the `Drafted` rows the lane
   handed over — including a status-only withdrawal into `Drafted` — on the
   rungs the dial releases; a held rung is not minted and
   surfaces to the owner as before. Those row ids are RECORDED on the minted
   row (`Adjudicates`, a new `wi_convert` column) and the brief — which
   re-derives its population live, because the row is claimed long after the
   merge — acts only on the intersection, so the act cannot widen past what the
   merge handed over. Its brief renders each row's WHOLE chain
   (`trace.spine_chain`, extracted from `reattest_model` so the judge and the
   owner's surface cannot disagree) and asks one question — approve, or return
   with findings — with the `--approves` argument of the approving commit
   derived rather than typed. Its verdict grammar is its own. The adjudication
   lane is exempt from rung 1, and it already runs ALONE
   (`dispatch._branch_exclusive`), which is the concurrency guarantee the ruling
   points the act at rather than a new mechanism.
3. **The amendment arm's aftermath is stated and true.** The stale "the flip is
   the mechanical tool's act, not yours" — false since OI-45 (b) retired that
   tool — is replaced by a DERIVED `{aftermath}` slot that reads the declared
   gate authority for the tiers shown and tells the session whether the
   re-attestation is its own act or the owner's.
4. **The doctrine says it once:** PROCESS.md §4's fixed points, linking to
   PROCESS_OPTIONS.md "Who performs the approval act" (the ruling, its two
   reasons, the division-of-labour table, the three holding mechanisms); OI-45
   (b) narrowed by one sentence; `gate-advance`, `spine-authoring` and
   `worker.template.md` updated.
5. **Tests** in the modules' existing style: five at the merge slot, four at the
   reader, four at the trigger, nine at the brief — including the pin that the
   brief's terminal sequence cannot stop before performing an approved row's
   flip-and-snapshot act, and the mutation-proven regression that an act cannot
   reach a row the merge did not hand it. The schema pin now covers the READ
   side's copy of the column list too, and `test_wi_loader_sync` carries the
   scope cell as the third member of its `bar`/`brief` triplet.

Two repairs the close itself unmasked rode this row rather than a follow-up,
because the bar fails where it surfaces: `wi_convert.read_specs` now walks the
folder home through the READ side's own `spec_paths` (a tracked `README.md`
under a status directory was a broken row to the writer and residue to the
reader), and the four `test_wi_convert.py` guards that a catch-all
`ConvertError` skip had kept dark since WI-504 run again.

Deviations, the ratchet re-stamps, and the one follow-on this row deliberately
does not take (narrowing the owner's approval brief to the held rungs) are in
`docs/log.d/WI-572-approval-act-adjudicator-only.md`.

## Context

Filed 2026-09-01 (evening supervised session) from the owner's ruling made in session (docs/log.d/2026-09-01-owner-ruling-approval-act.md, compiled): approval acts on spine rows - the Status flip and the anchoring snapshot - are the adjudicator's alone, on the serial trunk side, for whole-chain context and for concurrency. A lane's merge is refused on any flip, born-Approved row or snapshot write; a first-approval adjudication arm is minted at merge with the whole chain in its brief and flips + snapshots on trunk; the amendment arm's stale mechanical-tool line is replaced by the true aftermath; the doctrine is stated once. Serialized behind the copy-scope row (both touch intake.py and baseline_snapshot.py). Read the plan's section 2 before widening.

**Standing constraint (the ruling this row executes):** if this row authors
or amends spine rows (SR/LLR/TC), leave them `Drafted`; do NOT flip any
`Status`, and do NOT run `intake.py snapshot` or write
`docs/archive/last_approved/` on this lane — drive the new refusal and the
adjudication arm on a scaffold. The first-approval adjudication this row
ships is what performs the flip and the snapshot, on trunk.

Honoured: this lane moved no `Status` and wrote no snapshot; every arm is driven
on a scaffold repo built by the tests. It amended two rows its own code made
stale — `LLR-158`'s `code_symbol`/`Detail` (left `Approved`, the drift being the
signal) and `IF-091`'s requestors (already `Drafted`) — which the constraint
permits: a lane amends, an adjudicator approves. Checked against this row's own
reader rather than assumed — `lane_approval_refusal` returns `None` over the
branch delta, and `staged_spine_amendments` reports `LLR-158`, so the amendment
adjudication is raised for it at merge.
