# ADJUDICATE — WI-681 — first approval at 1ea526ac

Independent adjudication of the 32 spine rows authored `Drafted` that the
`human_approval_through = "DevStg-Boundary"` dial releases to an adjudication
session: six requirements (SR-183, SR-184, SR-185, SR-186, SR-220, SR-221),
eight design rows (LLR-205, LLR-206, LLR-210, LLR-259, LLR-260, LLR-261,
LLR-262, LLR-263) and eighteen test cases (TC-199 to TC-204, TC-208 to
TC-211, TC-252 to TC-259). The one question: is each row ready to be
APPROVED as it stands, or does it go back with findings. `Approved` blesses
the row's TEXT; the harness answers whether its tests pass, and I ran them
anyway, because a cell describing a test the suite does not run, or a
mechanism no module holds, is not blessable text.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the fifteen chains of SR-017, SR-139, SR-148,
SR-154, SR-156, SR-157, SR-163, SR-176, SR-183 to SR-186, SR-216, SR-220 and
SR-221 in full, about 265k characters; anchor `docs/archive/last_approved`
copied at bc6a245f). Every row was read upward (its parent SR and the need
that SR cites), sideways (the approved siblings in the brief) and downward
(its test cases, each evidence pointer resolved by file and function name
with an AST walk). Disclosure: I read WI-681's and WI-680's queued specs for
their Context, WI-604's and WI-674's recorded verdicts as the precedents the
assignment named, and the spine-authoring skill for rule (c); nothing below
rests on any session's account of its own intent. HEAD stayed at 1ea526ac
throughout, and the worktree was clean before this file was written.

