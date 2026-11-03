Reviewed: e5ecf9d7c4b2892adda57e5cf73241562539af78

Verified. HEAD of the lane worktree is e5ecf9d7c4b2892adda57e5cf73241562539af78. I read the full-lane diff c6e982882...e5ecf9d7c (scope exclusions applied), the WI-978 spec with its S3 tables and Trust section, the rubric, and the cited registry rows (SR-174, LLR-362, LLR-363, TC-158, TC-401, TC-402, IF-101). Failure classes I hunted first: a landing that admits an unreserved id (fail-open), two reservations getting overlapping ranges, a fold or writer that drops a record or lowers a mark (silent wrong content or data loss), and a landing route that judges the wrong tree. What holds up:
- The compare-and-swap is real. It runs `update-ref <ref> <new> <old>`, and an empty old value means "the ref must not exist" on first use. A lost swap writes nothing; the test is driven across two lanes, both moved and first-use.
- Each range starts one above max(carrier mark, trunk committed mark).
- Reservations are refused for WI, OI and DP, and for a 0 or out-of-range count. Every refusal comes before any write.
- `carried()` hands a lane only the record-justified marks, so a trunk-space mark never reaches a lane.
- Committed records are read as a union over every baseline (HEAD, MERGE_HEAD and other parents). A dropped record is refused.
- `--bump-ids` and `--correct-mark` keep the records verbatim. A reservation line never parses as a correction.
- The landing sweep reads blobs by object id, so export-ignore cannot hide a registry. It covers every carrier space: the spine, the off-spine and frame registries, and SN all live under docs/requirements and docs/test.
- The refresh folds only when the watermark is the sole conflict.
- The hand-squash step computes a real three-way staged tree.
- The act ledger, `_record_act` and act tests are untouched.
- PROCESS.md §4 states keep-or-mint once; spine-questions §0 cites it in one line. The Terra prompt drafts from @RESERVED@ and no longer contains `--bump-ids`. Recipes §4 and SKILL §4 are updated in all three copies (pinned by test_prompts.py).
- SN and SR cells name no code file or function. LLR-362 and LLR-363 detail cells name none.

Done-when coverage:
- Reserve-verb table: tests/test_id_carrier.py, COUNT_REFUSALS, WI_REFUSALS and test_each_reserve_refusal_writes_nothing, plus the usage-error case.
- CAS, first use and lost race: tests/test_id_carrier_git.py, test_first_reservation_seeds_the_carrier_from_trunk and test_a_lost_race_refuses_with_nothing_written.
- Sequential, stale-base and post-correction disjointness: test_sequential_reservations_are_disjoint, test_stale_base_reservations_are_disjoint and test_a_reservation_after_a_ruled_correction_starts_above_it.
- Fold, clean and conflicted: test_the_fold_* and test_fold_ids_on_a_conflicted_watermark.
- Hand-raise rule and committed records: the test_id_watermark.py cases TC-158 lists.
- Landing table on both callers: test_the_slot_refuses_each_unreserved_landing and test_the_hand_squash_refuses_each_unreserved_landing, parametrized over REFUSED, plus the unreadable-claim rung tests and both code-only cases.
- Landing fold and refresh-conflict fold: test_the_slot_folds_a_carrier_moved_after_the_lanes_refresh, test_a_hand_squash_folds_a_carrier_moved_after_the_lanes_fold and test_a_refresh_conflicting_only_on_the_watermark_is_resolved_by_the_fold.
- Text items: tests/test_prompts.py.
- Not yet due at this commit (landing or sitting time; I count them as pending, not as findings):
  - The checkpoint sitting.
  - This row's own ids reserved through its verb: `refs/heads/id-carrier` does not exist yet, since `git rev-parse -q --verify refs/heads/id-carrier` exits 1, and docs/id-watermark carries no record for LLR 362-363 or TC 401-402.
  - The open lanes named at landing.
  - docs/cli-reference.md and docs/interface-reference.md regenerated on trunk. Both are declared [generated], and neither lists `--reserve-ids` yet.

Coverage-extension note (not a finding): `landing_lines` returns before the landing-only-record row when a landing adds no carrier-space id. A record that neither the carrier nor the parent holds therefore lands with a code-only lane. The only route to such a record is a hand edit, which is outside the threat model, so this is noted only.

Commands:
- `git rev-parse HEAD` -> e5ecf9d7c4b2892adda57e5cf73241562539af78
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2-978-B/wi-978 tests/test_id_watermark.py tests/test_id_carrier.py tests/test_id_carrier_git.py tests/test_id_landing.py tests/test_module_size_ratchet.py tests/test_held_status_git.py tests/test_import_layers.py tests/test_integrate_admission.py tests/test_integrate.py tests/test_plan_gate.py tests/test_pre_commit_hook.py tests/test_rejudge.py tests/test_prompts.py tests/test_adjudicate_brief.py tests/test_dogfood_sync.py tests/test_retire.py` -> `712 passed, 20 skipped in 1279.89s (0:21:19)`. 19 of the skips are the posix-shell environment gate, unsatisfied on this box.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (986 work item(s), 872 done (88%), 34 cancelled, graph acyclic).` (exit 0)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=329 TC=356 orphans=0 integrity=0 ...` (exit 0)
- Probe (outside the repo, review-tmp/.../probe/test_probe_978.py, built on the lane's own fixtures, KIT_LOOP_SESSION unset):
  - test_retire_landed_on_trunk_then_code_only_lane FAILS, refusal quoted in finding 1.
  - test_control_after_manual_refresh PASSES: the same lane lands once refreshed by hand.
  - test_squash_of_unclaimed_branch_without_carrier exits 1: `FAIL reserved-ids ... ids added (SR-006) but the landing's work item cannot be read from its claim (no claimed spec under docs/work/active/feature/ at HEAD)`.

