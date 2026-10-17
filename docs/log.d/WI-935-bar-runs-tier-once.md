## 2026-10-16 — WI-935: the commit bar runs the smoke tier once

The builder's readings of the new bar, `run_menu.py smoke`, whose steps are
now both strict lints and the docs staleness check, then the budget step's
timed tier run, which is the bar's only tier run. Each run shows one pytest
session (one `timing:` line, one summary line: 2623 passed, 2 skipped). The
whole bar was timed around the launcher; the tier's time is the budget
step's own reading. Before the change the bar cost two tier runs, about 112
to 115 s quiet (2026-10-16). Every reading below is a lane-tip run with the
build uncommitted on 785b29e11. No run is confirmed quiet: right after the
third run, other lanes' test runs were on the box (30 Python processes, 73%
CPU), and every tier run reported its own 50% job-object cap.

- Run 1: bar 164.1 s, tier 113.3 s (pytest 112.25 s), exit 1 on the breach alone. <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="785b29e11 + the WI-935 build" -->
- Run 2: bar 116.6 s, tier 61.7 s (pytest 60.89 s), exit 1 on the breach alone. <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="785b29e11 + the WI-935 build" -->
- Run 3: bar 126.6 s, tier 65.3 s (pytest 64.54 s), exit 1 on the breach alone. <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="785b29e11 + the WI-935 build" -->

The tier was green in every run and the lints passed, so each bar's nonzero
exit is the 60 s budget. The three tests this row adds to the tier cost about
0.4 s together.

The quiet reading, on the lane tip c430b0b38 (rebased on 61ee4e165) on a
quiet box the owner gave on 2026-10-17, at normal priority with nothing else
running: one pytest session (one `timing:` line; 2623 passed, 2 skipped),
both strict lints and the docs staleness check clean, exit 0.

- Quiet run: bar 66.2 s, tier 42.3 s (pytest 41.75 s), exit 0, beside the old bar's 112 to 115 s. <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="c430b0b38" -->
