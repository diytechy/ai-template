+++
id = "WI-540"
title = "The adjudicator session-retention layer: adjudicator_session.py, the [adjudicator] dial shipped at 0, dedicated homes"
specref = ""
workstream = "process"
sr_refs = []
needs = ["WI-535"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

`adjudicator_session.py` — the retention layer's one home: the runtime session
STORE (keyed `(family, route_id)`, atomic write-temp + `os.replace`), the
per-family resume-argv ADAPTER, the per-family OCCUPANCY / session-id READERS,
the drain/reset RULE and the keep-warm TICK decision. Shipped INERT behind
`docs/process.toml [adjudicator] context_reset_pct = 0`
(`agent_common.adjudicator_config(...).enabled == False` short-circuits every
caller), so the OFF path is byte-for-byte today's one-shot behaviour;
`run_session` (IF-064), `build_argv`'s `(argv, stdin_input)` contract and the
`adjudicate_brief` redaction seam are untouched. Wired into `agent_loop`
(`adjudicator_launch` / `_adjudicator_resume_record` / `adjudicator_bookkeeping`
/ `route_session`, with `resolve_session_setup`→`map_preflight` carrying the
loaded `adjudicate-*` template paths) and `dispatch` (keep-warm over
`load_family`). The `[adjudicator]` dial + its fail-closed-to-OFF row land in
`process.toml`(.template), `docs/enforcement-audit.md`, and the spine (IF-174
owner declared by `adjudicator_session`; LLR-163 / TC-157 / IF-064 amendments).
Turning the dial ON and verifying it on-box is WI-541 (plan §5 step 4).

REVIEW-A round 002 (CHANGES-REQUESTED, findings=6) fully addressed, one
regression test per finding: (1) the store keys by `(family, route_id)` so a
route switch never resumes another route's transcript; (2) `governing_hash`
folds in the loaded adjudication templates so a changed judging instruction
drains the session; (3) OPENAI/OPENCODE telemetry flows through their emitted
JSON / rollout readers so the captured session id persists and later launches
resume rather than mint; (4–6) IF-174's `Rationale`/`Data`/`Contract` are
registry-clean (standing reason, 108-char typed pointer under the 160 ceiling,
`Contracts: IF-174` header + `Contract IF-174:` body on the owner). Deviations
from spec: keep-warm pings THROUGH the `12:00–19:00` UTC weekday blackout
(ANTHROPIC only) per owner ruling OI-69 (c2), superseding plan §2/§3.5 wording
(Sol #17). Green at close: smoke `1472 passed / 6 skipped`, budget `23.7s` vs
`60s`; full unfiltered suite passes (log fragment carries the totals).

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
