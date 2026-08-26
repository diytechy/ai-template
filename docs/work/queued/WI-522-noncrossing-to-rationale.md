+++
id = "WI-522"
title = "The non-crossing cleanup pass: M/X clauses leave `contract` for `rationale` (OI-63 ruled (d), 2026-08-25)"
specref = "docs/requirements/open-items.toml#OI-63"
workstream = "requirements"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable


## Context

`OI-63` is RULED (owner, in session 2026-08-25; record:
[../../log.d/2026-08-25-owner-rulings-oi63-oi64.md](../../log.d/2026-08-25-owner-rulings-oi63-oi64.md)):
option (d) — *"move information to rationale to clean up the contract text
itself before further shuffle."* This row is that pass.

**The input is the recorded verdict set, not a fresh reading.** For each row
the WI-516 verdict document
([../../plans/2026-08-25-if-contract-verdicts.md](../../plans/2026-08-25-if-contract-verdicts.md))
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
