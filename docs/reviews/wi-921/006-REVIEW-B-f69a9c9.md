Reviewed: f69a9c95f47212fdee4d4033ab5f8fdb37164191

**Verified.** The checkout was confirmed at f69a9c95f47212fdee4d4033ab5f8fdb37164191 before anything ran. I hunted the failure classes this change admits, worst first: fail-open (a trunk commit or a close carrying an unblessed Done-when change that the step passes), then a false hold in normal use, then silent wrong content in the census.

To drive the real shipped reader, I ran `integrate.staged_done_when_refusal` from the lane's scripts. The fixture was a trunk-plus-linked-lane repo I built outside this worktree (probe/probe.py in my writable area). Results:
- **Held:** a trunk Done-when amendment; a trunk squash that carries a lane's unblessed edit (the first commit of the two-commit landing); a lane close after an edit.
- **Passed:** a trunk edit outside the Done-when; a rename inside the claim folder; an evidence-only close on trunk; a CRLF-only rewrite; the lane's own edit commit.
- **Held, fail-closed:** a hand return to `queued/` and a move to a new claim folder on trunk.
- **Passed, the stated WI-922 residue:** a detached-HEAD close in the lane.

Code:
- `classify_delta` denies by default: every entry except a lone `A` counts.
- `staged_changes` reads the delta NUL-delimited, and the `(status, path)` pairing holds under `--no-renames`.
- `_copy_at` now lists paths losslessly at every hold point.
- A failed read of the delta or the branch holds, naming why. Off a git work tree nothing is judged (D-004).
- The hook runs under `set -e`, so a FAIL from the floor refuses the commit.

Census:
- `check.steps(80,"full","all")` gives 38 unique names, the same at other rungs.
- The census and the `test_commit_floor_census.py` cases are collected in the smoke tier (13 of 103 collected across the three modules).
- I spot-checked the reasons I quote against the hook header (lines 19-20 and 200-204) and against ruling 6 in docs/plans/2026-10-11-review-churn/README.md:110. They are accurate.

Red before the fix: I rebuilt the reviewed tree with e474f51dd's `integrate.py`, `kitlib/done_when.py`, `check.py` and `hooks/pre-commit`. Every new WI-921 test fails there, except the three census-function fault cases, which test the function itself:
- the census names `done-when-blessed: a built-in step in no class`;
- the trunk-amendment and index-delta cases assert on `None`;
- both hook-floor cases fail, the scaffold case included.

Rubric:
- K2 holds: the new SR-156 sentence names no artifact.
- K3 holds: each new function carries `Implements: SR-156, LLR-307` and appears in LLR-307's `code_symbol`, and `staged_done_when_refusal` is in LLR-309's.
- K4 holds: the RESYNC entry is present and anchored at a trunk commit.

Done-when map:
- (1) floor and comment: `test_every_built_in_step_is_classified_exactly_once` and `test_the_shipped_hooks_floor_holds_an_unblessed_hand_close`. Covered.
- (2) hook-driven test, scaffold case included: `test_the_shipped_hooks_floor_holds_an_unblessed_hand_close` and `test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree`. Covered, red before.
- (3) census plus three fault cases. Covered, red before.
- (4) two-commit landing and trunk amendment: `test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed[verdict|ruling]` and `test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not`. Covered, red before.
- (5) unlistable delta: `test_an_index_delta_git_cannot_list_holds_naming_why`. Covered, red before.
- (6) RESYNC anchored at the landing's parent: not met at this tip (see the last finding).
- (7) trace rows sat at the checkpoint: not met at this tip.
- (8) bar green on the landing tip: not this tip.

