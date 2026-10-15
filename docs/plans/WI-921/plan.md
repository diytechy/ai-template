# WI-921 plan, revision 1: the shipped hook runs `done-when-blessed`, the step holds what it must, a census classifies every built-in step, and the final gate reviews the tree that lands

Spec: `docs/work/active/wi-921/WI-921-hook-floor-done-when-census.md`. Its specref is WI-841's Deliverable (`docs/archive/work/complete/WI-841-done-when-blessed-in-lane.md`). The owner rulings it relies on are the spec's "Calls ruled at filing" and `docs/decisions/coordinator-2026-10-15.toml` D-002 and D-003.

The item's SRs are SR-156 and SR-019 (`docs/requirements/system-requirements.toml`). Fifteen TCs verify them (`docs/test/test-cases.toml`): TC-019, TC-021, TC-131, TC-132, TC-139, TC-144, TC-145, TC-205, TC-257, TC-259, TC-317, TC-325, TC-326, TC-327 and TC-328. A row below names each one, or the Excludes line at the end gives the reason it is left out.

## The first critique's finding, and what else this revision changes

**F1 [MAJOR, G4 / B4]: confirmed, except for its regeneration clause.**

- **The rule.** SR-156's acceptance clears a review-gated landing only from independent review sessions "over the lane from its recorded claim base to the reviewed tip". The merge slot holds a lane to that: `integrate._verdict_gate` (LLR-140) counts a verdict only while it names the branch's current non-record tree, and `docs/work/` is deliberately inside that tree. So `PROCESS_OPTIONS.md` ("The LLM-gate verdict protocol") and session-protocol §4 put the close before the final verdict round, and the reviewer sees the record it blesses. A hand landing owes the same order.
- **Where the first plan broke it.** P4 ended with the fresh full-lane gate. P5 then restored the views, rebased, re-anchored the RESYNC entry and closed the row. The landing would have carried authored text no gate saw: the filled Deliverable, the moved spec with its cleared specref, and the final anchor. A rebase after the gate is also the case coordinator-cycle §4 step 1 says repeats it.
- **Refuted: regenerating before the gate.** The trunk-only generated views are never committed from a work branch (SR-170; `gen_verdict_rollup.py` refuses on one). recipes §3 restores them to trunk's bytes before the final gate, so the gated range is authored work, and the landing rewrites them from the gated tree. The merge slot's identity steps over the station refresh's regeneration in the same way.
- **The new order.** P4 ends with the checkpoint's act. P5 rebases, restores the views, re-anchors the entry, closes the row in the lane and runs the bar, then takes the fresh full-lane gate over that tip as its last step. P6 lands that tip on the trunk commit it was gated on and adds only the regenerated views. If trunk moves after the gate, P5 runs again, gate included.

**Also changed, found while re-checking the first plan against the code:**

