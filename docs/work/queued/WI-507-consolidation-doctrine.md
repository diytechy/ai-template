+++
id = "WI-507"
title = "The consolidation doctrine lands: the 0->A->B clause in the three guides, the overlap baseline measured, antidote vendored (OI-58 ruled, 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-58"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-58's (a)+(b) halves plus the owner's vendoring instruction:

1. **The doctrine** — CLAUDE.md, AGENTS.template.md and PROCESS.md gain
   the consolidation clause BESIDE edit-conservatively (the two scoped:
   conservative WITHIN a task, consolidating ACROSS the codebase when the
   task is consolidation): "prefer the change that minimizes TOTAL
   behavior; when a fix wants the same code in two places, extract the
   shared stage — the 0→A→B rule; where outputs overlap, restructure so
   each behavior has one home." Byte-budget-guard convention on all three
   (AGENTS is at its cap — relocation, not growth).
2. **The measurement** — the WI-448 duplication census (function-body
   hashing; 477 residual lines at last stamp) becomes a standing
   warn-first check with a stamped baseline and downward-only restamps,
   burn-down visible; a call-graph behavioral-overlap measure added if it
   stays stdlib-cheap, else recorded as the follow-up.
3. **Vendor antidote** — the skill at C:/Projects/antidote/skills/antidote
   joins project-trajectory/skills/ as a default skill the pack ships
   (the existing vendored-skill pattern: source recorded, version/commit
   stamped, dogfooded into .claude/skills/), with a dependencies-ledger
   row naming what it is and why (external content entering the kit).
   State the shared principle once in the doctrine text: validate and
   implement at the boundary that owns the behavior, never at each
   caller.

RESYNC entries for the guide and skill changes; scaffold-verify the skill
lands in a fresh scaffold's agent surfaces.
