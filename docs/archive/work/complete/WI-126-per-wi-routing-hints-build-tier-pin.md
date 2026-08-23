+++
id = "WI-126"
title = "Per-WI routing hints - build-tier pin + plan-required flag (owner proposal)"
workstream = "unattended"
needs = ["~WI-121", "~WI-107"]
order = 125
+++

## Deliverable

WI-126 (2026-07-13, owner-proposed then implemented): per-WI build-tier routing for the unattended coordinator. (1) An OPTIONAL BuildTier column (strong|medium|quick; legacy weak reads as quick via agent_route.normalize_tier; empty/absent = today's phase-default routing) added to this work-items registry + the shipped work-items.template.csv - read by name, never-breaking. (2) A new declared docs/next-wi file in the docs/run-phase idiom (comment lines + one WI id on the last line, read via read_declared); the driver maintains it alongside status.md's Next action; absent/empty = byte-identical behavior. (3) agent_loop.build_tier_pin() honors the pin in managed mode + BUILD phase ONLY: it reads docs/next-wi once per iteration, looks the WI up in work-items.csv via _read_csv_rows, and uses a valid BuildTier as the session's STARTING tier in place of the phase default, printing one loud route [...] line (no-silent-swap); the escalation override (impl_tier_override, tier-up-never-down) still wins AFTER the pin, so a pin never caps escalation; a bad state (unknown WI id, or a BuildTier that does not normalize) prints one warning line and falls back to the phase default (LOUD, never fatal, never silent). The proposed plan-required flag was folded into existing SpecRef semantics (a filled spec = plan-ready) rather than a new column, per the WI-126 spec recommendation - PLAN is bounce-only and zero PLAN sessions run here. Docs single-homed: PROCESS_OPTIONS 'Unattended operation' documents BuildTier + docs/next-wi; the session-protocol skill (source + .claude/.agents byte-identical fan-out) gains the maintain-docs/next-wi line; both agent-resume launcher twins name docs/next-wi in AGENT_PROMPT. Seeded docs/next-wi = WI-087 (this repo's next slice; WI-087 carries no BuildTier, so its routing stays byte-identical). No spine change, no byte-budgeted file touched. Tests: test_agent_loop_review.py pin-honored / pin-absent-unchanged / bad-value-loud-fallback / unknown-WI-loud-fallback.
