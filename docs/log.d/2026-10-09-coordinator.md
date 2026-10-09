## 2026-10-08/09 (fourth session) — Coordinator: WI-852 and WI-869 landed; WI-874 filed

Resumed from [handoff-2026-10-08c-coordinator.md](../handoff-2026-10-08c-coordinator.md).
The next resume map is [handoff-2026-10-09-coordinator.md](../handoff-2026-10-09-coordinator.md).

**Landed.**
- **WI-852**, the attended review render (`f7e492bf`; acts 71-74). Steps this
  session:
  - The dispute ruling's patch (verdict 006: A, one whole-grammar VERDICT
    check at filing; B, refuse the rollup's own directory) was applied.
  - Its cross-component import was settled as seam (b): `ROLLUP_DIR` moved
    into `kitlib.verdict` (D-006).
  - Terra amended LLR-313 and TC-333; sitting 007 ruled both MEANING and
    blessed them.
  - The lane was rebased onto trunk; the watermark conflict was resolved
    trunk-first and re-bumped, and acts stayed unique.
  - The fourth full-lane review found that a `Rollup` branch filed a review
    the generator then pruned on Windows (case-insensitive path identity).
    It was fixed in-lane as finding B's ruled class, casefolded on every
    platform (D-007), red first.
  - The fifth review, `90c2f740`, was SOUND.
  - The landing's hook missed R-F (the closed row's SpecRef), cleared in
    `50570fab`. Re-mint WI-872 was closed as settled.
- **WI-869**, the smoke tier (`82f2866d`; act 75). One scoped unpause
  (`b58714c9`, restored byte-identical in `295687c7`).
  - Measured first, with the figures in
    [2026-10-09-wi-869-smoke-tier-measurement.md](2026-10-09-wi-869-smoke-tier-measurement.md).
    Cause: membership.
  - Three git-backed modules were re-tiered, and TC-325 to TC-328's tier
    cells went to Full (sitting 001).
  - The first full-lane review asked for the measurement in the log; the
    second, `931a6260`, was SOUND.
  - Re-mint WI-873 was closed as settled.

**Filed.** WI-874: `session_keep.primary_out_dir` spawns git on every store
access.

**Bar.** Trunk smoke at the WI-852 landing: 2436 passed, 2 skipped; enforce
61.5 s, over budget. At the WI-869 landing: 2300 passed, 2 skipped in 33.6 s;
enforce 40.9 s, within 60 s.

**Full suite** at `a68d3177` (a detached worktree, fixed basetemp under
`review-tmp/2026-10-08-coordinator-d/`, deleted once recorded): **1 failed,
5495 passed, 13 skipped** in 880.9 s. The failure,
`test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`, was real:
WI-852's two new rubrics (`docs/rubrics/kit-change-review.md` and
`scope-critique.md`) had no inbound link. The smoke tier does not run that
check. `docs/README.md` now links both, and the test passes (3 passed).

**Decisions.**
- `coordinator-2026-10-08d.toml` D-001 and D-002;
- `wi-852.toml` D-006 and D-007;
- `wi-869.toml` D-001 to D-003.

All await the owner's confirm or overrule.
