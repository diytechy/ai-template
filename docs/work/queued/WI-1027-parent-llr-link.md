+++
id = "WI-1027"
title = "LLRs decompose under an authored parent link, and every walk from an SR to its LLRs walks the tree"
workstream = "process"
sr_refs = ["SR-157", "SR-186", "SR-049", "SR-241"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md"
needs = ["WI-1023"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's seventh row (F-7), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F-call 5 with decomposition
(b) and an authored parent-LLR link (revision 35), and revision 36's
"every derivation that walks SR → LLR walks the tree". A child LLR names
one parent LLR and carries no `sr_refs`; only a top-level LLR carries
`sr_refs`; a child's SR is derived up the chain; the links are acyclic. A
parent is discharged by its children plus an integration TC.

Every LLR today is top-level, so no row migrates until a child is written.
The cost is in the readers. About thirty scripts read `sr_refs`; the walks
that matter are the orphan and coverage rules (`trace.py`), the stage
derivation (`derive_stage.py`), the review's scoped test set
(`review_set.py`, through its one walk in `kitlib.spine`), the acceptance
and adjudication briefs, the planning briefs, blast radius (WI-1024), the
build brief's component context (WI-1029) and the dashboard. The lane's
plan enumerates the walks from the code. PROCESS.md §4's ladder text
("TERMINAL", "the tier does not recurse, the activity does") changes with
decomposition (b).

**Needs:** WI-1023 (the loader refuses undeclared requirement-tier keys, so
`parent` is added to the declared set there, not beside it). It may be
built beside WI-1024 and lands after WI-1023.

## Scope answers

- **S1.** One deliverable: the cell, its rules and every walk changed
  together, so a child LLR's tests never drop out of the scoped set
  unseen (revision 36). The dashboard's requirement-tree view lands in the
  same lane, after the walks.
- **S2.** The scoped test set gates the review start (WI-995); this row
  changes the set's derivation, not its authority. No new authority.
- **S3.** `parent` admits one live LLR id; a cycle, a dead id, a child
  carrying `sr_refs`, or a top-level LLR with none is a finding.
- **S4.** `single`: schema, many reader families, a gate's input.
- **S5.** Adds the requirement tree; components and interfaces are
  unchanged.
- **S6.** No new package, tool or service.

## Done-when

- [ ] LLR rows accept an optional `parent` cell naming one live LLR. A child
      carries no `sr_refs`; a top-level LLR carries at least one. A cycle,
      a dead id or either `sr_refs` breach is a finding failing `--strict`.
- [ ] One walk, in `kitlib.spine`, returns an SR's LLRs down the tree, and
      a child's SR up the chain. Every reader that walks SR → LLR uses it:
      the orphan and coverage rules, the stage derivation, the review's
      scoped test set, the acceptance and planning briefs, blast radius and
      the dashboard. The plan's enumeration is in the Deliverable.
- [ ] A parent LLR is discharged by its children plus an integration TC
      that verifies it; a parent with children and no such TC is a finding.
- [ ] The dashboard's spine view shows the requirement tree as the
      component view shows nesting.
- [ ] PROCESS.md §4's ladder text states decomposition (b) once; the
      spine-authoring skill and `spine-questions.md` point at it.
- [ ] Tests build a three-level tree in a fixture and show each walk
      reaching a grandchild's TCs (red before the walk changes); every
      importer of a changed module runs green.
- [ ] A RESYNC entry (variant F) gives adopters the cell; existing rows need
      no change.
