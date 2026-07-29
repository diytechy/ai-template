+++
id = "WI-193"
title = "Dupes census gap - WI-188 in_phase helper duplicated into trace.py + gen_release_checklist.py is uncensused so the G3 dupes gate is red"
workstream = "scripts"
needs = ["WI-188"]
buildtier = "quick"
order = 200
+++

## Deliverable

WI-193 (2026-07-16): the pre-existing G3 dupes-gate red fixed (found while running the dupes gate during WI-191, filed there). WI-188 added an identical in_phase() SR-phase-filter helper to both trace.py:1342 and gen_release_checklist.py:162 - each independently filters SRs by the derived Phase column (~31 tokens; F5 small-helper duplication, deliberately not hoisted into a shared module) - but never censused the pair, so [step:dupes] (G3-only, and the branch unpushed OI-3) went red undetected. Fix: added the gen_release_checklist.py == trace.py pair to docs/dupes-allow with a WI-193 annotation, the same F5-sanctioned class as the ~50 existing census pairs; NO code change (the duplication is sanctioned, not eliminated - hoisting a shared module would violate F5). Verified: check_dupes OK (0 findings, was 1); the full check.py --gate G3 --jobs 0 now PASS (15/15 steps, 952 passed/1 skipped, 90.98% coverage). No spine change (census hygiene), no byte-budgeted file touched.
