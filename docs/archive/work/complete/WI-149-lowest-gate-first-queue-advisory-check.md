+++
id = "WI-149"
title = "Lowest-gate-first queue advisory (check_trajectory warn)"
workstream = "scripts"
needs = ["WI-093", "~WI-115", "WI-145"]
order = 148
+++

## Deliverable

check_trajectory warns when docs/next-wi selects a phase development WI ahead of an open [phase]-[g1|g2] anchor or a Draft SR in that phase; owner ordering remains authoritative. Both agent-resume prompts carry the lowest-gate-first instruction. 3 fixture tests.