- [APPROVE] SR-183 -> the delivered harness reports each source function's cognitive complexity against a stamped per-function baseline, and fails a declared gate on any divergence only where the repo enabled gating; acceptance fixes the exclusive threshold, the both-direction compare, the never-graded public-symbol count, exit zero in reporting mode, the three named remedies, a re-stamp that writes only the baseline, and no per-site suppression -> SN-007 (the kit holds itself to its own standard) and SN-012 (a heavy layer costs a non-user nothing) both reach it; LLR-206 decomposes every clause into `check_complexity.py`, TC-202 pins the metric and the boundary in process and TC-203 drives the modes and exit codes as a subprocess; the `docs/complexity-baseline` name is labelled "the current carrier", the sanctioned rewritable-evidence form, and `trace.py` raises no artifact advisory on it -> ready: one `shall`, every acceptance clause has a detector in its chain, the SN-012 opt-in clause is true of the shipped template (no `[step:complexity]`) and of this repo (enforce at DevStg-Impl).
- [RETURN] LLR-206 -> `cognitive()` by recursive descent with nesting, the elif flattening, the BoolOp run rule, the recursion increment; `census()` keyed on (path, qualified name) with a never-compared public-symbol count; `main()` comparing strictly-over-threshold rows by exact equality both ways, printing the three remedies, honouring no suppression token, with `--report`, `--restamp`, `--mode warn` (default) and `--mode enforce` as stated -> every mechanism clause is true of `check_complexity.py` (the argparse choices, the `> threshold` select, the exit-1-only-under-enforce return), the shipped template wires no step and this repo's `[step:complexity]` runs `--mode enforce` at DevStg-Impl over `--root .`, and TC-202/TC-203 pin it -> not ready as it stands, for one sentence: the rationale ends "Landing Drafted because its parent SR-183 is itself Drafted and approving this design is the owner's act." That is a status-and-provenance statement in a reason cell (the spine-authoring skill's cell hygiene: a cell states what is true now, never when or how it changed), and approving the row makes it false twice over: the row would read `Approved` beside "Landing Drafted", and under the declared dial the act is an adjudication's, not the owner's. A wrongly-approved cell is a false claim the record carries forward; the fix is deleting one sentence. Nothing else in the row is returned.
- [APPROVE] TC-202 -> in-process unit cases over the counting function: the elif ladder and the written-out else-if, BoolOp runs, nested def and the decorator exemption, the Sonar white-paper oracles, SLOC and public-symbol rules, the LF-only debt-headed baseline round-trip preserving the reason column, the checker under its own threshold, the exclusive boundary, and a module-level def under any control-flow container -> every arm maps to a named test in `tests/test_check_complexity.py` (38 tests: `test_elif_ladder_is_flat`, `test_written_out_else_if_is_nested_not_flattened`, `test_boolean_operator_runs`, `test_nested_def_is_charged_to_the_enclosing_function`, `test_decorator_shape_is_exempt_from_the_nesting_increment`, `test_white_paper_oracles`, `test_sloc_excludes_blanks_comments_and_docstrings`, `test_restamp_writes_lf_only_debt_headed_tsv`, `test_baseline_round_trip_preserves_the_reason_column`, `test_threshold_boundary_is_exclusive`, `test_collect_descends_through_every_control_flow_container`, `test_the_checker_passes_its_own_check`), green; Tier Smoke is true: the module is not in `SLOW_MODULES` -> ready.
- [RETURN] TC-203 -> synthetic fixtures run through `check_complexity.py` as a subprocess: `--report` exits 0 with every function, a matching baseline is OK under enforce, growth and an unstamped improvement and a vanished entry each exit nonzero under enforce with the remedies, a suppression-shaped comment changes nothing, repeated `--include` globs widen, an absent source directory is vacuously OK -> nine named tests in `tests/test_check_complexity_cli.py`, one per arm, green; Tier Full is true: the module is in `SLOW_MODULES` -> not ready as it stands (ruling 3, second sitting below): the Method's closing sentence, "Re-tiered into conftest.SLOW_MODULES because each case pays interpreter startup", narrates the row's history rather than stating where the evidence runs; a living cell states the system and its standing reason. My first-sitting line passed it on precedent; an approved row with the same defect is a reason to fix that row, not to approve this one. Every other cell stands; the fix is one sentence, returned with LLR-206.
- [APPROVE] SR-184 -> where a capability requires Critique acceptance, the delivered acceptance record identifies a fresh non-author reviewer session, applies a rubric derived from the SN/SR intent, and records each verdict and finding against numbered anchor ids; a record missing any of those, or whose rubric is copied from the verifying TC, fails; artifact adequacy is not judged -> SN-024's acceptance states each of those elements (a fresh critique session, a rubric derived from the SN/SR intent and not the possibly-lax TC, numbered anchor ids); SR-154 keeps scheduling, consent, family selection and escalation and the rationale draws that line explicitly; TC-209 inspects a complete record, an abnormal one and a TC-copied rubric against the procedure at `docs/test/inspection-procedures.md#critique-acceptance-provenance-inspection`, which exists -> ready. The `trace.py` advisory that its cells "name a CRITIQUE instrument while Verification is Inspection" is the lexical detector reading the row's SUBJECT (Critique acceptance records) as its instrument; the acceptance is an inspectable condition on a record and the row's method is Inspection throughout.
- [APPROVE] TC-209 -> follow the Critique acceptance provenance inspection; complete provenance accepted, each missing field or TC-copied rubric a finding, artifact quality left to Critique -> Automated No, Level Inspection, Tier Release, `inputs` (the procedure document and SR-184) and `max_age` 90 declared, both anchors (the procedure and its result section) resolve, `assumption_rules.observation_tc_findings` raises nothing on it -> ready.
- [APPROVE] SR-185 -> when a reviewed change alters one side of a requirement/interface relationship, the change record identifies the affected counterpart and carries the corresponding change or an explicit justification; the reviewer's semantic decision is recorded and not discharged by reference-existence tests -> SN-037's acceptance carries that sentence almost verbatim as its final clause; SR-162 owns the mechanical frame and this row the semantic review, as the rationale says; TC-210 inspects a semantic record and a reference-existence-only one against `#requirement-and-interface-counterpart-review-inspection`, which exists -> ready: `When` pattern, one `shall`, an observable record condition.
- [APPROVE] TC-210 -> follow the counterpart review inspection; the counterpart decision explicit, reference-existence alone insufficient -> the observation cells (inputs, max_age 90, Release, Inspection) are declared and pass the declaration check; both anchors resolve -> ready.
- [APPROVE] SR-186 -> the delivered requirements process requires each additional child within a required tier to carry an independent decision or verification purpose and records the stopping decision in the scoped decomposition record, retaining the four tiers -> SN-012's acceptance says "the proportionality doctrine governs LLR/TC granularity" and no other SR carries that clause; the rationale forecloses a row-count cap, a deletion quota and a new machine gate; TC-211 inspects a complete chain and a paraphrasing child against `#decomposition-proportionality-inspection`, which exists -> ready. The result section under that anchor records INCOMPLETE for its SR-161 sample; that is the harness's answer about a run, not a defect in the text, and the case's method is not weakened by it.
- [APPROVE] TC-211 -> follow the decomposition proportionality inspection; a purposeless child is a finding, otherwise the review records the independent value and why splitting stops -> declaration cells complete, anchors resolve -> ready.
- [RETURN] SR-220 -> while the queued work items include an overlapping set, the loop hands that set to a single judgement, at most once per state of the queued rows and never beside another queued or active judgement, and enacts the outcome as a recorded restructuring with each absorbed item terminal, naming its one successor, scope text unchanged -> a labelled DERIVED requirement under SN-025, judged by rule (c): (i) recorded in a cell something reads: `Hat-Refs` names UNATTENDED-OPS and PERFORMANCE, both roster hats whose `listens_for` names a failure this row prevents (an unbounded retry that pages nobody; an operating-cost risk left unassessed); (ii) the rationale argues both lenses and says why the need's text alone would not yield the row; (iii) fed back upward: the rationale states the sentence SN-025's acceptance could carry, and this verdict's recommendation section carries it to the owner. Sideways, SR-148 keeps work selection and SR-157 the overlap warning, and the row says so; downward, LLR-210 decomposes every acceptance clause and TC-208/TC-254 split the in-memory decisions from the repository act; the obligation closes WI-604's return -> not ready as it stands, for the form of one cell: the Requirement carries two `shall`s ("shall hand that set to a single judgement ... and shall enact the judgement's outcome"), and `trace.py` reports it as a requirement-form FINDING the moment the row is Approved, gating under `--strict` (driven: the flipped tree exits 1 on exactly this line). One row states one obligation (PROCESS.md §3; the skill's "one `shall`"); the remedy is dropping the second `shall` so the two clauses read as one obligation with two parts, or splitting the enactment into its own row. The derivation, the acceptance and the chain stand; only the sentence's shape returns.
- [APPROVE] LLR-210 -> `clusters` seeds candidate sets from `check_trajectory.queue_conflict_pairs` widened by the commissioning and module signals; `census_draft` returns the row a mint would write with its scope in `Adjudicates` and a queue sha plus spine sha in `Digests`; three refusals over typed cells; `parse_verdict`/`close_refusal` refuse by name a moved row not queued; `archive_absorbed` moves absorbed rows to the fourth terminal folder at the mint -> re-pointed to SR-220, which now demands exactly this; WI-604's wording finding is fixed ("the queued rows", not "the ready queue"); the component is CMP-008 under a loop row rather than a checker row; every named symbol exists in `consolidate.py` and TC-208 plus TC-254 drive them (86 passed across the two modules) -> ready.
- [APPROVE] TC-208 -> fifteen in-process cases on hand-built rows with no git: the digest's four moving and two still fields, the malformed digest, the two widened signals and the bare-name silence, one set from two disjoint pairs, a detector-only pair, the carrier-aware spine digest, and the six guards including the byte-identical archived spec -> fifteen named pointers in `tests/test_consolidate.py`, each resolving, green; Tier Smoke is true: `test_consolidate` is not in `SLOW_MODULES`, the split WI-604's return asked for -> ready.
- [APPROVE] TC-254 -> five cases on real repositories: one mint then silence while pending, the three-row absorb end to end with byte-exact specs less the inserted section and the census silent after, the claimed-row refusal by name, the hard `needs` edge, return-to-draft with the finding quoted -> five named pointers in `tests/test_consolidate_close.py`, resolving, green; Tier Full is true: the module is slow -> ready.
- [APPROVE] SR-221 -> the delivered harness lists, for a module a design row names, the test files the spine links to it through the design rows, the cases verifying them and their evidence, from the registries with no hand-kept map; acceptance: every linked file under the declared test root and no other, files not named for the module included, distinct refusals for no match and several matches (the latter naming candidates), read from the repository pointed at, the commit bar unchanged -> a labelled DERIVED requirement under SN-012, rule (c): (i) `Hat-Refs` names PERFORMANCE and TEST-ENGINEER, whose `listens_for` (operating cost; evidence that passes without examining the claimed behaviour) each name what the rationale argues; (ii) the rationale prices the guess and names what it costs; (iii) fed back through this verdict's recommendation. Sideways, no other SR lists tests for a module; downward, LLR-263 decomposes it and TC-258 drives the map, the command and the live registry -> ready: one `shall`, each acceptance clause observable; the "commit bar unchanged" clause is carried by the command being an act-and-exit arm that runs no check (LLR-263, TC-258's exit-0 arm) rather than by a test of the bar, which I note and do not return on.
- [APPROVE] LLR-263 -> `module_tests(llrs, tcs, module, test_root)` joins a design row's `Module` to the cases whose `Verifies` names it and their `Evidence` under the test root, every status included; `resolve_modules` by path, trailing part or stem through `norm_module`; `trace.py --tests-for` prints one path per line from the directory `--docs` names, test root from `stack.ini [paths] tests`, exits 0/1/2 as stated -> every clause is true of `kitlib/spine.py` lines 569-615 and `trace.py` `_cmd_tests_for`; both modules in the `module` cell hold the named symbols; IF-233 declares the seam with the same exit contract -> ready.
- [APPROVE] TC-258 -> the map over a synthetic spine (a Drafted case included; an SR-only case, another module's case and a document excluded; another test root yields none), resolution by path, suffix and stem with two matches and none, the command through `trace.py`'s entry point with `--docs` elsewhere and `--root` empty, exits 1 and 2, and the live map reaching `coherence.py`'s and `frame_rules.py`'s suites -> seven named pointers in `tests/test_evidence_join.py`, resolving, green; Tier Smoke is true -> ready.
- [APPROVE] LLR-260 -> `evidence_items(cell)` reads an Evidence cell as (path, node) pairs with the stated separators, parametrization, note and anchor rules; `tier_findings(tcs, tier_of)` judges approved cases only: Smoke with no smoke evidence is an error naming the case and paths, Full with no slow evidence an advisory, Release and below-approval silent; this repo binds `tier_of` in a per-commit test -> SR-157's acceptance says a rule added at a declaration site is in its scope by default, and this is such a rule with its severity declared; no approved sibling under SR-157 judges the tier cell; the code at `kitlib/spine.py` 544-660 reads exactly as the cell says, and `test_every_approved_smoke_case_has_evidence_in_the_smoke_tier` in the fast module is the binding -> ready. Noted, not returned: an adopter receives the pure rule and nothing runs it until they bind `tier_of`; the rationale says so and why (the harness's answer is not stack-neutral).
- [APPROVE] TC-255 -> the cell's spellings and the spaced parametrization; the tier rule over a literal table (slow-only Smoke errors, one fast item is silent, a document-only Smoke errors, all-fast and workflow-only Full are advisories, slow Full and Release silent, a Drafted Smoke unjudged); the live check bound to this repo's tiering -> nine named pointers in `tests/test_evidence_join.py`, resolving, green; Tier Smoke true -> ready.
- [APPROVE] LLR-261 -> `flag_axis.reading` counts flag functions (two or more parameters annotated bool or defaulting to a boolean literal, keyword-only included, named as the complexity census names them) and positional boolean-literal call sites; `compare` reports only counts that rose above the stamped row, an absent row reading zero; the `MEASURES` adapter runs it over touched `.py` modules under the declared roots from the change's new side, SKIP on an unparseable module; `REPORT_ONLY` holds it and a gating declaration gets one WARN and no refusal; the CLI always exits 0 and `--restamp` rewrites -> SR-216 asks for each declared measure over the touched parts against its own baseline, reported in one place, refusing only where declared gating; LLR-256 is the report and this row one measure of it; every clause is true of `flag_axis.py` (`flags`, `reading`, `compare`, `read_baseline`, `BASELINE`) and `check_readability.py` (`_flag_axis`, `MEASURES`, `REPORT_ONLY`, the WARN line); both modules named hold their symbols; IF-239 and IF-240 declare the seams -> ready.
- [APPROVE] TC-256 -> in memory: the two-flag function by default or annotation, the one-flag exclusion, `Class.method` naming, positional versus keyword literals; the CLI over three modules with totals, WARN above a stamped row at exit 0, re-stamp reading back level, SKIP on invalid Python or non-UTF-8 with and without re-stamp; compare naming only risen counts; the measure over an in-memory change naming the touched module above its row and nothing at its row or outside the roots; gating declared yet gating nothing with one WARN -> fifteen tests in `tests/test_flag_axis.py`, one or more per arm, green; Tier Smoke is true -> ready.
- [RETURN] LLR-262 -> the coordinator's session log names each session's phase and exact range; `scope_offenders` names every changed path but the REVIEW session's own round file for its train, ordinal and logged phase; the loop stops needing a human on any offender right after the session; every reader takes a log as the commit that added it recorded it; the merge ladder first refuses a commit that modified or deleted a session log, then re-derives the same rule from every committed REVIEW log; leftovers after a REVIEW or CRITIQUE session fail the draw and are stashed under one named entry, a failed stash stopping the run; `read_verdict` reads the blob at HEAD in both arms; `logged_rounds` reads a round at the end of its session's range only when that range changed it; `done_when.items`/`changes` with the closed-spec evidence grammar; the claim warns by name on a missing Done-when; the review brief quotes each change; the intake mints one brief-less adjudication row per claimed row whose Done-when changed -> SR-154 (a verdict from a session that did not author the work) and SR-156 (one fail-closed serial seam) both demand that the records the seam judges are not the judged lane's to rewrite; no approved sibling (LLR-140, LLR-207, LLR-045, LLR-082) states these rules; all twenty-three named symbols exist in the five modules the `module` cell lists, and I read `scope_offenders`, `read_verdict`, `stash_leftovers`, `judging_session_integrity`, `_review_scope_refusal` and `done_when.changes` against the cell; TC-257 drives the repository arms and TC-259 the pure rules; the row is wide (five modules, one property: the record a merge judges stays as its author committed it), every mechanism serves that one property and none re-words its parents, so the width is surfaced below and not returned on -> not ready as it stands, for one phrase: the Detail's evidence grammar reads "a capitalised completion word such as LANDED or DONE", and `trace.py` reports "such as" as a requirement-form FINDING on an Approved design row (the scope cannot be closed), gating under `--strict` (driven: the flipped tree exits 1 on exactly this line). The code closes the set (`done_when._EVIDENCE_TOKEN_RE`: LANDED, DONE, MET, VERIFIED, SHIPPED, PASSED, FIXED, COVERED); the remedy is enumerating those eight words in the cell, or naming them as the closed set the grammar lists. Everything else in the row stands.
- [APPROVE] TC-257 -> on git repositories in slow modules: a rewritten round leaves the gate refusing; a verdict its session never committed is no round; a log rewritten to launder a range is refused by name at the ladder; the ladder refuses a review range that changed files beside its verdict and passes a clean one; through a fake agent: a clean review accepted, a reviewer committing beside its verdict stops the run naming the file, an untracked leftover fails the draw with the file stashed and the redraw completing, a failing stash (index lock held) stops after one launch and neither cools nor arms a redraw when called directly, uncommitted CHANGES-REQUESTED verdicts from a reviewer and a critic cause no rework; a claim with no Done-when warns and one with it is silent; a reworded Done-when is flagged to the reviewer and mints one adjudication row idempotently while a ticked-with-evidence one does neither -> seventeen named pointers across `test_verdict_record.py`, `test_agent_loop_review.py`, `test_agent_loop_critique.py`, `test_integrate.py` and `test_intake.py`, each resolving, all green in the slow batch; Tier Full is true: all five modules are slow; IF-242 declares the done_when seam -> ready.
- [APPROVE] TC-259 -> in memory: a REVIEW session's changed paths naming no offender when only its own verdict (with and without the relaxed tag) or nothing changed, and naming a code file, log fragment, scoreboard and other-phase/ordinal/train round files; the range parsing from a log header, empty and placeholder ranges as none; Done-when items across subsections and continuation lines, none for a missing or empty section, a prose criterion counting; ticks, strikethrough and evidence after punctuation or a separator flagging nothing; reworded, narrowed, deleted, added items flagging; the three "Tests pass." qualifications each read as changed -> `tests/test_review_scope.py` (3 tests) and `tests/test_done_when.py` (8 tests, the Linux/Windows strings present at lines 111-114), green; Tier Smoke is true: neither module is slow -> ready.
- [APPROVE] LLR-259 -> `released_tiers(root)` asks `agent_common.human_approves_spine` once per spine tier through `SPINE_FILES`, holding no rung table; `dial_releases_chain` is true only for a chain with at least one owing row, every owing row on a released tier; `reattest_lines` keeps held chains in the owner's section, writes the stated no-held-chain line when every owing chain is released, and sets released chains apart in one closed `<details>` block labelled "Waiting for automated adjudication" with the chains' ids in its summary; the title claims no human act, the signing instruction is scoped, and no block renders when no tier is released -> SR-139's level is what this row consumes and its fail-safe direction (one held row keeps the chain; no owing row keeps it held) points the way SR-139 demands; WI-674's finding 3 is answered by the new "or, when every owing chain is released, a line in the owner's section" clause, and finding 2 by the summary assertions now in the suite; the code at `trace.py` 4225-4300 reads as the cell says (`_waiting_lines` puts the ids in the `<summary>`) -> ready.
- [APPROVE] TC-252 -> driven through the command on temporary repositories writing the live brief path, in a slow module: under a level holding SR and releasing LLR/TC, the Drafted-only chain inside one closed block whose summary carries the label and the id, full text inside, the Drafted-SR and mixed chains outside; the neutral title and scoped instruction; the amended-after-snapshot pair split by tier; no level declared, no block and every chain in the owner's section; every tier released, every chain in the block with its id in the summary and the stated empty ask; the freshness check on each written brief -> `tests/test_trace_briefs.py` lines 1040-1190 assert each arm, and the freshness check now runs on all four briefs (1075, 1096, 1115, 1190), WI-674's finding 1; the no-dial arm is `test_the_shipped_default_dial_holds_every_chain_and_collapses_none` (no dial reads as DevStg-Release, releasing nothing), which is what the Method's "no level declared" means; green in the slow batch; Tier Full is true: the module is slow; IF-224 is cited -> ready.
- [APPROVE] TC-253 -> in process on temporary repositories in a fast module: with a registry holding a pending, a ruled and a `-000` row, `schedule.load_oi_status` returns each minted row's status lowercased and drops the example, and the readiness gate holds the item waiting on the pending row and admits the one on the ruled row; with no registry the owner's reader answers None, the scheduler's read an empty map, and an item waiting on an open item is not ready -> LLR-058 owns the frontier's readiness and `hard_preds_satisfied` consumes `oi_status` fail-closed; `trace.open_item_states` drops `-000` rows and lowercases, `load_oi_status` wraps it as `or {}`, `dispatch.py` passes it into `schedule.frontier`; IF-176 declares the seam; the two named `tests/test_schedule.py` tests exist and passed; Tier Smoke is true -> ready.
- [APPROVE] TC-199 -> the inventory's two delivered finding classes where each can fail: the dogfood walk (an undeclared missing destination named, a stale absence reported, the lifecycle marker exempting only legal presences, bite-proofed by removing an entry) and the package direction on a real bootstrapped scaffold (the helper package holds exactly the kit's module set, a sibling import the inventory omits reported against MAPPING read as an AST); two nodes shared with TC-176 for a different arm -> LLR-203 states exactly those two arms as its own and records the undischarged remainder; five named pointers across `test_dogfood_sync.py` and `test_bootstrap.py`, resolving, green; the Expected honestly scopes to LLR-203's delivered arm; Tier Full is true: `test_bootstrap` is slow -> ready.
- [APPROVE] TC-200 -> the grammar on the shared function (a token opening a line yields ids; prose, a preceded token and a continuation line yield none) and the policy through the real command on a real scaffold (shortfall printed at exit zero, nonzero only under the strict arm) -> LLR-204 states the grammar and the warn-then-gate dial and records its direction and universe gaps; both named `tests/test_gen_arch_map.py` pointers resolve and passed; Tier Full is true: the module is slow -> ready.
- [RETURN] TC-204 -> the direct test on SR-163: `mapping_entries` normalization, `delivery_inventory`'s independent universe, the real-row end-to-end bite that removes a MAPPING row in a child process and drives `gen_arch_map.main()` through `--mapping-purpose` to a gate-class finding, the four-class checker on a synthetic inventory, the warn-versus-gate policy, and the standing evidence over the live package -> SR-163's acceptance names each of the four classes, the declared policy and the generator inheritance, and every Method arm maps to one of the eleven pointers, all resolving and green -> not ready as it stands: `tier = "Smoke"` while one pointer, `tests/test_mapping_purpose_cli.py::test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed`, sits in a `SLOW_MODULES` member, so the Method's end-to-end bite does not run in the per-commit tier the cell claims. This is WI-604's TC-208 return applied to the same fact, and the assignment's rule: Smoke evidence must not sit in a slow module. Ten in-process pointers are fast, so the remedy is a split (a Full case carrying the CLI bite and its sentence) or re-tiering the whole case to Full. Every other cell stands.
- [RETURN] LLR-205 -> `SECRET_CLASSES`, a tuple of `SecretClass(name, scan_pattern, redact_pattern)` rows over seven credential classes, either pattern may be None as a per-class decision; `check_privacy.py`'s `KEY_RE`/`TOKEN_RES` and `agent_common.py`'s `_SECRET_RES` derived from it by comprehension so LLR-017's and LLR-177's symbols still resolve; no exhaustiveness claim; the redactor deliberately looser on three classes -> SR-017 and SR-176 both cite it and the divergence it closes (a PEM block refused at the hook but passed unredacted into a transcript) is a real gap between the two parents' obligations; every clause is true of `kitlib/secret_classes.py` (stdlib `re`/`typing` only, seven rows with the asymmetry comments), `check_privacy.py` 196-197 and `agent_common.py` 2572; CMP-006 follows the ladder.py precedent the rationale cites; TC-201 drives it -> not ready as it stands, for the same one sentence as LLR-206: the rationale ends "Landing Drafted because SR-017 and SR-176 are both Approved and this row must not be read as amending either row's own attestation; approving it is the owner's act." Approving the row would make its own reason cell state a status it no longer has and attribute the act to an authority the dial does not hold for this tier. Delete the sentence; the rest of the row stands. (The dated plan citation earlier in the same cell has approved precedent in SR-176's rationale and is surfaced below rather than returned on.)
- [RETURN] TC-201 -> `Scanner` and `redact_secrets` driven three ways against a shared sample set: the five-sample decision table (PEM caught both sides, three deliberate floor-miss/redactor-catch asymmetries), one canonical positive per class reaching each consumer through the comprehension, and a frozen pre-table record compared by matching behaviour over threshold-straddling probes -> `tests/test_kitlib_secret_classes.py` holds `test_wi508_driven_table_matches_the_recorded_decision`, `test_every_class_has_a_driven_sample`, `test_each_side_catches_the_class_it_claims` and the two `test_pre_wi520_*_behavior_is_preserved*` batteries; green, one parametrized case skipped by design (the generic bearer token had no pre-table scan pattern, which is the None the LLR states); its text does not depend on LLR-205's returned sentence -> not ready as it stands (ruling 3, second sitting below): the Method narrates what "now catches" against what "was floor-catch/redactor-miss" and a record frozen "BEFORE this table existed" - changelog prose in a cell that must state the test as it stands; my first-sitting line did not see it. The three arms are real and the module is green; the fix is rewording the arms as standing claims (the PEM class caught on both sides; the three declared asymmetries; a frozen independent pattern record compared by behaviour), returned with LLR-205. Tier Full over a fast-only module is LLR-260's advisory class, never false; noted below.
## How the chain and the anchor were read

