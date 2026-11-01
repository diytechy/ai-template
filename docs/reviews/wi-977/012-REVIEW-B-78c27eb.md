Reviewed: 78c27eb50ff56679378441c2ca80751371f961b3

## WI-977 full-lane review (convergence stance), 41dfbb17e..78c27eb5

**Verified.** `git rev-parse HEAD` in the lane printed the reviewed commit. I read the whole diff in scope, the WI-977 spec and the rubric. I read no earlier verdict, no record under docs/reviews or docs/decisions, no critique and no lane commit message.

I hunted these failure classes, worst first:
1. A claim, assignment or resume that fails open on an empty or multi-item input.
2. A close or the peel acting on a multi-spec claim.
3. Silent prompt drift.
4. Admission still letting a second spine row through.

What I confirmed:
- **Claim.** `integrate.claim` and `main` refuse an empty value, a value that is only separators, any `;`/`,`/whitespace list, and any list or tuple. The refusal comes from `_claim_input_refusal` through the shared `agent_common.parse_wi_id`, and it runs before the hooks rung, the lock, the move, the commit and the branch. I probed it directly: `normalize_wi_id` and `parse_wi_id` accept ' wi-5 ' as WI-5, and refuse 'wi-5;wi-6', 'WI-5\n', 'WI-5​' and ('WI-5',).
- **Worker.** The `--wi` preflight treats an empty value as an assignment, so it refuses it rather than reading it as a plain launch. `is_drive_launch` now decides on whether a flag is present, not on its truthiness.
- **Resume.** `_admit_parked` refuses a parked multi-spec claim before `_pre_admit`, before the cycle count and before `_launch`. The shared `_stop_run` freezes admission while lanes are live, and `run` checks `state["fatal"]` before `_admit`.
- **Closes.** Both closes ask `_the_one_claimed_spec` before `_lane`, before any report and before any residue commit.
- **Peel.** `_closed_wi_ids` takes exactly one deletion that pairs with an addition of the same name. The one-source-branch clause it dropped really is implied by that.
- **Claim history.** `claim_base` parses the historical joined subject exactly as the old equality test did.
- **Admission.** `_kind_action` has no `batch` arm, and `_admission` admits `[first_w]` alone.

Pre-fix check: I copied the tip tree to scratch with the base revision's `project-trajectory/scripts` and `project-trajectory/prompts` laid over it, then ran the lane's new and changed tests there. 21 failed against the pre-fix code, which covers every refusal and retirement test: the claim multi and empty cases, the subject writer, the parked two-spec resume, spine one per turn, the explicit empty `--wi`, both two-spec closes, the two-row peel, the worker list and empty refusals, the help text, the template slot and the golden prompt. 11 passed, all of them preservation tests: the historical claim read, the one-row adjudication close, the single-report restore, high-risk one per turn, the ordinary-row bar, loop order, and the one-id-subject peel.

Spine check: every replaced clause in SR-144, SR-148, SR-156, LLR-144, LLR-149, LLR-150, LLR-151, LLR-152, LLR-161, LLR-207 and the TC rows names no code. The `Implements:` tags on the new functions (`parse_wi_id`, `_buildable_wi`, `_claim_input_refusal`, `_the_one_claimed_spec`, `_stop_run`) each name an LLR whose `module` and `code_symbol` carry them (K2, K3). No Status flips.

Done-when coverage map:

| Done-when item | Status |
|---|---|
| Admission | Covered: test_no_kind_maps_to_a_batch_arm, test_lanes_back_in_the_station_the_first_spine_row_admits_alone, test_spine_rows_admit_one_per_exclusive_turn |
| Claim | Covered: test_a_multi_item_claim_refuses_before_any_state_change, test_an_empty_claim_refuses_before_the_lock |
| Resume | Covered: test_a_parked_lane_claimed_with_two_specs_stops_the_run |
| Worker | Covered: test_the_worker_refuses_any_assignment_but_one_id, test_a_list_assignment_exits_preflight_before_a_provider_launches, test_the_wi_help_names_one_work_item, test_an_explicit_empty_assignment_is_refused_not_driven |
| Prompt | Covered: test_the_worker_template_has_no_assignment_block_slot, test_the_one_row_prompt_renders_as_today |
| Close | Covered: both two-spec close tests, test_a_partial_close_restores_the_single_report_after_move_refusal |
| Peel | Covered: test_a_mechanical_close_moving_two_rows_does_not_peel, test_a_two_row_close_under_the_one_id_subject_does_not_peel |
| Claim subject and history readers | Covered: test_the_claim_subject_composes_one_id_only, test_a_historical_joined_claim_still_reads_as_a_claim |
| Other readers | Covered: test_a_lane_whose_one_row_is_ordinary_runs_the_bar |
| RESYNC entry | Present, with both supersede notes |
| Generated pages | CATALOG regenerated. `docs/cli-reference.md` still shows the old list help, but it is a trunk-owned `[generated]` view regenerated at landing, so this is not a lane finding. |
| One checkpoint sitting | Not judged here: its record is under docs/decisions, which the convergence stance forbids me to read. |
| Spine target meaning | Partly met; see findings 1 to 4. |
| Text | Partly met; see finding 5. |

