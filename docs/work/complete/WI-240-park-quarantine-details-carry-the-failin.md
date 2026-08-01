+++
id = "WI-240"
title = "Park/quarantine details carry the failing step - shared failure-tail helper replaces the [:200] head truncation (2026-07-19 field finding; third bite)"
workstream = "unattended"
sr_refs = ["SR-096"]
buildtier = "quick"
safety_class = "ordinary"
order = 237
+++

## Deliverable

agent_common._failure_tail (extracts the LAST FAIL-marked step's banner+message else the bounded output tail); routed 17 dispatcher-family park/quarantine/journal detail sites off [:200] head slices; regressions + grep-census in test_agent_dispatch_decisions.py
