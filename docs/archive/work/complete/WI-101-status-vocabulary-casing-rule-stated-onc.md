+++
id = "WI-101"
title = "Status-vocabulary casing rule stated once + near-miss hint (M3)"
workstream = "scripts"
order = 100
+++

## Deliverable

trace.py matched the Draft magic value case-insensitively (is_draft.lower()) but Verified exact-case, so `verified` silently counted as not-verified — an undocumented asymmetry (safe direction, but surprising). Unified on the NON-BREAKING rule: case-insensitive for both magic values. Added is_verified() mirroring is_draft in trace.py + derive_gate.py (F5-duplicated, pinned equal by a new test_rule_sync::test_is_verified_agrees), routed the 3 trace.py Verified comparisons (audit counts + the G3 --require-verified gate) and derive_gate's gate computation through it, and stated the rule once in PROCESS.md §4 (+189 B flagged, baseline 59,827; re-stamped byte-budget-guard skill + its 2 agent copies). The status finding now notes matching is case-insensitive so a failure reads as a real mismatch, not a casing near-miss. No spine change (G3; derived gate unchanged — all meta SRs are exact-case Verified). Full suite 702 passed.
