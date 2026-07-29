+++
id = "WI-034"
title = "OKF export - traceability as a portable bundle"
workstream = "scripts"
sr_refs = ["SR-042"]
needs = ["WI-028"]
order = 33
+++

## Deliverable

Thread 48 Layer A landed (WI-1.51, 2026-07-10): gen_okf.py emits docs/okf (typed concepts + linked graph + indexes + UPSTREAM pin; deterministic, no clocks); --check wired as the G3 okf step AND a pre-commit hook step (the F2 floor rule); on-by-default/off opt-out; bundle committed with linguist-generated riders; meta bundle = 151 files; SR-042/LLR-039/TC-042. Layer B2 (process-doc concepts) deferred as the spec allows; loaders duplicated per the F5 rule instead of importing trace.py (recorded deviation).
