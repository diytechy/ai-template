# ADJUDICATE — WI-648 — amendment at c429dd0c

Independent adjudication of the six approved rows whose attesting cells WI-612
amended. The one question: MEANING or CLARITY. Brief: the kit's amendment brief
rendered for this row, with the caller's two changes (no commit by the
adjudicator; aftermath stated here for the integrator).

- [MEANING] LLR-140 detail -> the claim ladder carries a dirty-tree rung: any uncommitted change anywhere refuses the claim, and the trunk commit's staging mechanism is unstated -> no dirty-tree rung; the trunk commit goes through bookkeeping.commit, which refuses BY NAME only a dirty path the claim must write, before anything is written, and commits only the paths the claim wrote -> the refusal condition narrowed (a claim beside unrelated dirt used to refuse and now proceeds), and a new actor and a new obligation (path-named refusal, commit only what was written) were added. An implementation correct against the old text (refuse on any dirt) fails the new one.
- [MEANING] LLR-143 detail -> the drive loop refuses on any dirty trunk at the cycle top -> it refuses on a dirty trunk except a change confined to agent_common.OWNER_ONLY_PATHS, which is not dirt -> a case was removed from the refusal: an implementation that stops on a dirty owner scratchpad was correct before and fails now.
- [MEANING] LLR-151 detail -> the ladder runs before the dispatch lock "so the clean-trunk rung never refuses over the lock's own file", which presupposes a clean-trunk rung in the ladder -> the ladder carries NO clean-trunk rung; the claim commits through bookkeeping.commit, which refuses by name a dirty path the claim must write and never stages the lock's own file -> a rung the old text required is now forbidden, and a new obligation (the claim commit never stages the lock file) was added. The traced cells `module` (+bookkeeping.py) and `code_symbol` (+`;commit`) moved too; they are non-attesting.
- [MEANING] TC-132 method -> each claim refusal fires by name (at anchor time the set included "dirty tree", which the suite checked with an unrelated untracked file) -> each claim refusal fires by name, including a dirty path the claim must write, refused before anything moves -> the acceptance case changed: the old dirty-tree check now fails against the new behaviour, and the new case (an in-scope path named, nothing moved) is one the old method never demanded.
- [MEANING] TC-144 method -> pause/dirty-trunk/stall/crash-resume keep their serial-loop contracts at lanes=1 -> the same, plus the dirty-trunk stop reads past a change confined to the owner's scratchpad (OWNER_ONLY_PATHS) -> a case was added to what the test must show. A suite correct against the old method could lack it, or assert the opposite.
- [MEANING] TC-145 method -> the spine-claim, dispatch-lock and spine-batch checks, then "every pre-existing single-WI claim contract holds unchanged" (that included the claim refusing any dirty tree) -> the claim commits through the shared bookkeeping helper (IF-186) and refuses by name a dirty path it must write (the moved spec among them) where it once refused any dirty tree, and every OTHER pre-existing contract holds -> a case was added and one pre-existing contract was explicitly withdrawn. The traced cell `verifies` moved too (+IF-186); it is non-attesting.

## How scope was verified against the anchor

- I loaded both sides with `tomllib`. Live: `docs/requirements/low-level-requirements.toml` and `docs/test/test-cases.toml`. Anchor: the same paths under `docs/archive/last_approved/`, last copied at cbb6649f. I compared every key of every row, not just the six. Both files hold the same row sets (239 LLR, 234 TC).
- For the six rows, the brief's before/after cells match the anchor and live text byte for byte. A word-level diff shows only the edits quoted above. No other attesting cell moved on any of the six. `title`, `rationale`, `expected`, `level` and `tier` are identical, and `status` is still `Approved` on all six.
- Other cells that moved, all traced (non-attesting by ruling):
  - LLR-151: `module` and `code_symbol`.
  - TC-145: `verifies` (+IF-186).
  - Outside the six: TC-213 `verifies` (+IF-180, from WI-627) and TC-249 `verifies` (+IF-187, IF-188, IF-189, from WI-639).

  A re-anchor copies whole files, so it will copy all of these. Every IF row they name exists in `docs/requirements/interfaces.toml`.
- `baseline_snapshot.refresh_ledger` (a read-only call) agrees:
  - LLR file: absorbed LLR-140, LLR-143 and LLR-151 (`Detail`), with no flips.
  - TC file: absorbed TC-132, TC-144 and TC-145 (`Method`), with no flips.
  - `components.toml`: CMP-006 `Notes` also drifted. That row belongs to another act, and this re-anchor's scope does not include that file.

  `refresh_refusal(reattests=<the six>)` returns no refusal. The scope is exactly the LLR and TC files.
- HEAD moved during this sitting, from c429dd0c to e123eb6d (WI-635, which commits the `--reattests` flag), and another session has WI-628 staged. Neither the judged rows, the anchor, nor `bookkeeping.py`, `integrate.py`, `dispatch.py`, `agent_common.py`, `spec_move.py`, `trunk_step.py` or the three test files differ between c429dd0c and HEAD, or in the index.

## Aftermath

All six are MEANING. The tiers are released (`human_approval_through = "DevStg-Needs"`), so the adjudicator owes the re-attestation. I would bless all six. Re-anchor exactly:

    --reattests LLR-140,LLR-143,LLR-151,TC-132,TC-144,TC-145

(`python project-trajectory/scripts/intake.py snapshot --reattests LLR-140,LLR-143,LLR-151,TC-132,TC-144,TC-145`, in its own commit, with `Status` left at `Approved`.)

