Reviewed: fc168c5ef974c4c1780da6c6081506e51fd39448

Verified. This was a full-lane review in the convergence stance. The checkout was confirmed at fc168c5ef. I hunted these failure classes first, worst first.
- Fail-open: a `review` attestation peeled, or admitted by the merge slot.
- Data loss: a wrong peel feeding the refresh's `reset --hard`.
- Silent wrong content: an attestation naming a tree the bar did not see.

All three hold on the shipped paths.
- `refresh_attestation` admits only `bar` in LANDING_BARS (verdict.py:512). `work_tip` and `_peel_target` both go through it. `_merge_ready` names both bars when the tip carries only a `review` attestation.
- `bar_attestation` requires exactly one column-0 label line, the full grammar, a known bar, and its own tree and first parent.
- `_attest_commit` writes the tree before the bar runs. It refuses a bar that moved the index or the worktree, sets the index back, and undoes a commit that does not verify.
- `--message-file` cannot inject a second label line.

Done-when coverage:
- The grammar: tests/test_bar_attestation.py covers wrong tree, wrong parent, missing or unknown bar, missing tests, quoted or indented line, and duplicate label.
- The peel: test_work_tip_never_peels_a_review_attestation and test_governing_rev_never_peels_a_review_attestation. Both use a refresh subject, so they would fail if the bar filter were dropped. Also test_a_verified_refresh_still_peels_under_the_new_grammar and test_merge_ready_refuses_a_tip_carrying_only_a_review_attestation.
- The producer: tests/test_integrate_attest.py covers staged work, an empty commit, a red bar or red named test, a dirty worktree, and a missing key in 5 forms.
- The refresh: test_the_refresh_trailer_names_the_landing_bar, test_the_adjudication_refresh_names_no_bar, and the producer spies. All refresh tests pass.
- The tests digest: the two digest tests.
- The landing tip: `check_trajectory --strict` is clean. The commit bar was not run, per the round facts. LLR-207 is the sitting's call.

Red-before:
- Stage 1 (2b59fc592), run from an archive: all strict-xfail tests in test_bar_attestation, test_integrate_attest, test_hooks_on_routes and test_verdict_record xfailed (126 passed, 41 xfailed).
- Fix round 1: fc168c5's tests with e55302dbe's integrate.py give 10 failures. Every regression test added or changed in that round fails.
- Fix round 2: fc168c5's tests with f19a9f827's integrate.py and provenance.py give 6 failures. Every regression test that round added fails.

Interface and requirement counterparts:
- IF-175: retain. "trailer readers" already covers `bar_attestation`.
- IF-093: retain. The BAR_GREEN label is unchanged.
- SR-156: retain. Its landing-seam text is untouched, and the spec leaves a derived SR for the review record to the sitting.
- IF-173, IF-080, IF-154 and IF-022: carry the change (finding 1).
- LLR-140 and LLR-207: carry the change (finding 2).

Not verified: whether this repo's full landing bar leaves any untracked, non-ignored file in a lane worktree. That would now refuse the refresh. Running it is outside the brief's run set. The repo's .gitignore and the template's coverage arguments cover every output I could identify.

Coverage note (no severity): the review bar and named tests are green on exit 0 alone. A pytest run whose named tests all skip exits 0 and attests green. That matches the spec's S3 ("exit code 0 is green"), so it is an extension of coverage for a later row, not a defect here.

