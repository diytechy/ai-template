+++
id = "WI-232"
title = "Make needs-re-review actionable: dispatch the focused re-review or page NEEDS-HUMAN with the named conflict (2026-07-18 field finding 3)"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["~WI-231"]
buildtier = "medium"
safety_class = "high-risk"
order = 229
+++

## Deliverable

Adopted option (b) — a source-conflict park is human work. A run draining with any train parked needs-re-review now pages run-state NEEDS-HUMAN (in _finish_dispatch, before the attention/RUNNING path) with a WI-127 ask naming the train(s) and conflicted path(s); the conflict's merge inputs (train tip + integration head) and paths are recorded durably under refs/llm/conflict/<train> (commit-tree metadata, mirroring the reservation refs — the journal is a cache, never authority). The idempotence guard (_integrate_one_ready) skips the identical merge on any relaunch whose inputs are unchanged (journals integration-conflict-held, no second integration-conflict) and retries once when an input moves. Ruling recorded in the spec and canonical PROCESS_OPTIONS integrator section; real park -> relaunch -> page -> retry regression pins it.
