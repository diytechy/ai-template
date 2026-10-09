# Rubric — Scope critique where a row is born (WI-852)

**Adjudicates:** the scope of one work item as written, at the point it comes
into being: filed by hand, or minted from a lane (a successor draft, a
disposition, a split). It is judged before the row can be claimed.
**Used by:** an independent critic from another model family than the row's
author, rendered from the kit's critique brief by
`review_brief.py critique --rubric docs/rubrics/scope-critique.md`. The artifact
is the spec file and its `specref` target, never code.

## Intent

The owner's ruling 2 of 2026-10-07 (`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`):
scope is settled where a row is born, by a scope critique, and there is no
lane-size tripwire. A large row may be kept whole on purpose, but that choice
is made once, recorded in the spec, and not re-argued in the lane. The second
question exists because WI-841's verdict file came to release holds and
authorize acts without anyone stating who may write it or what its readers do
with a bad one (`docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` §1 and §2).

## Anchors

**S1 — Each independently landable deliverable is named.** List every
deliverable that could land on its own. If there is more than one, say which
lands first. The owner may keep them together; the answer is then recorded in
the spec. *Bad:* a Done-when that bundles a mechanism, a new brief class and a
new sitting under one row with no word on which lands first.

**S2 — Authority over a hold, an act or a gate is named.** Say whether any
deliverable gives a file authority over a hold, an act or a gate. If one does,
the spec carries a `## Trust` section before the claim: the file's producer and
what a failed write looks like, every consumer by path, and the ruling for an
absent, unreadable, failed or malformed input (PROCESS.md §3 "When a guard is
owed", linked, not restated). *Bad:* a verdict file that releases a hold, with
no stated reader rule.

**B1 — A deliverable hidden in prose.** A Context paragraph that commits to
work the Done-when does not list.

**B2 — A split that breaks the minting rule.** A proposed split whose successor
rows would be minted on a work branch rather than filed on trunk before the
claim.

## Verdict

One `- [BLOCKER|MAJOR|MINOR] <anchor> -> where/why -> the concrete change ->
@owner` line per finding, each citing S1, S2 or a B anchor, then the brief's one
machine line. A finding naming a new failure mode proposes a new `B#` anchor.
