+++
id = "WI-980"
title = "adjudicate: LLR-167, LLR-183, LLR-273, SN-036, SR-161, SR-165, TC-161, TC-178, TC-211 - approved/routed cell(s) amended on merged trunk a51cfae..574cfcd (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-161", "SR-165"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-167", "LLR-183", "LLR-273", "SN-036", "SR-161", "SR-165", "TC-161", "TC-178", "TC-211"]
needs = ["OI-117"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-161 `AcceptanceCriteria`: 'A decomposition round writes the perspective record beside its artifacts; a declared perspective applicable to the deco…' -> 'For one completed decomposition round, the applicable perspectives resolve from the declared hats roster, the decomposi…'
- SR-161 `Coincident`: 'The need asks for each decomposition examined from every declared perspective; the machine-readable record of each pers…' -> "The need asks that each decomposition round is reviewed against every applicable declared perspective; the sitting's re…"
- SR-161 `Rationale`: 'Realizes SN-036 — a decomposition produced from one perspective can look complete while omitting security, operations o…' -> 'A decomposition produced from one perspective can look complete while omitting security, operations or first-use failur…'
- SR-161 `Requirement`: 'The delivered planning content shall leave, with every decomposition it produces, a machine-readable record of the decl…' -> 'When a decomposition round is reviewed, the delivered planning content shall provide every applicable declared perspect…'
- SR-161 `Title`: 'Decompositions carry a perspective record' -> 'Each decomposition round is reviewed against its applicable perspectives'
- SR-161 `Verification`: 'Test' -> 'Inspection'
- SR-165 `Rationale`: 'Realizes SN-040 — a free-form partition leaves no record of the alternatives weighed, so the next reviser cannot tell l…' -> 'Realizes SN-040 — a free-form partition leaves no record of the alternatives weighed, so the next reviser cannot tell l…'
- LLR-167 `Detail`: 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…' -> 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…'
- LLR-183 `Detail`: 'The machine-readable half of the perspective record, sited on the row rather than beside it. spine_carrier declares hat…' -> 'The row-level provenance part of perspective review, sited on the row rather than beside it. spine_carrier declares hat…'
- LLR-273 `Detail`: 'baseline_snapshot.registry_stamps(root) returns (registry, short rev, date) for each registry the record holds a commit…' -> 'baseline_snapshot.registry_stamps(root) returns (registry, short rev, date) for each registry the record holds a commit…'
- TC-161 `Method`: 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…' -> 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…'
- TC-178 `Expected`: 'Satisfies the acceptance folded into LLR-183 (parent SR-161)' -> "Satisfies LLR-183's Hat-Refs provenance, name-resolution, severity and effective-set mechanics; SR-161's perspective-re…"
- TC-178 `Method`: 'Four halves, one per claim the row makes. RESOLUTION: build a spine whose SR and LLR rows carry a Hat-Refs naming a hat…' -> 'Four halves, one per claim the row makes. RESOLUTION: build a spine whose SR and LLR rows carry a Hat-Refs naming a hat…'
- TC-211 `Expected`: 'A child within a required tier with no independent decision or verification purpose is an Inspection finding; otherwise…' -> "The actual review record names every applicable perspective's outcome, each child within a required tier has an indepen…"
- TC-211 `Inputs`: 'docs/test/inspection-procedures.md;SR-186;docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md;docs/a…' -> 'docs/test/inspection-procedures.md;SR-161;SR-186;docs/requirements/hats.toml;docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c…'
- TC-211 `Method`: 'Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality…' -> 'Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality…'
- TC-211 `Verifies`: 'SR-186' -> 'SR-161;SR-186'
- SN-036 `Acceptance`: 'Each decomposition has a machine-readable record of the declared perspectives, the applicability decision for each pers…' -> 'Each decomposition round is reviewed against every applicable declared perspective, and the review record names each pe…'

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
- LLR-172 [project-trajectory/scripts/trajectory_arch.py :: component_findings] tests: TC-166 — Component derivation record: element completeness + the ran…
- LLR-183 [project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/check_trajectory.py :: load_hat_names/hat_findings/effective_hats] tests: (see TC-178) — The perspective record as a resolvable cell: Hat-Refs, its …
- LLR-202 [project-trajectory/scripts/acceptance_record.py :: staged_hat_refs_findings/traced_cells] tests: TC-198 — Staged Hat-Refs amendment guard
- LLR-360 [project-trajectory/scripts/plan_briefs.py;project-trajectory/scripts/adjudicate_brief.py;project-trajectory/prompts/adjudicate-first-approval.template.md;project-trajectory/prompts/adjudicate-amendment.template.md :: sitting_hat_block/round_hat_block/round_questions/fill_hat_slot/sitting_tail/hat_surface_for_work_item/NOT_A_ROUND/HAT_SLOT/HAT_PARENTS/_roster_refusal/compose/combined_values] tests: TC-399 — Perspective questions in a decomposition-round sitting
- TC-166 -> tests/test_components_registry.py (to be extended at implementation)
- TC-178 -> tests/test_trace_hats.py::test_an_undeclared_hat_name_is_a_finding; tests/test_trace_hats_driven.py::test_an_undeclared_hat_reds_a_real_run_under_strict; tests/test_trace_hats.py::test_the_rule_is_vacuous_without_a_roster; tests/test_trace_hats.py::test_an_unparseable_roster_is_vacuous_not_loud; tests/test_trace_hats.py::test_coverage_is_one_advisory_and_never_a_finding; tests/test_trace_hats.py::test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories; tests/test_trace_hats.py::test_effective_hats_unions_the_parents; tests/test_trace_hats.py::test_a_parent_re_ruling_moves_the_child_with_no_child_cell_edited; tests/test_trace_hats.py::test_a_dangling_parent_contributes_nothing_rather_than_raising; tests/test_trace_hats.py::test_the_roster_path_matches_the_hats_module; tests/test_trace_hats.py::test_the_design_tier_is_checked_too_and_names_its_own_id; tests/test_trace_hats.py::test_an_absent_roster_file_reads_as_no_names; tests/test_trace_hats.py::test_a_hat_no_row_is_attributable_to_is_reported

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-009 scripts/check_trajectory -> scripts/check: exit-code 0 clean · 1 hard error · 2 usage
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/amendment_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-023 docs/work/ -> scripts/check_trajectory;external:downstream adopter: file one Markdown spec per row; status is the directory
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks, build; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup;scripts/plan_coverage;scripts/review_brief: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N; finding is - [BLOCKER|MAJOR|MINOR] <text>, case-insensitive;…