- **`staged_closes` stays (C4).** The first plan retired it. But WI-922's spec (its deliverable 2 and its S4) names `kitlib.done_when.staged_closes` as its reader of the lane a staged close names, and WI-922 rebases onto this landing. The function keeps its name, and its return gains the failure reason, so no caller can read an unreadable delta as "no close".
- **The classifier denies by default.** Any entry for a claim copy other than a lone `A` is a change, so a status the first plan did not list (`T`, `U`) cannot pass unjudged.
- **Nothing more is read when nothing is listed.** A fresh repository's first commit (an unborn HEAD, where every entry is `A`) is never held by a failed read at HEAD.
- **A failed read of the branch identity gets its own test** (deliverable 5's third bullet).
- **TC-019's expected cell stays** unless LLR-019 gains the floor-membership rule, because a TC expects only what a requirement states.
- **One new risk:** the smoke tier's membership ceiling (R7).

## Steps, in build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The step's reader: a trunk commit's unblessed Done-when change holds, and so does a read the step cannot complete | D4; D5; SR-156; TC-325; TC-326; TC-328; TC-259 | IF-286; IF-080; IF-154; IF-242 | |
| P2 | The shipped hook's floor runs done-when-blessed, a census classifies every built-in step, and a test drives the hook's own floor | D1; D2; D3; SR-019; SR-156; TC-019; TC-021; TC-325 | IF-040; IF-134; IF-080 | P1 |
| P3 | The RESYNC_PACK.md entry | D6; SR-019; SR-156 | IF-134; IF-080; IF-286 | P1; P2 |
| P4 | The trace rows, authored in the lane and sat at its checkpoint, which ends with the act | D7; D8; D9; D10; D11; SR-156; SR-019; TC-325; TC-019 | IF-286 (TC-325 verifies it and LLR-307 states its reader) | P1; P2 |
| P5 | The lane's tip made final (rebased, views restored, entry re-anchored, row closed, bar green), then the fresh full-lane gate over that tip | D6; F1; SR-156; SR-019 | no interface: the rebase, close, bar and review cross no code seam | P3; P4 |
| P6 | The landing: the gated tip squashed onto the trunk commit it was gated on, the trunk-only views regenerated, the bar run on the landing tip | D12; F1; SR-156; SR-019 | no interface: the squash, regeneration and bar cross no code seam | P5 |

DELTA: within

**Clauses covered by two rows, each split stated.**

- **D6:** P3 writes the entry, and P5 sets its final anchor, the trunk commit P6 lands on.
- **F1:** P5 carries the order (the gate last, over the closed tip), and P6 carries the rule that the landing adds nothing authored after the gate.

**Architectural delta.** The row makes two outputs depend on inputs they never read before:

- **The hook's exit.** It now depends on the staged claim-copy changes and on their blessing, through the floor seam (IF-040 and IF-134). Both contracts stay as they are, and the floor list gains one name (P2).
- **The step's verdict.** On trunk it now depends on whether a commit changes a claim copy's Done-when, and everywhere on whether the step's own reads complete. These are the reader's contract (IF-286) and the step's refusal set (IF-080). P1 carries both, including the contract text and `staged_closes`' wider return.

The row adds no state, no value to a domain and no boundary. The verdict is still pass or hold, and the new hold reasons are text. No preparatory refactor is needed. So the change is within scope, and P1 and P2 carry it. The reordered landing (P5, P6) is procedure and changes no seam.

## P1: the step's reader

**Files.** `project-trajectory/scripts/kitlib/done_when.py` (IF-286's owner, and the one reader the Trust section names) and `project-trajectory/scripts/integrate.py`. The step comment in `project-trajectory/scripts/check.py` changes too, as a comment only.

**How the reader works.** It denies by default, and it names each input class in S3.

- **One read of the commit being made**, in `kitlib/done_when.py`:
  - Outside a git work tree it judges nothing, because no commit is being made. The test is the one `check.py`'s `_ruling_sync_refusal` and `_text_then_act_refusal` use: git cannot answer `rev-parse --is-inside-work-tree`. `plan_gate.staged_lines` likewise judges nothing off git.
  - Inside one, it lists the index delta (`git diff --cached --name-status --no-renames`). If git cannot list it, the read returns its reason, never an empty list. Probed on a scratch repository: an index git cannot parse still answers `true` to `--is-inside-work-tree` while `diff --cached` exits 128, so that case reaches the hold, not the off-git rule.
- **A pure classifier over the delta**, smoke-pinned below.
  - A work item's claim copy is changed when the delta has any entry for it under `docs/work/active/<branch>/` other than a lone `A`: an `M`, a `D`, a `T`, or any other status git reports.
  - The change is a close when the same delta adds the item's spec under a closed folder (`docs/archive/work/` or `docs/work/`, each with `complete`, `partial` and `cancelled`). Otherwise it is a change without a close; a `D` plus an `A` in the same claim folder (a new slug) is one.
  - A lone `A` there is a new claim copy. It has no parent copy to compare, so it is not listed. On an unborn HEAD every entry is `A`.
  - Any other path is not a claim copy.
- **Nothing more is read when nothing is listed.** The branch, the trunk's name and HEAD are read only for a listed change. A commit that touches no claim copy costs the work-tree test and the delta read. A fresh repository's first commit is never held by a read at a HEAD that does not exist yet (probed: on an unborn HEAD `diff --cached` lists the staged files as `A`, while `ls-tree HEAD` fails).
- **Which reading applies to each change** depends on the commit's branch identity. The step reads the current branch once, and a failed read holds, naming why. The own-branch test runs first, so a single checkout switched to its lane keeps the lane reading.
  - **On the claim's own branch** (the branch the claim folder names), only a close is judged, against the lane's integration base. This is today's lane reading. The commit that edits the Done-when there is never judged.
  - **On trunk** (the current branch is the one `agent_common.trunk_name` returns), every change is judged, close or not, against HEAD, the commit's parent (deliverable 5). The step never searches history.
  - **Elsewhere** (a detached HEAD or an alias branch), a close is judged against HEAD, as today. This is WI-922's identity class, and the landing re-judges it.
- **One predicate.** Each judged change asks `lane_hold(root, None, base, branch, [wi_id])`.
  - A covering accepted verdict or owner ruling in the index releases it, and a hold names the digest and the changes.
  - An unreadable claim copy or current copy already holds and names why, and so does a claimed row left with no copy (LLR-307's existing rule).
  - An integration base that cannot be read (`default_base` answers None) reaches `claim_copy` as no revision and holds the same way.
- **An unreadable delta** holds with one reason that names what could not be read: the index delta cannot be listed, so whether this commit changes a claimed Done-when is unknown.
- **`integrate.staged_done_when_refusal`** becomes a thin caller. It passes in what `agent_common` owns, as readers called only for a listed change:
  - the current branch, read through `agent_common.git` as today's step reads it, with a failed read returned as its reason;
  - the trunk's name (`trunk_name`);
  - the lane's integration base (`default_base`), read only for an own-branch close.
- **`staged_closes` stays, and fails closed (C4).** It becomes the closes of the one reading, and its return gains the reason: `(closes, why)`. WI-922's deliverable 2 reads the lane a staged close names through it.
- **Contract text.**
  - The `Contract IF-286` docstring in `done_when.py` names the trunk arm, the failed-read hold and `staged_closes`' new return.
  - The `Contract IF-080` docstring in `integrate.py` and the `done-when-hold` help line name the wider refusal.
  - The `done-when-blessed` step comment in `check.py` says the same.
  - The IF-286, IF-080 and IF-154 registry cells point at the module contracts or the unchanged argv, and do not change. IF-286 is Drafted, so its `v1` stays: `PROCESS.md` §4 communicates changed versions of approved interfaces only.
- **Ratchets.**
  - `tests/test_module_size_ratchet.py` holds `integrate.py` at an exact SLOC (1551 today), so its BASELINE entry is re-stamped to the measured value in the commit that moves it. It should move down.
  - New functions stay at or under `MAX_COMPLEXITY = 10` (`tests/test_complexity_ratchet.py`) and pass `check_complexity.py --mode enforce`.
- **Trace fields.** The builder keeps these current on every commit:
  - `Implements: SR-156, LLR-307` on the new functions;
  - LLR-307's `code_symbol`, which gains them (`staged_closes` stays named);
  - TC-325's `evidence`, which gains the new test ids.

  Row text waits for P4.

**Tests added.** Each is written first and run against the claim base's code, and the failure is recorded in the round's report before the fix lands with it.

- **`tests/test_done_when_blessing.py::test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed`** (D4), parametrized over a verdict and an owner ruling, replays WI-835's shape:
  1. The lane edits its Done-when and closes in a later commit.
  2. Trunk takes `git merge --squash` of the commit before the close.
  3. That index is held, naming the digest. The test asserts this through the function and through `integrate.main(["--root", trunk, "done-when-hold"]) == 1`.
  4. The same index passes once it carries the lane's accepted verdict, or the owner-confirmed `done_when` entry.
  5. After that commit, the close staged next compares against the blessed copy and passes.

  *Fails before:* trunk's step sees no close in the first commit and returns no hold.
- **`tests/test_done_when_blessing.py::test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not`** (D4) works on trunk:
  - an edit to the claim copy's Context alone is not held;
  - an edit to its Done-when is held, naming the digest;
  - an owner-confirmed ruling that binds that digest, in the same index, releases it.

  *Fails before:* the Done-when amendment is not held.
- **`tests/test_done_when_blessing.py::test_an_index_delta_git_cannot_list_holds_naming_why`** (D5) makes the lane's index unreadable by writing garbage bytes at `git rev-parse --git-path index`. The step then holds, naming the delta read, and `done-when-hold` exits 1. A directory outside any repository, with `GIT_CEILING_DIRECTORIES` pinned, is not judged; that half pins the off-git rule (C1). *Fails before:* the unreadable delta reads as "no close", so nothing holds.
- **`tests/test_done_when_blessing.py::test_a_branch_identity_git_cannot_read_holds_naming_why`** stages an unblessed close in the lane and makes the current-branch read fail. It substitutes `agent_common.git` in process for that one call, the read today's step also makes, so the same substitution reaches the old code and the new. The step holds, naming the branch read. *Fails before:* today's step takes git's error text as the branch name, judges the close against HEAD (the lane's own edited copy) and holds nothing.
- **`tests/test_done_when.py::test_the_staged_delta_classifies_each_claim_copy_change`** is a smoke-tier, in-process table test over delta listings. It checks:
  - `M` gives a change;
  - `D` plus `A` in each closed home gives a close;
  - `D` plus `A` in the same claim folder gives a change;
  - `D` alone gives a change, and so does `T`;
  - `A` alone is not listed, so an unborn HEAD's all-`A` delta lists nothing;
  - a path outside a claim folder is not listed.

  *Fails before:* no classifier exists, and `staged_closes` reports only closes. This is the per-commit pin for S3's classes; the cases above live in a slow module.
- **Two existing tests are updated.**
  - `test_the_hold_points_share_one_predicate` follows the hand-close point into the reader, which must still name `lane_hold`.
  - `test_a_hand_close_into_any_terminal_home_is_held` asserts `staged_closes`' new return, `([(BRANCH, WI)], None)`.

**Regression runs.**

- All of `tests/test_done_when_blessing.py`, the evidence of TC-325, TC-326 and TC-328, runs green. The existing hand-close, edit-commit, covering-verdict and unreadable-claim cases keep their results.
- `tests/test_done_when.py` (TC-259) runs green.

**Order.** P1 lands before P2, so the floor arms a step that already holds.

## P2: the floor, the census and the hook-driven test

**Files.** `project-trajectory/hooks/pre-commit`, `tests/conftest.py`, a new `tests/test_commit_floor_census.py`, and `tests/test_done_when_blessing.py`.

- **The hook.** `done-when-blessed` joins the batched `--run-steps` line. The floor's comment block gains an entry for it, which says:
  - it reads the index;
  - it refuses a staged close whose changed Done-when no accepted verdict or owner ruling binds, and a trunk commit that changes a claim copy's Done-when unblessed;
  - a read it cannot complete holds;
  - a lane's commit that edits its own Done-when is never refused;
  - the merge slot asks the same of the branch.

  The spec's bullet says "the commit that edits the Done-when is never refused". Deliverable 5 now refuses a trunk commit that edits a claim copy's Done-when unblessed, so the entry names the lane's commit, which is the one that stays free. This repository's `.githooks/pre-commit` delegates to the shipped hook and is unchanged.
- **One helper in `tests/conftest.py`** reads a hook's command lines: the non-comment `"$PY" ... check.py` invocations. It returns the batched floor (`--run-steps`) and the steps run by name (`--run-step`). It refuses a hook that has anything other than exactly one batched floor line. Both new test sets use it, for the kit's hook and for a scaffold's copy (C5).
- **The census** (`tests/test_commit_floor_census.py`) runs in the smoke tier, in process. A census function takes four inputs: the step names, the floor, the by-name steps and a table of steps not run at commit. It returns one finding for each of three faults: a step in no class, a name in two classes, and a listed name that is not a step.

  The live test feeds it `check.steps(80, "full", "all")`'s names (pinned inside `BUILTIN_STEP_NAMES` by `tests/test_stack_profile.py`), the kit hook's two lists, and the module's table of the 15 steps not run at commit. Each table entry has a one-line reason that cites where the kit states it. The table records today's classification and moves no step except `done-when-blessed`. If the builder cannot confirm a reason, the step goes to the coordinator and stays listed where it is.

  The proposed classification, which the builder confirms from each step:
  - **Floor (22 after this row):** the 21 on trunk plus `done-when-blessed`.
  - **By name:** `format`.
  - **Not at commit, for a reason the kit states (6):**
    - `tests+coverage`: the hook header's gate-scoped rule, and the floor rule at `trajectory-map`;
    - `traceability`: the hook's `registry-integrity` entry (the full `--strict` check is a gate criterion that must never block an early commit), and ruling 6 in `docs/plans/2026-10-11-review-churn/README.md` (`trace.py --strict` runs after each build, at the closure check and at landing, never in the commit hook);
    - `privacy`: its step comment. It is the tracked-tree sweep for what slipped in before the gate was enabled or past `--no-verify`, while the hook scans staged content itself;
    - `perf-budgets`: the floor rule;
    - `design-flows`: the floor rule;
    - `assumption-evidence`: the floor rule's gate context, since it reads the harness's results.
  - **Not at commit, under only the hook header's gate-scoped rule (9):** `lint`, `vocabulary`, `need-form`, `doc-navigability`, `backlink-coverage`, `test-first`, `assumption-gate`, `crossing-allocation` and `interface-allocation`. Each gets the reason the builder confirms from the step.

  The counts match the spec's: 21 + 1 + 15 + 1 = 38, the length of `check.steps(80, "full", "all")` on trunk today.
- **The hook-driven tests** go in `tests/test_done_when_blessing.py`. Like WI-913's `test_the_shipped_hooks_floor_refuses_an_unplanned_build`, they read the floor off the kit hook through the helper and run `check.py --run-steps <floor>` on the lane fixtures. The assertions read the step's own result line, because other floor steps may fail on a minimal fixture.
  - **`test_the_shipped_hooks_floor_holds_an_unblessed_hand_close`** has three cases:
    - a staged close with an unblessed Done-when gives `FAIL  done-when-blessed`, naming the digest, with a nonzero exit;
    - with the lane's covering verdict committed, it gives `PASS  done-when-blessed`;
    - the lane's own Done-when edit, staged without a close, gives `PASS  done-when-blessed`.
  - **`test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree`** uses a bootstrapped scaffold (the `scaffold` fixture). It prepares the scaffold as `test_hook_runs_end_to_end_when_sh_available` does (`make_minimal_project`, `git init`, `pin_autocrlf`), then commits it so nothing is staged. The scaffold hook's floor (`.githooks/pre-commit`) names `done-when-blessed`, every name resolves, and it exits 0.

**What each test fails on before the change.**

- The live census names `done-when-blessed` as unclassified.
- The three census-fault cases pass before and after, because they test the census itself.
- The lane tests find no `done-when-blessed` line, because trunk's floor does not run the step.
- The scaffold case finds the step absent from the scaffold's floor.

**Regression runs.** These slow modules read or run the floor:

- `tests/test_pre_commit_hook.py`, the evidence of TC-019 and TC-021. Its end-to-end and interpreter-floor hook runs execute the edited floor.
- `tests/test_plan_gate.py`, whose floor test now also runs this step.
- `tests/test_meta_repo_hook.py`, `tests/test_integrate_admission.py`, `tests/test_ruling_sync.py` and `tests/test_text_then_act.py`.

In the smoke tier, `tests/test_generated_freshness_census.py` also reads the floor line.

**Commit.** The hook edit, the helper, the census and the hook-driven tests go in one commit, so the smoke tier is never red. That commit takes the commit bar: `python -m pytest -q -n auto -m smoke` and `python scripts/check_smoke_budget.py --mode enforce`.

## P3: the RESYNC_PACK.md entry

The entry goes in `project-trajectory/RESYNC_PACK.md`, after the last entry before §5 (WI-913's). It is anchored at the lane's trunk base, with the pack's "Anchored at the preceding commit" parenthetical. P5 sets its final anchor, the trunk commit P6 lands on. It covers deliverables 4 and 5:

- the hook now runs `done-when-blessed`;
- the files form a set:
  - `hooks/pre-commit` goes with `scripts/check.py` (§2.3);
  - `scripts/integrate.py` and `scripts/kitlib/done_when.py` must be at this version, because the trunk arm and the failed-read hold ship in them. The spec's "WI-841's version or later" is only the floor for the step to exist;
- a hand close whose changed Done-when no verdict or owner ruling binds is now refused at commit, as the merge slot already refuses it;
- so is a trunk commit that changes a claimed row's Done-when unblessed, whether it is a landing's first commit or a trunk amendment;
- an index delta git cannot list holds;
- nothing changes in a repository that never claims into `docs/work/active/<branch>/`, or off git;
- no migration is forced.

The kit-owned files to overwrite are `hooks/pre-commit` (re-copied to `.githooks/pre-commit`), `scripts/check.py`, `scripts/integrate.py` and `scripts/kitlib/done_when.py`.

No test is added. `tests/test_resync_pack.py` (a slow module) runs green: anchors resolve, entries are in landing order, and no reserved heading is left.

## P4: the trace rows (coordinator-cycle §3: intent and checkpoint)

The rows are drafted once and judged once, against settled code.

- **Intent, after P1's first build round.** Terra authors the whole change set from the anchor (SR-156, SR-019) down, with the arms map. Existing statuses stay, and the coordinator verifies and commits the set without a sitting. During iteration the builder keeps only trace fields current, and proposed row text goes on the lane's spine change list.
- **The rows.** Terra amends approved rows by addition, keeping each approved cell verbatim (recipes §5).
  - **TC-325 (D8).** Its method, expected and evidence gain the hook-driven case (P2's lane test) and P1's two-commit, trunk-amendment, failed-read, branch-read and classifier cases.
  - **TC-019 (D9).** Its method and evidence gain the census. Its expected cell changes only if LLR-019 gains the rule below, because a TC expects only what a requirement states (recipes §5).
  - **LLR-019 (D10)** stays unchanged unless the sitting asks for the floor-membership rule. If it does, Terra drafts the rule and it is sat again.
  - **LLR-309 and LLR-307 (D11).**
    - For LLR-309, Terra drafts the trunk arm: a trunk commit that changes a claim copy's Done-when is judged against its parent.
    - For LLR-307, Terra drafts the failed-read hold (an index delta git cannot list, a branch identity git cannot read) and `staged_closes`' return naming it.
    - The sitting decides whether each is new. An amendment lands if the sitting reads its change as new. If it reads it as already stated, the coordinator takes the CLARITY re-attestation or withdraws the edit.
  - **SR-156's acceptance** exempts "the change's own commit". That clause goes to the same sitting (R1).
- **The checkpoint**, once a narrow round has no BLOCKER or MAJOR:
  1. The latch (coordinator-cycle §4): the lanes due to land ahead of this one have landed, and the lane has rebased, so its acts and the id watermark pull up.
  2. Terra, resumed, reconciles the whole set against the settled code.
  3. The closure check: `trace.py --strict-integrity`, `check_trajectory.py --strict`, arm coverage judged against the map, and each TC expected clause matched to a sentence of an LLR or SR in the set.
  4. One `combined` sitting. Returns are routed and re-sat.
  5. The acts: the amendment act first, then any first-approval act (recipes §3).

  P4 ends with the act. The fresh full-lane gate is P5's last step (F1).

No test is added. P1's and P2's tests are the evidence the amended rows cite.

## P5: the lane's tip made final, then the gate (F1; coordinator-cycle §3 step 4 and §4; recipes §3)

Everything authored that lands is on this tip before the gate reviews it. In order:

1. **Rebase** onto trunk's tip if trunk moved since P4's latch. A rebase that changes code or authored rows repeats P4's affected checkpoint (coordinator-cycle §4 step 1). After any rebase, `docs/archive/last_approved/acts.toml` is checked for duplicate act seqs (recipes §4). A duplicate means the act is taken again on the new base, as part of that repeated checkpoint.
2. **Restore the trunk-only generated views** to that base's bytes, the review rollup included (recipes §3). The lane keeps its module-size stamp.
3. **Re-anchor P3's entry** at the commit the lane now sits on. While trunk holds still, that commit is the landing's parent (D6).
4. **Close the row in the lane**, in its own commit (recipes §3, "Close the row"):
   - `## Deliverable` is filled and placed before `## Context`;
   - `specref = ""`;
   - `spec_move.py` moves the spec to `docs/archive/work/complete/`;
   - if `docs/status.md`'s hand text names the id, the same commit scrubs it.

   The armed step judges this close on the claim's own branch, against the integration base, and plan-gate reads it as the row's close.
5. **The bar on this tip:**
   - the commit bar (session-protocol §3): the smoke tier within its 60 s budget, and `check_docs.py --root . --stale`;
   - `check_trajectory.py --strict` clean;
   - `trace.py --strict` with no finding beyond LLR-292's, or none once WI-914 has landed;
   - `trace.py --strict-integrity`;
   - `check_complexity.py --mode enforce`;
   - the full unfiltered suite, once (recipes §7). The D2, D4 and D5 tests live in `tests/test_done_when_blessing.py`, a slow module the smoke tier never runs.
6. **The fresh full-lane gate, last.** `review_brief.py review --scope full` runs from the lane's trunk base to this tip, in the reviewer set the coordinator runs (recipes §1 and §7), and names the touched test modules. Each verdict is filed as the lane's round file. The gate reviews the code, the rows, the entry's final anchor and the closed spec together.

**On the gate's verdict.**

- **An APPROVE, or MINORs only:** go to P6. A MINOR the coordinator adopts is either fixed and then gated again, by another fresh full-lane review over the new tip, or recorded in the lane's decisions record for a successor. Nothing authored changes after the gated tip.
- **A BLOCKER or MAJOR:** the close is rewound. The lane is reset to the commit before it, and the discarded commit is archived as an extra parent on `archive/lanes`, because the adjudication entry point refuses a sitting on a row no longer under `active/` (recipes §8). The lane goes back to iterate, holds another checkpoint if rows change, and runs P5 again.

**Why the views are not regenerated here.** SR-170 writes the generated project-state artifacts only from the serial merge step, never from a work branch, and `gen_verdict_rollup.py` refuses on one. Each view is a function of the authored tree the gate reviews, so P6 regenerates them from exactly that tree.

## P6: the landing (recipes §3)

- **Preconditions.**
  - WI-911's plan pass record is committed in its lane (D-003 (1)). This row lands before WI-922, which rebases onto it because both edit the hook and the pack.
  - Trunk's HEAD is the commit P5 rebased onto, which the entry names. If trunk moved, P5 runs again from step 1, gate included (R6).
- **Squash** `wi-921` on trunk with `git merge --squash`. The message cites the gate's round files by the names read from disk. It is one commit, or two if the lane recorded an owner overrule (recipes §3: the squash up to the commit before the close, then the close). Either way the armed step judges the landing on trunk against HEAD. It compares trunk's claim copy with the closed copy; the Done-when is unchanged, or blessed in the lane and carried in the squash, so the landing passes.
- **Regenerate** with `trunk_step.py --regen` (by hand: `gen_arch_map.py` with `--src`, and `docs/ratify/CURRENT.md`). This writes `docs/interface-reference.md` (IF-286's and IF-080's contract text), `docs/cli-reference.md` (the `done-when-hold` help line), the components view if LLR text moved, the review rollup and the other trunk-only views. Nothing authored is added.
- **The bar on the landing tip (D12)**, on the staged landing, before the commit (recipes §6):
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's, or none once WI-914 has landed;
  - `trace.py --strict-integrity` on the staged squash (recipes §3);
  - `check_complexity.py --mode enforce` on the merged tree.
- **After the commit.**
  - Archive the tips to `archive/lanes`, with any rewound close as an extra parent.
  - Sweep: `intake.py sweep --merged "WI-921" --branch wi-921 --before <trunk before> --after <landing>`.
  - Close the re-mint citing the act.

## Interfaces, components and runtime flows

- **Interfaces** (`docs/requirements/interfaces.toml`):
  - **IF-286** (`kitlib/done_when`, CMP-008): the contract text gains the trunk arm, the failed-read hold and `staged_closes`' `(closes, why)` return (P1). The row is Drafted, and its cells and `v1` stay.
  - **IF-080** (`integrate`): the contract text and the help line widen `done-when-hold`'s refusal (P1).
  - **IF-154**: the argv is unchanged (`done-when-hold` takes no arguments).
  - **IF-242**: `items` and `changes` are read unchanged.
  - **IF-040** (check to hook) and **IF-134** (git to hook): the contracts are unchanged, and the floor list they carry gains one name (P2).
  - **IF-267**: unchanged. `--path-triggered` runs no built-in step, because `extra_steps` refuses a `[step:]` that shadows one.

  No IF row is added and no seam is proposed.
- **Components** (`docs/requirements/components.toml`): CMP-007 (W2 Gatekeeper: the hook and `check.py`) holds the floor and the census's subject. CMP-008 (W3 Autonomy: `integrate` and `kitlib`) holds the reader. No component is added or split.
- **Runtime flows** (`docs/runtime-flows.md`): Flow 3 draws the secrets and privacy floor at commit and push, and Flow 4 draws the station cycle. Neither draws the batched floor's step list or the Done-when hold, so no flow changes, and the flows' SR and LLR citations stay valid.

## Calls this plan makes that the spec does not settle

These are for the lane's decisions record, for the owner to confirm or overrule.

- **C1. Off a git work tree the step judges nothing.** This follows the sibling index steps, so a full `check.py` run outside a checkout stays green. `tests/test_check_harness.py::test_minimal_project_is_green` runs the full plan in a non-git scaffold, and the RESYNC promise that nothing changes for a non-claiming repository depends on this. Inside a work tree, every read that fails holds. The residue: a repository so broken that git cannot locate it reads as off-git, and git cannot make a commit there either.
- **C2. The trunk arm judges only a claim copy the parent holds**: any entry other than a lone `A`. A new claim copy has nothing to compare against, and an unborn HEAD lists only `A` entries.
- **C3. A trunk commit that removes a claim copy without closing it holds.** It has no copy, which is LLR-307's existing rule, and no blessing releases it. The sanctioned path is a terminal close, and the kit has no un-claim flow.
- **C4. The reader and the choice of reading live in `kitlib.done_when`**, the owner of IF-286. `integrate` passes in what `agent_common` owns. `staged_closes` stays as the closes of the one reading, and its return gains the failure reason, `(closes, why)`:
  - retiring it would strand WI-922's named reader;
  - keeping its list-only return would let a caller read an unreadable delta as "no close".

  The shared-predicate pin follows the delegation. LLR-307's sentence naming `staged_closes` stays true, and the failed read it now reports goes to the D11 sitting (P4).
- **C5. One hook-line helper lives in `tests/conftest.py`**, and both new test sets use it. The seven existing readers of the floor line, in `test_plan_gate`, `test_pre_commit_hook` (two), `test_generated_freshness_census`, `test_integrate_admission`, `test_ruling_sync` and `test_text_then_act`, are left alone. They are a consolidation candidate to surface, not fix here, and `test_plan_gate.py` is WI-922's file.
- **C6. The census gets its own smoke module.** TC-019's existing evidence module, `tests/test_pre_commit_hook.py`, is in `SLOW_MODULES`.
- **C7. The close is a lane commit, made before the final gate (F1).**
  - session-protocol §4 and `PROCESS_OPTIONS.md` ("The LLM-gate verdict protocol") order the close before the final verdict round.
  - coordinator-cycle §4 step 3 lists "close the row" among the landing's trunk steps, and WI-913 closed on trunk after its gate.
  - This lane follows the first, so SR-156's reviewed tip is the tree that lands. The cost is that a gate finding rewinds the close (R6).

## Risks

- **R1. SR-156's acceptance leaves "the change's own commit" unheld, and LLR-309 says the commit that changes Done-when text is not held.** A trunk amendment's own commit is now held. P4 puts both texts to the sitting, and the sitting rules whether they need amending.
- **R2. `ruling-sync` and the trunk arm now act on the same commit.** `ruling-sync` requires a commit that rules an open item to update the Done-when of every open row citing it, claimed rows included. On trunk, that update to a claimed row now also owes a blessing in the same commit: an owner-confirmed `done_when` digest entry. No claimed row cites an open item today (every claimed row's `needs` names WI ids only). The coordinator records this at close-out.
- **R3. A `spec_move` relink that rewrites a link inside a claimed row's Done-when reads as a Done-when change on trunk.** It is held like any other, as S3's "a Done-when change without a close", and the builder does not special-case it. Bookkeeping commits (a claim, a mint) are made with `commit-tree`, so the hook never sees them. The case arises only from a hand close whose relink reaches another claimed row and is carried onto trunk.
- **R4. The new D2, D4 and D5 tests live in a module the smoke bar never runs.** The builder runs the touched slow modules every round, and the full suite runs once on P5's tip, before the gate.
- **R5. `integrate.py`'s size baseline is exact-match.** It is re-stamped in the same commit that moves its SLOC.
- **R6. The gate is taken on a closed tip.**
  - A gate finding after the close rewinds the close (P5).
  - Trunk moving between the gate and the landing repeats P5, gate included, because the anchor and the rebase change the gated tree.
  - So the coordinator takes the gate only when this row is next to land.
- **R7. The smoke tier's membership ceiling is close.** `docs/stack.ini` declares `max-tests = 2600`, and WI-913's landing (`b803dd019`) recorded 2588 passed and 2 skipped. This row adds five in-process tests: P1's classifier pin, and P2's census with its three fault cases. If another landing takes the tier past the ceiling first, the ceiling is re-stamped deliberately with its reason (session-protocol §2; recipes §4). No test moves out of the tier to make room.

## Excluded TCs

Excludes: TC-327; TC-257; TC-205; TC-131; TC-132; TC-139; TC-144; TC-145; TC-317 — they verify arms this row does not change (the done-when and combined brief composition, the review-scope Done-when flags, the verdict record, the pause, the merge slot and its claims, spec moves, dispatch, and the blackout guard), and they run unchanged in the full suite on P5's tip, before the gate.

## Not in this plan

These are coordinator close-out records under coordinator-cycle §6:

- The last bullet of the coordinator-cycle recipes §6 says WI-841's `done-when-blessed` "has the same gap". That goes stale here, because the census now enforces the classification for any new built-in step.
- D-003's consequence for a trunk amendment of a claimed row's Done-when (R2 above) has no skill text yet.
- coordinator-cycle §4 step 3 lists "close the row" after the squash, while session-protocol §4 and the verdict protocol put the close before the final verdict round (C7). Reconciling the skill's text is a close-out correction.
- WI-922's lane should read `staged_closes`' new `(closes, why)` return once it rebases onto this landing. The coordinator names it in WI-922's planner and build briefs.

Findings surfaced, not fixed here:

- `PROCESS.md` §4 states the Done-when hold for a lane's own edit only. The trunk arm is stated in the RESYNC entry and in D-003, not there. `PROCESS.md` is byte-budgeted and the spec does not name it.
- `agent_common.trunk_name` ignores the exit code of its `git branch --show-current` fallback. Off git, it returns git's error text as the branch name. This row's reader judges nothing off git, and reads the trunk's name only for a listed change, after its own branch read has succeeded, so the step is unaffected.
