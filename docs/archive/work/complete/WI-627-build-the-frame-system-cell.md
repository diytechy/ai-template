+++
id = "WI-627"
title = "Build the frame's system-of-interest cell and a requirement's derived system (SR-187, SR-219)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-187", "SR-219"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built test-first against the approved chains SR-187 and SR-219:

- **LLR-211:** `kitlib.spine.SYSTEM_VALUES = ("operation", "delivery")`, the
  crossing tier's optional `system` key, and `System` in both carrier maps. The
  template's example crossing carries `system = "operation"`, and its header
  says what the cell means.
- **LLR-212:** `frame_rules.frame_system_findings`. An out-of-pair value joins
  the frame class and fails `--strict`, naming the crossing; a missing value is
  one advisory; a frame with no crossing is vacuous.
- **LLR-213:** `frame_rules.crossing_systems` and `sr_system_advisories`. A
  requirement naming crossings of both systems is one advisory naming it and a
  crossing of each. A crossing with no system, or with an out-of-pair value,
  places nothing, and nothing is written back.
- **Tests:** `tests/test_frame_rules.py` (TC-213, per-commit tier, 15 cases)
  and `tests/test_frame_system.py` (TC-212, registered slow, 7 cases), each seen
  failing before the code.
- **Seam:** IF-180, `scripts/frame_rules` called by `scripts/trace`, with its
  `Contract IF-180:` body in the module header, cited by TC-213's `verifies`
  (a traced pointer cell, so no re-attestation).
- **Shipped:** `bootstrap.MAPPING`, the bootstrap file list, the kit README,
  and a `RESYNC_PACK.md` entry. The size ratchet was re-stamped for `trace.py`
  (+5, composition only) and `bootstrap.py` (+1).

This repository's own frame reports one advisory per crossing until the C1
sitting commit (WI-643) writes the cells. WI-643's Done-when now asks it to
tighten TC-212's live-frame assertion at the same time.

Review: codex Sol (medium) NOT YET SOUND, 2 major and 1 minor, all applied (the
interface row; the live-frame leg coordinated with WI-643, since LLR-211 keeps
the cells out of this repository's frame until the sitting; a test that an
out-of-pair crossing places nothing).

## Context

The frame's `system` cell on each boundary crossing (operation or delivery), its findings, and the advisory for a requirement whose crossings span both systems. Builds `frame_rules.py`, the pure module the frame and need-tier rules share. The live frame gains the cell only in the C1 sitting commit (WI-643). Design rows: LLR-211, LLR-212, LLR-213. Test cases: TC-212, TC-213. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
