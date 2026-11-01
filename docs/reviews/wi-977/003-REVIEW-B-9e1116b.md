Reviewed: 9e1116bd778ca19e640b80fa133c29f9a8724b5c

Full-lane independent review of WI-977 (one work item per lane), range 55fe67d825ca7083dd349c0a3980c04d0d2afe7b...9e1116bd778ca19e640b80fa133c29f9a8724b5c, rubric docs/rubrics/kit-change-review.md.

## Verified

The checkout is the reviewed commit (`git rev-parse HEAD` printed 9e1116bd778ca19e640b80fa133c29f9a8724b5c). Failure classes I hunted first, worst first: (1) fail-open claim or close on an empty or multi-item input, (2) a close or peel that moves, or skips reviewing, more than the one claimed row (data loss or an unreviewed peel), (3) silent wrong content in the Approved spine rows this lane rewrites.

The retirement code holds up:
- Admission has no `batch` arm. Spine rows take `exclusive`, and `_admission` returns one id per assignment. `_claim_lanes` unpacks `(wi_id,)`, so a wider assignment cannot reach a claim.
- The claim's first rung is `_claim_input_refusal` → `ac.parse_wi_id`. It refuses before the hooks rung, the guard, the lock and any write. The CLI's `normalize_wi_id` keeps a joined value joined, so `parse_wi_id` refuses it.
- The worker's `--wi` goes through `type=str.strip` and is read by presence, so an empty `--wi` is a refused assignment, not a drive launch.
- Both closes call `_the_one_claimed_spec` before `_lane`, any report, residue commit or move.
- The peel's `_closed_wi_ids` needs exactly one active/ deletion paired with the same complete/ addition. `mechanical_close` composes through the one-id subject.
- `claim_base` still reads a historical joined subject through its own shape test.

Red-before check: I overlaid the base's `project-trajectory/scripts` on a tip export in my scratch directory and ran the new refusal tests. 18 failed on base, including `test_an_empty_claim_refuses_before_the_lock`, where base `integrate.main(["claim","--wi",";",...])` returned 0. That confirms the empty-claim fail-open was live and is now closed. Also red on base: `test_a_parked_lane_claimed_with_two_specs_stops_the_run` (base relaunched `('wi-401', ['WI-401','WI-402'])`), `test_a_partial_close_of_a_two_spec_claim_refuses_before_any_report` (base closed both), `test_a_mechanical_close_moving_two_rows_does_not_peel`, and the worker `--wi` list and empty cases. `test_a_historical_joined_claim_still_reads_as_a_claim` passes on both sides, as a preserved-behaviour pin should.

Done-when coverage:

| Done-when item | Covering test(s) |
|---|---|
| Admission | `test_no_kind_maps_to_a_batch_arm`, `test_lanes_back_in_the_station_the_first_spine_row_admits_alone`, `test_spine_rows_admit_one_per_exclusive_turn` |
| Claim | `test_a_multi_item_claim_refuses_before_any_state_change`, `test_an_empty_claim_refuses_before_the_lock` |
| Resume | `test_a_parked_lane_claimed_with_two_specs_stops_the_run` |
| Worker | `test_the_worker_refuses_any_assignment_but_one_id`, `test_a_list_assignment_exits_preflight_before_a_provider_launches`, `test_the_wi_help_names_one_work_item`, `test_an_explicit_empty_assignment_is_refused_not_driven` |
| Prompt | `test_the_worker_template_has_no_assignment_block_slot`, `test_the_one_row_prompt_renders_as_today` |
| Close | the two two-spec close tests, `test_a_partial_close_restores_the_single_report_after_move_refusal`, `test_a_partial_close_with_every_row_already_terminal_is_a_no_op` |
| Peel | `test_a_mechanical_close_moving_two_rows_does_not_peel` |
| History readers | `test_a_historical_joined_claim_still_reads_as_a_claim` |
| Refresh bar | `test_a_lane_whose_one_row_is_ordinary_runs_the_bar` |
| RESYNC entry | present; supersede pointers added to both older entries |

