+++
id = "WI-129"
title = "LLR/TC status-coherence warn - lint the unlifted-LLR readout drift"
workstream = "scripts"
needs = ["~WI-128"]
order = 128
+++

## Deliverable

Owner-filed 2026-07-13 (ratification-review sitting, after WI-128 lifted the v2 LLRs by hand): warn - don't mutate, don't gate - when an LLR reads below Verified while every TC that cites it is Verified. Added trace.llr_status_advisories(llrs, tcs): joins TCs->LLRs (ID_PATTERNS[LLR] match on Verifies), and for each non-Verified LLR (via the shared case-insensitive is_verified()) that is cited by >=1 TC and ALL of whose citing TCs are Verified, emits one warn-tier finding - on stdout (WARNING (advisory): LLR <id> reads '<status>' but every citing TC is Verified - lift to Verified (the evidence already exists)), in docs/test/report.md (new 'LLR status-coherence advisories (warn-only)' section), and in the llr-status-advisories=N summary tally. NEVER promoted to an error: not under --strict, not under --strict-integrity (the strict exit sets are unchanged) - mirrors the derived-gate stance that LLR status is non-gating (maturity_gate ignores LLR/TC Status past Draft; the SR's Verified drives G2->G3), so gating it would re-introduce the coupling the gate model dropped. Auto-lift rejected (registries are hand-owned SSOT; generators never write cells back). An LLR with no citing TC stays the orphan rules' job. Tests (tests/test_trace.py): test_llr_status_coherence_predicate (all done-when cases at unit level - warn/silence, case-insensitivity, not-all-Verified quiet, no-citing-TC quiet), test_llr_status_advisory_is_warn_only_and_reported (scaffold: the minimal project's LLR-001 Implemented under Verified TC-001 warns, --strict/--strict-integrity exit 0 unchanged, lifting LLR-001 silences it). registry-hygiene skill carries the fixer line; module docstring documents the warn. No spine change (warn-only, no new SR/LLR/TC), no PROCESS.md change (byte budget; self-explanatory in the warn text), derived gate stays G3. Commit bar green (smoke 552p/2s + check_docs OK); full suite 707p/2s.
