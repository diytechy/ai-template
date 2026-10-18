Reviewed: 8c1a9fce772c2ff53291c3943f3bc09b3fffc0d9

**Verified.** `git rev-parse HEAD` in the lane printed the reviewed commit. Failure classes hunted first, worst first: (1) fail-open, meaning the act turn reports success while an authorized act is still owed, or the act derivation lists an act no verdict authorizes (a RETURN row, an unblessed or held MEANING row, a held APPROVE row); (2) silent wrong content, meaning a wrong `--approves`/`--reattests` scope or a missing `--verdict` on a held-rung re-attest; (3) data loss or a stuck lane on an interrupted act.

I read `adjudicate_act.py` in full, plus the diffs of `coordinator_adjudicate.py`, `adjudicate_brief.py`, `kitlib/verdict.py`, `prompts.py`, `bootstrap_manifest.py`, the four briefs, the skill, `PROCESS_OPTIONS.md`, `RESYNC_PACK.md` and the spine rows. Then I drove the real assembler on real git fixtures with my own probes, under the scratch `probe/`:

- A combined verdict whose CLARITY re-attest and APPROVE flip share ONE registry lists both parts. After the real `copy_live --reattests` it lists only the first-approval part, and after the flip plus `copy_live --approves` it owes nothing. `left_owed` is None.
- A verdict with a held-rung CLARITY SR row and a released-rung `[MEANING+BLESS]` LLR row, on `DevStg-Reqs`, renders one `--reattests SR-001,LLR-001 --verdict <path>` command. On every tighter dial the blessed MEANING row drops out and `--verdict` stays.
- I checked the merge slot's per-row held filter (`acceptance_record._held_act_lines`) and the per-row `unaccepted_refusal`. Both admit that mixed command, so it is not refused at the merge.
- `git_out` does not strip, so `_status_paths`' `line[3:]` is sound. `git status` honours `.gitignore` (`out/`), so the recipe's background run does not dirty the lane.
- `ksitting.accepted_at` is the one reader. Its binding, outcome and grammar refusals all fail closed, before launch.

The pre-fix check: the new `test_no_judging_brief_orders_an_act` (all 4 cases) FAILS on `ace24c85c`'s templates and composer (`git archive` of the base, new test file copied in). The assertion is `'intake.py snapshot' not in ...`, which finds the old first-approval `--approves` order. `adjudicate_act` and the `act` command do not exist at the base, so their tests fail there by construction.

Other checks:
- The skill copies in `.claude/skills/` and `.agents/skills/` are byte-identical to the kit source (`diff -r`).
- The `PROCESS_OPTIONS.md` delta is +130 bytes (199,296 -> 199,426), matching the restamped byte-budget-guard row.
- The RESYNC entry is anchored `[since ace24c85c]` at the trunk base (K4). It lists every shipped file, forces no migration, and states the loop's missing act turn (Q3).
- K3 holds. Every new `Implements:` tag names an LLR whose `module` is that file and whose `code_symbol` carries the function: LLR-338, LLR-306, LLR-305 (`_add_act_template`, `ACTABLE`) and LLR-310 (`blessed_rows`, `BLESS_TAG`).
- K2 holds. SR-231's added text names no carrier.
- No Status flip in the range. SR-231 keeps `Approved` with amended text, and the new rows are `Drafted`.

**Done-when map:**
- (1) Every deliverable is in its target, each citing its ruling. "No judging brief orders an act" -> `test_no_judging_brief_orders_an_act`. WI-572's pin is succeeded by `test_the_act_turn_reports_success_only_when_no_listed_act_is_left`.
- (2) Refusal per Trust input -> `test_the_act_command_refuses_each_trust_input_before_launch` (12 cases) and `test_each_unaccepted_or_unreadable_verdict_is_refused_naming_why`.
- (2) Retained/fresh -> `test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`.
- (2) Combined order -> `test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act`.
- (2) Mixed `--approves` -> `test_a_mixed_first_approval_verdict_approves_only_its_approved_rows_registries`.
- (2) Unblessed MEANING -> `test_a_MEANING_row_without_the_bless_mark_is_left_unacted`.
- (2) Stops short / writes under `docs/reviews/` -> `test_the_act_turn_reports_success_only_when_no_listed_act_is_left` and `test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed`.
- (2) Flip/snapshot interrupt -> `test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full`.
- (2) Combined interrupt -> `test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act` (both modules).
- (2) Flip without copy -> `test_a_flip_committed_without_its_copy_is_refused_naming_the_row`.
- (2) Drafted row in a whole-registry copy -> `test_a_Drafted_row_present_unchanged_in_a_whole_registry_copy_is_owed`.
- (2) Marker on / off -> `test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line` and `test_without_the_marker_no_prompt_carries_the_line` (every brief class plus `act`).
- (3) The checkpoint sitting, SR-231's amendment with its act, and the new-shape sitting recorded as a decision: NOT YET DISCHARGED at this tip. There is no ADJUDICATE verdict under `docs/reviews/wi-912/`, and SR-231's copy is not re-anchored. The lane's own sequencing (D-006/D-007) puts the checkpoint after the counted rounds, so this is pending, not uncovered code.
- (4) The skill sync, the catalogue `--check` (fresh, 14 prompts) and the byte delta are all verified.
- (5) The RESYNC entry is verified.
- (6) The plan gate is in place: `docs/plans/WI-912/pass.toml` exists.
- (7) `check_trajectory --strict` is clean. The smoke tier is not run, per the round facts.

