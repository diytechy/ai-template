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

### Builders in parallel, and the worktree base

From WI-639 on, each item is built by a builder session in its own git worktree
under the session scratchpad, cut at the trunk's tip, with one shared brief (the
conventions WI-627 surfaced). The integrator reviews each commit with codex
Sol, squash-merges it onto `refactor_again`, closes the spec, regenerates and
runs the bar. The harness's own worktree isolation was tried first and dropped:
it cut the worktrees from the default branch's July commit (3abeb636), 2,948
commits behind; those builders were stopped before they committed anything and
their worktrees deleted. A session limit then interrupted all four builders
mid-work, and each resumed from its own worktree.

### WI-639 — the per-change readability report

- **Built:** `check_readability.py` over a new `[readability]` profile section
  and `[step:readability]`; the complexity adapter reuses `check_complexity`'s
  census, now factored as `functions()`, rather than copying it. This repo
  declares `measures = complexity` with no gating.
- **Tests first:** `tests/test_check_readability.py` (TC-249, slow): red `2
  failed, 9 errors`; green 12, then 15 after the rework.
- **Deviations, accepted at review:** `check_complexity.py` now ships to
  adopters (the shipped report imports it); the template carries its first
  active `[step:]`, and the template-plan identity tests exclude exactly it; the
  measure covers the profile's source and test roots only.
- **Sol review:** NOT YET SOUND, 1 blocker: the build exited 2 on an unknown
  name and 1 on an unreadable change, against approved LLR-256's "nonzero only
  for a worsening in a gating measure". The code was conformed rather than the
  row amended. And 1 major: the merge-base test could not tell merge-base from
  the previous commit, now mutation-checked against both wrong readings. Both
  fixed in the builder's rework.
- **Seams:** IF-187, IF-188, IF-189; watermark IF 180 -> 189. `bootstrap.py`
  ratchet 1666 -> 1668 (two MAPPING rows).
- **Findings for later filing** (not in scope): trace's IF-owner reachability
  advisory does not split `;`-joined `module` cells and builds
  `scripts/scripts/<mod>` keys, so IF-187 gets a false advisory;
  `check_complexity.py --mode enforce` already fails at 76a235bb
  (`route_session` 37 -> 38, stale `traj_*` paths after the `rendering/` move).

- **Commit bar:** smoke **1696 passed, 3 skipped** in 408.1 s; `check.py
  --run-step readability` PASS ("no worsening"); `check_docs --stale` OK;
  `check_trajectory --strict` clean; `trace.py --strict-integrity` 0 integrity;
  `CURRENT.md` fresh; the open-items view up to date. Seconds **FAIL** at 411.8 s
  against 60 s (D10; four builders were loading the box), recorded, not
  re-stamped. The builder's run of the affected slow modules (467 passed, 2
  skipped; then 51 after the rework) stands for the identical squashed tree.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=76a235bb -->