Commands:
- `git rev-parse HEAD` -> fc168c5ef974c4c1780da6c6081506e51fd39448
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../B/wi-956 tests/test_bar_attestation.py tests/test_integrate_attest.py tests/test_integrate_station.py tests/test_integrate.py tests/test_verdict_record.py tests/test_hooks_on_routes.py tests/test_hooks_on_census.py tests/test_kitlib_station.py tests/test_loop_provenance.py` -> 345 passed, 1 skipped in 703.30s (posix-shell gate skip)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (955 work item(s), 842 done (88%), 30 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 ... interface-findings=0
- Stage-1 red-before (archive of 2b59fc592): `pytest -n 4 tests/test_bar_attestation.py tests/test_integrate_attest.py tests/test_hooks_on_routes.py tests/test_verdict_record.py` -> 126 passed, 41 xfailed
- Fix-round-1 pre-fix (fc168c5 tests, e55302dbe integrate.py): `pytest tests/test_integrate_attest.py -k "untracked_files_whatever or main_checkout_holds or unreadable_message or missing_review_bar_key or declarations_staged"` -> 10 failed
- Fix-round-2 pre-fix (fc168c5 tests, f19a9f827 integrate.py and provenance.py): `pytest tests/test_integrate_attest.py tests/test_hooks_on_census.py -k "edits_a_tracked_file or stages_an_edit or joins_a_message or harness_floor or census"` -> 6 failed, 26 passed (the 26 are the census cases, which are not regression tests)

- [MINOR] docs/requirements/interfaces.toml:1138 -> The interface rows were not updated. Spec deliverable 5 says "IF-173's data cell gains `attest`", and plan P4/P5 add `bars` to IF-022 and `attest` to IF-154, IF-080 and IF-173. interfaces.toml is not in the diff: IF-173 still reads "claim, refresh, integrate, ...", IF-080 "claim | refresh | integrate | done-when-hold | audit", IF-154 has no attest argv, and IF-022 lists no `bars` section. Meanwhile integrate.py's own "Contract IF-080/IF-154" docstrings and docs/stack.ini's "(IF-022)" note already name the new surface, so the registry and the code contract disagree -> add `attest` to the IF-173 and IF-080 data cells, `attest --branch --bar --tests --message-file` to IF-154, and `bars` to IF-022, as the plan states (K1) -> @builder
- [MINOR] docs/requirements/low-level-requirements.toml:2190 -> The attest contract is stated in no LLR. These are its refusals before the bar (hooks off, primary-held branch, dirty worktree, an undeclared or empty `[bars] review` with no default), the named tests run through `[product] test` under a per-lane basetemp, and the index restored on every failed write. Amended LLR-207 says only "One producer writes every attestation and undoes a failed write". TC-132 now verifies these behaviours, but it declares `verifies = ["SR-156", "LLR-140"]` and "via the LLR-140 detail contract", and LLR-140's detail says nothing of attest. The new LLR-207 text also reads "the commit own tree" -> at the sitting, carry the attest contract into LLR-207's detail, or the derived SR the spec anticipates. Point TC-132's new clause at the row that states it (or move it into TC-205), and fix the wording to "the commit's own tree" (K1, K3) -> @sitting
- [MINOR] docs/test/test-cases.toml:1307 -> for clarity: TC-132 says attest "refuses before that bar for ... or a hook refusal". A commit a hook refuses is rejected after the bar has run: test_a_hook_refused_attest_commit_leaves_branch_and_index asserts the bar ran. Only "commit hooks not on" (`hooks_refusal`) refuses before the bar -> reword to "refuses before that bar when the commit hooks are off, ...; a commit a hook refuses or rewrites after a green bar leaves the branch and index unchanged" (K1) -> @builder
- [MINOR] project-trajectory/scripts/kitlib/provenance.py:349 -> The new `append_trailer` carries `Implements: SR-209, LLR-247`, but LLR-247's code_symbol (`LOOP_TRAILER/LOOP_SESSION_ENV/format_loop_trailer/parse_loop_trailer/loop_trailer_refusal`) does not list it. Its only new caller is the Bar-Green producer under LLR-207 -> add `append_trailer` to LLR-247's code_symbol, or tag it to the LLR whose symbol list will carry it (K3) -> @builder
- [MINOR] project-trajectory/scripts/integrate.py:3005 -> `_run_review_bar` restates run_menu.launch's "python first on PATH" rule, citing it, as `os.path.dirname(harness_python)`. It drops run_menu's POSIX half (`_interpreter_dir` writes `python`/`python3` shims, because the interpreter's directory "may hold another `python` ... or none"). Failure scenario: POSIX, no declared toolchain, harness = sys.executable = /usr/bin/python3, and /usr/bin has no `python` (stock Debian, Ubuntu or macOS). The review bar's `python ...` is then not found or is another interpreter, so attest refuses a green tree. This is a duplicate in intent (PROCESS.md §3 "Consolidate, don't duplicate") -> lift run_menu's interpreter-directory helper to one shared home (e.g. kitlib) and call it from both launch and `_run_review_bar` -> @builder
- [MINOR] project-trajectory/RESYNC_PACK.md:9276 -> for clarity: the entry says the producer now refuses "a bar that rewrites or stages files (a formatter run in fix mode)". `_bar_refusal` also refuses, on the refresh too, a bar that only leaves a new untracked, non-ignored file (it lists `??` entries through `_unstaged_dirt`), for example a junit or coverage report the adopter does not ignore. Before this change that refresh committed. An adopter reading the entry will not expect the new refusal -> name that case and its remedy (ignore the report path) in the entry's "What changed" -> @builder

VERDICT: CHANGES-REQUESTED findings=6
