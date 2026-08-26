+++
id = "WI-522"
title = "The non-crossing cleanup pass: M/X clauses leave `contract` for `rationale` (OI-63 ruled (d), 2026-08-25)"
specref = ""
workstream = "requirements"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

`OI-63` option (d) executed over all 46 `nonx > 0` rows of
[../../requirements/interfaces.toml](../../../requirements/interfaces.toml).
**36 rows MOVED** their M/X clauses out of `contract` into `rationale`, **8 are
FLAGGED** (citation-only or rot — not movable into a cell whose declared grammar
refuses a citation, and deletion was not ruled), **2 RE-JUDGED** as not
non-crossing at all (`IF-061`, `IF-078`). Measured, not estimated: `contract`
over the 108-row population **43,995 → 37,859 characters (−6,136, −13.9%)**;
over the 36 edited rows **18,611 → 12,475 (−33.0%)**; rows carrying a
`rationale` **1 → 37**; `trace.py`'s Contract-argues advisory **27 → 17 rows**,
its over-ceiling advisory **30 → 17**, all IF advisories **67 → 42**. Of
`OI-63`'s 6,715-character non-crossing population, **6,136 (91.4%) left the
cell**; the residual 679 is the ten flagged/re-judged rows.

The three cross-review re-adjudications all CONFIRM the reviewer and none of
them moved a span: `IF-050`'s *"every consumer reads it through
kitlib.stage.read_stage"* is a false universal (`kitlib/stage.py` names the two
display surfaces that deliberately do not) — a correction, not a relocation;
`IF-061`'s dual-write clause is rot and its both-homes allocation is live, so
its `nonx` is re-judged 78 → 0; `IF-098`'s remainder re-measures **219 → 81**
characters against the harvested-summary R2 surface.

The record is the per-row disposition addendum appended to
[../../plans/2026-08-25-if-contract-verdicts.md](../../../plans/2026-08-25-if-contract-verdicts.md),
so the placement re-ask reads one document. RESTATEMENT and REMAINDER clauses
are untouched, every row read `Drafted` before and after, and no kit-side file,
script or test changed — the pass is registry-and-docs only.

Two findings owed the owner, from checking the destination before writing into
it at scale: **nothing lints an IF `rationale`** (`IF_REASON_CELLS` is
`Notes`/`SignalNote`; no cap, no render, no reader) so the template's declared
grammar is author-held — this pass verified its own 36 cells against
`trace_text.provenance_tokens` (0 tokens); and an **empty** `rationale` is a
hard `spine_carrier` refusal, so a row carries the key or omits it. The registry
header now documents the field, which it did not.

## Context

`OI-63` is RULED (owner, in session 2026-08-25; record:
[../../log.d/2026-08-25-owner-rulings-oi63-oi64.md](../../../log.d/2026-08-25-owner-rulings-oi63-oi64.md)):
option (d) — *"move information to rationale to clean up the contract text
itself before further shuffle."* This row is that pass.

**The input is the recorded verdict set, not a fresh reading.** For each row
the WI-516 verdict document
([../../plans/2026-08-25-if-contract-verdicts.md](../../../plans/2026-08-25-if-contract-verdicts.md))
marks with non-crossing content (`nonx > 0`), move the M/X clauses out of
`contract` into the row's `rationale` field — the schema's own home, used
once today (`IF-141`). The verdict line is the starting claim and the
executor RE-JUDGES each clause before moving it (the verdicts are accurate
to the clause, not the character, by their own statement). The three rows
the cross-review addendum flags — `IF-050`, `IF-061`, `IF-098` — are
re-adjudicated here where their spans are touched, with the addendum's
evidence as input.

**Scope, tight.** Only M/X content moves, and `rationale` is the ruled
destination. RESTATEMENT and REMAINDER clauses are untouched — the owner's
"before further shuffle" is the boundary, and the placement re-ask happens
on the cleaned cells under a separate ruling. Content the executor believes
should be deleted outright (a changelog duplicating git history, carrying no
argument) is FLAGGED in the close with its row id, not deleted — deletion
was not ruled. Every IF row reads `Drafted`, so no approved text is touched
and the registry is off-spine; the ordinary safety class is that sentence's
claim, and `buildtier = "strong"` is where the care lives — a clause moved
wrongly pollutes the very cells the re-ask will be ruled on.

**Done-when:** every `nonx > 0` row is dispositioned (moved / re-judged as
not-actually-non-crossing with the reason / flagged for deletion); the
verdict document gains a per-row disposition addendum so the follow-on
re-ask reads one record; the before/after figures are measured, not
estimated (the 6,715-character population OI-63 names, and trace.py's
Contract-argues advisory count — 27 rows today — re-measured after);
`check_trajectory --strict` and the interface-registry checks stay clean.
