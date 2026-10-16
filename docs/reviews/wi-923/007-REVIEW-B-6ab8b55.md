Reviewed: 6ab8b55c9efe66188cea75c0c99928551fb3302b

Verified (full-lane review, convergence stance; range b5b9273e1..6ab8b55c9, reading scope as the brief sets it). Failure classes hunted first, in severity order: (1) fail-open, meaning two holders of the lock at once; (2) a lost record or lost lease, if an access refusal were read as "ours"; (3) a crash that still escapes, so the bug remains. `_try_lock` (project-trajectory/scripts/session_keep.py:328-346) returns None (meaning "ours") only after a successful `O_CREAT|O_EXCL` create. `FileExistsError` returns "" and keeps the stale rule. `PermissionError` returns its text and touches no file. Any other `OSError` propagates. So no new reading can grant the lock, and the stale takeover is unchanged. `dir_lock` (session_keep.py:300-325) retries every non-None reading until the deadline. It then raises `StoreBusy(path)`, adding the access-refusal text only when the last attempt met one, which matches Q1(a) and the Done-when. The release path is unchanged. No other script calls `_try_lock`. The twelve `coordinator_guard.py` `dir_lock` sites sit under `_hook_main`'s catch-all (coordinator_guard.py:1617) or the CLI, as before; StoreBusy is not an OSError, but no site wraps `dir_lock` in `except OSError`, so none loses handling. I drove the real code through a scratch Windows stress harness: six threads took and released the real `dir_lock` for 10 s. On the lane code that gave 15,513 holds, 0 overlaps, 0 StoreBusy and nothing escaping. On trunk's `session_keep.py` it gave 16,354 holds, 0 overlaps and 172 `PermissionError` escapes. This reproduces the defect and confirms the fix. I ran the red-before check by extracting the reviewed tree into scratch and putting back b5b9273e1's `session_keep.py`. The three tests the spec says fail on trunk did fail (access-denied-once, access-denied-past-the-wait, the observed path), each with an escaping `PermissionError`. The ENOSPC pin passed, as did TC-317's `test_the_store_lock_excludes_a_second_holder` and TC-329's `test_two_concurrent_first_calls_mint_one_session_and_run_one_unretained`. Both of those are unchanged in the diff. All six collect under `-m smoke`.

Done-when coverage:
- Access denied once, then taken: `tests/test_session_keep.py::test_a_lock_create_refused_once_as_access_denied_is_retried_and_taken`.
- Access denied to the deadline gives StoreBusy, naming the path and the refusal: `::test_a_lock_create_refused_as_access_denied_past_the_wait_is_busy_and_named`.
- Another refusal is raised as itself after one attempt: `::test_any_other_lock_create_refusal_is_raised_at_once`.
- The observed path (runs unretained, naming why, and the store holds only the first lease): `::test_a_first_call_whose_lock_create_is_refused_as_access_denied_runs_unretained`.
- TC-329 and TC-317 pass unchanged (run at `-n 2` per the round facts, not the smoke tier at `-n auto`).
- The Windows stress run: my own run above reproduced it. The lane log itself is outside this review's reading scope, so whether it records the run is not assessed.
- Trace rows:
  - IF-273's contract body in the module docstring (session_keep.py:38-46) and `dir_lock`'s docstring state the four outcomes and the deadline rule.
  - TC-267 gained the three primitive cases in method and expected, `IF-273` in `verifies`, and the three tests in evidence.
  - TC-329 gained the observed-path case and its test.
  - LLR-270's STORE paragraph gained one behaviour-voice clause that names no code beyond the existing store_lock vocabulary, and the clause is true against the code (K1).
  - SR-227 is unchanged.
  - Act 121 re-attests LLR-270, TC-267 and TC-329. The `last_approved` snapshot diff is byte-identical to the live registry diff, and the README carries the citation line. No Status flips (K3).
- RESYNC entry: present for `scripts/session_keep.py`, anchored `[since b5b9273e1]`, which is trunk's tip (K4). It states that no migration is forced.
- The bar: `check_trajectory.py --strict` is clean, and `trace.py --strict` exits 0 with integrity=0.

Requirement/interface counterpart decision: the changed side is IF-273's contract (the lock now reads an access-denied create as held). Its counterpart is the IF-273 registry row (docs/requirements/interfaces.toml:2435, data "dir_lock(directory, wait=10.0) -> context manager yielding Path; raises StoreBusy"). Retained: the row's signature and its one named failure still hold, and the change narrows when a raw `PermissionError` escapes rather than adding a channel. The requestor `scripts/coordinator_guard` needs no change, for the reason given above.

Registry sweep: I checked LLR-270's new clause against LLR-300, SR-227 and the registries' other exclusive-create and StoreBusy statements. I found no contradiction, overlap or limit conflict. K2 does not bite, because no SN or SR cell changed.

Coverage-extension note (not a finding): `PermissionError` also covers POSIX `EPERM`, which is read as held in the same way. That fails closed, ending in StoreBusy after the wait, labelled as an access refusal.

Commands:
- `git rev-parse HEAD` -> 6ab8b55c9efe66188cea75c0c99928551fb3302b
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/k/wi-923/gate/C/wi-923 tests/test_session_keep.py tests/test_coordinator_adjudicate.py tests/test_coordinator_guard.py tests/test_adjudicator_token.py tests/test_verdict_record.py tests/test_dispute.py tests/test_resync_pack.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py` -> 494 passed in 424.77s (0:07:04)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (930 work item(s), 806 done (87%), 30 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.
- `python project-trajectory/scripts/trace.py --strict` -> exit 0, same summary line.
- Red-before, in a scratch extraction of 6ab8b55c9 with b5b9273e1's session_keep.py: `pytest tests/test_session_keep.py -k "access_denied or other_lock_create or excludes_a_second_holder or two_concurrent_first"` -> 3 failed, 3 passed (the three spec'd-red tests failed with PermissionError).
- Stress harness, scratch `stress/stress.py`, 6 threads for 10 s on the real dir_lock: lane -> holds 15513 overlap 0 busy 0 escaped {}; trunk -> holds 16354 overlap 0 busy 0 escaped {'PermissionError': 172}
- `git status --short` in the worktree afterwards -> clean

VERDICT: APPROVE findings=0
