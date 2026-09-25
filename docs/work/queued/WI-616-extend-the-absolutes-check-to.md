+++
id = "WI-616"
title = "Extend the absolutes check to needs, SRs and LLRs, warn-first, reusing the recorded-waiver grammar (S1)"
workstream = "scripts"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#11-absolutes-note-0"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

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
