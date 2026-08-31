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
  input + cache-read + cache-creation + output; window = the unique `modelUsage`
  entry whose own four counters match those same totals, so a subagent with
  colliding input/output but different cache usage is never mistaken for the
  session's own window — left blank when a full match is absent or ambiguous,
  per the plan's own "never guessed" rule). OPENAI/OPENCODE return blank today: their
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
  (ANTHROPIC four-counter cache collision, ambiguous full matches, no usage,
  and the non-ANTHROPIC blank path) and for `write_session_log` carrying the
  new header keys through. The cache-collision case was driven red before the
  selector changed: it returned the first entry's 200,000-token window instead
  of the session's 1,000,000-token window.

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

### Review rework verification

- Driven collision characterization (`python -m pytest -q
  tests/test_agent_loop_policy.py -k family_context_telemetry`) failed before
  the selector change exactly as reviewed: **2 failed, 1 passed** — the cache
  collision returned 200,000 instead of 1,000,000 and the ambiguous full match
  returned 200,000 instead of blank. The same command after the change:
  **3 passed**.
- Final-tree smoke tier: `python -m pytest -q -n auto -m smoke` → **1426
  passed, 6 skipped, 34.97 s**. An immediately following loaded-host budget
  run passed every test but measured **107.9 s** and correctly failed the 60 s
  ceiling; no budget or tier was changed. Its isolated rerun (`python
  scripts/check_smoke_budget.py --mode enforce`) → **1426 passed, 6 skipped,
  27.61 s; 28.1 s vs 60 s budget → within** — one machine, two observed load
  conditions, neither generalized.
- `python project-trajectory/scripts/check_docs.py --root . --stale` →
  **OK — 1109 docs, 1587 intra-repo links, 0 broken (1 pre-existing orphan
  warning)**; `python project-trajectory/scripts/gen_open_items.py --check` →
  **0 pending rows; up to date**.
- Full unfiltered suite (`python -m pytest -q -n auto`) → **3190 passed, 16
  skipped, 804.06 s**.
- Declared effective-stage harness (`python
  project-trajectory/scripts/check.py --jobs 0`) → **RESULT: PASS**; generated
  freshness steps skipped on the work branch by design, and the reported
  `LLR-197` provenance finding is pre-existing at the integration base.
- No spec deviation, byte-budgeted file edit, spine-row change, or approval
  brief regeneration.
