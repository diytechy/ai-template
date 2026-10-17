Reviewed: 416f3b993868682ec3d84ef88678da9272c0dcf3

Verified. I worked in the convergence stance, so I read nothing under docs/reviews/ or docs/decisions/, no critique and no lane commit message. The pre-fix code came from `git log -p --format=%h` (bb71acb1d) and from `git show 785b29e11:project-trajectory/scripts/review_brief.py`, where ROLLUP_DIR is read at lines 504 and 507. The worst failure classes this deletion admits are data loss (a review filed into `docs/reviews/rollup/`, which `gen_verdict_rollup.py` prunes at its `_extras`, line 162) and fail-open (a branch the round reader cannot read back as a scope getting filed). I drove the real `review_brief.file_review` at the tip and at the base, in a scratch root. Results at the tip: `wi-900` files `docs/reviews/wi-900/001-REVIEW-A-abcdef0.md`; `rollup` and `Rollup` now file under their own directories, where the base refused both with "names the rollup generator's own directory"; `feature/wi-900` and `wi-900/x` are still refused at both revisions, with no file written. So the one PLAUSIBLE refusal survives, and the only behaviour that changed is the hand-named-branch case. The spec and PROCESS.md section 6 place that case outside every promise, and no kit route mints such a branch (the claim mints `wi-NNN`). The data-loss path is reachable only from that contrived input, and the RESYNC entry states it as residue.

Rubric anchors:
- K1: the amended LLR-313 clause ("file_review writes only an accepted verdict as that round record when the round reader reads its lane path back as that lane's scope") matches `file_review` at project-trajectory/scripts/review_brief.py:489-497. The amended TC-333 Method and Expected match the two tests as they now stand, and its test list still names `test_a_filed_coordinator_review_appears_in_the_rollup`, which still exists.
- K2: no SN or SR changes.
- K3: `file_review` keeps `Implements: SR-235, LLR-313`, LLR-313's module is review_brief.py, `file_review` is in its code_symbol, and both rows stay Approved. The amendments are exactly the deletions the spec's deliverable 4 grants. The last_approved snapshot carries the same word-level change, re-attested by act 123 (seq follows trunk's 122).
- K4: project-trajectory/RESYNC_PACK.md:8528 is anchored `[since 785b29e11]`, a commit that `refactor_again` contains, and it states the residue.

Requirement/interface relationship: the changed side is IF-288 and IF-289 (docstring and the regenerated docs/interface-reference.md) plus LLR-313 and TC-333. I kept both counterparts, each for a stated reason:
- SR-235 promises a record or a refusal and names no directory, so it is unchanged.
- IF-175's sentence on `ROLLUP_DIR` ("the one directory under docs/reviews/ that is no review scope") is still true of its reader: `gen_verdict_rollup._scopes` (gen_verdict_rollup.py:89-91) skips every path under ROLLUP_DIR before offering it to `round_file`.

No decomposition is added. A grep of the scripts, skills, PROCESS.md and the enforcement and machinery references finds no stale citation of the removed refusal; the only remaining mentions are in the 2026-10-08c handoff, the audit plan and the earlier RESYNC entry at line 7580, all of which are history.

Done-when coverage:
- D1, no ROLLUP_DIR or rollup compare in `file_review`: covered by inspection (grep at the tip finds none; the base has both). By the spec's own reasoning, no test is owed.
- D2, the S3 coverage construction: the read-back check stays at review_brief.py:492-497 and is covered by the `feature/wi-900` refusals in both tests; the residue is stated at RESYNC_PACK.md:8541-8546.
- D3, both rollup blocks gone and both tests passing: covered (38 passed).
- D4, LLR-313 and TC-333 amended: covered, act 123.
- D5, IF clauses gone and the reference regenerated: covered (`gen_arch_map --check` exits 0).
- D6, the RESYNC entry: covered.
- D7: `check_trajectory --strict` exits 0. The smoke-tier half was not run here, because the round facts forbid it.

Coverage-extension note, not a finding: a lane named `..` files outside `docs/reviews/` at both the base and the tip. That behaviour predates this range, and git's ref-name rules keep it unreachable from the command line.

Commands:
- `git rev-parse HEAD`: 416f3b993868682ec3d84ef88678da9272c0dcf3
- `python lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/opus/wi-930 tests/test_review_brief.py tests/test_review_brief_git.py`: 38 passed in 10.98s (exit 0)
- `python project-trajectory/scripts/check_trajectory.py --strict`: check_trajectory: clean (933 work item(s), 810 done (87%), 30 cancelled, graph acyclic). (exit 0; advisory WARNs only)
- `python project-trajectory/scripts/trace.py --strict-integrity`: Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ... (exit 0)
- `python project-trajectory/scripts/gen_arch_map.py --src project-trajectory/scripts --contracts-doc docs/interface-reference.md --check`: exit 0
- A `file_review` probe (scratch probe_file.py) at the tip and at the base, results as above.
- `git status --short` after all runs: empty, so the worktree was not changed.

VERDICT: APPROVE findings=0
