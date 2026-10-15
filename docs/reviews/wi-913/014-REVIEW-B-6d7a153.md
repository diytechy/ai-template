Reviewed: 6d7a153d23f463f0bb7546af142dacb28722da19

Verified: Full-lane review of 2025f841..6d7a153d (convergence stance), with the checkout confirmed at 6d7a153d23f463f0bb7546af142dacb28722da19. I hunted fail-open first, because the pass record is the one thing that releases the build. I read plan_gate.py, kitlib/plan_pass.py, the review_brief.py plan/critique/plan-file/pass code, and the check.py, integrate.py, kitlib/git.py and plan_coverage.py edits against the spec, its Trust section and S3. Then I drove the shipped code on fixture lanes (reviewer probes, scratch only).

- A side branch: a build committed on a branch with no claim folder and merged into the lane passes the lane hook, because the merge's own changes are empty. The merge slot's walk (`landing_refusal`) and the trunk `git merge --squash` hook path both refuse it, naming the side commit. The landing is the backstop the spec relies on.
- A plan edit staged together with a build is held ("binds another plan").
- Deleting the pass record lets only that one commit through, on its parent's record. The next build is held.
- A lane commit message with a non-UTF-8 byte still yields a readable SQUASH_MSG, because git re-encodes it, so `squash_commits` lists the commit and the squash is held.

Each Done-when item maps to a covering test:
- D1, the gate arms: tests/test_plan_gate.py.
- D2, the strict renders: test_plan_pass.py brief tests and test_the_plan_critique_refuses_a_missing_input_and_writes_nothing.
- D3, the filing refusals, the MINOR-only pass and the two-commit order: test_plan_filing.py, plus test_a_pass_record_committed_with_its_critique_is_refused_and_the_two_commit_order_passes and the reviewed-another-plan/Done-when tests.
- D4, the catalogue, the item-12 wording verbatim and no skill named: test_plan_pass.py.
- D5: the skill copies are byte-identical in .claude/ and .agents/ (cmp), and so are WI-000.template.md and its copy (cmp; test_dogfood_sync passed).
- D6: SR-154, LLR-313, TC-333, LLR-337, TC-367 and IF-288/289 (+IF-295) are present, with acts 113–115 recorded.
- D7: the RESYNC entry states that no migration is forced and that an out-of-set planmode is held.
- D8: check_trajectory --strict is clean. I did not run the smoke tier (the brief says not to). I did not run trace.py, because it rewrites docs/test/report.md in the worktree, which this round forbids.

Red-before: I ran each round-fix regression test against its pre-fix sources, extracted into scratch, and every defect test failed.
- Round 1 (3d98c674b's plan_gate.py, plan_pass.py and review_brief.py): non-string planmode ×9 failed ("assert '' is None" and an unpack of 0 holds); critique-3 failed ("assert 3 is None"); squash-without-branch failed; second-critique-misses-a-finding failed ("assert 0 == 2"). The two cap tests failed only on the then-absent write_dispute_findings.
- Round 2 (df7fbc8a3's sources and hook): the CRLF pass form failed ("HEAD does not hold the critique"); the hook floor failed (no "FAIL  plan-gate"); the partial-close refresh merge failed (log.d fragment held). The Done-when-digest test passes pre-fix, as expected: it was a coverage-gap finding, not a defect.

Rubric anchors:
- K2 holds: no SR names a script.
- K3 holds: every new Implements tag is in its LLR's code_symbol (LLR-313, LLR-337, LLR-069 _tree_text/_tree_tomls, LLR-302 squash_commits). The traced-only module/code_symbol edits to approved LLR-069 and LLR-302 are carried in the snapshot.
- K1: one finding, below.
- K4: one finding, below.

Commands:
- `git rev-parse HEAD` -> 6d7a153d23f463f0bb7546af142dacb28722da19
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/C/wi-913 tests/test_dogfood_sync.py tests/test_integrate.py tests/test_plan_coverage.py tests/test_plan_coverage_step.py tests/test_plan_filing.py tests/test_plan_gate.py tests/test_plan_pass.py tests/test_pre_commit_hook.py tests/test_prompts.py tests/test_review_brief.py tests/test_review_brief_git.py tests/test_text_then_act.py` -> 346 passed, 13 skipped in 270.58s (12 env-gated: posix-shell)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (915 work item(s), 798 done (87%), 30 cancelled, graph acyclic). exit=0
- round-1 fix tests against the pre-fix sources (scratch extraction) -> 14 failed, 1 passed (the passing one is the squash case's not-held parameter)
- round-2 fix tests against the pre-fix sources (scratch extraction) -> 3 failed, 1 passed (the Done-when-digest coverage test)
- reviewer probes on HEAD code (scratch) -> side-branch build: hook [] but landing and squash refuse it; plan edit with a build: held; record deletion: the next build is held; non-UTF-8 message: the squash is held

- [MINOR] docs/requirements/system-requirements.toml:711 -> for clarity (K1): SR-154's rewritten requirement puts the single-plan refusal inside the sentence opened by "The delivered loop content shall, when unattended work reaches integration, ...". It therefore reads as if build output is refused only at unattended integration. The acceptance criterion and the gate itself refuse it at every lane commit, attended included, and at landing. -> give the single-plan obligation its own condition clause (or its own sentence), e.g. "...; and, wherever a claimed work item is marked for an in-lane single plan, the delivered content shall refuse its build output at making or landing until ...", so the unattended-integration condition no longer scopes it -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:8302 -> K4: the entry is anchored `[since aac06695e]`, a trunk commit four commits before this lane's base 2025f841. An adopter whose recorded kit commit falls between them would read the entry as already applied. -> re-anchor at the landing's parent when landing (recipes §3 "RESYNC"), or at 2025f841 now -> @owner

VERDICT: APPROVE findings=2
