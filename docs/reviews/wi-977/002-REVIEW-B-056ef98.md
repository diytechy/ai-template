Reviewed: 056ef98d414bf37e357293bd569c9f0a2d8d74aa

**Verified.** Full-lane review of WI-977, 55fe67d82...056ef98d4, read under the brief's pathspec. I hunted three failure classes in order: a claim, close or resume that fails open on a multi-item or empty input; silent loss of an obligation from a requirement row; and a peel that admits an unreviewed close. The code side holds. `integrate.claim` refuses empty, separator-only, list-form and non-str input at its first rung (`_claim_input_refusal`), before the hooks rung, the guard and the lock. `integrate.main` normalizes and then refuses `;` and `""`. `agent_common.preflight` no longer skips an empty `--wi`, and `parse_wi_id` refuses lists, repeats and malformed ids. Both closes call `_the_one_claimed_spec` before resolving the lane. `_admit_parked` refuses a two-spec claim before `_pre_admit`, the cycle count and the launch. `_admission` has no batch arm, and every payload is a one-element list. `_closed_wi_ids` takes exactly one active deletion paired with exactly one complete addition. `claim_base` still reads a joined historical subject by its shape.

Red-before: I ran the lane's tests against the base scripts (base tree with HEAD's tests/). 18 of the new refusal tests fail there and 6 pass. The 6 are the intended characterizations (historical joined claim, single-report restore, the `;`/`WI-`/`wi-201` worker cases) plus the two-row no-peel test (finding below). Mutation: turning `close_adjudication`'s already-terminal no-op into a refusal is caught by `test_an_adjudication_close_moves_its_one_row`.

Done-when map:
- Admission: test_dispatch_admission no_kind_maps_to_a_batch_arm / first_spine_row_admits_alone, test_dispatch spine_rows_admit_one_per_exclusive_turn. COVERED.
- Claim: test_integrate multi_item_claim_refuses / empty_claim_refuses_before_the_lock. COVERED, red on base.
- Resume: test_dispatch parked_lane_claimed_with_two_specs_stops_the_run. COVERED.
- Worker and help: test_agent_loop_worker refuses_any_assignment_but_one_id / list_assignment_exits_preflight / wi_help_names_one_work_item. COVERED.
- Prompt: no_assignment_block_slot plus the golden one-row render. COVERED.
- Close: the two two_spec_claim tests in test_handback. COVERED.
- Peel: covered, but weakly (MINOR below).
- Claim subject and history readers: claim_subject_composes_one_id_only, historical_joined_claim_still_reads_as_a_claim (claim_base, loop_claimed, provenance). COVERED.
- Other readers' wording: read; OK.
- Text: PROCESS_OPTIONS paragraph gone, 199,839 -> 199,478 bytes, the byte-budget row matches. README, headers, runtime-flows and the concurrency-v2 §A4 note naming item 15: OK.
- RESYNC entry: present; test_resync_pack green.
- Spine "23 rows carry target meaning": NOT MET (three MAJORs below).
- "traced cells follow the code": NOT MET (MAJOR below).
- Checkpoint sitting: not yet held at this tip (plan W14).
- Generated pages: `docs/cli-reference.md`'s `--wi` row still reads the traincar list. It is trunk-owned under `[generated]`, so this is the landing's W15 regeneration, not a lane finding.

Requirement/interface counterparts, with my decision on each:
- IF-065: agent_common's contract text renames `parse_wi_list` to `parse_wi_id`. The row's data cell does not name the parser. Retain; the generated interface reference refreshes at the landing.
- IF-136: `spawn_worker` and `worker_argv` take one id instead of a list. The data cell states only the return shapes. Retain.
- IF-080: `claim --wi --branch` already names one value. Retain.
- IF-099: the WORKER template loses a slot. The data cell names the prompt set only. Retain.
- SR-026 -> LLR-061: the parent is unchanged and the child narrows to one id. Carried, but traced cells are stale (finding).
- SR-144 -> LLR-144 and LLR-161: SR-144 carried. Both children drop obligations (findings).
- SR-148 -> LLR-058, LLR-123, LLR-149, LLR-152: carried, except the lane-count ladder lost from LLR-149 (finding).
- SR-156 -> LLR-150 and LLR-151: carried, except content loss (finding).
- No decomposition is added.

Coverage-extension note (no severity): `dispatch._admit_parked`'s `(wi_id,) = wi_ids` (project-trajectory/scripts/dispatch.py:1093) raises an uncaught ValueError for a parked `active/<branch>/` that holds only a hand-made `WI-*.md` glob hit carrying no id. It fails closed (a traceback before any mutation) on input outside the declared set.

**Commands**
- `git rev-parse HEAD` -> `056ef98d414bf37e357293bd569c9f0a2d8d74aa`
- Brief's pytest set, first run: killed by the tool's time limit before printing a summary, no output.
- Brief's pytest set, rerun logged to reviewB/pytest-run2.log -> `738 passed, 1 skipped in 2136.61s (0:35:36)` (the skip is posix-shell gated)
- `check_trajectory.py --strict` -> `check_trajectory: clean (982 work item(s), 867 done (88%), 34 cancelled, graph acyclic).` exit 0
- `trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` exit 0
- HEAD tests against base scripts (`-k` over the new refusal tests) -> `18 failed, 6 passed in 55.93s`, then `-rA` on the 6 -> the PASSED list quoted above
- Mutant (`close_adjudication` no-op -> refusal), tests test_handback, test_consolidate_close, test_adoption_record, test_dispatch -> `1 failed, 132 passed in 567.38s`

