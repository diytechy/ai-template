+++
id = "WI-514"
title = "Render the reviewable spine text (anchor SR requirement, chain rows, drift) on both owner approval surfaces"
specref = ""
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Both owner approval surfaces now render an owing SR's own Requirement (verbatim)
and Rationale UNCONDITIONALLY — the gap SR-177 exposed. Record:
[../../../log.d/2026-08-24-wi514-brief-carries-text.md](../../../log.md#2026-08-24---puts-the-anchor-srs-own-reviewable-text-on-both-approval-surfaces).

**The gap.** `trace.reattest_model` (widened by `WI-513` to ask the `Drafted`
question of every chain row, not just the SR) already rendered a `Drafted`
LLR/TC's full cells and a drifted cell's before/after, un-hidden, on both
surfaces. What neither renderer ever rendered was the ANCHOR SR's own text
when the SR row itself carries no diff and is not `Drafted` — SR-177's exact
shape: `Approved`, undrifted, its whole amendment living in `Drafted`
children `LLR-196`/`TC-191`. In that shape `reattest_model` never appends the
SR to `entry["rows"]` at all (the `if cells or drafted:` gate), so the
markdown brief's `## SR-177 — …` section skipped straight to its chain rows,
and the HTML card's only copy of the SR's `Requirement`/`Rationale` sat
inside `_context_block`'s `.ctx` div — `display:none` until the "Collapse
unchanged text" toolbar box (checked by default) is cleared. Present in the
bytes, invisible on load: exactly the owner's report.

**The fix** (`project-trajectory/scripts/trace.py`,
`project-trajectory/scripts/gen_open_items.py`). A shared, explicit-marker
truncation, `trace.truncate_cell` (1,500-char threshold,
`"… [N more chars — read the registry row]"`, never silent), that
`gen_open_items.py` imports rather than re-deriving its own limit.
`trace._anchor_lines` (markdown) and `gen_open_items._anchor_block` (HTML)
render the anchor SR's `Requirement`/`Rationale` UNCONDITIONALLY for every
owing entry: right after the `## SR-ID — Title` heading in the brief, before
the no-baseline/chain-row branches; in the HTML, in a plain
`<div class="anchor">` placed BEFORE the collapsible `.ctx` div rather than
inside it, so it renders with the toolbar checkbox in its default (checked)
state. `_context_block`'s existing "rest of the SR" block now skips
`Requirement`/`Rationale` (`_ANCHOR_CELLS`) so the two never render twice.
The same `truncate_cell` was threaded through the two places that already
rendered full cell text (`_full_row_bullets`, `_cell_diff_lines`,
`gen_open_items._chain_row`'s full-cell branch and `_context_block`) so a
long `Detail`/`Method` degrades the same explicit way, not only the new
anchor block.

**Driven by tests** (`tests/test_gen_open_items.py`,
`tests/test_trace_briefs.py`): the anchor Requirement/Rationale render
visibly, before the `.ctx` div, for the exact SR-177 shape (an `Approved`,
undrifted SR with a `Drafted` child) and are not duplicated inside the
collapsed remainder; a cell above the 1,500-char threshold truncates with the
explicit marker and a cell below it renders untouched, on both surfaces; the
markdown brief's `test_reattest_brief_owes_a_drafted_llr_under_an_approved_
undrifted_sr` now also asserts the anchor `Requirement` line appears.

**Surfaces regenerated, no approval act taken.** `docs/open-items.html`'s
`SR-177-attest` card now opens with the Requirement paragraph and the
(truncated) Rationale paragraph immediately after the heading pill, before
`class="ctx"`. `docs/ratify/CURRENT.md`'s `## SR-177 — …` section now opens
with `> **Requirement.** …` / `> **Rationale.** …` quoted lines before its
`### LLR LLR-196` / `### TC TC-191` blocks. Full before/after text and gate
output are in the log fragment above.

## Context

The owner's report, verbatim (2026-08-24, in-session, reviewing SR-177's
entry): *"if I open open-items.html, and look at SR-177, I don't see the
actual requirement text in that document to be able to review."*

`WI-513` (same day) widened `owes()` so a `Drafted` LLR/TC under an
`Approved`, undrifted SR reaches the owner brief at all — SR-177 is one of
the ten SRs that widening surfaced. But widening WHICH rows appear did not
guarantee WHAT they show: `reattest_model`'s row-building loop only appends
the SR itself to `entry["rows"]` when it carries a cell diff or is itself
`Drafted` (`if cells or drafted:`), so an SR whose amendment lives entirely
in a child never gets its own row — and the only other place its text could
have appeared, `gen_open_items._context_block`'s "rest of the SR" block, was
built as COLLAPSED context (`.ctx`, hidden behind the "Collapse unchanged
text" toolbar box, checked by default) — a control built for genuinely
secondary fields (`SN-Refs`, `Boundary-Refs`, …), not for the one thing a
reader needs to review the acceptance at all.

Render the anchor SR's own Requirement/Rationale unconditionally on both
surfaces, outside any collapse toggle, with the same explicit-marker
truncation the rest of the reviewable-text surface now carries. Do not
approve anything: the corrected surface is what the owner reviews from,
next.