- The coordinator's filing-commit fills (`status = "Drafted"`, `phase = 6`
  on TC-256, TC-258, LLR-261 and LLR-263) were read as the rows now stand;
  each is consistent with its parent's phase (SR-216 and SR-221 are Phase 6).
- Upward: each parent SR's requirement, rationale and acceptance as the brief
  printed them and as the live file holds them; SN-007, SN-012, SN-024,
  SN-025 and SN-037 from `docs/requirements/stakeholder-needs.toml`; the hats
  roster through `python scripts/hats.py list` for every name in a Drafted
  SR's `Hat-Refs`. Sideways: every approved sibling in the fifteen chains,
  read for overlap with the row under judgement. Downward: every evidence
  pointer of every TC in scope resolved by file and, where named, by test
  function (an AST walk over the cited module); every named code symbol of
  every LLR in scope located in the module its `module` cell names.
- Anchor: `docs/archive/last_approved` at bc6a245f holds none of the 32 rows
  (all Drafted), so nothing here is a re-attest; the act's `--approves`
  names the three registries that hold at least one approved row.
- Off-spine rows cited by TCs in scope (IF-176, IF-177, IF-178, IF-224,
  IF-233, IF-239, IF-240, IF-242) exist in `interfaces.toml`, all Drafted;
  none is this act's and none is touched.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4
