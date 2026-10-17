+++
id = "WI-936"
title = "adjudicate: SR-154 - approved/routed cell(s) amended on merged trunk a278cb2..6515aee (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-154"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-154"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-154 `Requirement`: 'The delivered loop content shall, when unattended work reaches integration, obtain each review or critique verdict the …' -> 'The delivered loop content shall obtain, when unattended work reaches integration, each review or critique verdict the …'

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
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-044 scripts/agent_route <- scripts/agent_loop;scripts/session_service: call select() -> the chosen row plus its reason; load_registry(path) -> {id: row}, errors; parse_env(cell) -> {nam…
