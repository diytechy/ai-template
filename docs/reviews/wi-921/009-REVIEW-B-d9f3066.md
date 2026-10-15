Reviewed: d9f30665981928faea9839aeb2ee1efaaf6e48f0

Verified. The checkout is at d9f30665981928faea9839aeb2ee1efaaf6e48f0. Before hunting I named the failure classes this change admits, worst first: (1) fail-open, where an unblessed Done-when change reaches trunk at commit unjudged; (2) silent wrong content, where a classifier or path read names the wrong copy and an absent claim releases; (3) fail-closed breakage of ordinary commits, such as the claim commit, a lane's own edit, or a context-only trunk amendment.

I drove the real shipped hook end to end. I bootstrapped a scaffold from the lane's bootstrap.py, set core.hooksPath to .githooks and ran real `git commit`s, reading the `done-when-blessed` result line each time. Results:
- the trunk claim commit (lone `A`): PASS;
- a trunk amendment of the claim copy's context only: PASS;
- a trunk amendment of its Done-when: FAIL, with `integrate: REFUSED - WI-007: its Done-when differs ... (digest sha256:69dae9ed50843841)`;
- the same amendment made through `git commit -a`, `git commit -- <path>` and `git commit --include <path>` (a temporary index via GIT_INDEX_FILE): FAIL each time;
- a lane-branch edit of its Done-when in a linked worktree: PASS;
- a lane close with no blessing: FAIL;
- a detached-HEAD close in the lane worktree: PASS, which is the stated WI-922 residue.

Code read:
- `classify_delta`, `staged_changes`, `_staged_base` and `staged_hold` (project-trajectory/scripts/kitlib/done_when.py:515-625) match deliverable 5 and LLR-307. An unreadable delta and an unreadable branch each hold, naming why.
- `claim_copy` turns a `None` lane base into a named hold (done_when.py:236), so `lane_base()` returning None does not fail open.
- `_copy_at` now lists paths losslessly (done_when.py:259). With only that one line reverted on post-fix code, `test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other` fails (`AssertionError: None`), so that test isolates the fix.
- `check.steps(80, "full", "all")` yields 38 names, equal to `BUILTIN_STEP_NAMES`. No tier, stage or phase variant adds a name, so the census's input set is closed as the spec says.
- `tests/test_commit_floor_census.py` is not in `SLOW_MODULES`, so it runs in the smoke tier.
- Implements tags match the module and code_symbol of LLR-307 and LLR-309 (K3).
- RESYNC_PACK.md carries the entry with a well-formed `[since e474f51dd]` anchor (K4). Trunk has since moved to 4c216fd2f, so at landing the anchor must be re-pointed to the landing's parent, as the Done-when says.

Red before the fix. I exported the reviewed tree and overlaid e474f51's hooks/pre-commit, check.py, integrate.py and kitlib/done_when.py. Against that pre-fix code every new WI-921 test fails:
- the census fails, naming `done-when-blessed: a built-in step in no class`;
- `classify_delta` is missing (AttributeError);
- the two-commit landing, both parametrisations, fails;
- the trunk amendment, the unlistable index delta, the unreadable branch identity and the quoted path each fail;
- the shipped-floor test fails (`'PASS  done-when-blessed' in ...`);
- the scaffold-floor test fails (`assert 'done-when-blessed' in [...]`).
The three census fault cases pass on both versions, which is correct: they test the census function itself.

Done-when coverage map:
- (1) floor and comment: project-trajectory/hooks/pre-commit:276-297 and :318, covered by test_the_shipped_hooks_floor_holds_an_unblessed_hand_close and the census.
- (2) hook-driven test with the scaffold case: test_the_shipped_hooks_floor_holds_an_unblessed_hand_close and test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree; red before, green after.
- (3) census: test_every_built_in_step_is_classified_exactly_once plus the three fault tests; smoke tier; red before, naming done-when-blessed.
- (4) WI-835 replay and trunk amendment: test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed[verdict|ruling] and test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not; red before.
- (5) unlistable index delta: test_an_index_delta_git_cannot_list_holds_naming_why; red before.
- (6) RESYNC entry: present; re-anchor at landing.
- (7) trace rows: TC-325 and TC-019 amended, LLR-307 and LLR-309 amended, LLR-019 untouched.
- (8) the bar: check_trajectory --strict is clean. I did not run the smoke tier, per the round facts. I did not run trace.py --strict in the lane because it writes docs/test/report.md there, and a run in my history-less export cannot read the approval-record class.