-p no:cacheprovider`:

- Fast modules, one run: `tests/test_kitlib_secret_classes.py`,
  `tests/test_check_complexity.py`, `tests/test_consolidate.py`,
  `tests/test_evidence_join.py`, `tests/test_flag_axis.py`,
  `tests/test_review_scope.py`, `tests/test_done_when.py`,
  `tests/test_mapping_purpose.py`, `tests/test_assumption_rules.py`, the two
  named `tests/test_schedule.py` tests and the three named
  `tests/test_dogfood_sync.py` tests: **391 passed, 1 skipped in 6.79s** (the
  skip: `test_kitlib_secret_classes.py:214`, "generic bearer token had no
  pre-WI-520 scan pattern").
- Slow modules and named slow tests, one run: `tests/test_trace_briefs.py`,
  `tests/test_consolidate_close.py`, `tests/test_check_complexity_cli.py`,
  the named tests of `test_mapping_purpose_cli.py` (1), `test_bootstrap.py`
  (2), `test_gen_arch_map.py` (2), `test_verdict_record.py` (4),
  `test_agent_loop_review.py` (8), `test_agent_loop_critique.py` (1),
  `test_integrate.py` (2) and `test_intake.py` (2): **86 passed in 100.23s**.

No failures, no errors.

## The two derived requirements: recommendation to the owner

Both SR-220 and SR-221 pass rule (c) of the spine-authoring skill as written:
the lens is recorded in `Hat-Refs` against roster hats whose `listens_for`
names the failure the row prevents, the rationale argues the lens rather
than the need's text, and the feedback upward is this section. The
recommendation does not change either verdict.

- **SR-220: keep it derived; widen SN-025's acceptance anyway.** The row's
  obligation is real regardless of the label: the loop mints work one
  finding at a time, so a queue that overlaps is the ordinary state, and
  SN-025's promise ("with no human curating what comes next") is broken the
  moment a human has to merge duplicates. That makes the obligation a
  consequence of the need's own text once the loop mints, which is closer to
  a needs defect (the why-cell trap, seen from the acceptance side) than to
  a derived constraint. I would add to SN-025's acceptance the sentence the
  rationale already drafts, "the loop keeps its own queue free of duplicated
  work", so a blind re-derivation from the need alone yields the row; the
  derivation label then comes off at the next amendment. The two lenses
  (once per queue state; one strong-tier session per judgement) still
  belong in the rationale as the reason for the ONCE-PER-STATE bound, which
  the widened need would not state.
- **SR-221: keep it derived; do not widen SN-012.** The listing is an inner
  loop that changes no bar and no gate, and its whole argument is operating
  cost plus evidence adequacy: two lenses, honestly named, on a need whose
  text is right-sizing. Widening SN-012 to name a test listing would fix a
  stakeholder outcome to one tool shape (the SN-tier instrument trap), and
  the need already yields the row's premise (small changes stay cheap). The
  label is doing exactly its job here: it tells a later reader this is a
  convenience the kit chose, not an outcome a stakeholder asked for, so it
  can be retired without a needs change if the cost argument stops holding.

## How the verdict was corrected before the act

The first recording of this file approved SR-220 and LLR-262. Before the
approval commit, the flipped tree was driven through `trace.py --root .
--strict-integrity` and `--strict`, and the two requirement-form FINDINGS
above surfaced (they fire on Approved rows only, and gate under `--strict`:
exit 1). An approval that turns the gate red is not an approval, so both
rows are returned in this correction, recorded in its own commit ahead of
the act; the act then flips 27 rows. The same run reports two new
advisories, LLR-205 and LLR-206 "Drafted but every citing TC is Approved",
which are the expected shadow of returning the design rows while approving
their cases, and nothing else moved.

## Dispositions

Seven rows are returned (five at the first sitting's correction, TC-201 and
TC-203 at the second sitting) and every cell of every row in scope is left
byte-exact by this verdict. The follow-up is drafted in
`docs/work/queued/WI-681-adjudicate-batch-b-first-approvals.md`,
`## Dispositions`, as one fenced TOML block; intake mints it at this row's
merge, or the coordinator folds it into an open item on the same surface.

