# WI-925 adjudication 004: amendment of six rows and first approval of LLR-339 and TC-369

I judged the lane at `6c9ac8ffa` against the anchor in `docs/archive/last_approved`. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The diff:** I loaded both registries with `tomllib`. Since the anchor, the LLR registry moved in LLR-145 (its `code_symbol` trace cell only, so not under judgement), LLR-208, LLR-307 and LLR-337, and gained LLR-339. The TC registry moved in TC-206, TC-325 and TC-367, and gained TC-369.
  - LLR-337's `detail` and every amended TC cell keep the anchored text as an exact prefix.
  - LLR-208 rewrites one parenthesis.
  - LLR-307 rewrites its staged-close and residue sentences, and adds two.
- **Tests:** every test the six TCs cite exists. I ran each test newly cited by TC-206, TC-325, TC-367 and TC-369, plus `tests/test_spec_move.py::test_exact_relink_is_the_rituals_bytes_and_nothing_else`: 37 passed.
- **The code each row describes:**
  - the trunk reader (`trunk_name`) reads the declaration alone and refuses four shapes naming it;
  - the scaffold writes the declaration only into a policy file it created;
  - the plan gate's claim base falls back to HEAD only where HEAD holds no claim folder;
  - the relink exemption takes only a lone modification judged by the one shared byte-exact oracle;
  - the shipped `pre-commit` hook's `done-when-blessed` comment states the promise and one residue list: seven fail-open routes and two fail-closed shapes. The WI-925 resync entry points at that list rather than restating it.

## amendment

- [MEANING+BLESS] LLR-337 Detail -> the single-plan gate reads the lane's claimed rows at its claim base, with no case for an undeclared trunk -> the same, plus: with the trunk undeclared, a branch whose HEAD holds no claim folder is judged at HEAD, and any other branch is refused naming the declaration -> a new refusal and a new base rule. A gate that guessed a base when the declaration was missing satisfied the old text and fails the new one. **Blessed.**
  - It fails closed wherever the claim base needs the trunk.
  - It refuses nothing that never needed the trunk.
  - SR-154's gate is unchanged in every other respect.
- [MEANING+BLESS] TC-367 Expected and Method -> verify the gate's arms -> it adds the undeclared-trunk clause, and two named tests in `tests/test_plan_gate.py`, which its Evidence now cites -> a new verification obligation. **Blessed.**
  - One test asserts a claimed single lane gets one hold naming the declaration.
  - The other asserts a branch with no claim folder answers the same with the declaration removed as with it present.
- [MEANING+BLESS] LLR-307 Detail -> the staged reader judged any non-addition entry for a claim copy as a change. It read the trunk as the primary checkout's branch, so a linked worktree on the integration branch read as elsewhere, and it stated the amend, cherry-pick, revert, rebase, merge, hand fast-forward and linked-worktree residues in the row -> it adds four things and moves one:
  - an exact inbound redirect, caused by another spec's same-delta move into a terminal home, is not a change, while any other modification, an unreadable blob or bytes that are not UTF-8 is a change;
  - the declared trunk is judged as trunk in any worktree;
  - an undeclared trunk holds every listed claim-copy change, and a delta listing none never reads it;
  - the deleted close listing's sentence is dropped;
  - the residue moves to one home, the shipped hook's `done-when-blessed` comment.

  -> the behaviour changed: an exempt case was added, a fail-open residue was closed, and a new refusal was added. **Blessed.**
  - **Upward:** SR-156 holds a lane's own change to a claimed Done-when. A redirect written by another row's close is not the lane's change, and the exemption admits only the ritual's exact bytes. Everything else still holds, as plan-dispute F1's ruling (sitting 001) expected.
  - **The worktree residue is closed, not restated.**
  - **The unreadable staged-change hold that the dropped sentence carried survives** in the row's own "unreadable staged change set ... holds" clause.
  - **Naming the hook comment as the residue's one home is within this tier's naming rule,** because the hook is a shipped boundary artifact. It also follows the kit's one-home rule.
  - **Names:** `staged_closes` leaves the row, and no new carrier enters it.
- [MEANING+BLESS] TC-325 Expected and Method -> verify the holds, the trunk-commit clause and quoted paths -> it adds the declared-trunk linked-worktree case, the same-delta exact relink (with the real-edit, no-move and cross-landing cases), the trunk deletion of a claim copy, the undeclared-trunk hold and its no-claim-copy pass, and an inspection of the hook's one residue list -> new verification obligations. **Blessed.**
  - Every named test exists in a file its Evidence cites, and the new ones pass.
  - I made the inspection myself: the hook states one list, and no other shipped text restates it. The older WI-921 resync entry records what that version shipped, and the WI-925 entry says it replaces it.
