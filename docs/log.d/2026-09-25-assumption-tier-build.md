## 2026-09-25 — The assumption tier's build, test-first (WI-627 onward)

The build of the phase-6 chains approved at cbb6649f, one work item at a time
in the generated frontier's order, each test written from its approved test
case and seen failing before the code that turns it green (SN-042's own rule).
Reviews are codex Sol (medium); a Fable (medium) agent arbitrates any
disagreement. Attended, on `refactor_again`, with the loop paused.

Deferred open items: none — the owner-reserved decisions stay numbered in the
spine map §6, and none holds a gate or blocks a queue.

### WI-627 — a crossing's system of interest, and a requirement's derived one

- **Built:** `kitlib.spine.SYSTEM_VALUES = ("operation", "delivery")` and the
  crossing tier's optional `system` key, mapped both ways by the carrier
  (`System`); the template's example crossing carries it, and its header says
  what it means. `frame_rules.py`, a pure sibling of `coherence.py`:
  `frame_system_findings` (an out-of-pair value joins the frame class and fails
  `--strict`; a missing one is one advisory), `crossing_systems` and
  `sr_system_advisories` (a requirement naming crossings of both systems is one
  advisory naming it and a crossing of each). `trace.analyze` composes them.
- **Tests first:** `tests/test_frame_rules.py` (TC-213, in-memory, per-commit
  tier) failed at collection before the module existed;
  `tests/test_frame_system.py` (TC-212, scaffold + `trace.py`, registered in
  `SLOW_MODULES`) had 4 of 7 failing, the 3 vacuous cases passing. Both green
  after the build (15 and 7 passed), with `tests/test_external_frame.py`'s 20
  still green.
- **This repo's own frame** now prints one advisory per crossing (B-01, B-02,
  B-04, B-05) declaring no system. That is expected until the C1 sitting commit
  (WI-643) writes the cells; it never moves the exit code.
- **Ratchet:** `trace.py` 3372 -> 3377 (the composition lines alone, per D21)
  and `bootstrap.py` 1665 -> 1666 (the MAPPING entry), re-stamped with the
  reason at each entry.
- **Seam:** IF-180 (`scripts/frame_rules` called by `scripts/trace`), its
  contract body in the module header, cited by TC-213's `verifies`, a traced
  pointer cell that re-opens no attestation. `check_trajectory` requires a
  citing test case for every seam.
- **Sol review:** NOT YET SOUND, 2 major, 1 minor, all applied. The interface
  row was first left out on `coherence.py`'s precedent; Sol held the Done-when
  to its word. TC-212's live-frame leg: LLR-211 keeps the cell out of this
  repository's frame until the sitting, so the scaffold's frame is the live
  leg now, and WI-643's Done-when tightens the assertion when the cells land.
  Added a case pinning that an out-of-pair crossing places nothing.
- **Back-link coverage** reads 45.2% against the 50% dial. That predates this
  item (the 47 phase-6 design rows landed at c47143d4 with no code) and rises as
  the build lands.
- **Adopters:** `RESYNC_PACK.md` entry "A boundary crossing names its system of
  interest", anchored at the preceding commit per the pack's rule.
- **Commit bar:** smoke **1696 passed, 3 skipped** in 366.6 s; the slow frame,
  bootstrap and dogfood modules 124 passed, 1 skipped. Seconds **FAIL** at
  367.6 s against 60 s (D10; the box was loaded), recorded, not re-stamped.
  `check_docs --stale` OK; `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity; `CURRENT.md` fresh; the open-items view up
  to date.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=cbb6649f -->
