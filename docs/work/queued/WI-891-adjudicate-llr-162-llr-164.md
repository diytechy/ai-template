+++
id = "WI-891"
title = "adjudicate: LLR-162, LLR-164, TC-192 - approved/routed cell(s) amended on merged trunk 1916363..ad91c7b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-162", "LLR-164", "TC-192"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-162 `Detail`: '`load` reads a shipped template (or an operator override) and raises a named `PromptError`; `fill` refuses an unknown s…' -> '`load` reads a shipped template (or an operator override) and raises a named `PromptError`; `fill` refuses an unknown s…'
- LLR-164 `Detail`: '`render` is PURE — it takes no arguments and reads only the shipped templates — so `--check` and the write path cannot …' -> '`render` is PURE — it takes no arguments and reads only the shipped templates and composed fragments — so `--check` and…'
- TC-192 `Method`: 'gen_prompt_catalog.render is exercised directly rather than read. test_the_catalogue_lists_every_shipped_prompt_with_it…' -> 'gen_prompt_catalog.render is exercised directly rather than read. test_the_catalogue_lists_every_shipped_prompt_with_it…'
- TC-192 `Verifies`: 'SR-146;LLR-164' -> 'SR-146;LLR-162;LLR-164'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
