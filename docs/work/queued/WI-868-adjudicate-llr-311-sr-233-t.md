+++
id = "WI-868"
title = "adjudicate: LLR-311, SR-233, TC-332 - approved/routed cell(s) amended on merged trunk 7d7dd6f..02b0bff (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-233"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-311", "SR-233", "TC-332"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-233 `AcceptanceCriteria`: 'The review scope includes repository content agents write, supported configurations, and regressions of supported behav…' -> 'The review scope includes repository content agents write, supported configurations, and regressions of supported behav…'
- LLR-311 `Detail`: 'The §6 bold-lead paragraph `Review threat model` defines the review scope: normal-environment defects include repositor…' -> 'The §6 bold-lead paragraph `Review threat model` defines the review scope: normal-environment defects include repositor…'
- TC-332 `Expected`: 'The `Review threat model` bold lead occurs once; its paragraph contains `the content agents write into the repository`,…' -> 'The `Review threat model` bold lead occurs once; its paragraph contains `the content agents write into the repository`,…'
- TC-332 `Method`: 'Run test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing: it reads the §6 bold-lead paragraph, as…' -> 'Run test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing: it reads the §6 bold-lead paragraph, as…'

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
- LLR-311 [project-trajectory/PROCESS.md;project-trajectory/prompts/reviewer.template.md;project-trajectory/prompts/adjudicate-dispute.template.md :: Review threat model;REVIEWER;ADJUDICATE-DISPUTE] tests: TC-332 — Review threat-model definition and reviewer reference
- TC-332 -> tests/test_prompts.py::test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