Coverage-extension notes (fail-closed, out of the declared set, uncounted):
- A first-approval verdict that rules APPROVE on a row outside its `Adjudicates` scope has that row listed and flipped by the act turn, and the merge slot then refuses the flip by scope. The verdict grammar binds no row scope.
- A CLARITY re-attest where no approval record exists is not refused before launch (only an owed APPROVE is, `adjudicate_act.py:319`). The snapshot writer refuses it inside the act turn, which then exits 1.

**Commands:**
- `git rev-parse HEAD` -> `8c1a9fce772c2ff53291c3943f3bc09b3fffc0d9`
- `lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2/opus/wi-912 tests/test_adjudicate_act.py tests/test_coordinator_act.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_routing_and_prompts.py tests/test_done_when_blessing.py tests/test_assumption_observation_briefs.py tests/test_prompts.py` -> `394 passed in 266.63s (0:04:26)` (posix-shell gate unsatisfied, 0 skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (936 work item(s), 817 done (87%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ...` exit 0
- `python project-trajectory/scripts/gen_prompt_catalog.py --check` -> `gen_prompt_catalog: fresh (14 prompts).`
- base `ace24c85c` (`git archive`) plus the new `tests/test_adjudicate_brief.py`, `-k no_judging_brief` -> `4 failed, 77 deselected` (red before the fix)
- the reviewer probes `probe/test_probe.py` (same-registry combined act; mixed-rung blessed MEANING plus held CLARITY) -> `2 passed`

- [MINOR] docs/requirements/system-requirements.toml:1724 -> for clarity (K1): SR-231's requirement still says the entry point shall "read success only from a verdict that its own call wrote within that call's deadline", and its acceptance (line 1726) says "a valid claimed lane exclusively reserves a new verdict path". Read as binding the whole entry point, both contradict the added act-turn clauses, under which the turn reserves no verdict and reads success from the acts taken at HEAD -> scope the first sentence and the reservation/success clauses of the acceptance to the judging turn ("a judging call ...") at the checkpoint reconcile -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3466 -> (K1) LLR-338's detail, and TC-368's expected at docs/test/test-cases.toml:3560, say each authorized row "is owed or taken by its committed status and whole-row recorded copy". The code (project-trajectory/scripts/adjudicate_act.py:241-252, 265-266) has a third partition those rows never state. A re-attest of a row absent from the committed registries is a retirement: owed while the recorded copy holds it, taken once the copy drops it, and no act on a held rung. A first approval of an absent row is inconsistent. So shipped, tested behaviour has no LLR text -> add the retirement sentence to LLR-338's detail and TC-368's expected -> @owner
- [MINOR] docs/runtime-flows.md:247 -> (K1) Flow 6 has the JUDGING turn "confirm the judging lane claim and clean tree", but `coordinator_adjudicate.adjudicate` checks no tree state. Only the act turn's `_act_inputs` reads `git status`, and `lane_refusal` checks the worktree and claim only -> drop "and clean tree" from the judging turn's step -> @owner
- [MINOR] project-trajectory/scripts/adjudicate_brief.py:1846 -> (no rubric anchor; CLAUDE.md single source) the actable-class set is declared twice: `adjudicate_brief.ACTABLE` (it decides which retained identities carry the act brief) and `adjudicate_act.ACTABLE` at project-trajectory/scripts/adjudicate_act.py:101 (it decides which verdicts the act turn accepts). If one is widened without the other, an act brief can launch on a retained session whose identity never included it, so an edit to that brief would not drain it -> keep one definition (for example, `adjudicate_brief` imports `adjudicate_act.ACTABLE`) -> @owner
- [MINOR] project-trajectory/scripts/adjudicate_act.py:181 -> (no rubric anchor; CLAUDE.md single source) `_reattests` and `_approvals` restate the held-rung act policy: CLARITY on any rung, MEANING only on a released rung, APPROVE only on a released rung. The judging composer reads the same policy from `intake.adjudication_action` and says it is "never restated" (project-trajectory/scripts/adjudicate_brief.py:906, 916). The two agree today. If `adjudication_action` changes, the judging brief tells the judge one act and the act turn takes another -> derive each row's arm from `intake.adjudication_action(held, ruling)` ("flip"/"reattest" act; "recommend" owes none) instead of re-encoding it -> @owner
- [MINOR] project-trajectory/scripts/kitlib/sitting.py:606 -> the bless mark is honoured only by the act session keeping to its listed command. The merge floor's `judged_rows` counts any amendment MEANING ruling as authorizing a re-attest, and the act report (project-trajectory/scripts/coordinator_adjudicate.py:439) checks only under-acting. So an act turn that widens `--reattests` to an unblessed MEANING row exits 0 and merges. This is reachable only when the session disobeys its brief, hence MINOR -> have the merge floor authorize an amendment MEANING re-attest only for a row `kverdict.blessed_rows` reads in the accepted part. This adds a check. It cannot be made unrepresentable upstream, because the act is a session editing files and running a CLI. The merge slot is the single owning boundary that validates every act once, so the check belongs there rather than as a second post-call check in the entry point -> @owner

VERDICT: CHANGES-REQUESTED findings=6
