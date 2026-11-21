+++
id = "WI-1029"
title = "The build and plan briefs render each work item's component context, derived from its SRs down to interfaces and files"
workstream = "process"
sr_refs = ["SR-146", "SR-159"]
specref = "docs/plans/2026-10-11-review-churn/pointer-rules.md#derived-never-authored"
needs = ["WI-1024", "WI-1025", "WI-1027"]
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
(`worker.template.md`, `plan-single.template.md`,
`dual-plan-planner.template.md`, and this repository's
`.claude/agents/kit-builder.md`; rendered by `prompts.py` and
`plan_briefs.py`).

**The derivation (pointer rules, "Derived, never authored").** A work item's
`sr_refs` lead down the requirement tree (WI-1027) to its LLRs; through the
placement relation (a `constrains` cell, or the interface a verifying TC
names; WI-1024) to interfaces and their forms (WI-1025's reader); to their
owner components and `part_of` ancestry; and to each component's files by
their `Component:` headers (WI-1021). A work item with no `sr_refs` gets the
block from the interfaces its spec names, or none, said plainly.

## Scope answers

- **S1.** One deliverable: the derivation and its rendering in the briefs
  that start a build or a plan.
- **S2.** No: a brief's rendered context informs a session; it holds,
  releases or authorizes nothing.
- **S3.** Closed in Done-when 1 to 3: the size bound, the citation grammar
  for a work item with no `sr_refs`, and the two rendered states for links
  that do not resolve. Bounded to supported workflows and kit routes
  (PROCESS.md §6).
- **S4.** `single`: a derivation and several prompt renderers.
- **S5.** The brief renderers (`prompts.py`, `plan_briefs.py`, CMP-008)
  gain an input: the derivation. It lives in `kitlib.spine`, on the
  shared-kernel surface, so that import is not a seam. Where reaching the
  effective-contract reader crosses from CMP-008 into a non-kernel CMP-006
  file, the lane declares the `call` row, `Drafted`. Re-cut LLRs (text
  only, drifting): LLR-162 (prompts catalogued), LLR-071 (the dual-plan
  briefs); the lane's plan completes the list.
- **S6.** `needs` WI-1024: placement through `constrains`; WI-1025: the
  effective-contract reader renders each interface's form; WI-1027: the
  tree walk. WI-1021's headers are an ancestor through WI-1024 and
  WI-1023. No new package, tool or service.

## Done-when

- [ ] One derivation returns a work item's component context: each
      component with its `part_of` ancestry, its boundary interfaces with
      their forms (through the effective-contract reader), the LLRs and
      SRs constraining them, and its files by header. It renders two
      states for what does not resolve: "unplaced" for a requirement with
      no placement interface, and "unknown" for a cited id with no live row.
      It uses WI-1027's one tree walk.
- [ ] **The size bound.** The block is at most 12,000 characters.
      Components are ordered by how many of the work item's requirements
      they hold, most first; once the bound would be passed, each
      remaining component renders one line (its id, title, and counts of
      interfaces and files). The spec's own text is never cut.
- [ ] **A work item with no `sr_refs`.** The block is built from every
      `IF-NNN` token in the spec's `## Context` and `## Done-when` sections
      that names a live interface row; a token naming none renders as
      "unknown". With none, the block says the work item has no component
      context. When `sr_refs` is non-empty, spec tokens are not read.
- [ ] `worker.template.md`, `plan-single.template.md`,
      `dual-plan-planner.template.md` and `.claude/agents/kit-builder.md`
      render the block; the prompt catalogue (`gen_prompt_catalog.py`,
      SR-146) regenerates.
- [ ] Tests: a fixture work item renders its context; an unplaced LLR, an
      unknown id, the size bound's summary lines and a work item with no
      `sr_refs` each render as stated; every importer of a changed module
      runs green.
- [ ] The shipped templates change with a RESYNC entry (variant F).
