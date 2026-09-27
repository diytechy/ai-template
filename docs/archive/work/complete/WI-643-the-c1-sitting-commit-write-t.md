+++
id = "WI-643"
title = "The C1 sitting commit: write the redrawn frame, the stakeholder rows and the needs' cells, and move the dial"
workstream = "process"
specref = ""
sr_refs = ["SR-187", "SR-189", "SR-190"]
needs = ["WI-627", "WI-628", "WI-629", "WI-664", "WI-669"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

The C1 sitting commit, made by the owner's Fable stand-in under the owner's
recorded delegation (the package's 2026-09-25 ruling, OI-86 (a), PROCESS.md
§4). Every item of the package's §6 is done:

- **The frame:** 5 entities, 7 crossings and 1 relationship. Each crossing
  carries `system`, and the header is §1.3's text plus the §4 pointer to the
  dial.
- **Stakeholders:** STK-01..04 Approved on the Needs rung.
  `stakeholder_refs` are written on all 31 needs and `source` on SN-041 and
  SN-042.
- **The dial:** `human_approval_through = "DevStg-Boundary"`, its comment
  pointing at the value rather than paraphrasing it.
- **Ids:** B 11, EXT 7 and STK 4.
- **Test pins:** `test_external_frame` pins 5/7/1 and asserts the spent ids
  absent. `test_frame_system` now asserts `"system" in own`. In
  `test_dogfood_sync`, the REL bite-proof moves to REL-002, STK-ID leaves
  LIVE_ROWS_PENDING, and the REL tier is exempted from the generic growth
  floor. `test_hats` and the `test_intake` docstrings are updated.
- **The act:** one approval act for both registries (acts.toml seq 2).

**Reconciled against later acts:** SN-041..SN-044 stay Approved (phase-6
act and OI-86), and the package's stale watermark figures are superseded by
`--bump-ids`. The §2.2 sweep is WI-644. Decisions entry:
`docs/log.d/2026-09-27-c1-sitting.md`. Sol took three rounds (arbitration
rulings 15 and 16) and the last was SOUND.

## Context

Ruled 2026-09-25 (the C1 sitting package, `docs/plans/2026-09-25-c1-sitting-package.md`: build first with arms off, then one reviewed commit). Its §6 is the checklist: the frame rows of §1.2 and header of §1.3, STK-01..STK-04 Approved, every need's `stakeholder_refs`, SN-041 and SN-042's `source`, the dial at DevStg-Boundary, the frame-test pins, the dogfood bite-proof moved off REL-001, the id marks, and the acceptance-record refresh. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Every item of the package's §6 checklist is done in one reviewed commit.
- The frame's pinning test reads 5 entities, 7 crossings and 1 relationship, with the spent ids asserted absent.
- `tests/test_frame_system.py`'s three-leg comparison asserts `"system" in own` for this repository's frame, now that its crossings carry the cell (TC-212's live-frame leg; WI-627 left it passing without the key, as LLR-211 requires until this commit).
- The commit bar, `trace.py --strict` and `check_trajectory.py --strict` pass.
- `"STK-ID"` leaves `LIVE_ROWS_PENDING` in `tests/test_dogfood_sync.py` in the same commit that writes STK-01..STK-04 (WI-628's self-expiring exemption: both dogfood key tests fail once live stakeholder rows exist and the id is still listed).
