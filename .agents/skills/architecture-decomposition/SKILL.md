---
name: architecture-decomposition
description: Use when planning a work item (answering its architectural-delta question) or at DevStg-Arch (breaking down a component scope), and in an architecture audit — name the mode classes, state each boundary's value domain, tabulate output against input dependencies, and apply A8's two descent rules, judged against the shared architecture-decomposition rubric.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [architecture, decomposition, interfaces, components, planning]
scope: kit
---
**When to use.** Three moments: at `DevStg-Arch`, when a component scope is broken into sub-components; when planning a work item, to answer its architectural-delta question; and in an audit of a scope as it stands. *Why:* a boundary is worth its interface only when it hides a decision likely to change, and that is argued from the scope's states, domains and dependencies, not from the steps its processing runs through. The bar is the rubric at `docs/rubrics/architecture-decomposition.md`; this skill is the procedure that produces what the rubric judges, and it cites the rubric's anchors by id instead of restating them.

**Procedure.**
1. **Name the mode classes** (rubric A2). Record each one, with its transitions, as the scope's state flow in `docs/runtime-flows.md`.
2. **State each boundary's value domain** (A3, A6). Record it as the form of the boundary's interface row in `docs/requirements/interfaces.toml`.
3. **Tabulate output against input dependencies** (A4). Record the table beside the scope's flow in `docs/runtime-flows.md`, or, when planning, in the plan.
4. **Apply A8's two descent rules.** Requirement descent for the scope's obligations; component descent after comparing the candidate cuts, keeping the scope whole among them, under A1, A4 and A7. Record the result in the existing scoped decomposition or review record (process-options.md "(d2)"); where the component layer keeps one, that is the component registry's partition record.

Each output goes only to a home that already exists; the procedure never adds a file or a field to hold it.

**When planning a work item.** Each step's result answers one clause of the delta question. A new mode class or transition is "add a state"; a new case in a domain is "add a value"; a new cell in the dependency table is "a new input"; a new boundary interface is "cross a new boundary". The plan writes its `DELTA:` line from those results, and carries a `within` change as rows of its own.

**Below a component's boundary**, in its code, use the `deep-module-design` skill.