Other checks:
- **PROCESS_OPTIONS.md byte restamp:** correct. Measured 199,839 → 199,478 = -361, matching the restamp.
- **SR-144, SR-148 and SR-156:** they carry their target meaning, keep the H text the spec says stays, and name no carrier (K2 holds).
- **Generated pages:** `docs/cli-reference.md` (the `--wi` row) and `docs/interface-reference.md` (IF-065, IF-136) are stale on the lane. I regenerated both into scratch copies, and the only differences are this lane's docstring and help edits; the CLI reference is fresh at base. The plan (W15) and the trunk step's REGEN_STEPS regenerate both at the refresh and at landing, and the brief allows a lane not to carry them, so this is not a finding. The landing must carry them.
- **Coverage-extension note (no severity):** `_parked_branches` admits a claim directory holding any `WI-*.md` glob hit, while `_claimed_wi_ids` drops a name with no parseable id. Such a hand-made directory reaches `(wi_id,) = wi_ids` at project-trajectory/scripts/dispatch.py:1093 with an empty list and raises ValueError. It fails closed (a traceback before any launch or mutation), and the input is outside the spec's declared set.

## Commands

- `git rev-parse HEAD` → `9e1116bd778ca19e640b80fa133c29f9a8724b5c`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2B/wi-977 <the brief's 15 test files>` → `743 passed, 1 skipped in 1236.60s (0:20:36)` (1 skip is the environment-gated posix-shell case)
- `python project-trajectory/scripts/check_trajectory.py --strict` → `check_trajectory: clean (982 work item(s), 867 done (88%), 34 cancelled, graph acyclic).` (exit 0)
- `python project-trajectory/scripts/trace.py --strict-integrity` → `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md` (exit 0)
- `python project-trajectory/scripts/gen_arch_map.py --src project-trajectory/scripts --cli-doc docs/cli-reference.md --check` → `CLI reference STALE` at tip (`CLI reference up to date.` on a base export); `--contracts-doc docs/interface-reference.md --check` → `Interface reference STALE` at tip. Regenerated into scratch copies; the diff is only the `--wi` row, IF-065 and IF-136.
- Red-before run: the tip's tests over the base's scripts in a scratch export, 24 selected new tests → `18 failed, 6 passed in 59.19s`
- `git show 961f9e47:<registry>` for `contract_split`'s LLR-061, 144, 149, 151, 152 and 161 and TC-145, to compare the target meaning

## Findings

- [MAJOR] docs/requirements/low-level-requirements.toml:1528 -> K1/K3: the whole-cell restatements of six Approved LLRs (LLR-061:641, LLR-144:1432, LLR-149:1492, LLR-151:1516, LLR-152:1528, LLR-161:1637) delete obligations the spec says stay. They replace those obligations with pointers to text the same edit deleted ("retain their existing contracts", "retains its existing red-bar recovery contract", "retains its existing one-branch refresh behavior"). The spec allows replacing only the batch clause in LLR-152 ("only that clause is replaced ... the rest of the cell waits for item 5's migration"). It keeps "H's lock and bookkeeping-commit meaning" in LLR-151 and "H's adoption sentence" in LLR-161. What was lost:
  - LLR-152 lost the rank-1-without-renumbering slot, the no-bar refresh still committing a verified attestation, and the bar key's handoff to the gate.
  - LLR-151 lost "the claim REQUIRES the dispatch lock, acquired at one site; a hand claim during live lanes is unrepresentable".
  - LLR-161 lost the adoption sentence ("drafts one or adopts an already-filed one that supersedes the disposed row"), the report-path title and the loud no-report rule.
  - LLR-149 lost the lane-count ladder precedence and the gap-census sources.
  - LLR-144 lost the quarantine contract (records-not-pairs diff read, every return code checked, restore on a failed revert).
  - LLR-061 lost the collision-safe per-assignment logs, "a worker branch never edits root status, another branch's claims, the root log or generated artifacts", the branch-diff and rework-finding prompt inputs, and the blocked-trailer channel. TC-061 still verifies all of these.

  `contract_split`'s cells (961f9e47) keep every one of these. The 23-row Done-when ("carry their target meaning") is therefore unmet, and the checkpoint sitting would approve a weaker spine than the one it inherits. -> Re-author each cell from its H text with only the batch clause replaced, stating the kept obligations in capability voice, not as "existing contract" pointers (ruling 5 bars naming code, not stating meaning), then re-run the checkpoint sitting on the corrected cells -> @owner
