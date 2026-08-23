+++
id = "WI-486"
title = "Tighten the Implements harvester to literal declarations, ship the reverse-coverage scanner report-only with its dial in process.toml, and re-word the shipped mandate onto the dial (OI-42 ruled (b)+(e), 2026-08-20)"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Executed OI-42's (b)+(e) ruling. `gen_arch_map.implements()` now harvests
only literal `Implements:` declarations through `backlink_ids()` — the
kit's single definition of a back-link, physically shared with the reverse
scanner and kept clearly separate from WI-478's `Contracts:` grammar,
deliberately WITHOUT its hard refusal (a SystemExit over a reflowed
docstring would break map generation for every adopter; an uncounted
wrapped id is instead reported honestly by the percentage). The map's
third column dropped 50 symbols / 62 links → 2 / 4 (subagent_gate's two
genuine declarations) — exactly OI-42's predicted honest state, pinned by
a regression test asserting on the COLUMN. The reverse scanner
(`--backlink-coverage`) measures per live LLR whether any literal
declaration under `[paths] src` (not tests) names it: 1/161 (0.6%),
REPORT-ONLY at the shipped `[checks] backlink_coverage_min = 0` dial, 50%
recorded as WI-487's target; the `backlink-coverage` check.py step rides
the strict ladder from DevStg-Tests. PROCESS.md:161 and
AGENTS.template.md:83/:102 re-worded onto the dial (AGENTS −5 bytes, 52
free under cap; PROCESS +470 flagged); the enforcement-audit Implements
row corrected to the measured truth; two RESYNC entries. The scanner's own
SR/LLR/TC mint DEFERRED to the owner: its permanence turns on WI-487's
outcome and every spine tier is human-held. Full suite 2643/13 green.

## Context

Executes the (b)+(e) half of OI-42's ruling; the campaign half is WI-487
(hard-blocked on this row — the scanner is the campaign's instrument and a
fabricating harvester would measure it with invented inputs).

- **(b) THE HARVESTER, FIRST.** `gen_arch_map.implements()` (~:178-189)
  harvests any spine id from nearby prose: 60 of the 62 back-links in the map
  were never declared, 13 name no live row, five are sorting/counter-example
  illustrations. Require the literal `Implements:` token before harvesting;
  pin with a test that prose is no longer harvested; expect the map's column
  to empty for 48 of 50 symbols — that is the honest state, say so in the
  change. SHARED LANDING: WI-478 fixes the same module's `Contracts:`
  continuation-line grammar — land together so `gen_arch_map`'s two parsing
  rules move once.
- **(e) THE SCANNER, REPORT-ONLY.** For each live LLR row, does any literal
  `Implements:` declaration in the declared source surface name it? Scoping
  per the ruling: surface = `docs/stack.ini` `[paths] src` roots and NOT
  `tests`; file types = a declared extension list defaulting to
  `gen_arch_map._MODULE_EXTS` extended per the row's list, overridable;
  grammar = the literal `Implements:` token ONLY, shared as ONE definition
  with (b)'s tightened harvester. The threshold dial lives in
  `docs/process.toml`, ships at `0`/off (report the number, gate nothing),
  with 50% recorded as the target WI-487 is sized to clear.
- **THE GUIDE RE-WORDS ONTO THE DIAL, NOT INTO RETREAT.** `PROCESS.md:161`
  and `AGENTS.template.md:83/:102` move from an unconditional mandate to the
  dialed obligation (an adopter raises the number their practice earns) —
  `AGENTS.template.md` is byte-capped, so net-neutral or shrinking.
- **CORRECT THE STALE AUDIT ROW IN THE SAME CHANGE** (the ruling's explicit
  clause): `docs/enforcement-audit.md`'s entry still says the column is empty
  and the scripts carry none — two carry it and the column is populated,
  nearly all fabricated.

RESYNC entries owed (shipped script + shipped guide both move). If the
scanner is itself to be traced, the SR/LLR/TC mint is part of this row's
scope — judge at execution against the check's permanence.
