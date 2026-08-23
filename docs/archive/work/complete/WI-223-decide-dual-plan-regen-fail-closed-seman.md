+++
id = "WI-223"
title = "Decide dual-plan regen fail-closed semantics - trajectory-validator strictness can now abort a completed round (WI-220 review finding 2)"
workstream = "unattended"
sr_refs = ["SR-155"]
needs = ["~WI-220"]
buildtier = "medium"
safety_class = "high-risk"
order = 220
+++

## Deliverable

Ratified fail-closed SELECT disposition semantics: filed child rows and present OKF/dashboard views are one atomic transaction; a generator/trajectory validation failure leaves the integration ref unchanged, returns the generator plus validator tail, quarantines through the existing error path, and salvages DP-* evidence. Ruling recorded in the spec and canonical dual-plan PROCESS_OPTIONS section; real dangling-predecessor regression pins the behavior.
