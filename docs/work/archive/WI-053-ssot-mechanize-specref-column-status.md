+++
id = "WI-053"
title = "SSOT mechanize - SpecRef column + status coherence rules"
workstream = "scripts"
sr_refs = ["SR-037"]
needs = ["WI-030"]
order = 52
+++

## Deliverable

S1 (2026-07-10): SpecRef column on the work-items template + meta CSV (legacy CSV reads it empty); `deferred` first-class status; check_trajectory.py mechanizes the status.md<->registry SSOT rules - R-A (Deliverable non-empty iff done) a hard error at every run = the pre-commit floor, R-B..R-E (open WIs named in status.md, no done id there, every open WI's SpecRef resolves) warn plain and gate under --strict at G2+; --staged no-validation-delta warn; docs/specs/ scaffold (README + WI-000 Done-when example) via bootstrap; pre-commit gains the trajectory floor + staged step; check.py wires --strict at G2/G3; PROCESS_OPTIONS SSOT model; SR-037/LLR-034/TC-037 text extended (rides the pending G3 re-attestation). Tests in test_trajectory.py + test_pre_commit_hook.py.
