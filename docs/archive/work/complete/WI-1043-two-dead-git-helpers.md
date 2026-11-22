+++
id = "WI-1043"
title = "Two history helpers nothing calls are removed from the kit's scripts"
workstream = "process"
sr_refs = []
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1043`, cut from `refactor_again` at
`1b22c9355`, with the commit hooks on. The specref (the history-reader audit,
`docs/reviews/2026-11-history-readers/README.md`) is cleared at close, as a
terminal row's is.

- `13ad36174` (`WI-1043: delete two git helpers nothing calls`): the two
  deletions, the facade and test edits, two ratchet tightenings, the RESYNC
  entry, the decisions record and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**What landed.**

- `integrate._last_commit_time` is deleted. `ac.git` keeps its other
  callers, so no import goes.
- `traj_parse._git` is deleted. `subprocess` and `_run_captured` stay,
  because `_asof` calls them. The module docstring names the capture seam
  `_run_captured`/`_asof`, and `_run_captured`'s docstring names `_asof` as
  its one remaining caller.
- `gen_trajectory.py`'s `from traj_parse import (...)` block no longer names
  `_git`. Nothing read `gen_trajectory._git`.
- In `tests/test_traj_parse.py`,
  `test_run_captured_states_the_five_keywords_and_degrades_off_git` loses two
  assertions:
  - `assert tp._git(tmp_path, "rev-parse", "HEAD") == (1, "")`, under the
    shim that raises `OSError`;
  - `code, out = tp._git(tmp_path, "rev-parse", "--verify", "--quiet",
    "HEAD")` with `assert code != 0 and out.strip() == ""`, a real git
    outside a repository.

  Its comments, and the WI-346 note at the top of the module, no longer name
  `_git`. `_run_captured`'s off-git degradation stays covered. The same test
  still asserts that `_run_captured` itself lets the shim's `OSError`
  through, and that `_asof`, its one caller, returns `""` both under that
  shim and with a real git outside a repository. Those are the two off-git
  shapes the removed lines checked, read through the caller that remains.
- Two ratchets tighten, as their own rules direct.
  `tests/test_module_size_ratchet.py` re-stamps `integrate.py` down, 1793 ->
  1788 SLOC. `tests/test_stage_event_detectors.py`'s `splitlines()[0]` sweep
  drops `integrate.py` from its allow-list, because its one site was inside
  `_last_commit_time`. The first importer run failed on exactly that: the
  sweep found two files against an allow-list of three.
- `RESYNC_PACK.md` gains "Two private git helpers nothing called are deleted
  [since 1b22c9355]", with nothing forced. `check_resync.py` owed it for the
  three shipped scripts.

**The scope reading, D-001** (`docs/decisions/maint-wi-1043.toml`). The
audit and this row's Context said nothing called `traj_parse._git`. The
builder's grep found the test above calling it. That call came in with
`cde260dd0` and was already there at the audit's base `1aa6c439a` and at
`a0ca15d3f`. The builder stopped and reported. The coordinator ruled that
test-only use is not a caller, that Done-when 1's "no remaining reference"
already requires removing the facade re-export and the test lines, and that
the grep covers code (scripts, tests, skills, templates and shipped docs),
not records.

**The grep.** At the close-out commit, over the code, with the records
excluded:

```
EX="--exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=iteration --exclude-dir=reviews --exclude-dir=archive --exclude-dir=log.d"
grep -rn "_last_commit_time" $EX . | grep -v "^./docs/log.md:"
grep -rnE "(traj_parse|tp|gt|gen_trajectory)\._git\b" $EX . | grep -v "^./docs/log.md:"
grep -nw "_git" project-trajectory/scripts/traj_parse.py project-trajectory/scripts/gen_trajectory.py tests/test_traj_parse.py
```

The third prints nothing. The first two print only the three notes this row
wrote to record the deletion, which name the helpers as gone:
`docs/decisions/maint-wi-1043.toml` (D-001), the `RESYNC_PACK.md` entry, and
the re-stamp note on `integrate.py` in `tests/test_module_size_ratchet.py`.
Nothing calls, imports or re-exports either helper. The other `_git` names in
the scripts and tests are
separate helpers, each defined in its own module: the `kitlib.git.git_out`
aliases, `bookkeeping._git`, `tests/integrate_fixtures._git` and two
test-local ones. The records keep their mentions: `docs/log.md`, two
`docs/iteration/` logs, `docs/reviews/WI-378-REVIEW-A.md`, the WI-585
adjudication round, the audit, the scope critiques, this spec and its log
fragment.

**Tests.**

- The test modules importing a changed module (`integrate`, `traj_parse`,
  `gen_trajectory`), found by grep and by `trace.py --tests-for`, with
  `test_import_layers`, `test_module_size_ratchet` and `test_dogfood_sync`:
  80 modules, `2 failed, 3249 passed, 20 skipped in 3113.43s (0:51:53)`.
  This ran on the build's edits before the allow-list fix. The two failures
  were the `splitlines()[0]` sweep, fixed above, and the vocabulary red
  below.
  <!-- fig: cmd="python -m pytest -q -n auto (the union of: the test modules importing integrate, traj_parse or gen_trajectory by grep; trace.py --tests-for each of the three; test_import_layers, test_module_size_ratchet, test_dogfood_sync)" rev="1b22c9355 plus the build's edits, before the allow-list fix" -->
- `tests/test_traj_parse.py`, `test_stage_event_detectors`,
  `test_module_size_ratchet`, `test_import_layers`, `test_dogfood_sync`,
  `test_resync_pack` and `test_stage_ladder`: `1 failed, 99 passed, 1
  skipped in 36.94s`. The failure is the vocabulary red.
  <!-- fig: cmd="python -m pytest -q tests/test_traj_parse.py tests/test_stage_event_detectors.py tests/test_module_size_ratchet.py tests/test_import_layers.py tests/test_dogfood_sync.py tests/test_resync_pack.py tests/test_stage_ladder.py" rev=13ad36174 -->
- `run_menu.py smoke`, on the tree committed as `13ad36174`. The lints pass:
  `trace.py --strict` gives `orphans=0 integrity=0`, `check_trajectory.py
  --strict` is clean, `check_docs` gives `OK - 3606 doc(s), 3823 intra-repo
  link(s), 0 broken.`, and `check_resync` gives `OK, 3 shipped path(s)
  changed; entry anchored at 1b22c9355...`. The tier then gives `1 failed,
  3713 passed, 3 skipped, 18 warnings in 158.18s (0:02:38)`, with a CPU
  budget WARN only (748.0 s against 540). The failure is the vocabulary red.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev=13ad36174 -->
- The build commit's hook: 29 steps, all PASS.
- The unfiltered suite was not run.

**Outside this row: one red.**
`test_stage_ladder::test_this_repo_is_clean_at_the_ERROR_severity` fails on
a retired gate tag at lines 46 and 100 of
`docs/work/queued/WI-1024-constrains-coverage.md`. It is in the base
`1b22c9355` (from `1b15d07fb`), this row touches no such file, and trunk
fixed it at `dd8f79e6c`. The station's refresh brings the fix.

**Byte deltas:** `RESYNC_PACK.md` 737,613 -> 738,316 (unbudgeted). No
budgeted file was touched.

**Acts owed:** none. No spine row changed.

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, which
found two helpers that read git history and have no caller anywhere in the
repository: `integrate._last_commit_time` and `traj_parse._git` (checked by
grep at `a0ca15d3f`, compiled caches aside). Dead history readers invite a
later caller to recompute a decision from history.

The two deletions could land apart; they ride one row by choice, as one
cleanup the same review reads, and land together in one commit.

## Done-when

- [x] Both functions are deleted, with any import only they used; a grep of
      the repository shows no remaining reference.
- [x] The test modules importing `integrate` and `traj_parse` pass, with
      `test_import_layers` and `test_module_size_ratchet`; a RESYNC entry is
      added if the commit checks ask for one.
