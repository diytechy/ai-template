+++
id = "WI-797"
title = "Ship the kit glossary and align PROCESS.md's lane-lifecycle wording"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

`project-trajectory/GLOSSARY.md` ships the approved design note's glossary, reconciled with the checkpoint ruling A1 (eligible families per kind, family exclusions as ranked preferences, the `plan-dual` kind), with a strength entry naming where strength is defined today, both independence exceptions, and unbuilt machinery labelled Planned with what runs today. PROCESS.md links to it in one sentence (it has no lane-lifecycle section to rename: decisions D-001); it is kit-owned and scaffolds to `docs/glossary.md`. Codex 6.1 Sol: round 1 one MAJOR (the second independence exception, fixed), round 2 SOUND at 35ee2d87. Decisions: `docs/decisions/wi-797.toml`.

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-glossary, the first row of the note's
dependency graph (README "The dependency graph of successor rows", group
`contracts`). OI-101 Q5 puts the glossary in a kit-shipped
`project-trajectory/GLOSSARY.md`, linked from PROCESS.md; the README's "Glossary
draft" carries the text, and D-020 leaves the file to this row. One term per
concept: it retires the "adjudicator vs retained adjudicator" split. The README
matrix also gives this row the state names in the docs, and ch.1 §9.1 gives it
PROCESS.md's lane lifecycle (lane state, condition, decision). README A1 asks the
glossary to say where strength is defined today. D-019 sets the tier to medium.

## Done-when

- `project-trajectory/GLOSSARY.md` exists with the README's glossary draft, every
  term once, reconciled with the checkpoint ruling where they differ (README A1:
  family exclusions are ranked preferences within a kind's eligible families, and
  the `plan-dual` kind of D-032).
- PROCESS.md links to it, and PROCESS.md's lane lifecycle names the lane states,
  substates and conditions with the glossary's words (ch.1 §9.1), stated once and
  linked rather than restated.
- The glossary or the text it links says where strength is defined today, per
  README A1: the row's `tier` in `docs/agents.toml`, the row's effort, the
  per-phase default tier, each WI's `buildtier`, escalation (up only), the plan
  `Tier` column and the OI-103 Q5 dial.
- No code changes.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus `check_docs` and the byte budget (`byte-budget-guard` on PROCESS.md).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit, adding the kit-owned
  `GLOSSARY.md`.
