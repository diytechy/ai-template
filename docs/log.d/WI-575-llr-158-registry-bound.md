## 2026-09-02 — WI-575: LLR-158's declared registry bound corrected to the shipped APPROVAL_ACT_CSVS partition

Deferred open items: none — the re-anchor of LLR-158 is owed by the amendment adjudication this row's own merge mints, not by this lane.

The WI-572 lane rewrote `LLR-158`'s `Detail` to oblige the shared two-tree walk
and its four consumers, and closed it with a declared registry bound that was
already stale when it was written. The amendment adjudication ruled the row
MEANING and WITHHELD the re-attestation, because the bound was false on three
independent counts. This row corrects the text; it is a requirement-tier
correction only, and nothing in `acceptance_record.py`, `intake.py` or the tests
moved.

### What was false, and what the cell says now

- *"every reader here walks `SPINE_CSVS`, the three spine registries"* — the
  walk's universe is a parameter. `_spine_row_sides` defaults to `SPINE_CSVS`,
  which `staged_spine_amendments` and `staged_drafted_rows` take; but
  `staged_approval_acts` passes `APPROVAL_ACT_CSVS` — the spine three PLUS
  `stakeholder-needs.toml` — and `lane_approval_refusal` is the judgement over
  that reader. Two of the four named consumers do not walk `SPINE_CSVS` at all.
- *"the four other registries a snapshot anchors are listed in
  `OUTSIDE_THE_APPROVAL_ACT`"* — there are three: interfaces, external,
  components. `7 − 3 = 4` is the arithmetic the clause preserved from before
  the need tier joined the approval-act set.
- The pinned identity was left implicit and, as implied, wrong. It is
  `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT`, and the cell
  now states it literally.

The `code_symbol` cell carried `OUTSIDE_THE_APPROVAL_ACT` and neither of the
other two constants — the same miss, in the other cell. It now names all three.
Every symbol in it resolves as an attribute of the module the row owns.

### Driven, not read

Importing both modules and printing the tuples: `SPINE_CSVS n=3`,
`APPROVAL_ACT_CSVS n=4`, `OUTSIDE_THE_APPROVAL_ACT n=3`, `SNAPSHOTTED n=7`, and
the union identity `True`. `_spine_row_sides`'s `registries` default is
`SPINE_CSVS`; only `staged_approval_acts`'s body names `APPROVAL_ACT_CSVS`.
Each sentence of the new clause was checked against that output.

### No Status moved and no snapshot was written

`LLR-158` stays `Approved`. Nothing under `docs/archive/last_approved/` was
touched, and `intake.py snapshot` was not run in any form. That is not caution,
it is the route: amending an Approved row's text stages a
`staged_spine_amendments` hit, which mints an amendment adjudication at this
row's own merge, and that trunk-side adjudicator — on a rung released to the
loop, with the defect the last verdict withheld against now corrected — takes
the re-attestation. Taking the anchor on this lane would hard-refuse this very
merge, since `lane_approval_refusal` refuses any lane delta touching
`SNAPSHOT_DIR`; and the lane that authored the corrected text blessing its own
write is precisely what moving the approval act to the adjudicator prevents.
Because `copy_live` mirrors whole registry files, that one later act also
re-anchors the other amended LLR rows riding in the same file.

`docs/ratify/CURRENT.md` was regenerated — a generated surface, not the
snapshot — because this row amended a spine cell.
