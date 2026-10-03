# Sonnet review — WI-745 (build/wi-745)

Reviewer: Claude Sonnet 5.5 (Agent subagent, read-only). Builder: Codex Sol (gpt-6.1-sol, low effort). Range `2e13b2bd..b4d9d00b`.

b4d9d00b SOUND

**BLOCKER:** none

**MAJOR:** none

**MINOR**
- `tests/test_baseline_drift.py:55-56` says the live registries "carry no Drafted row since the 2026-08-20 signing"; false of the live tree today (one Drafted SR, one Drafted TC), true of the temp copy only because `_tree` forces it. Stale, harmless, not touched by the commit.
- `tests/baseline_snapshot_fixtures.py:31-42` hardcodes the LLR and TC paths beside the `SR_REL` constant. Cosmetic.

(Coordinator: both accepted as built; no fix round.)

**1. Re-seed equivalence.** Old setup `_seeded` = `_tree` + `copy_live(seed=True)`; new = `_tree` + plant a Drafted LLR + `copy_live(seed=True)`, the `_seeded_with_a_drafted_sr` pattern. The SR amendment, the Drafted->Approved flip and every assertion are unchanged.

**2. The `_tree` normalisation.** Only `test_baseline_snapshot.py` and `test_baseline_drift.py` use the fixtures. Every Approved->Drafted rewrite now finds a row; every Drafted->Approved flip follows a planted row or a self-built tree. Live state was SR 119/1, TC 270/1, LLR 268/0 (Approved/Drafted), so the one Drafted SR was already a latent coupling. The regex `(?m)^status = "[^"]+"` is column-0 anchored and byte-level; column-0 status lines equal row counts (120/268/271); the one mid-line hit (inside an SR rationale) is not matched. IF/CMP/SN registries untouched. Smallest change meeting the sweep clause; a fully drafted live spine is handled too.

**Commands:** in the worktree with `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`, `pytest -q -n 2 -p no:cacheprovider tests/test_baseline_snapshot.py tests/test_baseline_drift.py`: `128 passed in 124.12s`; `git status --short` clean after.