## Non-blocking findings (surfaced, not acted on)

1. **LLR-205's rationale cites `docs/plans/2026-08-25-remap-alignment.md
   S8`** and TC-203's method opens a sentence with "Re-tiered". Both are
   provenance shapes the cell-hygiene rule discourages; SR-176's approved
   rationale carries the same plan-citation shape, so I did not return on it.
2. **TC-201 is Tier Full over a module that is not slow**, LLR-260's
   advisory class (the cell understates where its evidence runs, never
   falsely). Re-tiering it to Smoke would put a five-sample regression
   witness in the per-commit bar for a few milliseconds.
3. **SR-163's checker has no design row.** LLR-203 and LLR-204 each say so
   in their own text ("named by no design row's Module or CodeSymbol"), and
   TC-204 verifies the SR directly. `gen_arch_map.mapping_purpose_findings`
   and `bootstrap.delivery_inventory` are the undecomposed mechanisms; a
   design row for them is authoring work, not this act's.
4. **LLR-262 lists five modules and twenty-three symbols under one title.**
   Every mechanism serves the one property, and the wave-4 ruling on the
   `module` cell admits the shape, but the row is the widest design row in
   the registry and a later split by carrier (the verdict record, the
   done-when rules, the loop's two checks, the merge rung, the intake mint)
   would cost nothing in obligation. The lane fixing its "such as" may take
   the split in the same act or leave it; the return is on the phrase only.
5. **SR-221's acceptance clause "the commit bar is unchanged by it"** has no
   test of its own; it is carried by the command's act-and-exit shape.
6. **`trace.py`'s Critique-instrument advisory on SR-184** is a false
   positive of the lexical detector on a row whose subject is Critique
   records; the row's verification is Inspection throughout.
7. **The inspection result under TC-211's anchor records INCOMPLETE** for
   want of an SR-161 machine record (LLR-183's undischarged obligation).
   The case's text is right; the run is the harness's business.

## Second sitting, 2026-09-27 - after wave-5 arbitration rulings 2 and 3

The first act (8a960cf1) was reverted (c7c2128e). Ruling 3: TC-201 and
TC-203 carry changelog prose in their Method cells ("now ... was ...",
"BEFORE this table existed"; "Re-tiered into") and are returned with the
design rows they verify, LLR-205 and LLR-206, which were returned for the
same class of defect; their lines above are re-labelled. Ruling 2: the
LLR-205 disposition need not be widened here; the coordinator folds every
return into WI-616 with the whole fix stated (the rationale's "live, dated
finding" and plan citation, the Detail's pre-table narration, and the two
Method cells). A one-line note in this row's Dispositions records the two
added returns.

Counts after this sitting: 25 APPROVE (SR-183, SR-184, SR-185, SR-186,
SR-221; LLR-210, LLR-259, LLR-260, LLR-261, LLR-263; TC-199, TC-200,
TC-202, TC-208, TC-209, TC-210, TC-211, TC-252, TC-253, TC-254, TC-255,
TC-256, TC-257, TC-258, TC-259), 7 RETURN (LLR-205, LLR-206, TC-201,
TC-203, TC-204, SR-220, LLR-262).

OUTCOME: RETURN rows=32
