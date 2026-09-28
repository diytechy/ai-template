+++
id = "WI-716"
title = "adjudicate: LLR-287, SR-226, TC-300 - spine row(s) authored Drafted on merged trunk 9b16cde..3bb6186 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-226"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-287", "SR-226", "TC-300"]
+++

## Deliverable

Ruled in spine-acts batch F by an independent Fable adjudicator from the kit's own brief, routed pointer cells included. Codex Sol cross-reviewed it in two rounds (wave-5 rulings 58 and 59): NOT YET SOUND on the first act, and SOUND on the re-taken act, after the correction returned LLR-270 (a receipt phrase) and ruled LLR-177's `SR-Refs`. The verdict (`docs/reviews/wi-716-adjudicate-llr-287-sr-226-t/001-ADJUDICATE-d7e1be0e.md`) ends:

    OUTCOME: APPROVE rows=3

The one act (ledger seq 8) approved SR-226, LLR-287, TC-300, TC-263, TC-265, TC-266 and TC-267, and re-attested LLR-177 and TC-172 on a MEANING verdict. SR-222, SR-227, LLR-266 to LLR-270, TC-262, TC-264 and TC-268 returned on fourteen cells, mostly receipts and history in standing cells. The follow-up is WI-718's one Dispositions draft, minted at this merge.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-226 amended in `docs/requirements/system-requirements.toml` (Boundary-Refs, Coincident, Requirement)
- LLR-287 amended in `docs/requirements/low-level-requirements.toml` (Rationale)
- TC-300 amended in `docs/test/test-cases.toml` (Method, Parameters)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

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
