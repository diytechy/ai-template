+++
id = "WI-614"
title = "State the fan-out rules in PROCESS.md: peer-tier kept, tiers not models, never from review roles (S12)"
workstream = "process"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#36-fanning-out-to-other-models-note-3"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Context

Ruled by the owner 2026-09-24 (sister plan S12, §3.6).

PROCESS.md permits two kinds of fan-out (`:52-55`, `:933-939`): stepping a
mechanical subtask down a tier, and peer-tier delegation for a dedicated
context or an independent review. The ruling keeps both, and adds three
statements: prose names tiers, not models; fan-out never happens from review,
critique, design-check or adjudication sessions; budgets wait for an
observability design. The second is prose, not enforcement, until that design
lands: no role is denied spawn tools today, and `subagent_gate` sees only
Claude's `Task` and `Agent`. NOT IN SCOPE: enforcement, per-provider spawn
denial, budgets.

## Done-when

- PROCESS.md states both delegation kinds as kept, names tiers rather than
  models, and forbids fan-out from review, critique, design-check and
  adjudication sessions, saying that this is prose until the observability
  design exists.
- No prompt or skill restates it; any that names a model for delegation names a
  tier instead.
- Byte budgets hold.