- [MAJOR] docs/requirements/low-level-requirements.toml:1631 -> LLR-161's rewritten detail deletes H's adoption sentence ("A disposition that owes a successor drafts one or adopts an already-filed one that supersedes the disposed row"), which the spec says "stays". It also deletes three non-batch obligations that contract_split 961f9e47 kept: a terminal spec with no report is LOUD; a genuinely second close is a second report and so a second row; a complete close is spot-checked at the declared rate. TC-156 (docs/test/test-cases.toml:1560) still verifies the adoption and the loud-no-report arms, so the child verifies what its parent no longer states, and no other LLR now carries the adoption obligation (K1) -> restore those sentences in LLR-161, replacing only the "EVERY report this call wrote / multi-spec lane cannot half-close" clause and removing the code names (`close_partial`, `intake._close_drafts`) per ruling 5 -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:1487 -> The port compresses approved LLR-144/149/150/151/152 and TC-143/144/145/146 well beyond their batch clauses. It deletes obligations that contract_split (961f9e47) kept and puts non-durable pointers in their place ("retain their existing contracts", "retain their existing checks", "retain their existing coverage", "retain their existing assertions", "as before"), which after landing point at text that no longer exists. Examples:
  - The lane-count ladder (CLI > AGENT_LANES > stack.ini > 1, absent/malformed/sub-1 falling to serial) is no longer stated in any registry row.
  - LLR-150 drops the explicit forwarding of the launch's session dials and the refresh running as its own overlapping subprocess.
  - LLR-151 drops the lock taken at one site, "a hand claim during live lanes is unrepresentable" and `dispatch_lock_held`.
  - LLR-144 drops the quarantine's record-wise rename read and restore-on-revert-failure.
  - TC-146 drops the asserted `bar = DevStg-Tests -> --gate DevStg-Tests`, no-`--gate` and malformed-refusal arms. The spec allows only the batch clause to change in LLR-152 and TC-146 ("only that clause is replaced, in the same voice").
  (K1, K2) -> re-author each cell from CS's text (where the spec says "CS's meaning") or H's text (LLR-152, TC-146), replacing only the batch clauses and stripping code names, so every non-batch obligation stays stated in its row -> @owner
- [MAJOR] docs/test/test-cases.toml:647 -> TC-061's method still asserts behaviour this lane deleted: "a row whose `WI:` trailer is committed while its spec is still in active/<branch>/ reads `started, not closed`, never `built`, and stays the walk's next row until its spec leaves", and "the branch diff of an earlier assigned row". `assignment_block`, which rendered that state, is gone; `current_assignment_wi` returns the one row; the tests that drove both are deleted. The spec told this two-row arm ("the every-row block, the sibling read as `built`") to become the one-id refusal (K1). `agent_brief.lane_completion` (project-trajectory/scripts/agent_brief.py:1046) keeps this clause alive with no production reader -> delete the `started, not closed` / walk-next-row / earlier-assigned-row clauses from TC-061, and either delete `lane_completion` with its test or state in the TC the one-row completion read it still pins -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:640 -> At the reviewed tip the traced cells do not follow the code (Done-when "traced cells follow the code"; K3):
  - LLR-061's `code_symbol` still names the deleted `assignment_block`.
  - New functions carry `Implements:` tags whose LLR neither lists them in `code_symbol` nor names their file in `module`: `parse_wi_id` (agent_common.py:660 -> LLR-061, whose module lacks agent_common.py); `_buildable_wi` (agent_loop.py:1357 -> LLR-061); `_claim_input_refusal` (integrate.py:750 -> LLR-151); `_the_one_claimed_spec` (handback.py:361 -> LLR-144); `_stop_run` (dispatch.py:1053 -> LLR-143, code_symbol `run`).
  - LLR-150's detail now states the parked-resume refusal, but its module is lane.py only; the refusal lives in `dispatch._admit_parked`.
  `trace.py --strict-integrity` and `check_trajectory.py --strict` both pass clean, so no instrument catches this -> run plan step W14's traced-cell reconcile (drop `assignment_block`, add each new symbol and its file, and put the resume refusal under the LLR whose module is dispatch.py) before the landing is judged -> @owner
- [MINOR] docs/test/test-cases.toml:1366 -> TC-138's evidence went from the whole `tests/test_handback.py` to the two new refusal nodes. TC-156, TC-061 and TC-154 had their module evidence narrowed the same way. As a result, the methods' other arms name no evidence: the partial move, the quarantine rename and restore, loud-no-report, second-close, trailer DONE and Blocked-WI exits, and the red-TC census. The tests still exist, but the TC rows no longer cite them -> add the new nodes alongside the existing module evidence instead of replacing it (K1) -> @owner
- [MINOR] tests/test_verdict_record.py:2030 -> `test_a_mechanical_close_moving_two_rows_does_not_peel` passes against the pre-change scripts (driven: PASSED on base). Its fixture composes the close subject from the first row only (tests/test_verdict_record.py:1910, `ks.mechanical_close_subject(rows[0][0])`), so the old attestor refused it on a subject mismatch rather than reproducing the pre-change two-row peel. The test therefore never fails on the behaviour it retires -> for the `rows` arm, write the subject the retired writer composed literally (`adjudicate: WI-401, WI-402 -> complete/ (mechanical close)`), so the test is red on the pre-change peel and green only through the one-row clause -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:750 -> `_claim_input_refusal` repeats in intent `agent_common.parse_wi_id` (project-trajectory/scripts/agent_common.py:660). Both are "exactly one WI-### id" validators over the same `WI_TOKEN_RE`, but they treat whitespace and non-str input differently (one strips, the other fullmatches the raw value and type-checks). That is two homes for one input rule (PROCESS.md §3, consolidate) -> make one agent_common parser, with the claim's type refusal included, that both the claim's first rung and the worker preflight call, keeping the CLI's case normalization at its boundary -> @owner

VERDICT: CHANGES-REQUESTED findings=7
