+++
id = "WI-540"
title = "The adjudicator session-retention layer: adjudicator_session.py, the [adjudicator] dial shipped at 0, dedicated homes"
specref = "docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists"
workstream = "process"
sr_refs = []
needs = ["WI-535"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Context

Plan §5 step 3 (the SpecRef anchor above): "The layer —
`adjudicator_session.py` + config + route_session hook + tests, shipped with
`context_reset_pct = 0`." The full mechanics are the plan's §2 (the dial), §3
(store / launch / occupancy / drain-reset / keep-warm / rule-3) and §4
(integration points). `needs = ["WI-535"]` — the telemetry-first row that
already shipped `session-id` + occupancy/window/pct columns and
`family_context_telemetry`; this row adds the mint/resume adapter those columns
describe.

The five owner rulings step 2 asked for are RULED as OI-69
(`docs/log.d/2026-08-30-owner-rulings-oi68-oi69.md`): (a1) the layer retains a
transcript a bounded process replays, not a resident actor — the no-daemon
doctrine STANDS (SN-016 untouched); (b1) `reset_on_same_artifact = false` by
default, the fork hardening banked; **(c2) keep-warm pings THROUGH the
`12:00–19:00` UTC weekday blackout** (Anthropic only) — this SUPERSEDES the
plan §2 / §3.5 "skipped inside the blackout" text, which read the arithmetic
backwards; (d1) the dial lives in `docs/process.toml [adjudicator]`; (e1)
dedicated CLI homes (`CODEX_HOME`, `CLAUDE_CONFIG_DIR`) **once the dial is on**
— today's shared home stands while it ships at 0.

Shipped at `0` the layer is inert by the plan's own semantics (§2): no session
ids minted, no resume argv, no occupancy computed beyond WI-535's telemetry
columns — so the OFF path must be a strict no-op and today's one-shot behaviour
is unchanged. The invariants the plan names as untouched stay untouched:
`run_session` (IF-064), `build_argv`'s `(argv, stdin_input)` contract, and the
`adjudicate_brief` redaction seam.
