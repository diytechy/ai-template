+++
id = "WI-901"
title = "A disposition brief composes for a close whose commit range is empty"
workstream = "process"
sr_refs = ["SR-144"]
specref = "project-trajectory/scripts/adjudicate_brief.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 (overnight leg 01, decision D-022 in
`docs/decisions/coordinator-2026-10-10.toml`). WI-894's disposition brief for
WI-828's partial close would not compose: `adjudicate_brief.disposition_values`
refused with "the range 24a3ff4f38..24a3ff4f38 does not resolve in this
repository". The range resolves. `_commit_facts` returns None both when git
fails and when the range holds no commits (an empty `git log` and an empty
`--name-status`), and the caller reports both as unresolvable. A close that
committed nothing (WI-828 stopped after build round 1 with no commit) is a
legitimate shape the handback writer records, so every such close's
disposition fails to compose. WI-894's sitting ran on the coordinator's note
alone; the adjudicator read the report and the repository itself.

## Done-when

- A disposition row whose report declares an empty but resolvable range
  composes its brief, with commit facts that say the range holds no commits;
  a range git cannot resolve still refuses, naming git's failure.
- Tests: an empty range composes and states it is empty; an unresolvable
  range refuses; a non-empty range is unchanged.
- The rows the change makes untrue (LLR-167's chain; the change amends neither SR-208 nor LLR-246, per WI-903's census note) state it and pass
  adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script changes).
