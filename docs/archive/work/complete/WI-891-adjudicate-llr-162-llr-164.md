+++
id = "WI-891"
title = "adjudicate: LLR-162, LLR-164, TC-192 - approved/routed cell(s) amended on merged trunk 1916363..ad91c7b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-162", "LLR-164", "TC-192"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-882's in-lane amendment sitting 001 (`docs/reviews/wi-882/001-ADJUDICATE-a8883e2.md`) ruled every listed row MEANING, blessed it and re-attested it (act seq 98, docs/archive/last_approved/acts.toml). At the landing ad91c7b4 the system, low-level and test registries are byte-equal to their approved snapshots under docs/archive/last_approved/.

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
