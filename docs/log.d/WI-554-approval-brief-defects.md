## 2026-09-01 — WI-554: two `trace.py --approve modified` renderer defects (OI-71)

Round 019 of the wi508 lane returned two findings that are defects of the
re-attestation brief renderer ON TRUNK, not of that lane (OI-71, decision 20 of
`docs/decisions-for-review-2026-08-31.md`). They reproduce on any lane that
regenerates the brief. This WI reproduces each as a failing test, fixes it, and
regenerates the brief.

### Defect 1 — a `Drafted` row's cells render under "_approved — re-attestation owed_"

`_cell_diff_lines` splits a changed row's cells into the §A5.1 two groups —
`approved — re-attestation owed` / `traced — routes to adjudication` — keyed on
the cell's COLUMN class (`acceptance_record.SPINE_APPROVED_CELLS`), independent
of the row's Status. So a `Drafted` row that drifted from the snapshot in both
an approved-class cell (a TC `Method`) and a traced-class cell (its `Evidence`)
renders its `Method` change under "_approved — re-attestation owed_" — asserting
an attestation window that never opened. A `Drafted` row was never approved: it
owes a FIRST approval wholesale (the section heading already says so), and no
cell of it arms a re-attest window.

**Fix:** `_cell_diff_lines` takes a `drafted` flag; for a Drafted row it renders
every changed cell in one undifferentiated list with no group heading — the
§A5.1 split is a property of a row that has been blessed. The renderer passes
`row["drafted"]`.

### Defect 2 — a changed cell is truncated, hiding what changed

`_cell_diff_lines` ran each of before/after through `truncate_cell` (1,500-char
prefix). A changed cell longer than the limit whose divergence sits past char
1,500 truncates before AND after to the SAME prefix, so the two render
identically and the reader cannot see what changed. Done-when calls for the
changed cell rendered WHOLE.

**Fix:** render a changed cell's before/after without truncation. The generous
`truncate_cell` cap stays on the CONTEXT surfaces (the anchor Requirement /
Rationale, `_full_row_bullets` whole-row dumps) — the change under review is the
one thing the reader must see entire.

### The "approved, then demoted" vocabulary gap (decision 9)

Banked, not fixed here — see `## Deliverable`. A lane-local approval reverted to
`Drafted` before reaching trunk reads as "never approved" because the ladder
enum carries no demoted state; this is orthogonal to the two rendering defects
and is filed forward.
