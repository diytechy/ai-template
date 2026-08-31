+++
id = "WI-535"
title = "Adjudicator telemetry first, dial off: session id and occupancy / window / percent per family; the stale grok slug"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Telemetry-first step of the adjudicator session-retention plan (plan §5 step
1), landed with the retention dial off — no mint, no resume argv, no session
store, no `[adjudicator]` table (WI-540's job):

- `project-trajectory/scripts/agent_loop.py`: new `family_context_telemetry(family, data)`
  reads session id and context occupancy/window/percent straight off the
  process's own JSON result, per family. ANTHROPIC's stream-json result
  already carries `session_id` on every call; occupancy sums the same four
  `usage` counters `session_meta` already partially reads
  (input + cache-read + cache-creation + output); window is picked from the
  `modelUsage` entry whose own input/output counts match those same
  top-level totals, so a subagent's aside on a different model is never
  mistaken for the session's own window — left blank on no exact match
  rather than guessed, per the plan's "never guessed" rule. OPENAI/OPENCODE
  return blank: their shipped one-shot templates carry no
  `--json`/`--format json`, so there is nothing to parse until WI-540's
  per-family adapter lands.
- `session_meta` writes four new session-log columns: `session-id`,
  `context-used`, `context-window`, `context-pct`.
- `project-trajectory/scripts/agent_common.py`: `write_session_log`'s
  header-key tuple carries the same four keys; `regenerate_index` gained a
  generated `Ctx %` column in `docs/iteration_index.md`.
- `docs/agents.toml`: `OPENCODE-GROK`'s `version` cell and `notes` prose
  corrected from "4.5" to "4.6" (the `model` cell and family comment were
  already fixed in a prior session) — the last of the stale grok slug.
- Tests: extended `test_session_meta_is_the_log_row_in_the_logs_own_column_order`
  for the four new keys; new coverage for `family_context_telemetry`
  (ANTHROPIC exact-match window pick, ANTHROPIC with no usage at all, and
  the non-ANTHROPIC blank path) and for `write_session_log` /
  `regenerate_index` carrying the new columns through.

Not in scope (WI-540, which `needs = ["WI-535"]`): session mint/resume, the
retention store, the `docs/process.toml [adjudicator]` table, and any
OPENAI/OPENCODE adapter.

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
