Reviewed: 24fabf54b06427f2e3b06c7e3446582ec0162316

**Verified.** The worktree HEAD is 24fabf54b06427f2e3b06c7e3446582ec0162316. I read the full-lane diff 4c216fd2f...24fabf54b, minus the excluded paths, against the WI-923 row, its specref `docs/specs/WI-923.md`, IF-273's registry row, LLR-270, LLR-300, TC-267, TC-317, TC-329 and the rubric's anchors.

The failure classes I hunted first, worst first:
- **Fail-open (two holders at once).** An access-denied create only ever returns "held". The caller never gets a lock its create did not make, so mutual exclusion cannot be weakened.
- **Swallowing a real fault.** Any refusal other than `PermissionError` still propagates after one attempt. Only `FileExistsError` reaches the stale-takeover branch.
- **Silent wrong message.** `held` is `""` for an existing lock, so StoreBusy shows the access-refusal suffix only when the last attempt was refused that way. The "[Errno N] strerror" text is always non-empty.

Callers: none of the 12 `coordinator_guard.dir_lock` sites, nor `keep_for`, `_apply_now` or `take_warm_lease`, wrap the lock in `except OSError`/`PermissionError`. Nothing in the code relied on the old escape, which matches the "no caller changes" claim in the spec.

Driving the real code:
- **Red before the fix.** I ran the lane's test file against trunk 4c216fd2f's scripts, extracted with `git archive` into my scratch dir. The three tests the spec says must fail on trunk do fail: refused once, refused past the wait, and the observed keep_for path. The ENOSPC pin passes, and TC-317's and TC-329's existing tests pass unchanged.
- **Windows stress run.** I wrote my own scratch harness: 6 threads take and release the real `dir_lock` (wait 10 s) for 10 s, with an overlap counter. On the lane's code: 10967 holds, 0 overlaps, no exception. On trunk's code: 11503 holds, 0 overlaps, 133 `PermissionError`s escaped. That reproduces the defect and confirms the fix.

Done-when coverage:
- Refused once, retried and taken: `test_a_lock_create_refused_once_as_access_denied_is_retried_and_taken`.
- Refused through the wait, busy and named: `test_a_lock_create_refused_as_access_denied_past_the_wait_is_busy_and_named`.
- Other refusal raised at once: `test_any_other_lock_create_refusal_is_raised_at_once`.
- Observed path: `test_a_first_call_whose_lock_create_is_refused_as_access_denied_runs_unretained`. Its `attempts == [True, False]` plus the holder named on stderr show the lock was retried and taken, and that the call ran unretained because of the lease, not because of StoreBusy.
- No new test uses a thread or timing, and each injects only at the `.lock` O_EXCL create.
- TC-317 and TC-329 tests unchanged and passing.
- IF-273 contract text and the `dir_lock` docstring state the four outcomes and the deadline rule.
- TC-267: method, expected, verifies (+IF-273) and evidence (three tests) as specified.
- TC-329: method and evidence as specified.
- SR-227 unchanged.
- RESYNC_PACK entry present, anchored [since 4c216fd2f], "no migration forced" (K4).
- `trace.py --strict-integrity`: only LLR-292's finding remains.
- `check_trajectory --strict`: clean.

Open at this tip: the checkpoint sitting, and the final stress readings in the lane log (see the finding).

Rubric:
- K1 holds. The LLR-270 clause and the TC-267/TC-329 text match what the code does: retried within the wait, busy and named past it, any other refusal raised after one attempt.
- K2: no SR is touched.
- K3: only the rows the spec grants are amended, and no Status flips.

Counterparts, judged:
- The IF-273 registry row (`data = "... raises StoreBusy"`) can stay as it is. The signature and the single failure class are unchanged, so the code-side contract change does not reach it.
- LLR-300 (the coordinator lease) states no lock-create mechanics, so it can stay too. It inherits the primitive.
- TC-317 can stay, because its exclusion behaviour is unchanged. The new readings are pinned at TC-267, which now verifies IF-273.

**Commands.**
- `git rev-parse HEAD` -> 24fabf54b06427f2e3b06c7e3446582ec0162316
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1/C/wi-923 tests/test_session_keep.py tests/test_coordinator_adjudicate.py tests/test_coordinator_guard.py tests/test_adjudicator_token.py tests/test_verdict_record.py tests/test_dispute.py tests/test_resync_pack.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py` (lowprio) -> `488 passed in 310.14s (0:05:10)`
- `python project-trajectory/scripts/check_trajectory.py --strict` (lowprio) -> `check_trajectory: clean (920 work item(s), 800 done (87%), 30 cancelled, graph acyclic).` (4 pre-existing WARN lines about other WIs)
- `python project-trajectory/scripts/trace.py --strict-integrity` (lowprio) -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 ...` (the one form finding is LLR-292's, the allowed pre-existing one)
- Red-before, run in a scratch `git archive` of 4c216fd2f with the lane's `tests/test_session_keep.py`: `pytest -q tests/test_session_keep.py -k "access_denied or other_lock_create or excludes_a_second_holder or two_concurrent_first"` -> `3 failed, 3 passed, 161 deselected in 1.92s` (the three failures are the access-denied tests, each `PermissionError: [Errno 13]` escaping)
- My own Windows stress harness, `.../r1/C/stress/stress.py` (6 threads, real `dir_lock`, 10 s). Lane -> `holds 10967 overlap 0 errors {}`. Trunk -> `holds 11503 overlap 0 errors {'PermissionError': 133}`

**Findings.**

- [MINOR] docs/requirements/low-level-requirements.toml:3037 -> The amended Approved rows (the new LLR-270 STORE clause, and TC-267 and TC-329 at docs/test/test-cases.toml:3017 and :3029) have not yet been sat at the lane's checkpoint. The tip commit labels them "unjudged until the checkpoint". docs/decisions/wi-923.toml:9 records the Windows stress readings as preliminary and to be re-run by the coordinator. So two Done-when items are still open at this tip: rows sat at the checkpoint, and the stress run recorded in the lane log. My own stress run above reproduces the expected trunk/lane contrast, but it does not replace the lane-log record (K3) -> before landing, hold the combined sitting over these three amendments, including whether LLR-270's clause is design the row did not already carry, and record the final stress readings -> @coordinator

VERDICT: APPROVE findings=1