Findings:
- [MAJOR] project-trajectory/scripts/integrate.py:3410 -> The slot's reserved-ids rung (`_reserved_id_refusal`, :3334-3346) compares the branch tip with trunk's tip. It runs in `_merge_refusal` BEFORE the pessimistic in-slot refresh, and is never re-run after it. So any id trunk deleted after the lane's base reads as "added" by the lane. Reproduced on the shipped path: lane wi-401 is code-only, and trunk later lost SR-003 (another lane's retire.py landing). `integrate_one` refused with: "SR-003 is added outside every reservation of WI-401 (no id carrier exists) — reserve it first with `trace.py --reserve-ids WI-401 SR=N`; nothing was merged". After a hand refresh the same lane lands. This is the slot's documented "second branch in a drain" sequence. It reaches every adopter running lanes, carrier or not, and its remedy points at a reservation that cannot help. Neither the spec ("added" = live in the landing tree, not in its FIRST PARENT) nor LLR-363 holds for the slot route (K1). -> Judge the tree that actually lands: run the rung after `_landing_ready` and the in-slot refresh, against the refreshed tip with trunk as its parent. Or read the lane's own delta, `merge-base(trunk, branch)..branch`, the way R1 (`_minted_id_refusal`) does. Add the retire-then-code-only case to tests/test_id_landing.py; it fails on this code. This changes the tree compared and adds no guard, so no unrepresentable clause is owed. -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:10271 -> "A trunk-only repository is unaffected: without a carrier nothing is folded and no landing adds an id it must reserve" is not true for an adopter who runs `git merge --squash` on any non-lane branch that adds registry rows. The shipped pre-commit `reserved-ids` step refuses that squash even with no carrier and no lanes: I drove it and quoted the result above. The behaviour matches the spec's unreadable-claim row, but the adopter-facing promise overstates it (K1). -> Name this forced change in the RESYNC entry: a local squash of an unclaimed branch that adds registry ids is now refused. Alternatively, scope the step to squashes of a claimed lane. -> @owner
- [MINOR] project-trajectory/scripts/id_carrier.py:469 -> Back-links point at the wrong LLR (K3):
  - `landing_lines`, `_outside_lines`, `landing_refusal`, `_added_ids`, `ids_at` and `rev_fold_lag` (id_carrier.py:447-590) carry `Implements: SR-174, LLR-362`, but they implement LLR-363, the landing. LLR-363's `module` omits id_carrier.py, and `landing_lines` sits in LLR-362's `code_symbol`.
  - `kitlib.git.write_blobs` (project-trajectory/scripts/kitlib/git.py:437) is tagged `SR-166, LLR-181`, rejudge's row, though its only caller is the landing sweep.
  - Many tagged functions are in no `code_symbol`, for example `reserve`, `carried`, `record_history_findings`, `committed_reservations`, `reserve_ids` and `live_ids`.
  -> Retag the landing functions to LLR-363 and add id_carrier.py to its `module`. Tag `write_blobs` to LLR-363. Complete both `code_symbol` cells at the checkpoint reconcile. -> @owner
- [MINOR] docs/requirements/interfaces.toml:1388 -> IF-101's `data` names a `fold_ids` call. The seam's call is `fold_watermark`; `--fold-ids` is only the CLI flag (K1). -> Name `fold_watermark`. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:995 -> For clarity. SR-174's title still reads "Work-item identity is allocated once and never re-issued", but the amended requirement now governs registry identities drawn from the reservation record too. Its new rationale sentence also records a review activity ("The keep-or-mint review checks LLR-153, ...") rather than a reason (K1). -> Retitle it to cover both halves, for example "Each minted identity is allocated once and never re-issued", and move the cross-reference record to the lane's decisions. -> @owner
- [MINOR] project-trajectory/scripts/check.py:2052 -> `_squash_work_items` re-implements "the WI ids a lane's claim folder holds". It parses `WI-<n>-*.md` names under `docs/work/active/<lane>/` at a revision, the same parse `integrate._claimed_specs`/`_spec_id` (integrate.py:999-1014) owns for the working tree. `id_carrier._claimed` (id_carrier.py:360) is a third claim-folder reader added by this diff. This repeats an existing reader (PROCESS.md §3, "Consolidate, don't duplicate"). -> Put one claim-folder reader at a tree-ish beside `kitlib.git.claimed_work_branch`, and have the squash step, the slot and the reserve verb call it. -> @owner
- [MINOR] project-trajectory/scripts/kitlib/git.py:371 -> `extract_paths` was lifted out of rejudge.py into kitlib.git, but rejudge.py stays its only caller. The landing that motivated the lift now uses `write_blobs`. What remains is a move unrelated to WI-978 that adds rejudge.py to the adopter's RESYNC overwrite list. -> Revert the lift (keep `_archive_chunk` in rejudge.py), or justify keeping it in the lane's record. -> @owner

VERDICT: CHANGES-REQUESTED findings=7
