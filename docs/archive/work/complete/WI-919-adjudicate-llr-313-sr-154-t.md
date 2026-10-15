+++
id = "WI-919"
title = "adjudicate: LLR-313, SR-154, TC-333 - approved/routed cell(s) amended on merged trunk 2025f84..b803dd0 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-146", "SR-154", "SR-235"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-313", "SR-154", "TC-333"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-913's in-lane sittings 010 (`docs/reviews/wi-913/010-ADJUDICATE-76dc674.md`: LLR-313 and TC-333 re-attested, act seq 113; LLR-337 and TC-367 approved, act seq 114) and 011 (`docs/reviews/wi-913/011-ADJUDICATE-c338f81.md`: SR-154 and TC-333 re-attested, MEANING, act seq 115) judged every row. At the landing b803dd01 the system, low-level and test registries are byte-equal to their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-154 `AcceptanceCriteria`: 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…' -> 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…'
- SR-154 `Rationale`: 'Realizes SN-026 (cross-family second opinions — every prior carrier of this contract demoted as routing machinery, so t…' -> 'Realizes SN-026 (cross-family second opinions — every prior carrier of this contract demoted as routing machinery, so t…'
- SR-154 `Requirement`: 'When unattended work reaches integration, the delivered loop content shall obtain each review or critique verdict the d…' -> 'The delivered loop content shall, when unattended work reaches integration, obtain each review or critique verdict the …'
- LLR-313 `Detail`: 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…' -> 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…'
- LLR-313 `SR-Refs`: 'SR-146;SR-235' -> 'SR-146;SR-154;SR-235'
- LLR-313 `Title`: 'Attended review and critique briefs and review records' -> 'Attended review, critique and single-plan briefs and records'
- TC-333 `Expected`: 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…' -> 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…'
- TC-333 `Method`: 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…' -> 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…'
- TC-333 `Tier`: 'Smoke' -> 'Full'
- TC-333 `Verifies`: 'SR-146;SR-235;LLR-313;IF-046;IF-047;IF-288;IF-289' -> 'SR-146;SR-154;SR-235;LLR-313;IF-046;IF-047;IF-288;IF-289'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-044 [project-trajectory/scripts/agent_route.py :: load_registry/resolve_enabled/parse_env/select] tests: (see TC-046) — Agent pair-row routing
- LLR-045 [project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/agent_brief.py :: main/reviewer_prompt/narrow_scope_line/narrow_reviewer_prompt/full_scope_line/review_round_brief/review_template_refusals/review_template/review_round_templates/close_round_scope/phase_tier] tests: (see TC-082) — Managed review dispatch
- LLR-046 [project-trajectory/scripts/score_reviews.py :: SEVERITIES/substance/fired_tripwires/record_round/_finding/parse_verdict] tests: (see TC-083) — Review substance scorer
- LLR-048 [project-trajectory/scripts/agent_brief.py :: load_critique_srs/build_scope_srs/critique_brief/critique_prompt] tests: (see TC-048) — Independent critique dispatch
- LLR-081 [project-trajectory/scripts/agent_route.py :: escalate/failure_action] tests: (see TC-084) — Fixed review escalation
- LLR-082 [project-trajectory/scripts/agent_loop.py :: main/critique_rounds/critique_failure_action] tests: (see TC-085) — Bounded critique rework

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-041 external:agent CLI <- scripts/agent_session: cli headless invocation; the prompt on stdin
