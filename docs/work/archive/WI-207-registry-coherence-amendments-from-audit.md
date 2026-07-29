+++
id = "WI-207"
title = "Registry coherence amendments from audit 108 - resolve the five 108-AUDIT.md findings through normal intake (the WI-206 disposition rule): [MAJOR] SR-040 rekey AGENT_CMD_MAP off the surviving {phase}-{gate} signal or retire per-run-phase routing (its docs/run-phase input was deleted by SR-059); [MAJOR] SR-048 vs SR-051 make ONE row own the How-SW top-view cap value and the other cite it; [MINOR] unify the Family-vs-provider-heterogeneity vocabulary (SR-045 vs SN-024/SR-047/052/053/054); [MINOR] SR-026 resume-authority text updated for the WI-registry/Git substrate; [MINOR] SN-008 state the --lenient carve-out or SR-006 cite the SN's intent. Registry text amendments only - spine-touching, one reviewed batch"
workstream = "self-adoption"
sr_refs = ["SR-040", "SR-048", "SR-051"]
buildtier = "strong"
order = 206
+++

## Deliverable

WI-207 (2026-07-17): all five 108-AUDIT.md findings resolved in one reviewed batch. F1 SR-040 rekeyed - the command-template selection keys on the in-process session phase (PLAN/BUILD/REVIEW-A/...; the SR-059-deleted docs/run-phase named as a non-input), Rationale/AC re-worded (run-phase -> session-phase; cross-provider -> cross-family). F2 the How-SW top-view cap single-homed: SR-048 declares TOP_VIEW_MAX = 10 as the cap value's ONE home; SR-051 cites the SR-048-owned cap. F3 vocabulary unified: provider-heterogeneous -> family-heterogeneous across SN-024 + SR-047/052/053/054 + the LLR/TC echoes (SR-045's legacy-Provider-read-as-Family stays the mapping of record; historical WI Deliverable prose left as record). F4 SR-026 resume authority split per mode: serial loop = docs/status.md, dispatcher = WI registry + durable Git reservations (SR-057/SR-064), status.md its integrator-generated reference (SR-059). F5 SN-008 gains the explicit --lenient carve-out (the one sanctioned degrade, never a CI/gate default; SR-006 unchanged). Reviewed by an independent fresh-context opus session over the diff (new-incoherence sweep + code-reality checks); trace --strict + check_trajectory --strict clean; OKF/dashboard regenerated.
