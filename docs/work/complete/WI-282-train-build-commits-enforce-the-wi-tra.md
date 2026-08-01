+++
id = "WI-282"
title = "Train build commits: enforce the WI: trailer at commit time (commit-msg floor hook + a loud reviewed-head mismatch diagnostic) - live 2026-07-23 failure: p0-g3-WI-281-9ae9 session 006 committed 45637d2 with a malformed trailer block, reviewed_train_head skipped it to the older CHANGES-REQUESTED head and parked an APPROVED train as rework; a one-line slip must fail at commit time, not cost a build+review cycle"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 279
+++

## Deliverable

Integrated from train p0-g3-WI-282-eb40 @ dd5c65f: WI-282: validate blocked trailer evidence
