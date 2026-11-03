+++
id = "WI-990"
title = "adjudicate: SR-174, TC-158 - approved/routed cell(s) amended on merged trunk 2f4ebb2..8894988 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-174"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-174", "TC-158"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-174 `AcceptanceCriteria`: 'Two actors finishing against the same tree cannot obtain the same work-item identity; an identity freed by deleting its…' -> 'Two actors finishing against the same tree cannot obtain the same work-item identity; an identity freed by deleting its…'
- SR-174 `Rationale`: 'Identity allocation is its own decision, not a consequence of serialization: serializing the writer makes a COLLISION u…' -> 'Identity allocation is its own decision, not a consequence of serialization: serializing the writer makes a COLLISION u…'
- SR-174 `Requirement`: 'The delivered loop content shall allocate each work-item identity at most once, so that no two concurrent actors receiv…' -> 'The delivered loop content shall allocate each identity it mints at most once. Work items are minted on the integration…'
- SR-174 `SN-Refs`: 'SN-025' -> 'SN-025;SN-027'
- SR-174 `Title`: 'Work-item identity is allocated once and never re-issued' -> 'Identity is allocated once and never re-issued'
- TC-158 `Expected`: 'A live id above its mark, a missing space, a malformed line, an absent file, a lowered mark and a hand-raised mark each…' -> 'A live id above its mark, a missing space, a malformed line, an absent file, a lowered mark and a hand-raised mark each…'
- TC-158 `Method`: "Run the id-watermark suite. It drives trace.py's CLI so the rules are asserted on the EXIT CODE, not just as a function…" -> "Run the id-watermark suite. It drives trace.py's CLI so the rules are asserted on the EXIT CODE, not just as a function…"

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-153 [project-trajectory/scripts/intake.py :: intake_after_merge/_amendment_drafts/mint_gap_rows/parse_dispositions/parse_disposition_section/next_wi_id/context_block/_inject_open_item/_pending_oi_lines/adjudication_action/flip_verified/_standing_successors/_title_identity_refusal/_repoint_owed] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…
- LLR-154 [project-trajectory/scripts/integrate.py :: integrate_one/_lane_bar_directives/_refresh_bar] tests: (see TC-148) — The merge slot's post-merge intake arm
- LLR-362 [project-trajectory/scripts/id_carrier.py;project-trajectory/scripts/trace.py :: WATERMARK/CARRIER_REF/TRUNK_SPACES/MAX_COUNT/LOST_RACE/RESERVE_VERB/CORRECTION_LINE/MARK_LINE/Refused/carrier_spaces/parse_marks/parse_corrections/parse_reservations/record_line/parse_counts/_count/plan_reservation/fold/carried/fold_lag/_ref_value/carrier_tip/carrier_text/_plumb/write_carrier/reserve/receiving_sides/record_history_findings/reserve_ids/check_work_item/committed_reservations/_baseline_texts/_reserved_highs/_basis/_trunk_name/_committed_marks/_cmd_reserve_ids/_cmd_fold_ids/render_watermark/bump_watermark/correct_watermark/_mark_history_findings] tests: TC-401;TC-158 — The shared carrier and reservation record for lane-minted i…
- LLR-363 [project-trajectory/scripts/id_carrier.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/integrate.py;project-trajectory/scripts/check.py;project-trajectory/hooks/pre-commit :: LANDING_DIRS/ids_at/_added_ids/_reissued_ids/_read_landing/_outside_lines/_retired_lines/_id_name/landing_lines/landing_refusal/rev_fold_lag/_watermark_at/live_ids/live_ids_at/landing_id_refusal/landing_fold_lag/fold_watermark/_reserved_id_refusal/_landing_ready/_merge_trunk_in/_lane_base/_fold_watermark_conflict/_fold_carrier_in/_reserved_ids_refusal/_squash_work_items/_reserved_ids_mode/FOLD_REMEDY] tests: TC-402 — A landing admits only its reserved identities and carries t…
- TC-147 -> tests/test_intake.py; tests/test_intake.py::test_a_replay_re_points_a_late_dependent_to_the_full_successor_set; tests/test_intake.py::test_a_title_match_off_the_drafts_lineage_refuses_the_mint; tests/test_intake.py::test_a_drafts_title_match_on_its_own_lineage_stays_standing; tests/test_intake.py::test_a_replay_with_nothing_left_to_re_point_commits_nothing; tests/test_intake.py::test_drafts_and_adoptions_together_hold_the_full_successor_set; tests/test_intake.py::test_a_recorded_adoption_re_points_a_dependents_needs
- TC-148 -> tests/test_integrate_station.py; tests/test_dispatch.py

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/amendment_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
