+++
id = "WI-825"
title = "adjudicate: LLR-140, LLR-270 - approved/routed cell(s) amended on merged trunk eae1f48..8868537 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-140", "LLR-270"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). The in-lane adjudicator ruled LLR-140 and LLR-270 MEANING and blessed them (verdict `docs/reviews/wi-822-context-guard/004-ADJUDICATE-4e8f207.md`), and both were re-attested at act seq 33 in the WI-822 lane. The low-level, system and test-case registries are byte-identical to their anchors under `docs/archive/last_approved/` at the landing.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-140 `Detail`: 'claim: §2.3 steps 1+2 with the refusal ladder, cheapest first (tracked pause via agent_common.tracked_pause; an existin…' -> 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
