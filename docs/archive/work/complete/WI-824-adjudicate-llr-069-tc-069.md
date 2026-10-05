+++
id = "WI-824"
title = "adjudicate: LLR-069, TC-069 - approved/routed cell(s) amended on merged trunk 883b3ed..7e001cc (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-069", "TC-069"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). The in-lane adjudicator returned both rows once and then ruled LLR-069 and TC-069 MEANING and blessed them (verdicts 001 and 002 under `docs/reviews/wi-803-plan-gate/`), and act seq 32 re-attested them. The low-level-requirements and test-cases registries are byte-identical to their `docs/archive/last_approved/` anchors at this row's mint (67b71374).

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-069 `Detail`: 'Parses rival plan tables; resolves clause/SR/IF coverage; validates dependencies; emits pairwise differences and distin…' -> 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…'
- LLR-069 `Title`: 'Rival-plan coverage comparison' -> 'Plan coverage gate'
- TC-069 `Expected`: 'Clean plans emit pairwise coverage; findings exit 1; malformed inputs exit 2; absent registries note without failure.' -> 'A reasoned exclusion passes and clean plans emit per-plan and pairwise coverage; a bad reference or plan graph, an unex…'
- TC-069 `Method`: 'Run rival plan coverage, reference, graph, absent-registry, and malformed-input cases.' -> 'Run dual and single plan coverage, reference, graph, exclusion, SR/TC-diff, absent-registry, and malformed-input cases.'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
