+++
id = "WI-705"
title = "adjudicate: LLR-282, LLR-283, LLR-284, SR-225, TC-292, TC-293, TC-294 - spine row(s) authored Drafted on merged trunk 4b7f6da..655c60a await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-225"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-282", "LLR-283", "LLR-284", "SR-225", "TC-292", "TC-293", "TC-294"]
+++

## Deliverable

Ruled in spine-acts batch D by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over three rounds (wave-5 rulings 49, 51, 52). The verdict (`docs/reviews/wi-705-adjudicate-llr-282-llr-283/001-ADJUDICATE-126cf5f2.md`) ends:

    OUTCOME: APPROVE rows=7

The one act (ledger seq 6) copied the SR, LLR and TC registries: 13 rows approved (SR-220 on its batch-C approval, confirmed unchanged), 76 re-attested. Those include the 66 WI-695 waivers and SR-178 carried from batch C, and the 81 routed pointer changes ruled explicitly, four of them completed first.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-225 authored in `docs/requirements/system-requirements.toml`
- LLR-282 authored in `docs/requirements/low-level-requirements.toml`
- LLR-283 authored in `docs/requirements/low-level-requirements.toml`
- LLR-284 authored in `docs/requirements/low-level-requirements.toml`
- TC-292 authored in `docs/test/test-cases.toml`
- TC-293 authored in `docs/test/test-cases.toml`
- TC-294 authored in `docs/test/test-cases.toml`

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
- LLR-282 [project-trajectory/scripts/agent_common.py :: decision_recording/DECISION_RECORDING_MODES/mode_word] tests: (see TC-292) — The decision_recording dial reads off when undeclared and r…
- LLR-283 [project-trajectory/scripts/kitlib/decisions.py :: DECISIONS_DIR/MODES/REQUIRED_KEYS/record_path/record_findings/owed/session_note] tests: (see TC-293) — The decisions record's path, format findings, obligation an…
- LLR-284 [project-trajectory/scripts/integrate.py :: _decision_record_refusal/_close_record_refusal] tests: (see TC-294) — The merge slot refuses a close that owes its decisions reco…
- TC-292 -> tests/test_decision_record.py::test_each_declared_value_reads_as_itself; tests/test_decision_record.py::test_an_undeclared_dial_reads_off; tests/test_decision_record.py::test_an_unrecognized_value_is_refused_and_read_as_record; tests/test_decision_record.py::test_a_padded_or_mixed_case_value_is_accepted_as_the_reader_reads_it; tests/test_decision_record.py::test_the_reader_and_the_validator_share_one_normalization; tests/test_decision_record.py::test_a_wrong_typed_value_is_refused; tests/test_decision_record.py::test_the_template_ships_off_and_this_repo_records
- TC-293 -> tests/test_decision_record.py::test_a_sound_record_yields_no_finding; tests/test_decision_record.py::test_a_record_with_no_entries_is_sound; tests/test_decision_record.py::test_each_missing_required_key_is_reported_by_entry; tests/test_decision_record.py::test_each_required_key_holding_non_text_is_reported; tests/test_decision_record.py::test_each_required_key_left_blank; tests/test_decision_record.py::test_a_non_table_entry_is_reported; tests/test_decision_record.py::test_a_decision_key_that_is_not_a_table_is_reported; tests/test_decision_record.py::test_a_malformed_hoist_is_reported; tests/test_decision_record.py::test_extra_keys_on_an_entry_are_not_judged; tests/test_decision_record.py::test_the_findings_never_raise; tests/test_decision_record.py::test_a_hoist_naming_an_absent_entry_is_reported; tests/test_decision_record.py::test_a_missing_hoist_is_reported; tests/test_decision_record.py::test_an_entry_id_outside_the_numbering_is_reported; tests/test_decision_record.py::test_an_unparseable_record_is_one_finding; tests/test_decision_record.py::test_a_000_entry_is_inert; tests/test_decision_record.py::test_the_shipped_template_is_sound_and_carries_the_example; tests/test_decision_record.py::test_the_record_path_is_one_file_per_run; tests/test_decision_record.py::test_which_closes_owe_a_record; tests/test_decision_record.py::test_the_session_note_names_the_path_only_under_a_recording_dial; tests/test_decision_record.py::test_a_build_session_is_handed_the_note_by_the_dial; tests/test_decision_record.py::test_an_adjudication_session_is_handed_the_note_too; tests/test_decision_record.py::test_a_review_session_is_not_handed_the_note
- TC-294 -> tests/test_decision_record_merge.py::test_a_recording_dial_refuses_a_close_without_its_record; tests/test_decision_record_merge.py::test_the_off_dial_reads_nothing; tests/test_decision_record_merge.py::test_a_lane_carrying_its_record_passes_the_rung; tests/test_decision_record_merge.py::test_a_malformed_entry_is_reported_and_does_not_refuse; tests/test_decision_record_merge.py::test_a_partial_close_without_its_record_is_refused_too; tests/test_decision_record_merge.py::test_a_partial_close_carrying_its_record_passes_the_rung; tests/test_decision_record_merge.py::test_a_dial_typo_is_refused_as_configuration_before_any_record; tests/test_decision_record_merge.py::test_a_padded_or_mixed_case_dial_reads_as_its_word

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
