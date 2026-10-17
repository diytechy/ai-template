## 2026-10-17 — WI-931: kept-test evidence at the claim base (P0)

### Kept-test evidence (D3–D11)

The plan's P0, before any code changes: the kept ordinary-kill selection
(15 items) at the claim base `785b29e11e53f65cc5fc8530f8ac0da485f6c4de`,
on Windows in the lane worktree (its code equal to the base) and on Linux
in WSL Ubuntu (owner ruling, wi-931 D-002), from a clone in WSL's own
filesystem checked out detached at the base. Both match the plan's
expected outcomes: Windows 15 passed; Linux 11 passed, 4 skipped, the four
skips the tests' own Windows-only marks.

#### Windows, claim base

```text
lane code equals the claim base
7a4e14ce85bd2d2ef5a1b3de84ec0cb9c1e7d3de
Python 3.11.9
pytest 9.1.1
conftest: this run is already inside another job object, so it could not join the shared 'ai-template-pytest' job and is capped at 50% ON ITS OWN rather than sharing one ceiling (concurrent runs can then total more than 50%)
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\wi-931
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs PASSED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] PASSED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] PASSED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise PASSED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

============================= 15 passed in 14.97s =============================
pytest exit=0
```

#### Linux (WSL Ubuntu), claim base

```text
785b29e11e53f65cc5fc8530f8ac0da485f6c4de
Python 3.12.3
pytest 7.4.4
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs SKIPPED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] SKIPPED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] SKIPPED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise SKIPPED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

=========================== short test summary info ============================
SKIPPED [1] tests/test_session_stdin.py:471: job containment is Windows
SKIPPED [1] tests/test_session_stdin.py:391: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:430: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:800: the job snapshot is Windows
======================== 11 passed, 4 skipped in 9.62s =========================
pytest exit=0
```

## 2026-10-17 — WI-931: kept-test evidence at the rebased base and the tip (P0 re-run, P7, P8)

### Kept-test evidence (D3–D11) at the rebased base and the tip

The lane was rebased from trunk's `61ee4e165` onto `2b2350add`
(WI-928's landing and WI-938's close), after trunk's `project-trajectory/`
and `tests/` had changed since the earlier base (WI-935, WI-928). So P8's
check 2 moves the base: the records above, at `785b29e11`, describe the claim base
the lane was cut from, and these four describe the base and the tip the
lane lands from. `BASE = 2b2350add0170f6cfa46cab385f451b1df2bdfb1`, the lane's merge base with trunk;
`TIP = 0f6b2747f513043991803bcc6a6b8360f1c49c81`, the lane commit whose `project-trajectory/`, `tests/`,
`conftest.py` and `pytest.ini` are final. Windows at `BASE` ran in a
detached scratch checkout at `BASE` (the lane worktree holds the change);
Windows at `TIP` in the lane worktree; Linux at both in the WSL clone, each
checked out detached. The rebase left `agent_session.py`,
`tests/test_session_stdin.py`, `tests/test_session_keep.py` and
`tests/test_agent_loop.py` byte-unchanged.

#### Windows, BASE

```text
2b2350add0170f6cfa46cab385f451b1df2bdfb1
Python 3.11.9
pytest 9.1.1
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\trunk-tmp
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs PASSED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] PASSED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] PASSED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise PASSED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

============================= 15 passed in 14.75s =============================
pytest exit=0
```

#### Linux (WSL Ubuntu), BASE

```text
2b2350add0170f6cfa46cab385f451b1df2bdfb1
Python 3.12.3
pytest 7.4.4
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs SKIPPED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] SKIPPED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] SKIPPED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise SKIPPED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

=========================== short test summary info ============================
SKIPPED [1] tests/test_session_stdin.py:471: job containment is Windows
SKIPPED [1] tests/test_session_stdin.py:391: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:430: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:800: the job snapshot is Windows
======================== 11 passed, 4 skipped in 8.62s =========================
pytest exit=0
```

#### Windows, TIP

```text
0f6b2747f513043991803bcc6a6b8360f1c49c81
Python 3.11.9
pytest 9.1.1
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\wi-931
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs PASSED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] PASSED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] PASSED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise PASSED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

============================= 15 passed in 14.53s =============================
kept exit=0
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\wi-931
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 1 item

tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises PASSED [100%]

============================== 1 passed in 0.56s ==============================
bound exit=0
```

#### Linux (WSL Ubuntu), TIP

```text
0f6b2747f513043991803bcc6a6b8360f1c49c81
Python 3.12.3
pytest 7.4.4
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs SKIPPED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] SKIPPED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] SKIPPED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise SKIPPED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

=========================== short test summary info ============================
SKIPPED [1] tests/test_session_stdin.py:470: job containment is Windows
SKIPPED [1] tests/test_session_stdin.py:390: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:429: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:543: the job snapshot is Windows
======================== 11 passed, 4 skipped in 8.60s =========================
kept exit=0
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 1 item

tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises PASSED [100%]

============================== 1 passed in 0.35s ===============================
bound exit=0
```

### P7 at the tip: module runs and complexity

