+++
id = "WI-059"
title = "Heterogeneous implementer/reviewer scheduling"
workstream = "unattended"
sr_refs = ["SR-154", "SR-155"]
needs = ["WI-042"]
order = 58
+++

## Deliverable

S8 (2026-07-11): the heterogeneous implementer/reviewer scheduling layer. agent_loop managed mode (gated on docs/agents-enabled presence; absent = today's behavior byte-for-byte) enforces docs/review-policy 0|1|2 - a committing build schedules REVIEW-A (2 also REVIEW-B) with a redacted (self-assessment-free) reviewer prompt (embedded default, --prompt-map/AGENT_PROMPT_MAP file override, {verdict} slotted), verdicts land as docs/reviews/NNN-<phase>.md repo files (log.md block + VERDICT machine line), merged mechanically no-debate. New scripts/agent_route.py routes each session's model from docs/agents.csv ([PROVIDER]-[MODEL_NAME]-[VERSION] ids, join-key-never-parsed) by the phase tier + reviewer heterogeneity (two providers, >=1 differing; degraded same-provider legal) + per-model cooldown (generalized rate-limit backoff), tier-up-never-down, every selection logged before launch; and holds the fixed win-stay/lose-shift escalation (margin>=2, swap after 2 failed gates, tier-up only after the swap fails, page-human on shared-failure/contradiction/tripwire) with docs/gate-policy-keyed failure semantics. New scripts/score_reviews.py is the advisory substance scorer (anchored precision/actionability/corroboration/confirmed-rate; length never positive; severity hygiene + 4 tripwires as non-scored gates) writing docs/reviews/scoreboard.txt. Ships agents.template.csv -> docs/agents.csv (scaffolded, inert until agents-enabled); PROCESS_OPTIONS routing/escalation subsection + gate-closure reviewer-floor narrowing; README bullet. Spine: SR-045 under SN-006/016 + LLR-044/045/046 + TC-046 + IF-044..047 (rides the pending G3 re-attestation). Tests: test_agent_route.py, test_score_reviews.py, test_agent_loop_review.py.
