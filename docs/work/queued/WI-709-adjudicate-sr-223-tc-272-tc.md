+++
id = "WI-709"
title = "adjudicate: SR-223, TC-272, TC-290, TC-297 - spine row(s) authored Drafted on merged trunk 83d866c..5934f4c await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-223"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-223", "TC-272", "TC-290", "TC-297"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-223 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria)
- TC-272 amended in `docs/test/test-cases.toml` (Evidence, Expected, Method)
- TC-297 authored in `docs/test/test-cases.toml`
- TC-290 amended in `docs/test/test-cases.toml` (Evidence, Expected, Method)

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
- LLR-280 [project-trajectory/scripts/agent_loop.py :: guardrails_core] tests: (see TC-290) — The guardrails payload is chosen by the policy's substring …
- TC-290 -> tests/test_guardrails_payload.py::test_the_longest_matching_substring_selects_the_payload; tests/test_guardrails_payload.py::test_a_guarded_session_carries_its_payload_and_the_policy_still_decides; tests/test_guardrails_payload.py::test_the_kit_ships_no_payload_so_every_model_gets_the_default_core

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-044 scripts/agent_route <- scripts/agent_loop: call select() -> the chosen row plus its reason; tiers strong · medium · quick
