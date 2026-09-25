+++
id = "WI-615"
title = "Terminology pass: SRs read as system specifications and LLRs as design expectations, prefixes unchanged (Q9, S2)"
workstream = "process"
specref = "docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md#11-staging"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Ruled by the owner: Q9 (prose name *system specification*, 2026-09-24) and
the sister plan's S2 (LLR -> *design expectation*, 2026-09-23; flag closed
2026-09-24). This is the assumption-tier plan's package T.

One prose pass over the kit's docs, prompts and dashboard labels, plus one
PROCESS.md glossary line each: `SR-###` rows are system specifications and
`LLR-###` rows are design expectations (the prefixes are historical), and
"expectation" inside a need row is ordinary English, not the tier. No old log
is edited. Id prefixes and rung names (`DevStg-LLReqs`) are unchanged here; the
prefix rename is a separate deferred item, taken last. `RESYNC_PACK.md` §4 is
the concept-rename table, and `check_vocab` may need the new words.

## Done-when

- PROCESS.md carries the glossary lines, including the ordinary-"expectation"
  note.
- Kit docs, prompts and dashboard labels call SR rows system specifications and
  LLR rows design expectations; grep evidence names what still says otherwise,
  and why (ids, rung names, quotations).
- No file under `docs/log.md`, `docs/log.d/` or `docs/archive/` is edited.
- `RESYNC_PACK.md` carries the rename where adopters or `check_vocab` need it;
  byte budgets and the dogfood sync hold.
