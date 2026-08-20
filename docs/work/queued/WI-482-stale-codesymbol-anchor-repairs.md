+++
id = "WI-482"
title = "Repair the three verified-stale LLR CodeSymbol anchors (LLR-087, LLR-088, LLR-112) — the review's other two anchor claims were refuted (repo review 2026-08-19 M-08, as verified)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "spine"
priority = 2
+++

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
