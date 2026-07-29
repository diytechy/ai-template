+++
id = "WI-115"
title = "Status-currency hardening - run-state coherence warn + policy-flip sweep"
workstream = "scripts"
needs = ["WI-053", "~WI-107"]
order = 114
+++

## Deliverable

WI-115 (2026-07-13): check_trajectory now warns when NEEDS-HUMAN/BLOCKED would park queued WIs with all hard predecessors done, and promotes it under --strict; absent run-state and DONE with no actionable queue stay vacuous. Added trajectory fire/vacuous/strict tests, policy-flip status sweep guidance to session-protocol + gate-advance (fan-out re-synced), and the reviewer policy-contradiction charter clause.
