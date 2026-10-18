+++
id = "WI-947"
title = "adjudicate: LLR-300, LLR-322, TC-345 - approved/routed cell(s) amended on merged trunk 45dfc96..9c6b7af (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-300", "LLR-322", "TC-345"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-927's in-lane checkpoint sitting
`docs/reviews/wi-927/005-ADJUDICATE-65a3405.md` blessed LLR-300, LLR-322
and TC-345 as MEANING+BLESS, and the lane's act turn took act seq 130,
which re-attested all three. At the landing 9c6b7af35 the low-level and
test registries are byte-equal to their approved snapshots under
docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-300 `Detail`: 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…' -> 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…'
- LLR-322 `Detail`: 'When the shipped coordinator-hook example declares guard hooks and the machine-local settings leave them off, an intera…' -> "The guard hooks' state over the shipped example and the machine-local settings is one of none, absent, on or occupied, …"
- LLR-322 `Rationale`: "Coordinator hooks change a contributor's interactive environment, so an explicit opt-in preserves existing configuratio…" -> "Coordinator hooks change a contributor's interactive environment, so an explicit opt-in leaves a declined setup reversi…"
- LLR-322 `Title`: 'Dev-setup consents to coordinator-hook opt-in' -> 'Coordinator guard hooks are read by name and installed only with consent'
- TC-345 `Expected`: "Consent enables the coordinator hooks in the machine-local settings, bound to the opt-in's interpreter, replacing only …" -> "The state is none, absent, on or occupied according to the guard events' command names. A missing machine-local file, o…"
- TC-345 `Method`: 'Decline and accept the interactive coordinator-hook offer with existing settings, and run the hook command against exam…' -> 'Read the four states over the Trust shapes; drive the consented install at the developer-setup offer and lease take, in…'
- TC-345 `Verifies`: 'SR-032;LLR-322' -> 'SR-032;LLR-322;SR-229;SR-237;LLR-300'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
