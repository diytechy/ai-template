Reviewed: bff20201428265f201256c780273bc9b4e21609a

**Verified.** This was a full-lane review in the convergence stance over 37bcca3b8..bff20201. I confirmed that `git rev-parse HEAD` prints bff20201428265f201256c780273bc9b4e21609a. I read the spec of record (docs/specs/WI-967.md: The record, Trust, Architectural delta, Critique dispositions), the row's Done-when and the rubric docs/rubrics/kit-change-review.md. I hunted three failure classes in severity order: silent wrong content (a wrong or missing `copied`), fail-open (an added entry without `copied` reaching trunk) and false refusal of a supported route (refresh, slot merge, squash landing).

- **Writer.** It records `copy_live`'s own `copied_rels`, the canonical SNAPSHOTTED paths `_copy_registry` actually wrote. It never rebuilds the set from row ids. The needs file is recorded by its `.toml` path when its `.md` carrier is live.
- **Readers.** `parse_acts` adds `copied` only when the entry carries it, so a legacy entry's dict is unchanged.
- **Whole-file rule.** `_copied_problems` checks the shape of `copied` and `_copied_order_problems` checks the order. Both are in `acts_problems`.
- **Commit rule, end to end.** I drove it through the real `trace.py --strict-integrity` on a scratch clone. Staging an appended seq-165 entry without `copied` gives `integrity=1` and exit 1, and the finding names seq 165 and the remedy. A `git merge --squash` of a lane holding such an entry is also refused (exit 1).
- **Regression tests fail on pre-fix code.**
  - With the base `baseline_snapshot.py` and `acceptance_record.py`, 19 of the new or extended cases fail and the 2 guards pass.
  - The fix-round remedy text is confirmed by `test_an_old_writers_uncommitted_act_is_recovered_by_abandoning_it`. It fails on the pre-fix blob 204090e0c at `assert _naming(stuck, "git checkout HEAD -- ...")`.
- **Consolidation (PROCESS.md §3).** `acceptance_record.added_ledger_entries` is now the one "entries a commit adds by seq" reading. `_added_acts`, `_acts_at` and the new rule share it. A grep finds no other seq comparison left.
- **K3.** Every new `Implements: SR-178, LLR-361` tag sits on a function listed in LLR-361's `code_symbol`, and LLR-361's module is baseline_snapshot.py. `added_ledger_entries` is tagged LLR-278, whose `code_symbol` gained it. `CodeSymbol` is a traced LLR cell (`SPINE_TRACED_CELLS`), so the Approved row needs no act. No Status flips.
- **IF-220 consumers (D5).** The `consumers` list equals the union of the plan's two `git grep`s at the tip: acceptance_record, gen_open_items, kitlib/sitting, trace.
- **Row sweep.** LLR-361 and TC-400 are both Drafted. LLR-361 is true to the code (K1) and names no carrier at the SN/SR tier (K2). It has no contradiction with LLR-239, LLR-271 or LLR-278. TC-400's evidence ids all exist.
- **Size ratchet.** It passes.
- **Done-when map.**
  - D1 and D2: bookkeeping (ticked).
  - D3: the approval, re-attest, traced re-anchor, mixed, re-seed and needs-canonical tests, all through `intake.py snapshot`.
  - D4: the six `_BAD_LEDGERS` copied cases, the legacy-parse test, the commit-adds, foreign-path, legacy-not-refused and merge tests, the readers test, and my live trace run.
  - D5: the IF-220 row (checked above).
  - D6: the RESYNC entry, with the MINORs below.
  - D7: a landing-tip gate that this review cannot discharge. At this tip `check_trajectory --strict` is clean, `--strict-integrity` gives `integrity=0` and the targeted suite is green.

Coverage-extension notes (no severity):
- `_copy_registry` deletes the stale copy of an in-scope registry that has no live carrier, and `copied` does not name that deletion. The spec defines `copied` as the files written, so this is within scope. It is a fact WI-963's settlement should know.
- `acts_findings` reads the working tree. The commit rule defers to it when the index ledger is malformed, so a partially staged malformed ledger is judged on the working tree's copy. This pre-dates the lane and is only reachable through a hand edit.

