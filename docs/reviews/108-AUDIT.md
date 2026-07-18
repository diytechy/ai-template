# 108-AUDIT — Whole-registry contradiction audit

**Rubric:** `docs/rubrics/registry-contradiction-audit.md` (WI-206). Independent
all-vs-all sweep, old-vs-old included; no privileging of recent rows.
**Swept:** 25 SN rows (`stakeholder-needs.md`, SN-001..SN-025) x 66 SR rows
(`system-requirements.csv`, SR-001..SR-066), all pairs. No LLR/TC or interface
row was needed to adjudicate a limit — every finding is citable from SN/SR text.
**Redaction honored:** rubric + SN + SR only; no status.md, log.md, specs,
scratchpad, code, or self-assessment consulted.

## Findings

- [MAJOR] SR-040 vs SR-059 -> C1/C4: SR-040 requires the coordinator to "select the agent command template per declared run phase (AGENT_CMD_MAP/--cmd-map, falling back to the single AGENT_CMD)", but SR-059 "delete[s] docs/next-wi and docs/run-phase outright" and removes "every live dependency - coordinator selection ... and their tests/generated outputs"; the "declared run phase" SR-040 keys on is exactly the deleted docs/run-phase, so SR-040's routing input no longer exists and the row was never amended -> rekey SR-040's AGENT_CMD_MAP off the surviving `{phase}-{gate}` branch signal or retire the per-run-phase routing, and scope any residual to the SR-059 compatibility window -> @owner
- [MAJOR] SR-048 vs SR-051 -> C2/C3: both own the How-SW top-view cap in their own terms — SR-048 as a literal ("bound the software-architecture top view at 10 items", "a <=10-module ... inventory is vacuous") and SR-051 as a named constant ("bounded above at the TOP_VIEW_MAX top-view cap") — so an amendment moving one leaves the other stale, and the registry never states TOP_VIEW_MAX = 10 -> make one row the sole owner of the cap value and have the other reference it by id (e.g. SR-048 defines the value, SR-051 cites SR-048; or both cite TOP_VIEW_MAX) -> @owner
- [MINOR] SR-045 vs SN-024/SR-047/SR-052/SR-053/SR-054 -> C4: the reviewer-heterogeneity axis is named "Family-keyed reviewer heterogeneity (two families ...)" in SR-045 — which explicitly deprecates the term ("legacy Provider read as Family") — while SN-024 and the four critique rows all require a "provider-heterogeneous" session; the same axis carries two vocabularies, one of them the deprecated word -> unify on one term (e.g. "family-heterogeneous") across the critique rows, or state provider = family once as the canonical mapping -> @owner
- [MINOR] SR-026 vs SR-057/SR-064 -> C4: SR-026 requires "agent_loop.py shall resume from docs/status.md", but SR-057 derives the frontier "from the tracked WI registry ... never from prose" and SR-064 reconstructs state "from Git alone" with the branch "its published projection, not the recovery authority" (status.md demoted to a generated snapshot by SR-059); the resume/recovery source moved off status.md, leaving SR-026's stated source stale -> amend SR-026 to name the WI registry + Git as the resume authority and status.md as a generated reference, or scope it to the serial legacy path -> @owner
- [MINOR] SN-008 vs SR-006 -> C1: SN-008's acceptance states unconditionally "check.py fails (not skips) on a missing required tool", while SR-006 provides "--lenient degrades it to SKIP"; the two reconcile only by reading SN-008 as "no silent pass," which its text does not carve out, so a --lenient gate that SKIPs a missing required tool contradicts SN-008 as written -> add the explicit --lenient exception to SN-008 (and clarify whether a --lenient gate may report pass) -> @owner

VERDICT: CHANGES-REQUESTED findings=5