- [MEANING+BLESS] LLR-208 Detail -> a direct rollup write is refused off the trunk, read as the primary checkout's branch, so a single checkout is its own trunk -> it is refused off the declared trunk, in any worktree, and refused naming the declaration when the trunk is undeclared -> the actor test changed: a single checkout on a work branch could write before and is refused now, and a linked worktree on the trunk while the primary checkout is elsewhere is allowed now. **Blessed.**
  - It tightens toward SR-170's "never by a work branch".
  - The `--trunk-step` and `--check` exemptions are verbatim.
  - The names it keeps (`_off_trunk_refusal`, `agent_common.trunk_name`) were in the approved text. The amendment adds none.
- [MEANING+BLESS] TC-206 Expected and Method -> verify the rollup's freshness, its two answers and the exclusive writer -> it adds that a linked worktree on the declared trunk writes while a work branch is refused, and that an undeclared trunk refuses the write naming the declaration -> new verification obligations. **Blessed.**
  - `test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can` drives the on-trunk linked worktree writing with the primary checkout on another branch.
  - `test_an_undeclared_trunk_refuses_each_caller_naming_the_key`, now cited, drives the rollup write's refusal.

VERDICT: MEANING rows=6

**For the later act turn:** all six rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-337, TC-367, LLR-307, TC-325, LLR-208 and TC-206. No row is held, and no row is returned.

**Advisories, not blocking:**
1. **TC-206's Method** keeps its approved sentence that the single-checkout fixtures "are their own trunk ... which is why the refusal had to be driven through a real linked worktree to be driven at all". Under the declared trunk, those fixtures write because they sit on the declared trunk, and a single checkout on a work branch would now be refused too. A later edit could restate that rationale.
2. **LLR-307's non-UTF-8 and unreadable-blob arms** are the shared oracle's. They are held by `test_exact_relink_is_the_rituals_bytes_and_nothing_else`, in a file TC-139 cites, not by a clause of TC-325.
3. **LLR-309 still says "the commit-time base and its owner-ruled residues are stated by LLR-307".** LLR-307 now states where they live, so the pointer still resolves, but through one more hop.

## first-approval

- [APPROVE] LLR-339 -> the integration branch is one declaration in the policy home:
  - a checkout on that branch is trunk, primary or linked;
  - the trunk is never inferred from the current branch;
  - an absent, non-text, empty or non-local declaration is refused naming it by every reader that judges or writes against the trunk;
  - with the trunk undeclared, step selection reads the change as unknown and runs every opted-in step, the readability report skips each measure naming the declaration, and the preflight keeps its guard;
  - a scaffold declares its own branch only in a policy file it created (in an unborn repository, the branch git will create), and otherwise keeps the template and names the line;
  - a lane's base is its merge base with the declared trunk.

  -> its chain:
  - **Upward:** SR-156's serial seam and lanes are defined against "the integration branch". This row gives that branch one identity, and its absence fails closed.
  - **Sideways:** LLR-307, LLR-337 and LLR-208 each state only their own reader's specialization (a reader refuses only when it needs the trunk). The step-selection degradation agrees with the trigger row's "unknown changes run them".
  - **Downward:** TC-369 verifies every arm.

  -> ready. It is a closed, observable contract: no carrier is named, there is no `shall`, and it fails closed. The trace cells are filled.
- [APPROVE] TC-369 -> verify:
  - the reader consults neither the checkout nor the worktree list;
  - each undeclared shape is refused naming the declaration, at every trunk reader;
  - the three degradations;
  - the scaffold's created-file-only declaration, including the unborn, no-repository and detached cases;
  - linked-worktree trunk identity;
  - no refusal for a change with no claim copy.

  -> its chain:
  - All 15 cited tests exist across nine files, and all pass.
  - It cites `test_default_base_keeps_the_trunk_boundary_after_a_single_checkout_resume` for the lane-base arm.
  - `Tier = Full` is correct, because `test_bootstrap` is in `SLOW_MODULES`.

  -> ready. It claims nothing its evidence does not carry. **Advisory:** its Expected never states the lane-base arm in words; only the Method's cited test holds it. A later edit could add "a lane's integration base is its merge base with the declared trunk, in a single checkout as in a linked worktree".

OUTCOME: APPROVE rows=2

**For the later act turn:** flip LLR-339 and TC-369 from `Drafted` to `Approved` and anchor their copies. Neither rung is held.

SITTING: JUDGED kinds=amendment;first-approval
