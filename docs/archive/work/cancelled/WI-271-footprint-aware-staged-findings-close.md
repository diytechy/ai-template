+++
id = "WI-271"
title = "Footprint-aware staged_findings — close the re-attestation false-positive in the no-validation-delta warn"
workstream = "scripts"
needs = ["~WI-270"]
buildtier = "medium"
safety_class = "ordinary"
order = 268
+++

## Deliverable

RETIRED 2026-07-29 — owner ruling (in-session), adopting the handoff-2026-07-28c §3 disposition. The warn's own spec says it still earns its keep: an over-trigger costs a moment's investigation, the lesser evil against a missed paper-close, so the footprint-aware widening is noise reduction, not a correctness fix. Per the disposition, the un-defer trigger now lives in `staged_findings`'s docstring (check_trajectory.py) — reopen as a FRESH WI only if the false-positive rate erodes the signal. Spec archived to docs/archive/specs/WI-271.2026-07-29.md (the widened design is there, ready if the trigger ever fires).
