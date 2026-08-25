+++
id = "WI-516"
title = "The (e) measuring pass: per-row contract verdicts over the 108 non-CLI rows, no cell edited (OI-62 ruled 2026-08-24)"
specref = ""
workstream = "requirements"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

All 108 non-CLI `contract` cells read per row, never regexed; **no registry
cell edited**, as ruled. Both of `OI-62`'s obligations discharged.

**1. The durable per-row verdict record:**
[../../../plans/2026-08-25-if-contract-verdicts.md](../../../plans/2026-08-25-if-contract-verdicts.md)
— one line per row keyed by IF id, with the live cell length split into
restatement / irreducible remainder / non-crossing characters, the taxonomy
letters, and a per-row verdict naming the home each restated clause is
recoverable from. The table IS the derivation: summing its four numeric
columns reproduces every headline figure.

**2. The relocation question filed:** `OI-63`, pending, carrying the measured
per-family numbers and the kit-wide blast radius (PROCESS.md §8, the shipped
templates, `test_dogfood_sync` parity, a `RESYNC_PACK` entry). Watermark
`OI 62 -> 63`.

**The numbers, per family, reported separately.** Restatement by characters:
CLI (the `WI-512` comparison) **87.7%** → tranche 1 non-CLI `Provides` (19
rows) **75.9%** → tranche 2 `Consumes` (89 rows) **60.8%** → combined
**64.3%**. Rows carrying a remainder: 40.7% → **84.2%** → **61.8%** →
**65.7%**. The CLI family's result does NOT generalize, in the direction
`OI-62`'s option (d) predicted.

**Taxonomy extended, and said so.** `WI-512`'s three kinds (written artifact,
fail-loud guarantee, exclusion) plus seven: typed shape, closed vocabulary,
**consumer-side obligation**, posture, compatibility guarantee, counterparty
calling convention, and a NON-CROSSING class that is not a remainder kind at
all — 15.3% of characters are registry bookkeeping, provenance and argument
belonging in neither home. Four of the seven were already latent in
`WI-512`'s own kept clauses, which is recorded rather than claimed as new.

**The 5 ambiguous (d) tripwire findings triaged inside tranche 1**: all five
FALSE POSITIVES, each with a concrete narrowing (`IF-038` env-var keys,
`IF-072` the row's own endpoint cells, `IF-061` id placeholders, `IF-132`
root-relative first segment, `IF-143` an authoring fix). `IF-055` left
standing as ruled. Banked beside them: **`IF-117` is a second demonstrated rot
exhibit** (three false claims, unreachable by any token grammar) and two
further stale claims (`IF-057`, `IF-061`). `OI-61`'s (c) is NOT re-raised.

## Context

`OI-62` ruled (e) (owner, in session 2026-08-24; record:
[../../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../../log.d/2026-08-24-oi62-rule-and-spine-approval.md)):
MEASURE, DO NOT REWRITE. This row is that pass. It READS the 108 non-CLI
`contract` cells (`docs/requirements/interfaces.toml` — the 135 live rows minus
the 27 the WI-512 pass already thinned) with the same per-row discipline
WI-512's dossier used — never regexed, every clause classified by judgement —
and WRITES NO REGISTRY CELL. `safety_class = "ordinary"` is deliberate and is
this sentence's claim: the pass's outputs are a verdict record and a filed
open item, nothing on the spine; `buildtier = "strong"` is where the care
lives, because a fabricated or fatigued verdict poisons a kit-wide relocation
ruling even though no cell moves.

**The verdict, per row:** which clauses of the cell are RESTATEMENT — content
recoverable from the owner row, the module, or a generated reference — and
which are the IRREDUCIBLE REMAINDER, a typed fact with no other home (WI-512's
categories: a written artifact, a fail-loud guarantee, an exclusion in a
comparison; extend the taxonomy where the population demands it, and say so).
Run at (b)'s tranche grain: the non-CLI `Provides` rows first (structurally
closest to the measured CLI population), then the `Consumes` rows; report each
family's numbers SEPARATELY so a heterogeneous population cannot hide behind
one average. The comparison figure: WI-512's uniform-population result, 87.7%
restatement by characters, 11/27 rows (40.7%) carrying a remainder
(docs/log.d/2026-08-24-wi512-contract-generalization.md).

**The two ruled obligations, verbatim from the ruling — they are what makes
(e) better than (b) rather than worse:**

1. The per-row verdicts are recorded DURABLY as the follow-on pass's input —
   a committed document (docs/plans/ or docs/reviews/, the executor's call,
   named in the close), one line per row, machine-findable by IF id. Session
   notes do not satisfy this.
2. At the close, the relocation question is FILED as its own open item: does
   the irreducible remainder move to a contract header / output-interface
   declaration on the owning component's side — the `Contracts: IF-###`
   docstring line 57 of 76 modules already carry, harvested by
   `gen_arch_map.py`, policed both ways by `check_trajectory.py` — or does it
   stay in the cell? The brief carries the measured per-family numbers and
   the kit-wide blast radius (PROCESS.md §8, the shipped templates,
   `test_dogfood_sync` parity, a RESYNC_PACK entry).

**Folded in, not separate:** triage of the 5 ambiguous (d) tripwire findings
(`IF-038`/`IF-072`/`IF-061`/`IF-132`/`IF-143`) inside tranche 1; `IF-055` is
already-known real rot and its fix is whatever row owns it, not this one.

**Out of scope, explicitly:** editing any `contract` cell (that is the
follow-on's, under whatever the relocation ruling says); re-raising OI-61's
(c) (its condition — a demonstrated residual rot class — is unchanged).
