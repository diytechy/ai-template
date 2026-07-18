# 003 — REVIEW-A (independent)

Work under review: WI-226 BUILD, base `808f95d..752a378` — the strong/high-risk
**dispatcher decomposition** (`docs/specs/WI-226.md`, review-18 H-02 slice B,
absorbs L-04): characterize `dispatch_run`, extract value-only decisions from
effects, then split the tests along the new boundary. Diff touches only
`project-trajectory/scripts/agent_dispatch.py` (+97 lines net), the three test
modules, `test_complexity_ratchet.py` (one re-stamp), the WI-226 spec, and the
two session telemetry logs. No SN/SR/LLR/TC rows added or changed → no registry
sweep needed. Not a gate-ratification commit (WI-226 stays `queued`,
work-items.csv unchanged) → no batch-ratification hierarchy required.

## Harness (run and observed, not trusted)

- `check.py` (derived gate **G3**) → `RESULT: PASS`, all 16 steps green
  (`tests+coverage` 212.8s). An earlier FAIL was my own artifact — two
  `pytest --cov` runs colliding on `.coverage`; re-run clean is PASS.
- `pytest -q -n auto --cov=... --cov-fail-under=85` → **1115 passed, 3 skipped**,
  total coverage **91.22%** (agent_dispatch.py 84%; the gate is total, not
  per-file).
- `trace.py --strict --no-placeholders --require-verified --strict-schema` →
  `SN=25 SR=66 LLR=76 TC=76 orphans=0 integrity=0 status-findings=0
  placeholders=0 schema-findings=0 interface-findings=0` (spine intact).
- `ruff C901 --max-complexity=10` over the scripts → census **52 entries**;
  `dispatch_run = 40` exactly (the declared Stage-2 target); no new function
  over 10. `test_complexity_ratchet.py` re-stamped `dispatch_run 84 -> 40`,
  baseline count 52, test passes.
- New `tests/test_agent_dispatch_decisions.py` → **46 passed in 0.06s** with no
  repo/git/worktree/journal/session fixture (needs-git skip absent), confirming
  the value-only claim.

## Verification of behaviour preservation (read against 808f95d)

- All 8 pure decision functions reproduce the original inline logic exactly:
  head-reconcile (fast-forward / needs-human / publish), train-evidence
  classification (foreign→quarantine priority preserved), dispatch/retry
  eligibility, worker-exit disposition, integration-result mapping (journals
  the raw `result`, not the mapped state — correct), idle action, terminal
  run-state/banner/exit-code.
- Effect wrappers (`_reconcile_owned_trains`/`_reconcile_reserved_train`,
  `_spawn_worker`, `_handle_worker_exit`, `_resume_reconciled`,
  `_frontier_snapshot`, `_integrate_parked`, `_apply_idle_action`,
  `_finish_dispatch`) preserve journal event names, fields, ordering, and ref
  discipline. The tricky `needs_human_ask = ask or needs_human_ask` caller
  pattern faithfully reproduces the original set-only/never-reset semantics.
- Public surface unchanged: only `_`-prefixed private functions added; the two
  removed defs were the nested `spawn_worker`/`handle_exit` (not public). No
  downstream migration burden — spec non-goal honoured.
- Test split faithful: the 6 packing cases moved from the effect modules with
  assertions preserved or strengthened (full-dict equality), no duplication;
  the 40 decision cases relocated from `test_agent_loop_dispatch.py` into the
  dedicated module; `schedule` import correctly dropped from the train module.

## Findings

None.

VERDICT: APPROVE findings=0
