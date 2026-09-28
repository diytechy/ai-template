+++
id = "WI-706"
title = "adjudicate: LLR-173 - approved/routed cell(s) amended on merged trunk e1b7cf9..eecd656 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-173"]
+++

## Deliverable

Already judged and re-anchored; nothing owed. LLR-173's amended detail (the
coordinator's in-place amendment, wave-5 ruling 37) was judged MEANING and
blessed in WI-693's second sitting
(`docs/reviews/wi-693-adjudicate-llr-158-llr-173/001-ADJUDICATE-1d84d77c.md`),
and act seq 5 re-attested it (`docs/archive/last_approved/acts.toml`).
`trace.py --approve modified` shows no drift on it. This row was minted only
because the amendment and the act landed in one squash, and the sweep's
amendment trigger (`staged_spine_amendments`) does not check whether the
same range re-attests the row. That gap is recorded for the owner in the
wave-5 log fragment; it arises only when an amendment and its act share a
merge, as they did on this hand path.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-173 `Detail`: "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…" -> "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
