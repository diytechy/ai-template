## 2026-08-30 — WI-535: adjudicator telemetry first, dial off

Step 1 of the adjudicator session-retention plan's sequenced work
(`docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists`).
OI-69 (step 2, the owner rulings) is already ruled, and its recommendation
names this telemetry row as unblocked with the dial off; WI-540 (the
retention layer proper) needs it.

### What landed

- `docs/agents.toml` — `OPENCODE-GROK`'s `version` cell and `notes` prose
  still read "4.5" after a prior session (`9ab30d64`) corrected the `model`
  cell and the family comment to `grok-4.6`; the remaining two cells now
  match.
- `project-trajectory/scripts/agent_loop.py` — new
  `family_context_telemetry(family, data)`: per family, the session id and
  context occupancy/window/percent read straight off the process's own JSON
  result, no mint/resume/adapter. ANTHROPIC's stream-json result already
  carries `session_id`, and occupancy/window come from the same `usage` /
  `modelUsage` fields `session_meta` already partially reads (occupancy =
  input + cache-read + cache-creation + output; window = the `modelUsage`
  entry whose own input/output counts match those same totals, so a
  subagent's aside on a different model is never mistaken for the session's
  own window — left blank on no exact match rather than guessed, per the
  plan's own "never guessed" rule). OPENAI/OPENCODE return blank today: their
  shipped one-shot templates carry no `--json`/`--format json`, so there is
  nothing to parse until WI-540's adapter lands.
- `session_meta` now writes four more columns: `session-id`,
  `context-used`, `context-window`, `context-pct`.
- `project-trajectory/scripts/agent_common.py` — `write_session_log`'s
  header-key tuple carries the same four keys; `regenerate_index` gained a
  `Ctx %` column in the generated `docs/iteration_index.md` table (not
  touched directly — the trunk lane regenerates it).
- Tests: extended
  `tests/test_agent_loop_policy.py::test_session_meta_is_the_log_row_in_the_logs_own_column_order`
  for the four new keys; added coverage for `family_context_telemetry`
  (ANTHROPIC exact-match window pick, ANTHROPIC with no usage at all, and the
  non-ANTHROPIC blank path) and for `write_session_log` carrying the new
  header keys through.

### Harness

_(filled at close)_
