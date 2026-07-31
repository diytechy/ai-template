+++
id = "WI-375"
title = "Make PROCESS_OPTIONS' \"Unattended operation (walk-away runs)\" describe the flow that actually ships. Two defects today: (1) the section (:542) promises \"a coordinator grinds work from a single entry point while nobody watches\" while that entry point exits 2 with a map, and it describes the model in terms of `integrate.py claim` and `agent_loop.py --wi` as steps without naming what invokes them; (2) the capability table (:29) cites `docs/run-*` as a live mechanism and that artifact does not exist - `ls docs/run-*` returns No such file or directory, it was deleted with the dispatcher at Phase 5. This is shipped kit text every adopter reads to decide whether to wire up walk-away runs. Hard-gated behind WI-374 because the section must describe the flow that exists - but NOTE defect (2) is wrong regardless: if WI-374 stalls or is re-scoped, split that half out and fix it alone. Includes searching for any OTHER kit text still promising the retired dispatcher's behaviour, rather than assuming these two sites are all of them."
workstream = "docs"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
needs = ["WI-374"]
+++

## Deliverable

The shipped kit text describes the walk-away flow that actually exists. PROCESS_OPTIONS "Unattended operation" opens its model with the real single entry point (the plain-launch drive mode, drive.py, frontier re-derived every cycle) and its capability-table row cites drive.py/integrate.py instead of the deleted docs/run-*; PROCESS.md section 4 points at the stop banner + typed exit codes instead of docs/run-state; ADOPTING.md's v4 parallel-dispatch bullet is rewritten as the retirement + upgrade recipe (registry CSV to spec folder, drain old trains, seed [generated], delete AGENT_JOBS/run-state/tracks/next-wi/run-phase/refs-llm/parallel-ready reliance) and its WI-260 bullet is marked historical; the downstream-resync skill's section-3 recipe is replaced by the integration-seam migration (per-agent copies re-synced, skills-sync green). Sweep performed over all kit markdown: every remaining dispatcher/run-* mention is a historical retirement record, not a live promise. The spec-of-record docs/specs/unattended-entry-point.md archived to docs/archive/specs/ at close (R-F: no open citer remains). Byte deltas flagged and baselines re-stamped: PROCESS.md +18 (64,319), PROCESS_OPTIONS.md +556 (163,157), ADOPTING.md +167 (unbudgeted).
