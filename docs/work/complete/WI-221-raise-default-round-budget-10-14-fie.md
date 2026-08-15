+++
id = "WI-221"
title = "Raise DEFAULT_ROUND_BUDGET 10 -> 14 (field-proven; zero fallback headroom bit gilbert twice)"
workstream = "unattended"
sr_refs = ["SR-155"]
buildtier = "quick"
safety_class = "ordinary"
order = 218
+++

## Deliverable

Raised plan_round.DEFAULT_ROUND_BUDGET from 10 to 14 so the 8-session happy path plus two legal repairs retain fallback/relaunch headroom; explicit budget overrides and budget-exhaustion PAGE behavior are unchanged; the default and new_round propagation are regression-tested. PROCESS_OPTIONS did not restate the numeric default, so no budget-watched process doc changed.