- `tests/test_session_stdin.py`, `tests/test_agent_loop.py` and
  `tests/test_session_keep.py` with `-n auto` at `TIP`: 258 passed.
- `check_complexity.py --mode enforce`: unchanged from baseline.
- Coverage: the rebase changed none of `agent_session.py` or its test
  modules, so the figure measured at the pre-rebase tip `4e6b1318f`
  stands: `agent_session.py` 86.55% over a 16-module subset (floor 72).

### P8 completion check

1. Four records: the four above each list the same 15 items, and each
   item's outcome matches the plan's expected-outcome table, skip reasons
   included: Windows 15 passed at `BASE` and `TIP`; Linux 11 passed and 4
   skipped at both, the skips "job containment is Windows", "a .cmd shim
   is Windows" (twice) and "the job snapshot is Windows".
2. The records describe the landing: `git diff --quiet BASE
   $(git merge-base wi-931 refactor_again) -- project-trajectory tests
   conftest.py pytest.ini` and `git diff --quiet TIP wi-931 -- ...` are
   both silent at this record's commit.
3. Unchanged kept bodies: `git diff BASE TIP -- tests/test_session_keep.py`
   is empty. `git diff BASE TIP -- tests/test_session_stdin.py` deletes the
   six tests and five helpers (`_marker_child`, `_session_outcome`,
   `_InterruptingThread`, `LATE_SPAWNER`, `_late_spawn_round`), adds the one
   D2 assertion line and D8's two comment lines, and deletes one line
   beyond the plan's three things: the module's `import subprocess`, which
   only the deleted tests used.
4. D3–D11 met: Windows 15 passed at 2b2350add and 0f6b2747f; Linux 11
   passed, 4 skipped as documented at 2b2350add and 0f6b2747f; kept bodies
   unchanged.

## 2026-10-17 — WI-931: P7 and P8 again at the tip after round 1's reflow

Round 1's one code change (wi-931 D-006), a comment in `agent_session.py`
reflowed with its words unchanged, makes `4dbd3bd78` the new `TIP`
(P7: a commit that changes `project-trajectory/` moves it). `BASE` is
unchanged, `2b2350add`, so its two records above still stand. Both legs
ran again at the new `TIP`: Windows in a detached scratch worktree at
`TIP` (the lane worktree was in use by its checkpoint sitting), Linux in
the WSL clone checked out detached.

#### Windows, TIP

```text
4dbd3bd781d6ea1395ac8910328d91070ef81361
Python 3.11.9
pytest 9.1.1
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\review-tmp\2026-10-17-coord\wi-931\parent-wt
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs PASSED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] PASSED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] PASSED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise PASSED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

============================= 15 passed in 15.49s =============================
kept exit=0
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Projects\ai-template\.venv\Scripts\python.exe
rootdir: C:\Projects\ai-template.wt\review-tmp\2026-10-17-coord\wi-931\parent-wt
configfile: pytest.ini
plugins: cov-7.1.0, xdist-3.8.0
collecting ... collected 1 item

tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises PASSED [100%]

============================== 1 passed in 0.58s ==============================
bound exit=0
```

#### Linux (WSL Ubuntu), TIP

```text
4dbd3bd781d6ea1395ac8910328d91070ef81361
Python 3.12.3
pytest 7.4.4
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 15 items

tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs SKIPPED [  6%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[python-parent] PASSED [ 13%]
tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild[cmd-shim] SKIPPED [ 20%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[python-parent] PASSED [ 26%]
tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild[cmd-shim] SKIPPED [ 33%]
tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise SKIPPED [ 40%]
tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error PASSED [ 46%]
tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child PASSED [ 53%]
tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape PASSED [ 60%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick] PASSED [ 66%]
tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[finish] PASSED [ 73%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick] PASSED [ 80%]
tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[finish] PASSED [ 86%]
tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree PASSED [ 93%]
tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed PASSED [100%]

=========================== short test summary info ============================
SKIPPED [1] tests/test_session_stdin.py:470: job containment is Windows
SKIPPED [1] tests/test_session_stdin.py:390: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:429: a .cmd shim is Windows
SKIPPED [1] tests/test_session_stdin.py:543: the job snapshot is Windows
======================== 11 passed, 4 skipped in 9.10s =========================
kept exit=0
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
rootdir: /root/wi-931-posix
configfile: pytest.ini
collecting ... collected 1 item

tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises PASSED [100%]

============================== 1 passed in 0.52s ===============================
bound exit=0
```

### P8 completion check, renewed

The four records are now Windows and Linux at `BASE` (above) and Windows
and Linux at this `TIP`. Check 1 holds: the same 15 items, each outcome as
the plan's table states, skip reasons included. Check 2's two diffs are
silent at this record's commit. Check 3 holds as before:
`tests/test_session_keep.py` is unchanged and `tests/test_session_stdin.py`
changes only as recorded above, since the reflow touched neither.

D3–D11 met: Windows 15 passed at 2b2350add and 4dbd3bd78; Linux 11 passed, 4 skipped as documented at 2b2350add and 4dbd3bd78; kept bodies unchanged.
