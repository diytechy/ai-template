<!--
Contracts: IF-047 — the interface seam this directory declares (process.md §8;
row of record in ../requirements/interfaces.toml).

Contract IF-047: the review record. One `*.md` verdict file per reviewer per
    round, each carrying its findings in the log's block form — one line per
    finding, `[SEVERITY]` then the anchor then the issue then the concrete
    change — and closing with one machine line,
    `VERDICT: APPROVE|CHANGES-REQUESTED findings=N`, which is the only line a
    reader parses. Beside them `scoreboard.txt` holds the
    decayed per-provider substance tallies and the round history the escalation
    policy consults. The scoreboard is ADVISORY state and never a source of
    truth: a declared finding count disagreeing with the counted finding lines
    is a tripwire, not a score, and nothing here auto-selects the next round's
    routing.
-->

# `docs/reviews/` — the review record

Retained evidence, one file per reviewer per round, plus the advisory
`scoreboard.txt`. These are records rather than navigation: they are referenced
from [`../log.md`](../log.md) at the round that produced them and are declared as
an expected orphan class in [`../orphans-allow`](../orphans-allow). Nothing here
is edited after the round closes — a later correction is a new round, not a
rewrite of an old verdict.
