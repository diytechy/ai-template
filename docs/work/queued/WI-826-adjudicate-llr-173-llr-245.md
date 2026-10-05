+++
id = "WI-826"
title = "adjudicate: LLR-173, LLR-245, TC-173 - approved/routed cell(s) amended on merged trunk 7db81c9..fcf8120 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-173", "LLR-245", "TC-173"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-173 `Detail`: "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…" -> "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…"
- LLR-173 `Rationale`: 'The baseline had to leave git history. The derivation it replaces walked the registry for the newest commit at which a …' -> 'The baseline had to leave git history. The derivation it replaces walked the registry for the newest commit at which a …'
- LLR-245 `Detail`: 'refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows…' -> 'refresh_refusal computes, per registry, the absorbed rows (rows whose recorded copy claims approval and whose approved …'
- TC-173 `Expected`: 'Satisfies SR-179 AcceptanceCriteria via the LLR-178 detail contract' -> 'Satisfies SR-179 AcceptanceCriteria via the LLR-178 detail contract; satisfies LLR-302 by exercising the same two-tree …'
- TC-173 `Method`: 'Run the mirror-invariant half of the baseline-snapshot suite over real temp repos - the half TC-167 no longer covers, w…' -> 'Run the mirror-invariant half of the baseline-snapshot suite over real temp repos - the half TC-167 no longer covers, w…'
- TC-173 `Verifies`: 'SR-179;LLR-178' -> 'SR-179;LLR-178;SR-140;LLR-302'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
