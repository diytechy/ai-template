## 2026-08-30 — WI-535: adjudicator telemetry first, dial off

Step 1 of the adjudicator session-retention plan's sequenced work
(`docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists`).
OI-69 (step 2, the owner rulings) is already ruled, and its recommendation
names this telemetry row as unblocked with the dial off; WI-540 (the
retention layer proper) needs it.

Deferred open items: none — telemetry-only row, no owner decision owed.

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

- Smoke tier + budget (the per-commit bar): `python -m pytest -q -n auto -m
  smoke` → **1426 passed, 6 skipped, 23.33 s**; `python
  scripts/check_smoke_budget.py --mode enforce` → **23.8 s vs 60 s budget →
  within**.
- `python project-trajectory/scripts/check_docs.py --root . --stale` →
  **OK — 1108 doc(s), 1587 intra-repo link(s), 0 broken (1 pre-existing
  orphan warning)**.
- `python project-trajectory/scripts/gen_open_items.py --check` → **0
  pending rows; up to date**.
- Spine validators: `python project-trajectory/scripts/trace.py` → the one
  `FINDING` names `LLR-197`, pre-existing at the branch base and untouched
  here; `python project-trajectory/scripts/check.py` → **RESULT: PASS**
  (derived-stage / approval-fresh SKIP on a work branch by design,
  concurrency-restructure §5.2). No spine row minted or re-statused by this
  WI — no approval-brief regen owed.
- Full unfiltered suite (`python -m pytest -q -n auto`): **3190 passed, 16
  skipped, 663.82 s**.
