+++
id = "WI-993"
title = "An owner-held step is an open item: any step only the owner can take is filed as a pending item the row's needs cites, never only as handoff prose"
workstream = "process"
sr_refs = ["SR-049"]
specref = "docs/specs/WI-993.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand on 2026-11-02 (attended) at the owner's request, carrying the
owner's ruling of 2026-10-25 and its seven filing calls
(coordinator-2026-11-02 D-004); the ruling and its calls are the spec of
record, `docs/specs/WI-993.md`. Call (5)'s pending items (OI-121 to OI-123)
and OI-124 were filed in the same commit, outside this row. Owes its scope
critique before its claim.

## Done-when

- PROCESS.md's open-items paragraph states the ruling once: an open item is
  anything keeping a row from building forward (an owner decision, an owner
  act, an approval or signature, a credential, the owner's presence), filed
  as a pending row the held work item's `needs` cites in the same commit;
  the coordinator-cycle skill's "Owner-held steps" step 3 points at it
  instead of restating it, and every other site stating the narrower
  "a decision only the owner can make" rule is amended to point there.
- A lane keeps its claim at a planned owner-held step only while the
  pending item is filed and cited on trunk; the text sites of OI-70's
  "partial is the only stop" are amended to say so; a re-scoping owner
  answer still closes the lane partial (call 1).
- A sitting verdict that rules MEANING on a held-rung row writes the
  pending open item for its owner act (the row, the verdict, the command),
  so no coordinator files it by hand (call 1, mechanized).
- The owner queue on `open-items.html` counts claimed rows that cite a
  pending item, not only queued ones (call 2).
- A routine push files no item (call 3); an act's item closes by the
  owner's ruling or a delegated decision (call 4).
- No detector is built for a session that stopped and filed nothing
  (call 7).
- RESYNC_PACK: one entry; adopters' owner-held rows gain pending items at
  their next re-sync.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