Why each new text is true of the current tree, and where it is exercised:

- **LLR-140 (SR-156).**
  - `_claim_refusal` has no dirty-tree rung.
  - `_claim_locked` calls `bookkeeping.commit` with the scope `spec_move.planned_writes` plus `trunk_step.regen_writes()`.
  - The pre-check refuses with the path list and "nothing was written" before `write()` runs.
  - The commit is built in a temporary index from the in-scope changes only.
  - Exercised by TC-132's evidence: `test_integrate.py::test_claim_refuses_a_dirty_path_it_must_write` checks that the path is named, the spec is unchanged, no `active/` directory exists and no branch was cut.
  - The claim changes nothing SR-156 promises: branch before trunk (`before_advance`) and a compare-and-swap advance.
- **LLR-143 (SR-026 chain).**
  - `dispatch.run`'s tick-top check calls `ac.substantive_working_tree_dirty`, which drops lines whose path is in `OWNER_ONLY_PATHS = ("OWNER_SCRATCHPAD.md",)`.
  - Exercised by TC-137's evidence, `tests/test_dispatch.py`:
    - `test_a_dirty_owner_scratchpad_does_not_stop_the_drive` shows the scratchpad is read past.
    - `test_drive_refuses_a_dirty_trunk_before_resuming` shows real dirt still stops the run.
  - TC-137's unchanged method ("a dirty trunk ... stop[s] the run by name") stays true.
  - It narrows an existing refusal inside the row's own chain. It adds no capability beyond SR-026.
- **LLR-151 (SR-156).**
  - The ladder runs before `_dispatch_lock` and carries no clean-trunk rung.
  - The lock file (`out/agent-loop.lock`) is in no bookkeeping scope: `regen_writes` has no `out/` path, and `planned_writes` names only spec and markdown paths.
  - Exercised by TC-145's evidence, `tests/test_integrate.py`. The `claim_repo` fixture does not ignore `out/`, and `test_claim_moves_the_spec_commits_the_trunk_and_cuts_the_branch` asserts an empty `git status` after a hand claim. If the lock rode the commit, the release's unlink would leave a tracked deletion.
- **TC-132, TC-144 and TC-145 (SR-156).**
  - Each new clause matches a passing test in the row's own Evidence file (named above).
  - TC-144's scratchpad test runs at lanes=1: the fixture has no `stack.ini`, so `_lane_count` gives 1. That fits SR-156's "a single-lane setting preserves the serial semantic".
  - The "shared" helper is real: `intake._mint` calls the same `bookkeeping.commit`, and the merge slot (`integrate.integrate`) reads past `OWNER_ONLY_PATHS` the same way.

Bar I produced (not claimed): on this tree, `python -m pytest -q -n auto -p no:cacheprovider tests/test_integrate.py tests/test_bookkeeping.py tests/test_integrate_admission.py tests/test_integrate_station.py` gave **141 passed in 455.61s**. `tests/test_dispatch.py` gave **36 passed in 335.09s**.

## Dispositions

None owed. Every row is blessed, and no row is returned.

## LLR-140's "non-ordinary safety_class" clause

It is **not part of the amended text**. The clause is byte-identical in the anchor and the live cell. The amendment deleted "dirty tree," from the same list and appended the bookkeeping clause; it did not touch this item.

The clause is **false of the code**. `_claim_refusal` has no safety-class arm: WI-381 deleted it, and LLR-151 says so. The same list also omits two rungs the code does run, the WI-370 specref rung and the WI-358 status-prose rung. The IF-080 contract text in `integrate.py` still lists "a non-ordinary spec" as well, in the very sentence WI-612 edited.

It **does not change my blessing**:
- The re-anchor copies that clause byte for byte onto an anchor that already carries it, so the record neither gains nor loses a blessing of it.
- Withholding LLR-140 would leave the clause in both copies, and it would refuse the whole LLR-file copy, which would take LLR-143 and LLR-151 with it.

The fix belongs in its own authoring amendment: delete the rung and reconcile the list with the code. That amendment would itself be MEANING, because it removes a case. Per instruction, I have not acted on it.

## Non-blocking findings (surfaced, not acted on)

1. **Evidence gap (traced cells).** `tests/test_bookkeeping.py` is the only direct proof of three things:
   - LLR-140's "commits only the paths the claim wrote";
   - the positive case that a claim beside unrelated dirt now succeeds;
   - the merge slot reading past the scratchpad.

   No TC's `Evidence` cites it. Adding it to TC-132 and TC-145 Evidence is a traced-cell edit and arms no re-attest.
2. **Cross-chain test (existing pattern).** TC-144 verifies LLR-150 (`lane.py`), yet its new clause checks behaviour LLR-143 owns (`dispatch.run`, SR-026). The amendment extends a clause that already had this shape.
3. **LLR-154, unamended.** It still says the mint commits "docs/work/ + the declared generated set". The mint's scope is now `docs/work/` + the watermark (+ open-items and archive moves) + `trunk_step`'s regen table, and `bookkeeping.py` says that table is deliberately NOT the declared `[generated]` set. It deserves a look by the authoring lane.
4. **`integrate.claim` docstring, point 1.** It says the next bookkeeping commit overlaps a crashed claim's residue because "the regenerated artifacts always do". That holds only if the crash came after the regeneration wrote. After WI-612, residue from a crash mid-move that misses the next hand claim's scope no longer stops that hand claim. The dispatcher's tick-top check still does.

VERDICT: MEANING rows=6
