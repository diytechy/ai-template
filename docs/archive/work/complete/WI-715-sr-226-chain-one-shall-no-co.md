+++
id = "WI-715"
title = "SR-226 chain: one shall, no coincident waiver, B-01; close LLR-287's 'such as' and TC-300's 'minimal'"
workstream = "process"
sr_refs = ["SR-226"]
specref = ""
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Deliverable

Built by one builder, reviewed SOUND by Codex Sol at 2305a648 (`docs/reviews/2026-09-27-wave5/sol-wi715.md`). The six cell fixes batch E's adjudicator drafted, on three Drafted rows: SR-226 states one `shall` (the record and its two warn-only reports as the observable responses), drops the `coincident` waiver it could not honestly hold under approved SR-193 (now unclassified), and adds B-01; LLR-287's rationale closes its "such as" to the case set `retire.records` tests; TC-300 names its fixture in a new `parameters` cell instead of "minimal". With the three rows approved in a scratch tree, `trace.py --strict` shows no form finding. The rows stay Drafted for the next spine-acts batch.

## Context

Drafted by WI-712 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE — six cells across three rows, amended in place with every status
left `Drafted`, then the first-approval adjudication the merge's sweep mints.
Before handing back, flip the three rows to `Approved` in the working tree,
run `python project-trajectory/scripts/trace.py --root . --strict`, confirm
`form-findings=0`, and flip them back: the gate is silent on a Drafted row.

1. `SR-226.requirement`: it carries two `shall`s ("shall write ... and shall
   report ..."), against PROCESS.md §3 ("one requirement, one `shall`"; the
   Singular characteristic), and the form gate reports an Approved SR with
   more than one. Re-word to ONE `shall` over the row's one decision — the
   record a retired row leaves, found by its id — with the same-change write,
   the four cells and the two warn-only reports kept as the response's
   qualifiers. NOT a split: the acceptance criteria stay byte-exact, the
   obligation set is unchanged, and LLR-286, LLR-287, TC-299 and TC-300 keep
   their `SR-Refs`/`Verifies`.
2. `SR-226.coincident`: drop the cell. It fails approved SR-193's test ("why
   its own specification ALONE delivers its needs"): the rationale itself
   says SN-010's text does not name this outcome, and SN-010 is delivered
   jointly with the link check, the vision tag and every generated
   artifact's `--check`. The row is honestly unclassified, the state the SR
   rung reports without failing, until OI-97 gives the tier a class for a
   derived requirement. Do not invent a DA and do not re-word the waiver.
3. `SR-226.boundary_refs`: add `B-01`. The text's "write, in the same change
   that deletes the row" is a governed write from a session into a registry
   and a tracked record — B-01's crossing, carried for the same reason by
   SR-174 and SR-176. B-09 stays.
