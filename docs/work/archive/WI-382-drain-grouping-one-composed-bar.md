+++
id = "WI-382"
title = "Drain grouping: one composed bar per drain"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
disposition = "retired"
+++

## Deliverable

RETIRED 2026-07-31, unbuilt — **subsumed by WI-386** (the station protocol),
not abandoned. Reasoning in `docs/concurrency-v2.md` §A2 and §A6.1.

**Original scope, kept as the record.** Amortise the gate bar by composing ALL
finished claimed branches onto one candidate and barring ONCE per drain instead
of once per branch. Measured 2026-07-31: the full G3 bar is ~11 minutes, of
which `tests+coverage` is 634 s and all nineteen other steps total ~25 s — so
three WIs handled singly cost three bars where grouped they cost one. It was
the cheaper half of the owner's grouping requirement: the 3-bars-to-1 win
WITHOUT session grouping's failure coupling, since each WI is still built and
reviewed independently and only the BAR is shared. Red-bar attribution was the
trade, mitigated by falling back to per-branch barring on red.

**Why retired.** WI-386 makes *trunk is an ancestor* a precondition for
entering the merge queue, so the composed tree becomes byte-identical to the
branch tree and the integrator's composed bar **disappears** rather than being
amortised. A deletion beats a discount, and both of this row's benefits then
come for free and better:

- **The saving is exceeded.** The bar runs once per WI on the branch instead of
  twice — a self-reported builder close bar plus a mechanical integrator bar.
- **Class C coverage survives with better attribution.** Whichever branch merges
  second must refresh onto a trunk containing the first and bar there, so every
  pair composes exactly once on the real tree and a red names the refresh that
  caused it — no bisecting, and no per-branch fallback path to build.

Retired rather than deleted so the measurement and the reasoning stay traceable.
