<!--
Contracts: IF-047, IF-160 — the interface seams this directory declares
(process.md §8; rows of record in ../requirements/interfaces.toml).

Contract IF-047: the review record. One `*.md` verdict file per reviewer per
    round, each carrying its findings in the log's block form — one line per
    finding, `[SEVERITY]` then the anchor then the issue then the concrete
    change — and closing with one machine line,
    `VERDICT: APPROVE|CHANGES-REQUESTED findings=N`, which is the only line a
    reader parses. A declared finding count that disagrees with the counted
    finding lines is a tripwire, not a score.
Contract IF-160: `scoreboard.txt` in this directory, written by the review
    scorer and by nothing else. A four-line `#` banner naming its writer, then
    one `provider <name> substance=<float> rounds=<int>` line per provider in
    sorted order, then one `round <n> verdict= tier= margin= primary=
    tripwire= contradiction=` line per recorded round in order. Recording a
    round rewrites the whole file — the standing tallies decayed by a declared
    factor, the new round appended — LF on every platform, so the same inputs
    give the same bytes. Recording a round first reads the standing tallies
    back (the read side is the directory's read row), then rewrites the whole
    file. It is ADVISORY state: nothing here auto-selects the next round's routing, and no gate takes it as
    evidence.
-->

# `docs/reviews/` — the review record

Retained evidence, one file per reviewer per round, plus the advisory
`scoreboard.txt`. These are records rather than navigation: they are referenced
from [`../log.md`](../log.md) at the round that produced them and are declared as
an expected orphan class in [`../orphans-allow`](../orphans-allow). Nothing here
is edited after the round closes — a later correction is a new round, not a
rewrite of an old verdict.
