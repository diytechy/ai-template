+++
id = "WI-170"
title = "CHANGES-REQUESTED rework routing - carry review findings into the next BUILD scope (a rework pointer outranking docs/next-wi) so remediation never depends on a driver noticing dangling verdicts"
workstream = "unattended"
needs = ["WI-059"]
buildtier = "medium"
order = 169
+++

## Deliverable

Managed review dispatch now writes a coordinator-owned docs/rework-wi pointer on CHANGES-REQUESTED. It overrides docs/next-wi for the next BUILD prompt, telemetry WI label, and BuildTier lookup; survives repeated review rounds and coordinator restarts in its own telemetry commit; and clears only when that same scope receives APPROVE, leaving the advanced backlog pointer intact. PROCESS_OPTIONS is the single-home contract. Regression test advances next-wi before a requested-change verdict, proves WI-OLD remains the rework scope, then proves APPROVE clears the override and resumes WI-NEW.
