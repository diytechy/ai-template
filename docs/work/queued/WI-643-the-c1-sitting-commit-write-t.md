+++
id = "WI-643"
title = "The C1 sitting commit: write the redrawn frame, the stakeholder rows and the needs' cells, and move the dial"
workstream = "process"
specref = "docs/plans/2026-09-25-c1-sitting-package.md#6-the-sitting-commit"
sr_refs = ["SR-187", "SR-189", "SR-190"]
needs = ["WI-627", "WI-628", "WI-629"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

Ruled 2026-09-25 (the C1 sitting package, `docs/plans/2026-09-25-c1-sitting-package.md`: build first with arms off, then one reviewed commit). Its §6 is the checklist: the frame rows of §1.2 and header of §1.3, STK-01..STK-04 Approved, every need's `stakeholder_refs`, SN-041 and SN-042's `source`, the dial at DevStg-Boundary, the frame-test pins, the dogfood bite-proof moved off REL-001, the id marks, and the acceptance-record refresh. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Every item of the package's §6 checklist is done in one reviewed commit.
- The frame's pinning test reads 5 entities, 7 crossings and 1 relationship, with the spent ids asserted absent.
- `tests/test_frame_system.py`'s three-leg comparison asserts `"system" in own` for this repository's frame, now that its crossings carry the cell (TC-212's live-frame leg; WI-627 left it passing without the key, as LLR-211 requires until this commit).
- The commit bar, `trace.py --strict` and `check_trajectory.py --strict` pass.
