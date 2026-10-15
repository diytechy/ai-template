Reviewed: bd4d7da21deff440078053769770503a4af0567f

Verified. Before hunting, I named the failure classes this change admits, worst first. (1) Fail-open: an unblessed Done-when change reaches trunk unjudged, through the two-commit landing, a trunk amendment, an unreadable delta or branch, or a misclassified staged entry. (2) A false hold in normal use: the new trunk arm or the armed floor refuses an ordinary commit, such as a claim, a lane's own Done-when edit, a landing that carries its blessing, or a scaffold with nothing staged. (3) The census silently admitting a step.

I drove the shipped code paths, `integrate.staged_done_when_refusal` -> `kdone.staged_hold` -> `_staged_base` / `lane_hold`, in a probe repository of my own (a trunk amendment of a claim copy is held, naming the digest) and through the new tests. Findings:
- Claims are plumbing commits (`bookkeeping.commit`, commit-tree), and a new claim copy is a lone `A`, so the trunk arm never holds a claim.
- On the claim's own branch, `branch == current` is asked before the trunk test. A lane's own Done-when edit is therefore never judged, even in a single checkout whose primary is on the lane branch, where `trunk_name()` equals the lane.
- A single-commit squash landing that carries its verdict is judged as before.
- The two-commit landing is held at its first commit, and its close then compares against the blessed parent copy.
- A failed `git diff --cached` and a failed `branch --show-current` each hold, naming why. A `None` lane base holds, because `claim_copy` refuses a missing revision.
- Consolidation archives only queued rows, and no recipe moves an active claim copy to a non-terminal folder. The new deny-by-default `change` kind for a lone `D` therefore has no false-hold path in normal use.

Red-before: I exported the reviewed tree to my writable area and put back the base versions of `hooks/pre-commit`, `check.py`, `integrate.py` and `kitlib/done_when.py`. Every new or changed test then fails: the census (`done-when-blessed` unclassified), the classifier, both two-commit landing cases, the trunk amendment, the failed index delta, the failed branch read, the hook-driven floor test, the scaffold floor test and the `staged_closes` shape. The three census fault cases test the census function, so they pass before and after, as designed.

Rubric K4: the `RESYNC_PACK.md` entry is anchored `[since e474f51dd]` at a trunk commit. Rubric K3 back-links: the four new functions carry `Implements: SR-156, LLR-307`, and LLR-307's module and `code_symbol` name them. `staged_done_when_refusal` stays LLR-309's. The census's 38 names equal `check.BUILTIN_STEP_NAMES`, and its cited texts exist: the hook header's gate-scoped rule (pre-commit:19), the floor rule at `trajectory-map` (pre-commit:177-178), and ruling 6 in docs/plans/2026-10-11-review-churn/README.md:18,110. This repository's `.githooks/pre-commit` still delegates to the shipped hook unchanged.

Done-when map:
- The floor runs `done-when-blessed`, and its comment describes the step: project-trajectory/hooks/pre-commit:276-284 and :305. Covered by tests/test_done_when_blessing.py::test_the_shipped_hooks_floor_holds_an_unblessed_hand_close and tests/test_commit_floor_census.py.
- The hook-driven test, its scaffold case included: test_the_shipped_hooks_floor_holds_an_unblessed_hand_close and test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree. Both are red before the change.
- The census in the smoke tier, red before naming the step, with three fault cases: tests/test_commit_floor_census.py, which is not in `SLOW_MODULES`.
- The WI-835 replay and the trunk amendment: test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed[verdict|ruling] and test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not. Both are red before the change.
- A failed index delta holds: test_an_index_delta_git_cannot_list_holds_naming_why. Red before the change.
- The RESYNC entry: present.
- The trace rows sat at the checkpoint: UNCOVERED at this tip (finding 2).
- The bar: `check_trajectory --strict` is clean, and `trace.py --strict` reports LLR-292's one finding only. I ran no smoke tier, per the round facts.

Commands:
- `git rev-parse HEAD` -> bd4d7da21deff440078053769770503a4af0567f
- The round's pytest selection (16 modules, `-n 2`, the literal `--basetemp`) -> `389 passed, 14 skipped in 589.09s`. 12 of the skips were the `posix-shell` env gate.
- The same with `C:\Program Files\Git\bin` on PATH, over tests/test_pre_commit_hook.py, tests/test_meta_repo_hook.py and tests/test_plan_gate.py -> `65 passed in 121.88s`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (919 work item(s), 800 done (87%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 ...`
- `python project-trajectory/scripts/trace.py --strict` -> exit 1, whose one finding is `LLR LLR-292 Detail uses 'minimal'` (pre-existing and allowed by the Done-when)
- `python project-trajectory/scripts/check.py --run-steps approval-fresh,approval-immutable,done-when-blessed` -> approval-fresh SKIP (work branch), `PASS  approval-immutable`, `PASS  done-when-blessed`
- The red-before replay: the base versions of the four production files in an exported tree, running the new tests -> `13 failed, 3 passed` (the 3 passes are the census fault cases)
- A probe in my writable area, probe/probe.py, through `integrate.staged_done_when_refusal` on a trunk amendment: an ASCII slug -> held, naming the digest; a non-ASCII slug -> `None` (finding 3)
- `git status --short` in the lane -> empty (nothing changed)

- [MINOR] docs/requirements/system-requirements.toml:742 -> (K3, K1; for clarity) SR-156's approved acceptance criteria are amended, but the spec's Done-when trace list grants amendments only to TC-325, TC-019, LLR-019, LLR-309 and LLR-307, never SR-156. The amendment is needed: the old cell's "the change's own commit remain[s] unheld" literally exempts a trunk amendment, which deliverable 5 holds. But its new sentence, "That exemption applies only to the change's own lane", follows a clause with two exemptions (review or adjudication sessions, and the change's own commit), so its referent is ambiguous -> name SR-156 in the checkpoint sitting's scope explicitly (or in the spec's trace list through its amendment route), and reword it the way LLR-309 does: "The exemption for the commit that changes the Done-when text applies only to the change's own lane" -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3286 -> (K3) The Done-when item "the change's trace rows ... where their text changes, sat at its checkpoint" is not met at this tip. SR-156, LLR-307, LLR-309, TC-019 and TC-325 carry amended text, still at Status Approved, and the range holds no sitting record. This is the lane's stated next step (the intent commit says "unjudged until the checkpoint"), not a code defect -> sit the combined checkpoint over these five rows and land the act before the landing. If the sitting returns code, repeat this full-lane gate -> @owner
- [MINOR] project-trajectory/scripts/kitlib/done_when.py:561 -> (B1; confirmed by probe) The index delta is read with a plain `git diff --cached --name-status`. Under git's default `core.quotePath`, a claim copy whose path has a non-ASCII byte prints quoted (`"docs/work/active/wi-007/WI-007-caf\303\251.md"`) and matches `_ACTIVE_SPEC_RE` nowhere. A trunk amendment, or a close, of such a copy's Done-when is therefore not judged: fail-open, `staged_done_when_refusal` -> `None`. It is reachable only for a hand-named file, because minted slugs are `[a-z0-9-]` (`wi_convert.slugify`) and claim folders are `wi-NNN`. `_copy_at`'s plain `ls-files`/`ls-tree` share the shape, which predates this lane -> read the delta NUL-delimited and unquoted (`diff --cached -z --name-status --no-renames`, decoded as `kitlib.git.git_paths` decodes for WI-818's two-tree rules), so a quoted path cannot reach the classifier. This changes the one reader rather than adding a guard -> @owner

VERDICT: APPROVE findings=3
