Reviewed: 2bb01681c4a75ea1768717eb21ddb7dad686b695

Verified. `git rev-parse HEAD` printed 2bb01681c4a75ea1768717eb21ddb7dad686b695. I ran the review in the convergence stance. I read no earlier verdict, no decision record, no lane log and no lane commit message.

Failure classes hunted first:
- fail-open in the relink exemption (a real Done-when edit excused);
- fail-open from the trunk reader (a fallback left in place, or a caller that swallows the refusal);
- a TrunkUndeclared escaping as a traceback on a supported route;
- data loss in bootstrap (an adopter's process.toml rewritten).

None was found:
- `trunk_name` reads only `[policies] trunk` through `agent_policy.process_config`. That read answers `{}` on a malformed file, which is then refused as absent. The worktree-list, current-branch and worker fallbacks are deleted.
- I grepped every `trunk_name(`/`default_base(` caller in shipped and repo scripts: adjudicate_brief, agent_brief, agent_common.worker_base and stale_terminal_assignment, check, check_readability, gen_verdict_rollup, handback, integrate, plan_gate, review_brief, scripts/check_resync, scripts/coordinator/overnight_legs. Each one catches `TrunkUndeclared` (overnight_legs catches its `ValueError` base) and refuses or degrades as LLR-339 states.
- The relink exemption passes only:
  - a lone `M` of the claim copy;
  - whose index bytes are exactly `spec_move.expected_relink(HEAD bytes)`;
  - over a remap built from the same delta's `D` under `active/` plus exactly one closed-home `A` of the same WI;
  - and that is a non-empty rewrite.
  An unreadable blob, non-UTF-8 bytes, a second entry or no move all stay a change.
- `declare_scaffold_trunk` writes only into a process.toml this run created, so an adopter's file is never rewritten.
- `integrate._relinked_exactly`, `plan_gate.build_paths` and `kitlib.done_when.staged_hold` all call the one `spec_move.exact_relink`. The claim recognizer's only behavioural delta is the added non-empty-rewrite requirement, which no git-listed `M` with identical bytes reaches except a mode-only change.
- `staged_closes` is gone from every shipped file and test. The only remaining mentions are the generated `docs/interface-reference.md`, which is regenerated at landing, and archived plans and handoffs.
- The hook diff changes comment lines only.
- The RESYNC entry is anchored `[since 8d64910f2]`. It names the forced migration, the overwrite set and the deletion.

Red-before. I exported the tip tree to my scratch area and overlaid the base (8d64910f2) versions of every changed script and hook. The new tests then FAIL on the pre-fix code:
- the squash relink landing: held with "WI-802: its Done-when differs ... added since claim: 'Y ships after `[X](../../../archive/work/complete/WI-801-x.md)` lands.'". So deliverable 3 reproduces.
- the linked worktree on the declared trunk (verdict and ruling cases);
- the single checkout on `side`;
- each undeclared shape at every caller;
- the hold-by-rename text;
- every `test_trunk_name.py` case;
- the reviewer slot, which rendered `git diff side...`;
- the rollup's linked-worktree write;
- the bootstrap key;
- the config-check type.

The three hold-stays-held pins (a real edit beside the relink, a relink with no same-delta move, and the cross-landing reach) pass on both trees, which is what a guard against over-exemption should do.

Done-when map:
- **The trunk, declared:**
  - `test_a_linked_worktree_on_the_declared_trunk_holds_an_unblessed_done_when_change[verdict|ruling]`
  - `test_a_single_checkout_on_a_branch_not_named_for_its_claim_does_not_judge_a_non_close_change`
  - `test_an_undeclared_trunk_refuses_each_caller_naming_the_key[4 shapes]`: done-when step, preflight, reviewer prompt, rollup write, handback close
  - `test_a_commit_touching_no_claim_copy_is_not_refused_over_the_key`
  - plan_gate's two undeclared tests
  - `test_the_reviewer_prompts_trunk_slot_renders_the_declared_name`
  - `test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`
- **No fallbacks:** `test_the_reader_reads_no_worktree_list_and_no_current_branch` and `test_a_repository_with_the_key_reads_it_and_one_without_refuses`.
- **Scaffold and config:** `test_a_scaffold_declares_the_branch_it_was_scaffolded_on`, `test_a_non_string_trunk_is_refused_by_the_config_check` and `test_the_policy_home_declares_the_trunk_as_a_string`.
- **The relink:**
  - the reproduction pin: `test_a_squash_landing_that_relinks_another_claims_done_when_link_is_not_held`
  - the real-edit pin: `test_a_squash_landing_with_a_real_edit_beside_the_relink_is_held`
  - the no-move pin: `test_a_relink_with_no_move_in_the_same_delta_is_still_a_change`
  - C2: `test_a_relink_reaching_an_existing_lanes_claim_copy_across_the_landing`
  - the shared stage, checked by reading the code
  - unit pins: `test_exact_relink_is_the_rituals_bytes_and_nothing_else`
  - the claim recognizer's 4 relink tests in `tests/test_integrate.py` and the plan gate's existing tests are unchanged and pass.

  "Recorded in the lane's log" is not checked: the session notes are outside this reading scope.
- **The hook comment:** checked by reading `project-trajectory/hooks/pre-commit:276-329`. It states the promise and one list (7 fail-open, 2 fail-closed). The linked-worktree and single-checkout shapes are gone.
- **`staged_closes` gone:** checked by grep.
- **The hold-by-rename text:** `test_the_finding_names_a_recovery_the_trunk_floor_permits`, which is red at base.
- **Spine:**
  - LLR-307, LLR-208, LLR-339 + TC-369, TC-325, IF-179, IF-286, and the LLR-145/LLR-337 `code_symbol` cells are amended as listed.
  - SR-156, SR-170, SR-137, SR-019, LLR-309 and TC-326 are untouched.
  - K3: every new `Implements:` names an LLR whose module and `code_symbol` carry the function.
- **RESYNC_PACK.md:** carries the entry.
- **The bar:** `check_trajectory --strict` is clean and trace integrity=0. I did not run the smoke tier, as the brief directs.

Coverage-extension note (prose, no severity): the 24 env-gated posix-shell skips from the brief's run were re-run with `C:\Program Files\Git\bin` on PATH, and they pass.

Disclosure: `trace.py --strict-integrity` wrote its report to the worktree's `docs/test/report.md`. That file is git-ignored, and `git status --short` stayed clean.

Commands:
- `git rev-parse HEAD` -> 2bb01681c4a75ea1768717eb21ddb7dad686b695
- the brief's pytest selection (15 files, `-n 2`, `--basetemp .../opus/wi-925`) -> `567 passed, 25 skipped in 851.36s (0:14:11)` (24 env-gated posix-shell skips)
- `check_trajectory.py --strict` -> `check_trajectory: clean (947 work item(s), 834 done (88%), 30 cancelled, graph acyclic).` exit 0
- `trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=305 TC=319 orphans=0 integrity=0 verified-mechanized=124 verified-demonstrated=6 verified-attested=0 drafts=3 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=245 interface-findings=0 ac-advisories=1 paraphrase-advisories=3.` exit 0
- `pytest tests/test_integrate.py -k relink` -> `4 passed in 10.65s`
- with Git\bin on PATH: `pytest tests/test_done_when_blessing.py tests/test_step_path_trigger.py tests/test_check_resync.py tests/test_plan_gate.py` -> `194 passed in 254.50s`
- pre-fix overlay (tip tree, base scripts and hook), new WI-925 tests in done_when_blessing, holdban and trunk_name -> `16 failed, 6 passed in 25.34s` (each failure on the pre-fix behaviour; the 6 passes are the hold-stays-held and unrelated `-k` matches)
- pre-fix overlay, the reviewer slot, rollup, bootstrap, config, real-edit, no-move and cross-landing tests -> `4 failed, 3 passed in 15.86s` (the 3 passes are the hold-stays-held pins)

- [MINOR] docs/requirements/low-level-requirements.toml:3358 -> The detail cell of LLR-337 (Approved) gains a new sentence: "With the trunk undeclared, a branch whose HEAD holds no claim folder is judged at HEAD; any other branch is refused naming the declaration." The Approved TC-367 (docs/test/test-cases.toml:3547-3551) and TC-206 (docs/test/test-cases.toml:2108-2112) also gain method, expected and evidence text. WI-925's Done-when spine list grants LLR-337 only a `code_symbol` follow and names neither TC. The behaviour these cells record is real and the text is true, but per anchor K3 an approved row changes only where the spec grants it -> the concrete change: add LLR-337's detail and TC-206/TC-367 to the spec's spine list, or confirm that the lane's checkpoint sitting judged them explicitly, so that their re-attestation is on record -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3262 -> For clarity (K1). LLR-307's new bound sentence calls the hook's list "the routes outside the supported commit routes and the two fail-closed shapes within the supported routes". But project-trajectory/hooks/pre-commit:292-310 heads its seven items "Seven routes fail open", and three of them are not routes outside the supported ones: item 5 (git failing mid-commit inside an ordinary commit), item 6 (the mint's silent skip) and item 7 (a detached-HEAD commit) -> the concrete change: word the LLR sentence and the hook's heading as "fail-open shapes" (routes outside the promise plus the shapes inside it), so the bound and the list say the same thing -> @owner

VERDICT: APPROVE findings=2
