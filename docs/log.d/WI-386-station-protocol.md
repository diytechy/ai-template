## 2026-08-01 — WI-386: the station protocol (refresh before merge)

**Summary.** Rebuilt the integrator on the one constraint of
[`concurrency-v2.md`](../concurrency-v2.md) §A2 — *a branch may not enter the
merge queue unless trunk is already an ancestor of it* — and deleted the
machinery that constraint makes unrepresentable. The bar now runs ONCE per WI,
mechanically, on the branch, instead of once self-reported by the builder and
again on a composed candidate tree.

**Deliverables.**

- **The constraint, enforced.** `integrate.trunk_is_ancestor` (one
  `git merge-base --is-ancestor`) plus `bar_green_attestation` (a `Bar-Green:`
  trailer in the refresh commit) are the two reads `_merge_ready` makes before
  the slot merges `--no-ff`. The attestation is a property of the SHA, so a
  later commit on the branch revokes it — no ref namespace, no state file,
  nothing that can outlive the tree it describes.
- **`integrate.py refresh`** — the lane-side station refresh, in the branch's
  own lane worktree: merge trunk in → `trunk_step.py` (compile, then regen) →
  the declared bar → commit. Order pinned by recording stub harness scripts, so
  a reordering fails a test instead of quietly changing what was barred.
- **The refresh is a disposable commit** (§A2.1). `_work_tip` peels it off; a
  retry resets there and redoes the sequence, so a second refresh REPLACES the
  first rather than stacking a merge that would conflict on `docs/log.md`'s
  append-compiled end. Every failure path — conflicting trunk merge, failed
  trunk step, red bar, floor-refused commit — leaves the branch at that work
  commit with a clean tree and nothing parked for a human to unpick.
- **Deleted** from `integrate.py`: the merge-conflict arm, all four
  `merge --abort` paths, `_candidate_worktree` (with its parked-half-merge
  cleanup), the composed-tree bar call, `_teardown`, `CANDIDATE_BRANCH` and the
  `candidate-red` parking branch. `drive._ensure_worktree` went too — the lane
  worktree has one home now (`integrate.lane_worktree`), shared by the worker
  and the refresh so a red is fixable where the lane already lives.
- **The owner's two requirements, built.** `_slot()` is the only `acquire_lock`
  call site in the file, asserted against the source; `drive._drain`'s single
  speculative `refresh` call is the whole speculation, and deleting it restricts
  the design to pessimistic with no other edit and no config dial. The
  pessimistic sequence is not dead code: `integrate_one` refreshes IN the slot
  for any branch that arrives un-refreshed or stale, which every drain that
  merges a second branch reaches by construction.

**Deviations from spec, and why.**

1. **`_composed_tree_script` was kept, renamed `_branch_tree_script`** — the
   only §A9 ledger row not deleted. Verified against the code before cutting:
   the helper exists because a branch may change a generator or the harness
   itself (WI-368), and the invoker is still trunk-vintage whenever `drive.py`
   drives the loop in-process. Deleting it would regenerate and bar the
   refreshed branch with the trunk's copy of `check.py` — reintroducing the very
   defect it was written for. The *composed tree* died; the behaviour did not.
   Its three tests were relocated, not deleted (the Phase 5 precedent).
2. **`check.py --trunk-lane` — a new flag, unanticipated by the plan.** The
   freshness gates stand down on a claimed work branch (SR-133/LLR-141), which
   rests on "a work branch never commits a generated artifact". The refresh
   makes that false for exactly one commit, so without the flag the only
   mechanical bar in the loop would pass over the artifacts the same step had
   just written. Opt-in, so a caller that forgets it gets the stricter answer.
   **This puts LLR-141's Notes out of date (incomplete, not false) — recorded
   for the §A9.1 program close, not amended here.**
3. **`_shed_residue` — added machinery the design did not predict.** The bar
   now runs in the lane worktree, so its own IGNORED tool residue
   (`.pytest_cache/`, `__pycache__/`, a coverage report) made §5.6's unload
   refuse to GC the lane over caches the integrator had itself just created —
   measured, not theorised: the first green e2e run exited nonzero on it. The
   refresh deletes what its own bar added and nothing that predates it, so the
   `out/run-logs/` stream WI-359 names still blocks the unload.
4. **`_verdict_gate` now measures code-time at `_work_tip`.** Structural
   consequence of moving the bar onto the branch: the refresh is the last commit
   before the merge and lands after the review by construction, so counting it
   as "code" would have made RULING-7 unpassable for every WI.
5. **The refresh stages BEFORE it bars, and commits the staged index.** A
   declared bar is the adopter's command; staging first means whatever it writes
   can never be swept into the attested commit by an `add -A` that ran after it.
6. **No spine amendment.** SR-132's description of the composed-tree bar and
   candidate worktree is now false, and LLR-140/LLR-141's Notes are out of date.
   Per the owner ruling (spine work waits, batches, runs alone) and §A9.1, that
   is the program-close row's scope.

**Reviewed baseline bump.** `check.py` 1523 → 1545 in
[`test_module_size_ratchet.py`](../../tests/test_module_size_ratchet.py); nine
of the 22 lines are the argparse help and the comment recording why an opt-in
override to a fail-closed rule is safe. Reason at the entry. Complexity ratchet
untouched (`main` stayed at 16 — the flag is an assignment, not a branch).

**Bars.** Full unfiltered suite `pytest -q -n auto`: **1720 passed, 12 skipped,
2 failed in 505s**; `ruff check .` and `ruff format --check .` clean (146
files); `check_trajectory.py --root . --strict` clean (388 work items, graph
acyclic, only the pre-existing IF-registry connectivity warns §A9.1 already
records). Both failures are pre-existing on this branch and neither is this
change: `test_check_lane.py::test_this_repo_is_not_a_work_branch` (the standing
work-branch failure — the kit's own checkout IS a claimed branch in a claim
worktree), and `test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`
via a stale `work/deferred/` link in `concurrency-v2.md`.

**Finding, not fixed here.** `docs/concurrency-v2.md` links `work/deferred/`
twice, and git tracks no such path — the trunk checkout only resolves it because
an EMPTY untracked directory survives there on disk. Every fresh clone and every
new worktree reds `check_docs` on it. Worth its own row.
