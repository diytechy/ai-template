# P0b accounting completion review — Opus 5, high

Provider session: 9d8bf415-ff0d-42ef-a07f-ce70ed85ba51

Subject SHA256: `6400b9c48325f806a9f1d38580da5e6f6b10495c124d3dc6149ecb42ce1c955a`

## Blockers

**1. `phase_draw_ordinal` now counts non-worker calls, and only lowercase spelling hides it.**

`invoke_and_persist` writes `phase = metrics.get("role", "")` into the header of every `call_*.log`, in the same `docs/iteration` directory the draw-rotation counter scans. `select_with_probe` → `route_session` derives its ordinal from `phase_draw_ordinal(ctx.draw_iter_dirs, phase)`, so a planner or probe row whose role string equals a routed phase silently shifts worker route selection.

Nothing in the code enforces disjointness. The one test that could catch it — `test_planner_logs_coexist_with_worker_numbering_and_index` — asserts `phase_draw_ordinal(logs, "CRITIQUE") == 1` while passing `attribution={"role": "critique"}`; it passes because of letter case, not because `call_` logs are excluded. `test_interactive_boots_exactly_one_session`'s `== 0` proves nothing either: `INTERACTIVE` is not a phase name under any filtering rule. The first caller that passes `role="CRITIQUE"` or `"REVIEW-A"` (the natural spelling — every other role constant here is upper-case) perturbs the rotation with no failing test.

Fix where `next_session_number` already draws the line: a `call_`-named log has no session ordinal, and it should have no draw ordinal. Filter `phase_draw_ordinal` on the same predicate (name prefix, or `train` presence), and re-drive the dual-plan test with `role="CRITIQUE"` so the invariant is asserted rather than spelled.

**2. Provider-controlled strings reach the `# key: value` header unsanitized.**

`_result_accounting` copies `session-id`, `reported-model`, and `usage-scope` verbatim from parsed provider JSON, and `write_session_log` emits them as `"# {}: {}".format(...)`. A value containing a newline writes additional header lines that `read_log_meta` will parse as real fields — forging `outcome: COMPLETED`, `wi:`, or `commits:` into a tracked, committed log and into the regenerated index. `redact_secrets` covers the transcript only; the header is below that boundary.

Three of the four affected keys are new-ish arrivals and this change puts them on three more paths, so it belongs here. One line at the writer: coerce each value to its first line (`str(v).splitlines()[0] if ... else ""`) rather than at each producer — the writer is the single place that owns the header grammar.

## Optional, smaller

- `_dp_session` sets `role` and `requested-model` but no `source-event`, so planner rows are the only one of the three classes not identifiable by event; probes and interactive both set it. `metrics.setdefault("source-event", "dual-plan")` costs one line and makes the three paths symmetric.
- `metrics.update(phase=metrics.get("role", ""))` overwrites unconditionally. No current caller sets `phase`, so this is pre-emptive only — `setdefault`-style would be truer to "caller-owned metadata," but leaving it is defensible.
- The `finally` body can replace a propagating launch exception with a persistence exception (unwritable `docs/iteration`, root not a directory). `test_interactive_launch_error_is_recorded_then_raised` pins the happy path of the re-raise, not this one. Narrow, not a robustness layer: the write/commit pair is already best-effort in spirit — a bare `except Exception` around just those two calls, printing to stderr, keeps the original traceback authoritative.

## Checked, no finding

Probe telemetry lands before `before = head_sha(root)`, so it is correctly outside the worker's `commits` range; the `--only -- <rels>` scope holds on the paths arm; a non-git root returns early from `commit_telemetry` without crashing (exercised by the interactive error test); `call_<uuid>` names cannot collide across parallel lanes and are correctly invisible to `next_session_number`'s ordinal regex; the attached runner's `("", False)` result flows to an honest `usage-status: unavailable` rather than a fabricated zero; `timed_out` as `"idle"` classifies TIMEOUT correctly; probe `COMPLETED` with a failed `OK` predicate is the intended split.

**Verdict: changes requested** — both blockers are local, and the persistence boundary itself is the right shape.
