+++
id = "WI-562"
title = "Unload residue and scratch: integrate.lock declared, the worker told where scratch belongs (OI-76 / plan 2.7)"
specref = "docs/plans/2026-08-31-verdict-record-and-queue-blockers.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Commissioned by `OI-76`'s ruling (plan section 2.7, findings E/F). The
`out/agent-loop.lock` omission made every merged lane end UNLOAD INCOMPLETE
until it was declared (decision 40, fixed with a test); `out/integrate.lock`
is the same class and is still undeclared. Worker scratch files under
`out/` were correctly refused by name, but no brief names where scratch
belongs, so the refusal will recur.

## Done-when

1. `out/integrate.lock` is declared in the unload residue set, with the
   same test-and-fixture treatment the agent-loop lock received.
2. The worker brief names the scratch home in one line, so a session's
   temporary files land where the unload expects nothing.
3. The full suite stays green; no other residue class regresses.
