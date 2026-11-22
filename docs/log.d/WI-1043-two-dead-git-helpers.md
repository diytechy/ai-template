## 2026-11-21 — WI-1043: Two history helpers nothing calls are removed from the kit's scripts

Deferred open items: none. No spine row changed, and the one scope question
(D-001 below) was the coordinator's to rule and is ruled.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1043` from `1b22c9355`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1043-two-dead-git-helpers.md`).

- **The deletions** (`13ad36174`): `integrate._last_commit_time` and
  `traj_parse._git`, which the history-reader audit found uncalled
  (`../reviews/2026-11-history-readers/README.md`). `gen_trajectory.py` no
  longer re-exports `_git`, and `traj_parse.py`'s docstrings name `_asof` as
  `_run_captured`'s one remaining caller.
- **Deviation from the spec, by the coordinator's ruling (D-001,
  `../decisions/maint-wi-1043.toml`):** the audit and the spec said nothing
  called `traj_parse._git`, but `tests/test_traj_parse.py` did, twice. The
  builder stopped and reported. The coordinator ruled that test-only use is
  not a caller and that the no-reference grep covers code, not records. So
  the two `tp._git` assertions went. `_run_captured`'s off-git degradation
  stays pinned by the same test's `_asof` assertions.
- **Two ratchets tighten:** `integrate.py` re-stamped down 1793 -> 1788 SLOC
  in `tests/test_module_size_ratchet.py`, and the `splitlines()[0]` sweep in
  `tests/test_stage_event_detectors.py` drops `integrate.py`, whose one site
  was inside `_last_commit_time`.
- **RESYNC:** one entry, nothing forced, for the three shipped scripts.
- **Tests:** the 80 modules importing a changed module, with the three
  whole-tree tests: `2 failed, 3249 passed, 20 skipped in 3113.43s
  (0:51:53)` before the sweep's fix. The seven targeted modules at
  `13ad36174`: `1 failed, 99 passed, 1 skipped in 36.94s`. `run_menu.py
  smoke`: the lints pass (`orphans=0 integrity=0`; `check_trajectory`
  clean; `check_resync` OK), and the tier gives `1 failed, 3713 passed, 3
  skipped, 18 warnings in 158.18s (0:02:38)`, with a CPU budget WARN only.
  The build commit's hook: 29 PASS. The unfiltered suite was not run.
  Review round 1 (Sol's MINOR, adopted): the test's off-git checks seed a
  source so `_asof` reaches `_run_captured`, and each records its `log` call.
  The test now fails with `_asof`'s `except OSError` removed. After the fix:
  `3 passed in 2.46s` for `tests/test_traj_parse.py`, and `1 failed, 99
  passed, 1 skipped in 50.08s` for the seven targeted modules (the
  vocabulary red).
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Outside this row:** every failure left is
  `test_stage_ladder::test_this_repo_is_clean_at_the_ERROR_severity`, a
  retired gate tag in WI-1024's queued spec. It is in the base (from
  `1b15d07fb`) and fixed on trunk at `dd8f79e6c`.
- **Byte deltas:** `RESYNC_PACK.md` 737,613 -> 738,316 (unbudgeted). No
  budgeted file was touched.
- **Acts owed:** none.
- **Review:** round 1, OpenAI Sol (low) over the whole diff and Gemini
  Hydrogen (low, the Antigravity CLI) over the prose: Hydrogen APPROVE; Sol
  one MINOR (the `_asof` checks never reached `_run_captured`), adopted and
  fixed in `b47cae466`. Round 2, narrow: Sol `VERDICT: APPROVE findings=0`.
