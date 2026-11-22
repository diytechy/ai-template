<!--
The review record's format (IF-047) and the scoreboard's (IF-160) are
stated once, in `project-trajectory/scripts/score_reviews.py`, the
scorer that parses the one and writes the other (process.md §8).
-->

# `docs/reviews/` — the review record

Retained evidence, one file per reviewer per round, plus the advisory
`scoreboard.txt`. These are records rather than navigation: they are referenced
from [`../log.md`](../log.md) at the round that produced them and are declared as
an expected orphan class in [`../orphans-allow`](../orphans-allow). Nothing here
is edited after the round closes — a later correction is a new round, not a
rewrite of an old verdict.
