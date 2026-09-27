+++
id = "WI-616"
title = "Absolutes: extend the check to needs, SRs and LLRs, then run the OI-37 sweep with it and route the rewrites for approval (S1)"
workstream = "scripts"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#11-absolutes-note-0"
buildtier = "strong"
priority = 3
safety_class = "ordinary"
needs = []
supersedes = "WI-617"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-617 (Run the OI-37 absolutes sweep over the needs, then the SRs, and route the rewrites for approval (S1)). The sweep's input is the check's output; the 2026-09-26 handoff already sequenced them check-then-sweep. One lane, check first. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

The sweep's rewrites are Drafted amendments: needs go to the owner's brief, SRs to the spine-acts batch. Open-world absolutes that are really assumptions are listed for C2 (WI-655), not written into it.

Ruled by the owner 2026-09-23 (sister plan S1, §1.1).

Today `trace_text.ac_advisories` (`:269-289`) scans only SR acceptance cells,
its term list (`:146-156`) holds only comparatives, and it only warns, while 23
of 27 needs and 66 of 79 SRs carry an absolute. The ruled matrix: needs scan
`need` and `acceptance`, waiver in `why`; SRs scan `requirement` and
`acceptance_criteria`, waiver in `rationale`; LLRs scan `detail`, waiver in
`rationale`; TCs are not scanned. The waiver reuses `recorded waiver:
<reason>`. The suppression predicate is defined before shipping: an absolute is
satisfied when it names its domain from a closed list (a registry, an id space,
a declared set), with the tokenization documented; whether a named domain is
really closed stays a review question in the spine-authoring skill. The OI-37
sweep is its own item.

## Done-when

- The check scans the matrix's cells, warn-first, and never TCs.
- A waiver uses `recorded waiver:` in the tier's reason cell; there is no second
  grammar.
- The suppression predicate and tokenization are documented where the check
  lives, with tests for a closed-domain absolute (suppressed), an open-world
  one (warned) and a waived one.
- The spine-authoring skill carries the closed-domain question, kit master and
  this repo's copy in sync.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-617 (Done-when, verbatim)

- Every absolute the check reports in a need is classified with a one-line
  reason, and then every one in an SR.
- Rewrites land as amendments for the approval route (needs to the owner's
  brief, SRs to the adjudicator); none is approved in the lane.
- Open-world absolutes that are really assumptions are listed for the
  assumption tier's C2, not written into it.