**Commands.**
- `git rev-parse HEAD` -> f69a9c95f47212fdee4d4033ab5f8fdb37164191
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2/C/wi-921 <the 16 prescribed modules>` -> `390 passed, 14 skipped in 599.20s` (12 of the skips are the posix-shell env gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (919 work item(s), 800 done (87%), 30 cancelled, graph acyclic).` (exit 0)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 ...` (exit 0; the one form finding is LLR-292's, which predates this range)
- `python project-trajectory/scripts/check.py --run-steps approval-fresh,approval-immutable,done-when-blessed` -> `SKIP approval-fresh` (work branch), `PASS approval-immutable`, `PASS done-when-blessed`
- `python project-trajectory/scripts/trace.py --approve modified` (filtered to the changed rows) -> `Waiting for automated adjudication — 3 chain(s): SR-019, SR-156, SR-224`, listing SR-156, LLR-307, LLR-309, TC-019 and TC-325
- Red-before: the same reviewed tree with e474f51dd's four step files swapped in; `pytest -n 0 -rA -k "<the WI-921 tests>"` -> 10 failed, 3 passed (the 3 are the census-function fault cases)
- Driven probe: `python -I probe/probe.py <lane> <fixture dir>` -> T1 pass, T2 pass, T3 HELD, T4 HELD, T5 pass, T6 HELD, T7 pass, L1 pass, L2 HELD, L3 pass, T8 HELD

**Findings.**

- [MINOR] project-trajectory/hooks/pre-commit:284 -> The shipped comment says a trunk hand return of a claim copy to the queue is held, "the kit's own return route, handback.py, commits with the hook bypassed". handback.py has no return-to-queue route. Its module docstring (lines 23-24) records that "the old contract moved a returned spec back to `queued/`" and was replaced. `close_partial` moves to the terminal `partial/` (handback.py:459). The only `hand_back` in the scripts is coordinator_guard.py:1300, a lease hand-back. So adopters are pointed at a route that does not exist. The probe (T3, T4) confirms that a hand return or a move to a new claim folder on trunk is held. The hold then reads "held until the claim copy reads" (`_NO_COPY`, kitlib/done_when.py:477), and no blessing can release it (D-006). This fails closed, so it is a coverage-extension note -> Say in the comment that the kit has no un-claim route, so a hand return or re-cut of a claim copy committed on trunk is held and no blessing releases it. Drop the handback.py parenthetical. (K1) -> @coordinator
- [MINOR] docs/requirements/low-level-requirements.toml:3286 -> For clarity: LLR-309's new sentence says "The exemption for the commit that changes Done-when text applies only to the claim's own lane". The code (`_staged_base`, kitlib/done_when.py:597) and LLR-307's own new sentence ("elsewhere, only a close is judged") also leave unheld a non-close Done-when change committed on a branch that is neither trunk nor the claim's: another lane's branch, or a detached HEAD. The two amended rows disagree, and a TC written from LLR-309 would expect a hold the code does not make -> Reword LLR-309 to match LLR-307: the edit commit is held only on the trunk (judged against its parent); elsewhere only a close is judged at commit, and the landing re-judges the change. (K1) -> @coordinator
- [MINOR] docs/requirements/system-requirements.toml:742 -> For clarity: SR-156's appended acceptance sentence "That exemption applies only to the change's own lane; ..." follows the review-gated-landing sentence. So "That exemption" has no antecedent there: the exemption it means ("the change's own commit remain unheld") sits two sentences earlier. The sentence also says "trunk commit" where the row says "integration branch" throughout -> Move the clause next to "the change's own commit remain unheld", and say "a commit on the integration branch". (K1) -> @coordinator
- [MINOR] project-trajectory/RESYNC_PACK.md:8351 -> At this tip, Done-when items 6 and 7 are not met. Their text changed under `status = "Approved"`: LLR-307, LLR-309 and SR-156, along with TC-019 and TC-325. `trace.py --approve modified` reports the SR-019 and SR-156 chains "Waiting for automated adjudication". The RESYNC entry is anchored `[since e474f51dd]`, the lane's base, while trunk has moved to c0ab27e03. The passed plan's P4 (checkpoint sitting and act) and P5 (re-anchor, close, final gate) carry both, so this is sequencing rather than a code defect. This tip is not a landing tip -> Take P4's combined sitting and act and P5's re-anchor before the landing, and re-gate that tip, as the plan orders. (K3, K4) -> @coordinator
- [MINOR] .claude/skills/coordinator-cycle/references/recipes.md:355 -> The two-commit landing recipe still says "Until WI-921 lands, the hook judges neither commit's Done-when change ... stage the full squash, run done-when-hold, `git reset --hard HEAD`, then land the two commits". The same text is in project-trajectory/skills/coordinator-cycle/references/recipes.md:356. This lane makes that workaround obsolete (the first commit is now judged against its parent), but the lane does not touch the skill. CLAUDE.md asks for the skill to change with the convention -> Replace the interim bullet: the first commit must carry the lane's verdict or owner ruling in its own tree, or it is refused naming the digest. Update both copies in the lane or at the landing. (K1) -> @coordinator

VERDICT: APPROVE findings=5
