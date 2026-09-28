+++
id = "WI-702"
title = "adjudicate: LLR-279, LLR-280, LLR-281, SR-223, SR-224, TC-289, TC-290, TC-291 - spine row(s) authored Drafted on merged trunk 47f8b57..4ecdc99 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-223", "SR-224"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-279", "LLR-280", "LLR-281", "SR-223", "SR-224", "TC-289", "TC-290", "TC-291"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-223 authored in `docs/requirements/system-requirements.toml`
- SR-224 authored in `docs/requirements/system-requirements.toml`
- LLR-279 authored in `docs/requirements/low-level-requirements.toml`
- LLR-280 authored in `docs/requirements/low-level-requirements.toml`
- LLR-281 authored in `docs/requirements/low-level-requirements.toml`
- TC-289 authored in `docs/test/test-cases.toml`
- TC-290 authored in `docs/test/test-cases.toml`
- TC-291 authored in `docs/test/test-cases.toml`

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
- LLR-281 [project-trajectory/scripts/gen_skills_index.py :: refuse_short_descriptions/short_descriptions/DESCRIPTION_FLOOR] tests: (see TC-291) — The skills-index check refuses a description under the floo…
- TC-290 -> tests/test_guardrails_payload.py::test_the_longest_matching_substring_selects_the_payload; tests/test_guardrails_payload.py::test_a_guarded_session_carries_its_payload_and_the_policy_still_decides
- TC-291 -> tests/test_skills_index.py::test_check_refuses_a_description_under_the_floor; tests/test_skills_index.py::test_every_shipped_description_clears_the_floor

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-019 scripts/gen_skills_index -> external:downstream adopter: file skills/INDEX.csv: banner comment, header, one row per skill (name, scope, stacks, domains, phases, tags, desc…
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-035 project-trajectory/skills/ -> scripts/gen_skills_index;scripts/bootstrap: file SKILL.md frontmatter: name, scope, stacks, domains, phases, tags; each other file in the skill directory, mat…
