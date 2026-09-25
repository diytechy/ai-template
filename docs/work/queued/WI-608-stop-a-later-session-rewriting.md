+++
id = "WI-608"
title = "Stop a later session rewriting an earlier review round's verdict file: reproduce first, then fix (review pack C4)"
workstream = "unattended"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-24 code-facts research, by reading, not driven;
filed by the owner from the
review pack's Part C.

The implementer-touch check excludes the train's own review folder, and the
gate reads each round file at the branch tip (`integrate.py:1386` through
`kitlib/verdict.py:854`). So a later build session could edit an earlier
round's verdict file, and the gate would read the edited text. That would
undermine SR-154's independence: a verdict from a session that did not author
the work.

The owner's S9 ruling (sister plan §5, 2026-09-24) re-checks each review
session's recorded range at merge; a later builder session editing a round
file is outside that check.

## Done-when

- A test reproduces the rewrite, or shows it cannot happen, in which case this
  row closes with that evidence.
- If reproduced: a round's verdict is read as its review session committed
  it, so a later edit cannot change what the gate counts; prefer that to a
  new refusal (the antidote question).
- If a refusal is still needed, it names the round file and the commit that
  touched it.
