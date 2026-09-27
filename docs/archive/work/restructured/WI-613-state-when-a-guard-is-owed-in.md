+++
id = "WI-613"
title = "State when a guard is owed in PROCESS.md, and link it from the reviewer and builder prompts (S15)"
workstream = "process"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#42-when-a-guard-is-owed-note-3"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Deliverable

Restructured into WI-615.

## Context

Ruled by the owner 2026-09-23 (sister plan S15, §4.2).

The guard doctrine is scattered: the `antidote` skill ("validate once at the
boundary, then trust the type"), PROCESS.md:244-247, `AGENTS.template.md`, and
the reviewer prompt's "why the defect cannot be made UNREPRESENTABLE" clause.
What is missing is where the boundary is. Its one home is PROCESS.md, beside
the 0->A->B rule, linked from the reviewer and builder prompts, not copied into
them. It must not go in the `antidote` skill, which is vendored verbatim from
upstream with three byte-identical copies.

The rule, as ruled: "A guard is owed only where the input crosses a trust
boundary — a file on disk, the network, a person, another process, or a model's
output — or where the operation is irreversible or exposed to attack. Data this
code produced in-process is trusted: fix the producer instead." Two
consequences to state with it: the registries are hand-edited files on disk, so
validating them is owed; and a model's output is a boundary, so validating
structured output is owed.

## Done-when

- PROCESS.md states the rule once, beside the 0->A->B rule, with its two
  consequences.
- The reviewer and builder prompts link to it and restate nothing; the
  vendored `antidote` copies are unchanged.
- Byte budgets on PROCESS.md and the prompts hold (the byte-budget-guard
  report quoted), and the dogfood sync test stays green.
