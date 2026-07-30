## 2026-07-30 — WI-371: shoot.mjs cleans only the PNGs it owns

The shot harness's whole-dir `rmSync` destroyed any baseline a session
stored under `shots/` — hit twice in the 2026-07-30 render session (both
builders lost their first BEFORE set and re-shot from a worktree).

- **Deliverable:** the pre-run clean in
  [shoot.mjs](../../scripts/dashboard-shots/shoot.mjs) removes only the
  harness's own top-level `*.png`; subdirectories (session baselines)
  survive; the listing prints only PNGs; the
  [README](../../scripts/dashboard-shots/README.md) states the contract.
  Spec archived:
  [WI-371](../work/archive/WI-371-shoot-mjs-deletes-session-baselines.md).
- **Deviations from spec:** none (the spec's first option, as recommended
  there). No pytest coverage, deliberately: meta-only Node dev tooling
  with no test harness — verified live (a planted `shots/before/` marker
  survived a full 36-shot run).
- **Suite:** smoke 551 passed / 1 failed (the standing WI-357 work-branch
  conditional); full `pytest -q -n auto` (posix-shell gate satisfied) at
  the close: 1682 passed / 11 skipped / 1 failed — the same sole standing
  conditional, re-green on trunk. `check_trajectory.py --strict` exit 0.
