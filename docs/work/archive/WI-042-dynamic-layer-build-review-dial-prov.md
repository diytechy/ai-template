+++
id = "WI-042"
title = "Dynamic-layer build - review dial + provider routing"
workstream = "unattended"
sr_refs = ["SR-040"]
needs = ["WI-024", "WI-025"]
order = 41
+++

## Deliverable

AGENT_ROLES R1/R3/R6 build calls landed (WI-1.49, 2026-07-10): docs/review-policy scaffolded (0|1|2 default 1; surfaced in the banner, enforced by convention); AGENT_CMD_MAP/--cmd-map per-phase command templates (parse_model_map reuse; entries preflighted; REVIEW-A/-B free-form keys route providers); status.md size guard = warn-only preflight (AGENT_STATUS_WARN_BYTES, default 8192, 0 silences — the micro-call resolved to the cheap tripwire); --prompt-map stays deferred until role drift. SR-040/LLR-037/TC-040; PROCESS_OPTIONS reviewer-dial section; launcher template slots.
