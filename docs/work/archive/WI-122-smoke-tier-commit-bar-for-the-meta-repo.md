+++
id = "WI-122"
title = "Smoke-tier commit bar for the meta repo (populate + re-point per-commit tests)"
workstream = "scripts"
needs = ["~WI-071", "~WI-075"]
order = 121
+++

## Deliverable

Owner-directed 2026-07-13: the meta commit bar drops from the full suite to the fast smoke tier. Design is OPT-OUT (defends never-a-false-green): tests/conftest.py's pytest_collection_modifyitems marks every collected test `smoke` unless its module is in SLOW_MODULES (nine heavy end-to-end modules - full pre-commit/pre-push hook runs, scaffold bootstraps, dev-setup, profile byte-compares, perf/design-flow gate-step scaffolds), which get `slow`; smoke+slow partition the suite (531+153=684, none in neither/both) so a NEW test is in the bar by default. root pytest.ini registers smoke/slow/full/release + --strict-markers. Commit bar re-pointed at `pytest -q -n auto -m smoke` in the ONE home (session-protocol skill 3, fan-out .claude/.agents byte-identical) with CLAUDE.md/agent-resume.{sh,cmd}/status.md Bar linking to it; full unfiltered suite stays the close/gate/CI bar (PROCESS_OPTIONS 'Phase cadence' already sanctioned pytest -m smoke per commit generically - this is the meta adoption). Measured smoke ~47s/531 vs full ~66s/684 (~30%; suite is subprocess-bound + already xdist so the floor is spawn overhead, reported honestly); check.py --tier smoke now meaningful for the meta (was empty). Guard: test_smoke_tier.py asserts the partition is total + SLOW_MODULES are real files. Close bar green: full suite 681 passed/3 skipped, check_docs 0 broken.
