+++
id = "WI-510"
title = "Decompose the two stray orphan SRs no queued row owns: SR-160 (front-door launchers) and SR-164 (declared SN scope)"
specref = "docs/log.d/2026-08-22-orphan-foldins.md"
workstream = "requirements"
sr_refs = ["SR-160", "SR-164"]
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Context

Owner-directed 2026-08-22: the orphan-debt mapping placed five of the
seven undecomposed SRs (plus LLR-164's missing TC) with queued rows that
already own their subjects (SR-151/152 → the test-evidence carrier row,
SR-162 → the wi455 lane, SR-163 → the remap program, SR-177 + LLR-164 →
the session-continuity row — each carries a fold-in note and the sr_ref).
This row takes the two strays:

- **SR-160** — front-door launchers for the two universal contributor
  actions (`run_menu` / the `agent-resume.*` surface). Read the row and
  the live launchers; decompose into LLR/TC, or — if the obligation is
  genuinely a launch-surface inspection rather than a testable behavior —
  re-class its Verification to Analysis/Inspection with the reasoning on
  the row (the orphan rule accepts that honestly; do not re-class just to
  clear the finding — the WI-475 launcher tests suggest the behavior IS
  testable, which is the default expectation here).
- **SR-164** — stakeholder-need scope is a declared, checked value. The
  declared-surface + checker pattern is well-worn (the SN scope
  declaration and whatever validates it); decompose to the LLR naming the
  checker seam and the TC driving it.

Both mints land Drafted (no selection movement — the effective stage
excludes drafts) and ride the ordinary approval machinery under the
DevStg-Needs dial. Closing this row plus the four fold-ins zeroes the
orphan debt, which is what currently holds the ladder at DevStg-LLReqs.
