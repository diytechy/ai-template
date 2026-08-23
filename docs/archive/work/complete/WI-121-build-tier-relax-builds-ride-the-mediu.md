+++
id = "WI-121"
title = "BUILD tier relax - builds ride the medium default (owner dial turn)"
workstream = "unattended"
needs = ["WI-113", "~WI-119"]
order = 120
+++

## Deliverable

Owner-ruled 2026-07-12 evening on WI-119's evidence (the first live run spent 78% of wall time in the two strong-tier BUILD sessions, ~$31.50 of ~$36): BUILD drops from the launcher's strong pin to the engine's built-in medium default - AGENT_TIER_MAP emptied in both launcher twins (unlisted phases use DEFAULT_PHASE_TIER: PLAN/DESIGN-CHECK/CRITIQUE strong, BUILD/REVIEW-A/B medium), fallback AGENT_MODEL_MAP BUILD=opus for coherence (managed routing stays the active path), AGENT_MODEL stays claude-fable-5 (an unknown phase routes UP). The relax leans on the designed safety the original pin's comment named: tier-up-never-down re-raises a contested build to strong via the per-slice review escalation - which is why the per-slice review leg stays ON (see the WI-123 ruling-pending proposal). Registry Notes (agents.csv fable/opus rows), status.md unattended-layer bullet, and the README config table updated to match. Config + docs only - no engine change, no spine change.
