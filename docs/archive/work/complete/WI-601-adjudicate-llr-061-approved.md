+++
id = "WI-601"
title = "adjudicate: LLR-061 - approved/routed cell(s) amended on merged trunk 67e6a50..dc36375 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Ruled in an attended sitting on `refactor_again` (the loop is paused), from the
before/after cells, against the design-row record last written at 2e1197fd:

    VERDICT: MEANING rows=1

LLR-061's `detail` gains an obligation: on a lane claimed with more than one
row, the worker prompt names every assigned row with its walk state, taken from
the walk's own two-part completion predicate. The traced `code_symbol` gains
`assignment_block`. A prompt that names the focus row alone satisfies the
BEFORE text and fails the AFTER. The verdict is
`docs/reviews/wi-601-adjudicate-llr-061-approved/001-ADJUDICATE-f263118.md`.

The design-row tier is released to the adjudicator, so the re-attestation is
this row's. The new text was judged blessable: it sits within SR-026, it is
true of `agent_loop.assignment_block` at f263118, and three tests in TC-061's
evidence file drive it. The re-anchor is a separate commit, joint with WI-603's
LLR-167, so that the whole-file copy carries no unruled text.

One finding, folded into WI-603's disposition and filed as WI-645: TC-061's
`method` does not name the multi-row block its evidence file already tests.

Review: codex Sol (medium) confirmed the call, the blessing checks and the
re-anchor's safety; its wording corrections (re-attestation is the copy, not the
verdict; the collateral's exact row set) are applied. A Fable arbiter upheld the
one-row count (WI-566's rule).

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-061 `Detail`: 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …' -> 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