**Commands**
- `git rev-parse HEAD`: 78c27eb50ff56679378441c2ca80751371f961b3
- The brief's pytest set (17 modules, `-n 2`, the literal `--basetemp`): `755 passed, 2 skipped in 1130.26s (0:18:50)`. The 2 skips are the posix-shell environment gate.
- `check_trajectory.py --strict`: `check_trajectory: clean (982 work item(s), 867 done (88%), 34 cancelled, graph acyclic).` exit 0
- `trace.py --strict-integrity`: `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` exit 0. It rewrote the gitignored `docs/test/report.md`; `git status --porcelain` stays empty.
- Pre-fix check: the new and changed tests on a scratch copy (tip tree with the base revision's scripts and prompts) gave `21 failed, 11 passed`.
- Direct probe of `agent_common.parse_wi_id` and `integrate.normalize_wi_id` / `_claim_input_refusal`; results as quoted above.

Coverage-extension notes (outside the threat model, no severity):
- `dispatch._admit_parked` unpacks `(wi_id,) = wi_ids`. A hand-made claim directory holding only a `WI-*.md` file that carries no id therefore raises ValueError, which fails closed, rather than giving a named refusal.
- `WI_TOKEN_RE` (`\d`) accepts Unicode digits ('WI-٣'). This predates the lane, and such an id fails closed later at the spec lookup.

**Findings**

- [MINOR] docs/test/test-cases.toml:1450 -> The lane rewrote the whole of Approved TC-146's method, not just its batch clause. The spec allows only that clause to change ("only that clause is replaced, in the same voice, and the rest of the cell waits for item 5's migration"; Done-when "TC-146 ... in their single-WI parts only"). The rewrite also lost three precise assertions: "(the reserved slot, pinned by name)", "(fail toward the bar)" for unreadable frontmatter, and "asserted off the recording stub's own argv" -> Restore the approved method text and replace only "a mixed batch bars as usual (fail toward the bar)" with the single-row clause "a lane whose one row is any other kind bars as usual (fail toward the bar)" (rubric K3: an approved row changes only where the spec grants it) -> @owner
- [MINOR] docs/requirements/system-requirements.toml:641 -> For clarity: SR-148's rationale does not carry the target meaning the spec set for it ("the rationale says admission cardinality here and claim cardinality in SR-156 bound one contract at two boundaries"). SR-148's acceptance ("Each assignment admits exactly one work item") and SR-156's ("empty or multi-item claim, assignment and resume inputs refuse") now both state the one-item rule. Meanwhile SR-148's own rationale still claims its invariant "is stated here and nowhere else", so the overlap goes unexplained -> Add the spec's boundary sentence to SR-148's rationale (rubric K1) -> @owner
- [MINOR] docs/test/test-cases.toml:647 -> For clarity: TC-061's method still says "a --wi list with a malformed or repeated id are rejected". The spec said that phrase becomes "any value that is not exactly one well-formed id", and the cell now also says no list form exists, so the method contradicts itself -> Replace the phrase with "any --wi value that is not exactly one well-formed id" (rubric K1) -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:1241 -> For clarity: LLR-123's rationale still says "deriving WHICH traincars are eligible", although the spec lists all three of the row's cells under the traincar -> work-item rename and its title and detail were renamed -> Rename the rationale's "traincars" to "work items" (rubric K1) -> @owner
- [MINOR] project-trajectory/PROCESS_OPTIONS.md:288 -> The shipped text still tells adopters that "a run of *independent, off-spine* dev slices may batch into one BUILD session + one review round". That is the multi-WI assignment whose own paragraph this lane deleted, and the worker preflight now refuses it (`--wi` takes exactly one id). An adopter who follows the sentence gets an EXIT_PREFLIGHT refusal rather than the capability it promises -> Delete the parenthetical relaxation, or restate it as "independent dev slices run as separate lanes", and add it to the RESYNC entry's text list (rubric K1) -> @owner
- [MINOR] project-trajectory/prompts/worker.template.md:53 -> For clarity: the worker rule "Work ONLY the Assignment above — this session's focus row first, and no row that is not listed there" keeps the multi-row wording of the retired assignment block ("focus row first", "rows listed there"). The spec's Prompt Done-when removes that block and its operator notes, and the Assignment now lists one row -> Reword it to "Work ONLY the one work item in the Assignment above", then regenerate CATALOG.md and the golden prompt (rubric K1) -> @owner

VERDICT: CHANGES-REQUESTED findings=6
