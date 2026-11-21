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
that matter are listed in Done-when 2, and the lane's plan confirms the
list from the code. PROCESS.md §4's ladder text ("TERMINAL", "the tier does
not recurse, the activity does") changes with decomposition (b).

**Siblings.** Blast radius is WI-1024's and the build brief's component
context is WI-1029's; both use this row's walk. WI-1029 waits on this row.
WI-1024 and this row both wait only on WI-1023 and may land in either
order: whichever lands second moves blast radius onto the tree walk.

## Scope answers

- **S1.** One deliverable: the cell, its rules and every walk changed
  together, so a child LLR's tests never drop out of the scoped set
  unseen (revision 36). The dashboard's requirement-tree view lands in the
  same lane, after the walks.
- **S2.** The scoped test set gates the review start (WI-995); this row
  changes the set's derivation, not its authority. No new authority.
- **S3.** Closed in Done-when 1 and 3: the cell's form and its findings,
  and when a parent is discharged.
- **S4.** `single`: schema, many reader families, a gate's input.
- **S5.** Adds the requirement tree; components and interfaces are
  unchanged. Re-cut LLRs (text only, drifting): LLR-001 and LLR-201 (the
  join and orphan rules), LLR-367 (the review test set), LLR-186 (the
  effective stage), LLR-197 (the spine row vocabulary); the lane's plan
  completes the list from the walks it changes.
- **S6.** `needs` WI-1023: the loader refuses undeclared requirement-tier
  keys there, so `parent` joins the declared set rather than sitting
  beside it. No new package, tool or service.

## Done-when

- [ ] LLR rows accept an optional `parent` cell naming one live LLR. A child
      carries no `sr_refs`; a top-level LLR carries at least one. A cycle,
      a dead id or either `sr_refs` breach is a finding failing `--strict`.
- [ ] One walk, in `kitlib.spine`, returns an SR's LLRs down the tree, and
      a child's SR up the chain. These readers use it: the orphan and
      coverage rules (`trace.py`, `coherence.py`), the stage derivation
      (`derive_stage.py`), the review's scoped test set (`review_set.py`),
      the acceptance brief, the adjudication briefs
      (`adjudicate_brief.py`), the planning briefs, blast radius (when
      WI-1024 has landed; otherwise WI-1024 adopts it) and the dashboard.
      The Deliverable lists every reader changed.
- [ ] **A parent's discharge.** A parent is an LLR some child's `parent`
      names. It must itself be named in the `verifies` of at least one TC
      (its integration TC); a parent with none is a finding failing
      `--strict`. An SR's coverage and the stage are derived over the
      whole descendant tree: each descendant counts exactly as a top-level
      LLR counts today, so an unverified or `Drafted` descendant holds its
      SR as one would now.
- [ ] The dashboard's spine view shows the requirement tree as the
      component view shows nesting.
- [ ] PROCESS.md §4's ladder text states decomposition (b) once; the
      spine-authoring skill and `spine-questions.md` point at it. The S5
      LLRs are amended (drifting, listed for adjudication).
- [ ] Tests build a three-level tree in a fixture and show each walk
      reaching a grandchild's TCs (red before the walk changes), a parent
      with no integration TC, and an unverified grandchild holding its SR;
      every importer of a changed module runs green.
- [ ] A RESYNC entry (variant F) gives adopters the cell; existing rows need
      no change.
