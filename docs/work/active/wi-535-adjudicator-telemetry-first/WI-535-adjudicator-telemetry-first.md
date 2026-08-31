+++
id = "WI-535"
title = "Adjudicator telemetry first, dial off: session id and occupancy / window / percent per family; the stale grok slug"
specref = "docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable


## Context

Step 1 of the adjudicator session-retention plan's sequenced work (plan §5,
the SpecRef anchor above): "Telemetry first, dial off — session-id capture +
occupancy/window/pct columns per family; fix the stale
`opencode-go/grok-4.5` slug (install has grok-4.6). Independently useful: it
shows how full today's one-shot adjudications already get." OI-69 (the five
owner rulings step 2 asked for) is already RULED
(`docs/log.d/2026-08-30-owner-rulings-oi68-oi69.md`,
`docs/requirements/open-items.toml#OI-69`), and its own recommendation says
this telemetry row is unblocked and lands with the dial off — WI-540 (the
retention layer proper, `adjudicator_session.py` + the `[adjudicator]` table)
`needs = ["WI-535"]` and starts after this row.

Scope is telemetry only: no mint, no resume argv, no session store, no
`docs/process.toml [adjudicator]` table (WI-540's job). What this row adds is
what today's plain one-shot call from each family already reports about its
own session and context, captured into the existing session-log columns
(plan §3.2/§3.3): ANTHROPIC's stream-json result already carries
`session_id` on every call, and its `usage`/`modelUsage` fields already carry
enough to compute occupancy, window and percent without any adapter change.
OPENAI (codex) and OPENCODE do not emit any of this from their shipped
one-shot templates (no `--json`/`--format json`), so their columns read
blank until WI-540's per-family adapter lands — consistent with how `tokens`,
`cost-usd` etc. already read blank for those families today.

The stale grok slug: `docs/agents.toml`'s `OPENCODE-GROK` row had its `model`
cell already corrected to `opencode-go/grok-4.6` and its family-comment prose
in a prior session (`9ab30d64`, 2026-08-30), but the row's own `version` cell
and `notes` prose still read "4.5" — the remainder of that same staleness.
