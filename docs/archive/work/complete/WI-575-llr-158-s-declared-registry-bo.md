+++
id = "WI-575"
title = "LLR-158's declared registry bound is stale: state the shipped APPROVAL_ACT_CSVS partition in the Detail and code_symbol cells"
workstream = "process"
specref = ""
buildtier = "medium"
priority = 2
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Deliverable

**`LLR-158`'s declared registry bound now states the shipped partition, and
every statement in it was checked by driving the module rather than reading it.**
Three false counts, corrected in one clause of the `Detail` cell:

1. *"every reader here walks `SPINE_CSVS`, the three spine registries"* → the
   walk's universe is a PARAMETER. `staged_spine_amendments` and
   `staged_drafted_rows` take the `SPINE_CSVS` default (three); `staged_approval_acts`
   passes `APPROVAL_ACT_CSVS` (four — the three PLUS `stakeholder-needs.toml`),
   and `lane_approval_refusal` is the judgement over that reader, so it refuses a
   lane signing a NEED as readily as one signing an LLR.
2. *"the four other registries a snapshot anchors are listed in
   `OUTSIDE_THE_APPROVAL_ACT`"* → THREE (interfaces, external, components).
   `7 − 3 = 4` was the arithmetic the stale clause preserved from before the
   need tier joined the approval-act set.
3. *"the two lists are pinned … against `baseline_snapshot.SNAPSHOTTED`"*
   without naming which two → the pinned identity is stated literally:
   `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT`, over
   `SNAPSHOTTED`'s seven.

The `code_symbol` cell named `OUTSIDE_THE_APPROVAL_ACT` alone of the three
constants; it now carries `SPINE_CSVS/APPROVAL_ACT_CSVS/OUTSIDE_THE_APPROVAL_ACT`,
and every symbol in the cell resolves as an attribute of the module the row owns.

**Driven, not read.** Importing `acceptance_record` and `baseline_snapshot` and
printing the three tuples: `SPINE_CSVS n=3`, `APPROVAL_ACT_CSVS n=4`,
`OUTSIDE_THE_APPROVAL_ACT n=3`, `SNAPSHOTTED n=7`, and
`sorted(SNAPSHOTTED) == sorted(APPROVAL_ACT_CSVS paths + OUTSIDE_THE_APPROVAL_ACT)`
→ `True`; `_spine_row_sides`'s `registries` default is `SPINE_CSVS`, and only
`staged_approval_acts`'s body names `APPROVAL_ACT_CSVS`.

**NO STATUS MOVED AND NO SNAPSHOT WAS WRITTEN.** `LLR-158` stays `Approved`;
nothing under `docs/archive/last_approved/` was touched and `intake.py snapshot`
was not run in any form. Amending an Approved row's text stages a
`staged_spine_amendments` hit, which mints the amendment adjudication at this
row's own merge; that trunk-side adjudicator, on a rung released to the loop and
with the defect that withheld the last re-attestation now corrected, takes the
re-anchor. Taking it here would have hard-refused this very merge
(`lane_approval_refusal` refuses any lane delta touching `SNAPSHOT_DIR`), and
having the lane that authored the corrected text bless its own write is exactly
the separation the act was moved to the adjudicator for.

Only the one cell pair on the one row changed in the registry. The approval
brief `docs/ratify/CURRENT.md` was regenerated because a spine cell moved.

## Context

Drafted by WI-573 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

VERDICT THIS CONTINUES: `docs/reviews/wi-573-adjudicate-llr-136-llr-158/001-ADJUDICATE-07cbabb.md`,
governing line `VERDICT: MEANING rows=2` over `LLR-136` and `LLR-158`. Both are
MEANING, so the flip-back arm does not apply; this successor exists because the
re-attestation the rung released to the loop was WITHHELD, and why it was
withheld is a build gap rather than a signature gap.

IN SCOPE — one cell's last clause and one `code_symbol` cell.
`LLR-158`'s `Detail` closes with *"every reader here walks `SPINE_CSVS`, the
three spine registries … the four other registries a snapshot anchors are listed
in `OUTSIDE_THE_APPROVAL_ACT`"*. The module it owns says otherwise:
`staged_approval_acts` and `lane_approval_refusal` walk `APPROVAL_ACT_CSVS` —
the spine three PLUS `stakeholder-needs.toml` (`acceptance_record.py:144`, :541;
`tests/test_acceptance_record.py:216`) — `OUTSIDE_THE_APPROVAL_ACT` holds three
registries and not four (:165), and the pinned exhaustive identity is
`SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT` (:162,
`tests/test_acceptance_record.py:234-235`). The cell was written at `d5b3e124`
and the widening landed after it at `94b77a26`; the row was never re-read
against its own rework. Re-state the bound as shipped, add `APPROVAL_ACT_CSVS`
to the row's `code_symbol` beside `OUTSIDE_THE_APPROVAL_ACT`, and say which
constant each of the four readers walks — the row's whole claim is that a tier
joining the snapshot cannot reach no approval reader, and a false partition
makes that claim unfalsifiable rather than merely imprecise.

OUT OF SCOPE — the design. `APPROVAL_ACT_CSVS` covering the need tier is the
2026-09-01 ruling as WI-572 round 028 applied it, and this row does not reopen
it. Nothing in `acceptance_record.py`, `intake.py` or the tests changes; this is
a requirement-tier correction to make the row true of the code that shipped.

NOT ON THIS LANE — the anchor. This lane corrects the text and then STOPS. It
does not run `python project-trajectory/scripts/intake.py snapshot` in any
form and it writes nothing under `docs/archive/last_approved/`. Taking the
snapshot is never a work lane's act — the approval act (the `Status` flip and
the anchor that records it) belongs to a trunk-side adjudication session
(`docs/plans/2026-09-01-approval-act-adjudicator-only.md` §2a) — and
`lane_approval_refusal` refuses any lane merge whose delta touches
`SNAPSHOT_DIR`, so taking the anchor here would hard-refuse this very row's
merge.

WHERE THE RE-ANCHOR HAPPENS INSTEAD — at THIS successor's merge. Correcting an
Approved row's text stages a `staged_spine_amendments` hit, which mints an
amendment adjudication at that merge. That trunk-side adjudicator, on a rung
released to the loop and with the defect this verdict withheld against now
corrected, performs the re-attestation under the released-rung aftermath arm of
`project-trajectory/prompts/adjudicate-amendment.template.md`: every row's
`Status` stays `Approved`, and `python project-trajectory/scripts/intake.py
snapshot --approves "docs/requirements/low-level-requirements.toml=<that
adjudication row's id>"` is taken on trunk in its own reviewed commit. Nothing
about that is owed to this lane, and nothing about it is owed to the owner: the
LLR rung sits above the approval threshold.

Because `copy_live` mirrors whole registry files, that one act also re-anchors
`LLR-136` — whose amended text this adjudication verified accurate and would
have blessed on its own — and `LLR-058`, `LLR-144`, `LLR-198`, the WI-566
MEANING set whose text likewise matches the tree. Naming only the LLR registry
there is deliberate: the SR and TC registries hold rows this row did not judge.
