+++
id = "WI-1029"
title = "The build and plan briefs render each work item's component context, derived from its SRs down to interfaces and files"
workstream = "process"
sr_refs = ["SR-146", "SR-159"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md#derived-never-authored"
needs = ["WI-1024", "WI-1027"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Variant F's ninth row (F-9), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Confirmed in the review-churn plan, revision 35: "the derived
component context in the build brief", built with item 11's phase-3 work,
with no `if_refs` cell on the work item (a third home once requirements name
their interfaces). The owner's question behind it (revision 20): is the
component a requirement ties into included in the work item, so the builder
can find the relevant component information?

Today no builder or planner prompt carries component or interface context
(`worker.template.md`, `plan-single.template.md`, the dual-plan templates,
and this repository's `.claude/agents/kit-builder.md`; rendered by
`prompts.py` and `plan_briefs.py`).

**The derivation (pointer rules, "Derived, never authored").** A work item's
`sr_refs` lead down the requirement tree (WI-1027) to its LLRs; through the
placement relation (a `constrains` cell, or the interface a verifying TC
names; WI-1024) to interfaces; to their owner components and `part_of`
ancestry; and to each component's files by their `Component:` headers
(WI-1021). An unplaced requirement is listed as unplaced. A work item with
no `sr_refs` gets the block from the interfaces its spec names, or none, said
plainly.

**Needs:** WI-1024 (placement through `constrains`) and WI-1027 (the tree
walk).

## Scope answers

- **S1.** One deliverable: the derivation and its rendering in the briefs
  that start a build or a plan.
- **S2.** No: a brief's rendered context informs a session; it holds,
  releases or authorizes nothing.
- **S3.** The block's inputs are registry rows and file headers, each
  already validated by its own check; an unresolvable link is rendered as
  "unplaced" or "unknown", never dropped.
- **S4.** `single`: a derivation and several prompt renderers.
- **S5.** No change to the architecture; a new view of it.
- **S6.** No new package, tool or service.

## Done-when

- [ ] One derivation returns a work item's component context: each
      component with its `part_of` ancestry, its boundary interfaces with
      their forms (through the effective-contract reader), the LLRs and
      SRs constraining them, and its files by header; plus the unplaced
      requirements. It uses WI-1027's one tree walk.
- [ ] The builder's and planner's briefs render that block, bounded in
      size by a stated rule (largest components summarized first), with
      the spec's own text unchanged.
- [ ] A work item with no `sr_refs` renders the block from the interfaces
      its spec names, or says it has none.
- [ ] Tests: a fixture work item renders its context; an unplaced LLR and a
      work item with no `sr_refs` each render their stated line; every
      importer of a changed module runs green.
- [ ] The shipped templates change with a RESYNC entry (variant F).