**Commands**
- `git rev-parse HEAD` -> bff20201428265f201256c780273bc9b4e21609a
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../g-967-B/wi-967 tests/test_baseline_snapshot.py tests/test_acceptance_record.py tests/test_snapshot_readers.py` -> `219 passed in 637.23s (0:10:37)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (985 work item(s), 871 done (88%), 34 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` (lane) -> `Traceability: SN=31 SR=138 LLR=327 TC=354 orphans=0 integrity=0 ... drafts=2 ...`, exit 0
- scratch clone, appended seq-165 entry without `copied`, staged, `trace.py --strict-integrity` -> `... integrity=1 ... approval-record=1`, exit 1
- scratch clone, `git merge --no-ff --no-commit lane` (lane commit holds a legacy-shaped seq-165 entry) -> `integrity=0`, exit 0; `git merge --squash lane` -> `integrity=1`, exit 1
- scratch clone, base `baseline_snapshot.py` and `acceptance_record.py` with the tip's tests, `pytest -k <new cases>` -> `19 failed, 21 passed`
- scratch clone, pre-fix blob 204090e0c, `pytest ...::test_an_old_writers_uncommitted_act_is_recovered_by_abandoning_it` -> AssertionError at the `git checkout HEAD --` remedy assertion
- scratch clone, base `acceptance_record.py` with the tip's `baseline_snapshot.py`, `trace.py --strict-integrity` -> `AttributeError: module 'acceptance_record' has no attribute 'added_ledger_entries'`, exit 1
- `pytest tests/test_module_size_ratchet.py` -> `4 passed`

**Findings**

- [MINOR] project-trajectory/RESYNC_PACK.md:10181 -> Rubric anchor B1, confirmed by running. In a merge, the commit-bound rule exempts every entry MERGE_HEAD holds (project-trajectory/scripts/baseline_snapshot.py:1763), so the slot's `integrate` `git merge --no-ff <lane>` landing never judges an entry the lane added. Scenario: an adopter re-syncs while a lane already has a committed act taken by the un-re-synced writer, and that lane lands through the slot before trunk takes another act. The entry then reaches trunk legacy-shaped, with exit 0 (reproduced above). From then on it reads as "copy set unknown" for a post-re-sync act. The RESYNC entry covers only an act that is "not yet committed". The plan's rejection of cut (c) also rests on a false premise: it claims the slot's commit "judges every entry the landing adds against trunk" (docs/plans/WI-967/plan.md:51). The read is fail-safe (unknown, never a wrong set), hence MINOR. -> Add one RESYNC bullet: before re-syncing, land (or abandon and retake) every lane holding a committed act, or retake such a lane's acts after it refreshes, because the slot's merge does not judge them. This is a wording remedy, not a guard; judging against the merge base instead would falsely refuse every trunk refresh into a pre-re-sync lane. -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:10175 -> Rubric anchor B1, confirmed by running. The entry's overwrite list names `scripts/baseline_snapshot.py` and the README template only. But `baseline_snapshot.py` now calls `acceptance_record.added_ledger_entries`, which this lane added to `scripts/acceptance_record.py`. An adopter who keeps a locally edited `acceptance_record.py` (a §1.2 preserve call) and takes the listed files gets `AttributeError` on every `trace.py --strict-integrity`, and so on every commit's registry-integrity step (reproduced above). §2.2's "refresh the scripts/ set coherently" softens this to MINOR. -> Add `scripts/acceptance_record.py` (the new shared `added_ledger_entries`) to the entry's Overwrite bullet. -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3738 -> Rubric anchor K1, for clarity. LLR-361's `detail` states the commit rule twice, once positively ("An entry a commit adds relative to each parent carries `copied` naming only snapshot registry files") and once as a refusal of the same condition. The phrase "relative to each parent" also leaves open whether the entry is judged when it is absent from any one parent or only when it is absent from all of them. The code means the latter. -> Merge the two sentences into one: "An entry whose seq no parent's ledger holds (HEAD's, and MERGE_HEAD's during a merge) is refused when it lacks `copied` or names a file outside the snapshot's registry files." -> @owner

VERDICT: APPROVE findings=3
