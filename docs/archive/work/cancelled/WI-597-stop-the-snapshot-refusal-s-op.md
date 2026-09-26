+++
id = "WI-597"
title = "Stop the snapshot refusal's opening line claiming nothing authorises an act whose next line names what it authorises"
workstream = "process"
specref = ""
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Deliverable

CANCELLED as DONE ELSEWHERE (backlog audit, owner go-ahead 2026-09-26).

WI-635 (e123eb6d) rewrote both lines this row targets: the header now reads
"…for rows this act neither approves nor re-attests:" and the scoped arm
"This act WRITES …", and `tests/test_baseline_snapshot.py` asserts on the
header text, the pin this row asked for. Prose elsewhere that still tells a
user to run `intake.py snapshot` without naming `--reattests` is drafted
separately (the wave-2 draft G).

## Context

Drafted by WI-591 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`baseline_snapshot._refusal_text` opens every refusal with the constant
"…and nothing in this working tree authorises it:", then — on the scoped arm —
follows it with "This act DOES authorise <registry>…". WI-584 ruled the gate
scoped to the act's write set and added the second sentence, but left the first
one standing, so the arm the ruling built is the arm whose message contradicts
itself in consecutive lines. WI-584's own `## Context` named this header as
false and worth correcting "under either reading", and its `## Deliverable`
states the naming went "in place of" it; driven at the WI-591 tip, it did not.
IN SCOPE: branch the OPENING line on the same `scope` the middle line already
branches on — the empty-write-set arm keeps today's wording, because there the
claim is true; the scoped arm says what is actually wrong, which is that the
listed rows would ride along on an authorisation that does not cover them. Pin
both arms with a test that asserts on the header text, not just on "REFUSED" —
the existing tests pass today precisely because none of them reads the first
line. EXPLICITLY NOT IN SCOPE: the scoping rule itself, the unscoped arm, and
the three-ways-forward paragraph — all ruled and correct; this is the wording
WI-584 said it had already fixed.
