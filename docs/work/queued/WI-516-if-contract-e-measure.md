+++
id = "WI-516"
title = "The (e) measuring pass: per-row contract verdicts over the 108 non-CLI rows, no cell edited (OI-62 ruled 2026-08-24)"
specref = "docs/requirements/open-items.toml#OI-62"
workstream = "requirements"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable


## Context

`OI-62` ruled (e) (owner, in session 2026-08-24; record:
[../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../log.d/2026-08-24-oi62-rule-and-spine-approval.md)):
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
