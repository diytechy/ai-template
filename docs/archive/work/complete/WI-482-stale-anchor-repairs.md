+++
id = "WI-482"
title = "Repair the three verified-stale LLR CodeSymbol anchors (LLR-087, LLR-088, LLR-112) — the review's other two anchor claims were refuted (repo review 2026-08-19 M-08, as verified)"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "spine"
priority = 2
+++

## Deliverable

Repaired the three verified-stale LLR CodeSymbol anchors by re-pointing
each to its live realizing symbol, verified by READING the target code
first: LLR-087 → `traj_render._drill_layer_svg/_render_drill` (module cell
moved too — gen_trajectory only imports the names, which module_bindings
does not count); LLR-088 → `traj_render.DRILL_SCRIPT` (the descend/
breadcrumb logic lives inside that embedded-JS constant, matching sibling
LLR-100's existing citation shape); LLR-112 → `gen_trajectory.HTML_TEMPLATE`
(the literal carrier of the querySelectorAll wiring and roving tabindex
TC-117 exercises). TRACED-cell moves only — no normative text touched; the
snapshot refreshed byte-identical; `check_doc_refs` shows zero occurrences
of the three ids in the dangling/untraced lists post-fix;
`--strict-integrity` exit 0. The spec's second half (a declared
planned-symbol form) EVALUATED AND DEFERRED with reasoning: no live row
needs it today (both NOT-BUILT rows anchor on symbols that resolve), and a
marker grammar in `check_doc_refs.symbol_findings` should follow WI-472's
obligation SR rather than precede and pre-empt it.

## Context

The review claimed five bad live anchors; verification 2026-08-19 confirmed
THREE and refuted two — repair only the three:

- **LLR-087** cites `gen_trajectory::_drill_svg` / `_drill_edges`: neither
  name exists anywhere under `project-trajectory/scripts/`; the live
  descendants are `traj_render._drill_layer_svg` and `traj_render._render_drill`
  (different module, different names). Re-point after reading what the row
  actually pins.
- **LLR-088** cites `_descend` / `_breadcrumb`: zero occurrences in any
  script.
- **LLR-112**'s `code_symbol` is a SENTENCE ("emitted querySelectorAll
  wiring; tabindex + native-link emission"), not an identifier — the
  underlying constructs exist in `gen_trajectory.py`; the cell needs a real
  resolvable symbol (or the row needs the declared not-yet-resolvable form,
  below).

REFUTED, recorded so nobody re-litigates: LLR-015's `trace.py::budget_findings`
exists (a populated local + `Findings` field doing exactly the row's stated
job), and LLR-172 honestly self-labels `Drafted`/"NOT BUILT YET" with its
`code_symbol` naming the extension point by documented intent.

Second half, from the review's suggestion: give PLANNED symbols a declared
form so a future-tense anchor is distinguishable from a stale one (LLR-172 is
the exemplar case), and judge whether `check_doc_refs` should default to live
normative registries with historical scans opt-in — the broader promotion of
live CodeSymbol resolution waits on OI-42's direction and WI-472's obligation
row; this WI is only the three standing repairs plus the planned-form
convention.

Spine note: these are LLR cell edits — `safety_class = "spine"`, and the cheap
window is BEFORE the sitting signs (the amendment window is open; each spine
amendment re-reddens the ratify brief's freshness check, so batch these with
other pre-sign acts if possible). WI-472 (the CodeSymbol obligation SR) is
adjacent but independent: neither blocks the other.