None of the findings below is a Done-when gap, a fail-open outside the owner-ruled residue class, or data loss. All are MINOR.

Commands:
- `git rev-parse HEAD` -> d9f30665981928faea9839aeb2ee1efaaf6e48f0
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r3/C/wi-921 <the 18 listed modules>` -> `406 passed, 14 skipped in 650.36s (0:10:50)`. The 12 environment-gated skips are the posix-shell gate (sh.exe not on PATH).
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (919 work item(s), 800 done (87%), 30 cancelled, graph acyclic).` exit 0
- The new WI-921 tests against pre-fix code (export at .../r3/C/prefix) -> `10 failed, 3 passed in 16.79s`. The 3 passes are the census fault cases.
- test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other with only `_copy_at`'s lossless listing reverted -> `1 failed in 1.98s`
- E2E probes .../r3/C/probe/e2e.py and e2e2.py (real `git commit` through the scaffold hook) -> the results quoted above.
- A `git merge --no-ff` of a branch carrying an unblessed Done-when edit onto the probe's trunk -> `merge exit=0`, with no done-when-blessed line printed (see finding 1).

- [MINOR] project-trajectory/hooks/pre-commit:291 -> The stated fail-open residue list leaves one route out. It names amend, cherry-pick, revert, rebase and hand fast-forward, but not a merge commit made by a non-conflicting `git merge` onto trunk. Git runs no pre-commit hook for that merge, and the kit ships no pre-merge-commit hook. In the probe, `git merge --no-ff` of a branch carrying an unblessed Done-when edit committed onto trunk with exit 0 and no done-when-blessed line. The same omission is at project-trajectory/RESYNC_PACK.md:8366 and docs/work/active/wi-921/WI-921-hook-floor-done-when-census.md:257. This is the owner-ruled class (D-014: a commit not judged against its real parent, caught by the merge-time mint, with a successor row at the branch-ref update), so it is graded MINOR, not a new fail-open. -> Name "a merge commit made without conflicts (git runs no pre-commit hook for it)" in all three residue lists, or hand it to the successor row with the others. This is wording only and adds no guard. If the owner prefers closing it, a shipped pre-merge-commit hook that delegates to pre-commit is the single owning boundary, which is the successor row's scope. (K1) -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3286 -> For clarity. The amended LLR-309 says "The exemption for the commit that changes Done-when text applies only to the claim's own lane". LLR-307 (low-level-requirements.toml:3262) says "elsewhere, only a close is judged against the current commit", and the code agrees: `_staged_base` (project-trajectory/scripts/kitlib/done_when.py:586) returns `()` for a non-close change off trunk and off the claim's branch. A Done-when edit on a detached HEAD or an alias branch is therefore also exempt, so the two rows contradict each other. -> Reword LLR-309 to "applies to the claim's own lane, and off trunk elsewhere (LLR-307), never on trunk", or similar, so that it agrees with LLR-307. (K1) -> @owner
- [MINOR] docs/requirements/system-requirements.toml:742 -> The lane amends approved SR-156's acceptance_criteria ("That exemption applies only to the change's own lane; a trunk commit that changes a claimed Done-when is held against its parent ..."). The spec's Done-when trace-row list (docs/work/active/wi-921/WI-921-hook-floor-done-when-census.md:307-313) grants TC-325, TC-019, LLR-019, LLR-309 and LLR-307, not SR-156. Whether the checkpoint sitting asked for this amendment is outside my reading scope. The cell also repeats the "only the change's own lane" wording that finding 2 shows is inexact. -> Either name SR-156 in the spec's trace-row grant, citing the sitting that asked for it, or confirm the amendment through its approval authority at the checkpoint. Align its wording with LLR-307's elsewhere arm. (K3, K1) -> @owner
- [MINOR] docs/test/test-cases.toml:3315 -> For clarity. TC-325's evidence lists test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other, but its method neither runs nor asserts it. The lossless path read it pins is not stated in LLR-307's detail either. The RESYNC entry nonetheless advertises that read as a fail-open fix at every hold point ("before such a copy read as never claimed and passed"). -> Add the test to TC-325's method, with one assertion clause, and add one LLR-307 detail clause: claim and current listings and the staged delta are read unquoted, so a path git would quote is judged like any other. (K1) -> @owner

VERDICT: APPROVE findings=4
