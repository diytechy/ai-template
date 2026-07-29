## 2026-07-29 — WI-355: `--gate` is silently ignored by `--run-step`/`--run-steps`

`check.py` now honours an explicitly passed `--gate` when it builds a
`--run-step`/`--run-steps` command, while a *defaulted* `--gate` still resolves
to `"all"` — so the documented per-WI bar is the bar that actually runs, and the
pre-commit floor stays warn-first.

**Deliverables**

- `project-trajectory/scripts/check.py`: new module-level `_step_gate(explicit)`
  (beside `resolve_gate`), returning `explicit or "all"` — deliberately *not*
  `resolve_gate`, which reads `docs/gate` and would have armed `--strict` in the
  commit floor the `trajectory` step's comment forbids. `main()` computes it once
  and both step-plan branches use it in place of the hardcoded `"all"`. Name
  lookup is unchanged (the plan is searched unfiltered), so a gate-scoped step
  like `format` is still findable at any gate. One line added to the `--run-step`
  CLI docs; the `trajectory` step's comment now names `_step_gate` instead of
  claiming the flag resolves at `"all"` unconditionally.
- `tests/test_check_harness.py::test_step_gate_honours_an_explicit_gate` — the
  sentinel and the command it builds (`--strict` present at G2/G3, absent at
  `all`), driving `check.steps()` directly.
- `tests/test_pre_commit_hook.py::test_run_steps_gate_promotes_the_warn_first_floor`
  — the behavioral half on the R-E fixture (dangling SpecRef): no `--gate` exits
  0, `--gate G3` exits nonzero naming R-E, and a repaired row goes green at G3
  (so it is not a blanket failure). Both halves pinned together, per the spec.
- Net `check.py` growth +11 lines (1487 → 1498, under the 1500 monolith ratchet);
  `main()` gained no branch, so its pinned mccabe 16 is unchanged; the lane
  region (`_work_branch`/`_TRUNK_FRESHNESS_STEPS`/`_git_out`) was not touched.

**Direct proof**

`check.py --gate G3 --run-steps trajectory` now prints
`... check_trajectory.py --strict`; the same command with no `--gate` prints
`... check_trajectory.py`.

**Deviations / findings**

- The spec's open question "decide what `--list` should print" is answered for
  the explicit case (`--gate G3 --list` and `--gate G3 --run-steps` now agree).
  A residual, by-design divergence remains: with no `--gate`, `--list` reports
  the gate from `docs/gate` while `--run-steps` runs the warn-first floor. That
  is the hook contract, not a defect — left as-is rather than widened here.
- The stale "`--gate` is inert" warnings in `../handoff-2026-07-28*.md` are
  historical session records and were deliberately left unedited (finding, not
  fixed).
- Two failures and four errors are **pre-existing on this branch's base**,
  reproduced identically with this diff stashed (same counts before and after):
  `test_check_lane.py::test_this_repo_is_not_a_work_branch`, which fails by
  construction on any work branch carrying a `docs/work/active/<branch>/` claim;
  and the `test_wi_convert.py` group, which errors on
  `ConvertError: ... directory 'wi-355' is not a status — the spec form knows
  only archive, deferred, queued`. **Finding for the trunk (not fixed here):**
  the Phase 4a claim writes `docs/work/active/<branch>/`, a directory shape
  `wi_convert` rejects, so *claiming any WI* reds five tests in the full tier
  for the life of the branch. That is claim-machinery scope, not WI-355's.

- **Finding hit while closing (not fixed):** §5.2's freshness skip keys on
  `docs/work/active/<branch>/` *existing on disk*
  (`check.py::_claimed_work_branch`). Archiving a branch's LAST spec empties that
  directory, so if it is then removed the branch stops looking claimed and
  `status-map`/`trajectory-map` arm on the very commit that closes the WI —
  demanding the worker regenerate trunk-only artifacts, which §5.2 forbids. Left
  the (now empty, untracked) claim directory in place, which is what `git mv`
  alone leaves; but the close flow should not depend on nobody running `rmdir`.

**Verification** (worktree, main repo's venv, `PYTEST_DEBUG_TEMPROOT` unset)

- Smoke: `630 passed` (2 failed, 4 errors — the pre-existing pair above).
- Full unfiltered: `2 failed, 1881 passed, 8 skipped, 4 errors in 899.11s
  (0:14:59)` — same two pre-existing failures, +3 passing from this WI.
- `check_docs.py --stale`: `OK - 306 doc(s), 906 intra-repo link(s), 0 broken`.
- `check_dupes.py --src project-trajectory/scripts`:
  `OK - no duplicate blocks in 40 file(s)` — no census impact.
- Freshness steps report `SKIP (work branch 'wi-355')` as §5.2 intends.
