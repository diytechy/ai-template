+++
id = "WI-554"
title = "Approval-brief renderer defects: a Drafted row shown approved, a changed Method cell truncated (OI-71)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Both `trace.py --approve modified` renderer defects (OI-71, decision 20 of
`docs/decisions-for-review-2026-08-31.md`) are reproduced as failing tests
first, then fixed; the fix is carried into the HTML owner view too so the two
renderers agree (IF-074). The "approved, then demoted" vocabulary gap is banked
forward, not fixed here (below).

**Defect 1 — a `Drafted` row's cells shown as "approved — re-attestation
owed".** `_cell_diff_lines` (markdown brief) and `_chain_row` (the
`gen_open_items.py` HTML view) split a changed row's cells into the §A5.1 two
groups keyed on the cell's COLUMN class (`acceptance_record.SPINE_APPROVED_CELLS`),
independent of the row's Status. A `Drafted` row that drifted in both an
approved-class cell (a TC `Method`) and a traced-class cell (its `Evidence`)
therefore rendered its `Method` change under "approved — re-attestation owed" —
asserting a re-attestation window that never opened, since the row was never
approved. Fixed: both renderers collapse the split for a `Drafted` row and
render its changed cells in one unlabelled list; the row owes a FIRST approval
wholesale, which its own section heading/tag already states. Reproduced by
`tests/test_trace_briefs.py::test_reattest_brief_never_labels_a_drafted_rows_cells_approved`
(markdown) and
`tests/test_gen_open_items.py::test_drafted_row_cells_are_not_labelled_approved`
(HTML).

**Defect 2 — a changed cell truncated, hiding the change.** The markdown
brief's `_cell_diff_lines` ran each of before/after through `truncate_cell` (a
1,500-char PREFIX). A changed cell whose divergence sat past the cutoff
truncated before AND after to the identical prefix, so the two rendered the same
and the change vanished. Fixed: a changed cell's before/after renders WHOLE; the
generous cap stays on the CONTEXT surfaces (the anchor Requirement/Rationale,
the whole-row `_full_row_bullets` dumps). The HTML view already rendered changed
cells whole via `word_diff`, so this defect was markdown-only. Reproduced by
`tests/test_trace_briefs.py::test_reattest_brief_shows_a_long_changed_cell_whole`.

Both fixes were driven end-to-end (the tests run `trace.py --approve modified`
as a subprocess and regenerate `open-items.html`), showing a `Drafted` row as
Drafted and a changed cell whole. `trace.py`'s module-size baseline was bumped
+8 SLOC (reviewed) and `_chain_row` was decomposed into
`_changed_cell_groups`/`_changed_cell_lines` to stay under the C901 ratchet; the
one-non-literal-LF-site pin moved with the code. This WI re-statused no spine
rows, so no `docs/ratify/CURRENT.md` regeneration is owed.

**The "approved, then demoted" vocabulary gap — BANKED, its own future row.**
Decision 9 of the same delegated-decisions doc measured that the generator has
no vocabulary for "approved, then demoted": a row whose lane-local approval is
reverted to `Drafted` before reaching trunk reads as "never approved", because
the maturity-ladder enum (`Drafted`/`Approved`/`Founded`) carries no demoted
state. That is orthogonal to the two rendering defects fixed here — it is an
enum/ladder question, not a renderer bug — and touching it risks re-litigating
the D-9 ladder (see `[[d9-ladder-and-cell-attestation]]`). It is therefore
banked, not fixed: it wants its own OI, minted at a trunk sitting (a worker
branch does not mint coordination ids — collision risk on the shared OI
watermark). Its record today is decision 9 of
`docs/decisions-for-review-2026-08-31.md` and this Deliverable; the successor
OI should cite both.

## Context

Round 019 of the wi508 lane returned three MAJORs; two are defects of
`trace.py --approve modified` ON TRUNK, not of the lane (`OI-71`; decision 20
of `docs/decisions-for-review-2026-08-31.md`), and they will reproduce on ANY
lane that regenerates the re-attestation brief — which is why `OI-71`'s
ruling files them ahead of the wi508 close and its successor:

1. a `Drafted` row renders as "approved — re-attestation owed"; related,
   decision 9 banked that the generator has no vocabulary for "approved, then
   demoted" (a lane-local approval reverted before reaching trunk reads as
   "never approved");
2. a changed `Method` cell is truncated in the brief, so the adjudicating
   reader cannot see what actually changed.

## Done-when

Both defects are reproduced as failing tests against the brief renderer,
fixed, and a regenerated brief shows a `Drafted` row as Drafted and a changed
cell whole; the "approved, then demoted" vocabulary gap is either fixed
alongside or explicitly banked with a pointer to its own future row.
