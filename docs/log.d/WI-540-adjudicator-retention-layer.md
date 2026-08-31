## 2026-08-31 — WI-540: the adjudicator session-retention layer, shipped inert at dial 0

Plan §5 step 3 of the adjudicator session-retention plan
(`docs/plans/2026-08-29-adjudicator-session-retention-plan.md`). The layer that
turns WI-535's telemetry into an opt-in retained session: a session store, a
per-family resume-argv adapter, occupancy readers, the drain/reset rule and the
keep-warm tick — all guarded behind `[adjudicator] context_reset_pct`, shipped
at `0` (inert: today's one-shot behaviour byte-for-byte). Turning the dial on
and verifying it on-box is WI-541 (plan §5 step 4).

Owner rulings honoured (OI-69, `docs/log.d/2026-08-30-owner-rulings-oi68-oi69.md`):
(a1) no-daemon — a retained transcript a bounded process replays, not an actor;
(b1) `reset_on_same_artifact = false` default; (c2) keep-warm pings THROUGH the
blackout (Anthropic only) — the plan's own §2/§3.5 "skipped inside the blackout"
text is superseded by this ruling and the code follows the ruling; (d1) dial in
`docs/process.toml [adjudicator]`; (e1) dedicated CLI homes once the dial is on.

Deferred open items: none.

Deviations from spec: keep-warm pings through the blackout per OI-69 (c2),
against the plan §2/§3.5 wording (Sol #17); recorded above and in the spec
Context.