- [MAJOR] docs/test/test-cases.toml:1439 -> K1/K3: the TC methods restated in this lane delete verification obligations the same way. TC-145 says "H's text stays; its batch-claim arm becomes CS's", but the new method keeps none of H's assertions. It drops the dispatch-lock refusal naming the lock, dispatch_lock_held proceeding, the abandoned-claim re-cut, the minted-id rung and the scratch-worktree isolation arms, keeping only "Drive the dispatch-lock, dirty-path, relink, bookkeeping and checkout-isolation arms as before". TC-146 (1450) is "single-WI part only" in the spec, but it is rewritten whole and loses "bar = DevStg-Tests reaches check.py as --gate DevStg-Tests (asserted off the recording stub's own argv), an undeclared bar passes no --gate". TC-143 (1417) and TC-144 (1428) replace the lanes-ladder, gap-census, NEEDS-HUMAN handback, red-refresh quarantine and pause/stall/crash-resume assertions with "retain their existing checks/coverage". After this lane no TC states what those tests must assert, so a later edit can weaken them with nothing in the spine to hold it to. -> Restore each method's H text and replace only its batch arm, as the spec's per-row instructions say -> @owner
- [MINOR] docs/test/test-cases.toml:647 -> K1: TC-061's method still asserts that "a row whose `WI:` trailer is committed while its spec is still in active/<branch>/ reads `started, not closed`, never `built`, and stays the walk's next row until its spec leaves". No code renders `started, not closed` any more (grep over project-trajectory/ and tests/ is empty), and the walk no longer exists: `current_assignment_wi` returns `worker["assigned"][0]`. The tests that drove the clause were deleted in this range (`test_a_built_but_unclosed_row_is_still_the_walks_next_row`, `test_the_brief_never_calls_an_unclosed_row_built`). The predicate behind it, `agent_brief.lane_completion` (project-trajectory/scripts/agent_brief.py:1046), now has no production caller, only `test_the_false_partial_class_turns_only_on_the_close_ritual`. -> Drop the `started, not closed` and walk's-next-row clause from TC-061 (it was the batch block's vocabulary). Then either delete `lane_completion` and its re-export, or give it the one production reader the spec's "two-part completion predicate the walk reads" still promises. A deleted path is the unrepresentable form here; no guard is added -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:640 -> K3: traced cells do not follow the code (a Done-when item). LLR-061's `code_symbol` still names the deleted `assignment_block`. Five new functions carry `Implements:` tags their LLR's `module`/`code_symbol` do not list:
  - `parse_wi_id` (project-trajectory/scripts/agent_common.py:660) implements LLR-061, whose `module` does not include agent_common.py.
  - `_buildable_wi` (agent_loop.py:1360) implements LLR-061.
  - `_the_one_claimed_spec` (handback.py:361) implements LLR-144.
  - `_claim_input_refusal` (integrate.py:750) implements LLR-151.
  - `_stop_run` (dispatch.py:1053) implements LLR-143, whose `code_symbol` is only `run`.

  `trace.py --strict-integrity` is clean, so no instrument catches this. -> Update the five LLRs' `module`/`code_symbol` cells to the built symbols (plan step W14 names this work, but the reviewed tip does not carry it) -> @owner

VERDICT: CHANGES-REQUESTED findings=4
