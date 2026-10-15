Reviewed: f69a9c95f47212fdee4d4033ab5f8fdb37164191

Verified. Checkout confirmed at the reviewed commit. Read the whole diff
`e474f51dd...f69a9c9` (exclusions as briefed), the spec
docs/work/active/wi-921/WI-921-hook-floor-done-when-census.md, its specref
(WI-841 deliverable), the rubric, and the amended rows SR-156, LLR-307,
LLR-309, TC-019, TC-325. Failure classes hunted first: (1) the trunk arm
failing open (a Done-when change on trunk not judged), (2) an unreadable
read passing as "no close", (3) the hook floor not actually running the step,
(4) approved spine rows amended without authority. For (1)-(3) I drove the
shipped reader and the registered step: `kitlib.done_when.staged_hold` via
`integrate.staged_done_when_refusal` and `check.py --run-steps <the floor read
off the hook>` on the lane fixtures, at the tip and against a clean
`git archive` of the base e474f51dd with the new tests copied in. At the base
the two-commit landing's first commit, the trunk amendment and the corrupt
index all return None (fail-open confirmed); at the tip each holds naming the
digest or the failed read, and a staged verdict or an owner ruling releases
it. `_staged_base`'s three readings match LLR-307's amended detail (own branch:
close only, against the lane base; trunk: every change against HEAD;
elsewhere: close only against HEAD), `classify_delta` denies by default (any
entry but a lone `A`), `git diff -z --name-status` pairs are consumed
correctly, `claim_copy` with a None base returns UNREADABLE so a failed
`default_base` holds. `hook_check_lines` reads exactly the one `--run-steps`
line (hooks/pre-commit:312) and the one `--run-step format` line (:347); the
census's 22 + 1 + 15 classification covers the 38 built-in names, and it is a
smoke-tier module (not in SLOW_MODULES). K3: every new function carries
`Implements: SR-156, LLR-307` and LLR-307's code_symbol names them;
`staged_done_when_refusal` stays on LLR-309. K2: SR-156's new sentence names
no artifact. K4: RESYNC entry anchored `[since e474f51dd]`, a trunk commit.
Red-before: all seven hook/trunk/failed-read tests and the census fail on the
base extract (census names `done-when-blessed` as unclassified). Note: 12
tests in the brief's selection are environment-skipped here (posix-shell), so
the sh hook itself was not executed on this box; the floor list was driven
through check.py as the spec's deliverable 2 asks.

Done-when map: floor + comment block - hooks/pre-commit:273-312, covered.
Hook-driven test incl. scaffold, red before - test_the_shipped_hooks_floor_holds_an_unblessed_hand_close,
test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree, covered.
Census in smoke, red before, three fault cases - tests/test_commit_floor_census.py, covered.
Two-commit replay + trunk amendment + no-change not judged, red before -
test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed[verdict|ruling],
test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not, covered.
Unlistable index delta holds naming why, red before - test_an_index_delta_git_cannot_list_holds_naming_why, covered.
RESYNC entry anchored at the landing's parent - RESYNC_PACK.md:8351, covered.
Trace rows authored and, where text changes, sat at the checkpoint - authored (TC-325, TC-019, LLR-307, LLR-309, SR-156); the sitting is UNCOVERED at this tip (finding 1).
Bar green on the landing tip - the brief's selection 390 passed / 14 skipped; check_trajectory --strict clean; smoke tier and trace --strict not run per the brief.

Commands:
- `git rev-parse HEAD` -> f69a9c95f47212fdee4d4033ab5f8fdb37164191
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../B/wi-921 <the 16 modules>` -> `390 passed, 14 skipped in 607.83s (0:10:07)` (12 skips are the posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (919 work item(s), 800 done (87%), 30 cancelled, graph acyclic).` (5 pre-existing WARNs about open-WI overlaps, none naming WI-921)
- base extract (`git archive e474f51dd` + the tip's tests/conftest.py, test_commit_floor_census.py, test_done_when.py, test_done_when_blessing.py), `pytest -k "census or classifies or two_commit or trunk_amendment or index_delta or branch_identity or shipped_hooks_floor or scaffold_hooks_floor or git_quotes or share_one_predicate or any_terminal_home"` -> `15 failed, 3 passed, 85 deselected`; the two-commit, trunk-amendment and index-delta cases fail on `assert held` with `held is None`; the census fails with `done-when-blessed: a built-in step in no class`
- `git ls-files docs/reviews/wi-921*` -> 001/002/003-REVIEW-*-bd4d7da.md only (no ADJUDICATE / sitting record at this tip)

Findings:
- [MAJOR] docs/requirements/system-requirements.toml:742 (also docs/requirements/low-level-requirements.toml:3261-3262 and :3286, docs/test/test-cases.toml:202 and :3315) -> five Approved rows (SR-156 acceptance, LLR-307 and LLR-309 detail, TC-019 and TC-325 method/evidence) are amended in this range with no sitting verdict or act in the reviewed tree (docs/reviews/wi-921/ holds only the three round-1 reviews; lane commit bd4d7da21 itself says "unjudged until the checkpoint"), while the spec's Done-when requires each changed trace row to be "sat at its checkpoint" and the brief requires changed child content re-attested through its applicable authority before the landing this full-lane review judges; the hook's approval-immutable step does not hold a text amendment of an Approved row, so this review is the only enforcer and the landing of f69a9c9 as-is would carry re-worded approved requirements under their old attestation (K1/K3) -> run the P4 combined sitting over SR-156, LLR-307, LLR-309, TC-019, TC-325 in the lane, commit its verdict and act, and re-gate the tip that then lands (no new guard is added: the sitting is the existing authority, and the spec's own Done-when clause already owns it) -> @coordinator
- [MINOR] docs/test/test-cases.toml:3315 -> for clarity: TC-325's method names seven new tests and no lossless-path case, while its evidence (:3318) lists an eighth, `test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other`, so method and evidence disagree on what the case runs and asserts -> add the test to the method's "Also run" list and one assert clause ("a claim copy whose path git quotes is judged like any other") -> @coordinator
- [MINOR] docs/requirements/system-requirements.toml:742 -> for clarity: "That exemption applies only to the change's own lane" is appended after the review-gated-landing sentence, so its antecedent (the change's own commit remaining unheld) sits two sentences back and reads as the review-session clause on first pass -> reword to name it ("The unheld change-commit exemption applies only to the change's own lane; ...") or place it directly after the sentence it qualifies -> @coordinator
- [MINOR] project-trajectory/scripts/kitlib/done_when.py:598 -> in the "elsewhere" reading (current branch is neither the claim's branch nor what `trunk_name` returns, e.g. a linked worktree checked out on the trunk branch while the primary checkout sits on another branch) a staged non-close change to a claim copy's Done-when is not judged at all, which fails open for that commit; the spec declares this reading and the landing re-judges a close, so it is a coverage-extension note, not a reachable normal-use scenario; the hook comment (hooks/pre-commit:273-288) names two residues but not this one, nor the hand fast-forward of a lane that edited without closing (no commit is judged, and the later trunk close compares the edit with itself, by design under the enforce-at-the-commit ruling) -> state both residues in the hook's comment block beside the two it already names; the structural alternative, judging every non-own-branch change against HEAD (a smaller rule set, no added guard), is the `antidote` question's answer should the owner want it closed -> @coordinator

VERDICT: CHANGES-REQUESTED findings=4