4. `LLR-287.rationale`: "a clone with less history, such as a shallow
   checkout in continuous integration, reads unknown" — `such as` is an
   open-ended enumeration the form gate refuses ("the scope cannot be
   closed ... enumerate it"). Keep the argument; close the set to the
   checkouts `retire.records` reads as unknown (an uncommitted record, a
   shallow clone, a squashed history) and drop the escape phrase.
5. `TC-300.method` and `TC-300.parameters`: "the shared minimal project" —
   `minimal` is on the form gate's vague-term list ("no test can settle it —
   name the measurable"). It is a fixture's nickname, not a threshold: name
   the fixture (`tests/traj_fixtures.py make_repo`, with `_rendered_history`
   for the committed variants) in a `parameters` cell, and let Method say
   "the shared fixture project". No arm of the Method changes.

OUT OF SCOPE: SR-226's rationale (it argues the derived lens correctly and
feeds back upward), its acceptance criteria, `Hat-Refs` MAINTAINER and
`SN-Refs` SN-010; every other cell of LLR-287 and TC-300 (read at HEAD and
found blessable; Detail, Title, Expected and every evidence pointer stand);
the two approved children; `retire.py`, `traj_views.py`, `gen_trajectory.py`
and their tests; and the `Form` advisory `trace.py` prints on SR-226 (no SR
in the registry declares one).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-286 [project-trajectory/scripts/retire.py :: RETIRED_DIR/CENSUS/fragment_text/parse_fragment/drop_row/retire/parse_exclusions/seed_census/missing_findings/shallow_boundary/edited_findings/retirement_findings/records/main] tests: (see TC-299, TC-300) — The retirement record's one home: the command that deletes …
- LLR-287 [project-trajectory/scripts/rendering/traj_views.py;project-trajectory/scripts/gen_trajectory.py :: retired_panel/_retired_view/fresh_view/_unresolved] tests: (see TC-300) — The dashboard lists the retirement records with their delet…
- TC-299 -> tests/test_retire.py::test_retiring_a_live_row_removes_it_and_writes_its_record; tests/test_retire.py::test_a_retirement_without_a_successor_records_none; tests/test_retire.py::test_each_refusal_writes_nothing; tests/test_retire.py::test_an_id_already_recorded_is_refused; tests/test_retire.py::test_the_log_fold_leaves_retirement_records_in_place; tests/test_retire.py::test_the_seed_declares_the_spent_ids_once; tests/test_retire.py::test_a_spent_id_without_a_record_is_reported; tests/test_retire.py::test_the_missing_rule_is_pure_over_its_four_sets; tests/test_retire.py::test_an_unreadable_record_is_reported; tests/test_retire.py::test_a_record_changed_after_it_landed_is_reported; tests/test_retire.py::test_an_uncommitted_record_is_not_an_edit; tests/test_retire.py::test_off_git_the_edit_report_is_silent; tests/test_retire.py::test_the_reports_never_change_the_exit_code; tests/test_retire.py::test_trace_prints_the_reports_as_advisories; tests/test_retire.py::test_the_seed_never_declares_an_excluded_id; tests/test_retire.py::test_a_malformed_exclusion_is_refused; tests/test_retire.py::test_the_census_is_replaced_only_before_it_lands; tests/test_retire.py::test_a_shallow_clone_says_the_record_is_unverifiable; tests/test_retire.py::test_a_record_outside_the_declared_format_is_unreadable; tests/test_retire.py::test_the_final_newline_alone_is_not_a_body; tests/test_retire.py::test_an_exclusion_run_excludes_every_id_in_it_and_nothing_else
- TC-300 -> tests/test_retire_dashboard.py::test_a_landed_record_reads_its_landing_commit; tests/test_retire_dashboard.py::test_an_uncommitted_record_reads_unknown; tests/test_retire_dashboard.py::test_a_record_in_a_root_commit_reads_unknown; tests/test_retire_dashboard.py::test_a_shallow_clone_reads_unknown; tests/test_retire_dashboard.py::test_records_come_in_tier_then_number_order; tests/test_retire_dashboard.py::test_no_record_renders_no_tab; tests/test_retire_dashboard.py::test_the_panel_renders_one_escaped_row_per_record; tests/test_retire_dashboard.py::test_the_caption_counts_the_ids_retired_before_the_record; tests/test_retire_dashboard.py::test_the_dashboard_carries_the_tab_only_when_a_record_exists; tests/test_retire_dashboard.py::test_a_fabricated_deleting_commit_is_stale_where_history_answers; tests/test_retire_dashboard.py::test_a_checkout_that_cannot_resolve_the_commit_accepts_the_page; tests/test_retire_dashboard.py::test_any_other_change_to_a_record_is_stale

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-011 scripts/gen_trajectory -> scripts/check: exit-code 0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --check
- IF-024 docs/work/ -> scripts/gen_trajectory;external:downstream adopter: file None
- IF-056 scripts/check_trajectory <- scripts/gen_trajectory: call check_trajectory loaders: validate, read_registry_rows, load_wis, load_known_srs, read_trajectory_enabled, WI…
- IF-071 scripts/schedule <- scripts/gen_trajectory: call load_registry_rows, load_wis, frontier, evaluate; empty when the module is absent
- IF-102 scripts/spine_carrier <- scripts/trace;scripts/acceptance_record;scripts/check_trajectory;scripts/gen_arch_map;scripts/plan_coverage;scripts/spine_rules;scripts/traj_status;scripts/check_test_first;scripts/rejudge;scripts/retire: call spine_carrier.load / resolve / stem / carriers / rows_from_text / rows_seq_from_text / status_cells; rows und…
- IF-227 scripts/traj_parse <- scripts/gen_trajectory: call need_assumptions(root) -> {need id: {assumptions: [{id, text, standing, level, citing}], coincident, unclassi…
