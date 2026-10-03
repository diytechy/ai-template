+++
id = "WI-768"
title = "adjudicate: SR-033 - approved/routed cell(s) amended on merged trunk 30ee386..4ba5890 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-033"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-033"]
+++

## Deliverable

Spine-acts batch O (act seq 22): SR-033's WI-667 amendment (the release
checklist's assumptions section; `SN-Refs` gaining SN-043) ruled MEANING and
re-attested by an independent Claude Opus 5.5 adjudicator in one combined act
with WI-769, WI-772 and WI-773.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-033 `AcceptanceCriteria`: 'Running the generator emits the checklist content: the perf-budget section lists each warn-tier PB with its id and allo…' -> 'Running the generator emits the checklist content: the perf-budget section lists each warn-tier PB with its id and allo…'
- SR-033 `Rationale`: 'Realizes SN-004 — the release gate has a generated checklist surfacing the budgets a human must tick off, because a war…' -> 'Realizes SN-004 — the release gate has a generated checklist surfacing the budgets a human must tick off, because a war…'
- SR-033 `Requirement`: 'The delivered release-checklist generator shall emit the release-gate checklist, including the warn-tier performance bu…' -> 'The delivered release-checklist generator shall emit the release-gate checklist, including the warn-tier performance bu…'
- SR-033 `SN-Refs`: 'SN-004' -> 'SN-004;SN-043'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-296 [project-trajectory/scripts/gen_release_checklist.py :: assumption_checklist_lines] tests: TC-310 — Assumption confirmations in the release checklist
- TC-033 -> tests/test_check_perf.py::test_release_checklist_lists_perf_budgets
- TC-310 -> tests/test_release_assumptions.py

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)`; assumption confi…
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-107 scripts/spine_carrier <- scripts/gen_release_checklist: call spine_carrier.load for SR, TC, LLR and IF rows by phase; folded_needs for the need tier; an int phase renders…
- IF-228 scripts/rejudge <- scripts/intake;scripts/gen_release_checklist;scripts/adjudicate_brief: call observation_test_cases(root, rev) · due_cases(root, rev, now) -> tc, row, why, digest, record, changed · chec…
