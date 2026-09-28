+++
id = "WI-696"
title = "adjudicate: SR-220, TC-279 - spine row(s) authored Drafted on merged trunk 4719865..bcf1e9a await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-220"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-220", "TC-279"]
+++

## Deliverable

Ruled in spine-acts batch C by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over four rounds (wave-5 rulings 37, 38, 44, 45). The verdict (`docs/reviews/wi-696-adjudicate-sr-220-tc-279-s/001-ADJUDICATE-1d84d77c.md`) ends:

    OUTCOME: APPROVE rows=1

The act (ledger seq 5) was narrowed to the LLR and TC registries (ruling 38): 31 rows approved, 9 amendment rows re-attested. The SR registry was not copied, so SR-220, SR-223 and SR-224 stay Drafted, and the SR-tier amendments (WI-695's cells, SR-178) stay drifted and visible for a later act. Batch C's returns are one follow-up, drafted in WI-695's `## Dispositions` and minted at this merge.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-220 amended in `docs/requirements/system-requirements.toml` (Boundary-Refs, DA-Refs)
- TC-279 authored in `docs/test/test-cases.toml`

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
- LLR-210 [project-trajectory/scripts/consolidate.py :: census_draft/queue_digest/queued_work/spine_digest/clusters/enacted_absorbs/judged_absorbed/consolidation_successors/prior_absorbs/prior_line/HAND_LABEL/parse_verdict/close_refusal/archive_absorbed] tests: TC-208 — The consolidation census: which queued rows are one work it…
- LLR-264 [project-trajectory/scripts/intake.py :: _cmd_consolidate] tests: - — The consolidation census as a command, its reason included
- TC-208 -> tests/test_consolidate.py::test_the_queue_digest_covers_the_four_fields_that_change_the_question; tests/test_consolidate.py::test_a_malformed_digests_cell_reads_as_no_recorded_digest; tests/test_consolidate.py::test_a_shared_open_item_edge_is_a_commissioning_signal; tests/test_consolidate.py::test_the_module_signal_reads_both_the_llr_join_and_the_row_prose; tests/test_consolidate.py::test_the_module_signal_does_not_fire_on_a_bare_module_name; tests/test_consolidate.py::test_two_disjoint_overlapping_pairs_make_one_candidate_set; tests/test_consolidate.py::test_a_pair_only_the_queue_conflict_detector_sees_seeds_a_cluster; tests/test_consolidate.py::test_the_spine_digest_hashes_whichever_carrier_is_live; tests/test_consolidate.py::test_no_row_is_minted_while_a_judgement_is_in_progress; tests/test_consolidate.py::test_no_row_is_minted_beside_a_pending_consolidation; tests/test_consolidate.py::test_a_queued_judgement_naming_a_candidate_refuses_by_name; tests/test_consolidate.py::test_a_queued_judgement_naming_no_candidate_holds_nothing_back; tests/test_consolidate.py::test_a_judgement_row_is_never_a_candidate_and_never_moves_the_queue_digest; tests/test_consolidate.py::test_the_example_row_is_never_a_candidate; tests/test_consolidate.py::test_a_queue_state_that_has_been_judged_is_never_judged_again; tests/test_consolidate.py::test_a_consolidations_own_successor_does_not_seed_the_next_census; tests/test_consolidate.py::test_a_hand_consolidations_host_is_not_read_as_judged; tests/test_consolidate.py::test_a_judgement_that_enacted_no_consolidation_makes_no_successor; tests/test_consolidate.py::test_a_consolidation_scope_with_no_recorded_verdict_makes_no_successor; tests/test_consolidate.py::test_a_queued_judgement_that_would_run_first_refuses_by_name; tests/test_consolidate.py::test_prior_labels_a_hand_consolidation_as_unjudged; tests/test_consolidate.py::test_prior_absorbs_reports_each_consolidations_absorbed_set; tests/test_consolidate.py::test_prior_keeps_an_absorption_after_its_successor_is_itself_absorbed; tests/test_consolidate.py::test_re_absorbing_a_row_a_consolidation_minted_is_refused_by_name; tests/test_consolidate.py::test_a_malformed_verdict_block_refuses_and_never_defaults; tests/test_consolidate.py::test_the_close_refuses_a_row_that_left_the_queue_by_name; tests/test_consolidate.py::test_an_absorbed_rows_scope_text_is_byte_identical_and_specref_kept
- TC-254 -> tests/test_consolidate_close.py::test_the_census_mints_one_row_and_refuses_a_second_while_it_is_pending; tests/test_consolidate_close.py::test_a_consolidate_verdict_absorbs_its_cluster_end_to_end; tests/test_consolidate_close.py::test_the_close_refuses_by_name_when_an_absorbed_row_was_claimed; tests/test_consolidate_close.py::test_queue_with_edge_writes_the_hard_needs_edge; tests/test_consolidate_close.py::test_return_to_draft_moves_the_row_back_with_the_finding_quoted
- TC-260 -> tests/test_intake.py::test_the_consolidation_census_dry_run_names_the_cluster_and_mints_nothing; tests/test_intake.py::test_the_consolidation_census_mints_one_row_then_says_why_not_again; tests/test_intake.py::test_a_refused_consolidation_mint_says_why_on_stderr_and_exits_1; tests/test_intake.py::test_the_consolidation_census_says_why_it_proposes_nothing

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-090 scripts/intake <- scripts/integrate;scripts/dispatch;scripts/agent_loop: call intake_after_merge (integrate) · mint_gap_rows (dispatch) · context_block (agent_loop, advisory)
- IF-091 scripts/acceptance_record <- scripts/intake;scripts/integrate: call staged_spine_amendments and staged_drafted_rows records (intake) · the merge_approval_refusal text, the amend…
- IF-092 scripts/wi_convert <- scripts/intake: call wi_convert.COLUMNS (the 19-column row schema) and write_spec_file; ConvertError is the mint's refusal input
