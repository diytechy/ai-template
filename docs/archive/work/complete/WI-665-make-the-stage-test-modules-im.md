+++
id = "WI-665"
title = "Make the stage test modules import on their own under xdist"
workstream = "tests"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

Seven test modules failed at collection when an xdist worker was handed only
that module: `test_derive_stage`, `test_phase_rule`, `test_pre_commit_hook`,
`test_kitlib_ladder`, `test_kitlib_station`, `test_kitlib_secret_classes` and
`test_kitlib_stage`. Each ran `from kitlib import ...` before anything had put
the kit's `scripts/` on `sys.path`. `tests/conftest.py` now calls
`_put_scripts_on_path()` when it is imported. The helper removes every
existing spelling of the path and puts it at index 0 exactly once, and
`load_script` shares it. Index 0 matters because the kit's `trace.py` must
shadow the stdlib's.

- **Evidence:** each module was red alone at `-n 2` (ImportError), then
  green. The new slow module `tests/test_conftest_isolation.py` pins the
  class: a subprocess collects `tests/test_kitlib_station.py` alone at `-n 1`,
  and an in-memory test asserts ordering and idempotence. Both were red with
  the fix reverted. The test runs under xdist because a serial run does not
  reproduce the defect: `pytest_sessionstart` loads a script on the
  controller before collection, and xdist workers skip that hook.
- **Review:** Sol's first round asked for the regression and the index-0
  guarantee (arbitration ruling 2). The fix round was SOUND.
- **Out of scope, noted:** about 15 modules still carry their own now-redundant
  path workarounds. They are harmless.

## Context

`tests/test_derive_stage.py` and `tests/test_phase_rule.py` fail at collection
when an xdist worker collects only that module:
`from kitlib import ...` runs before anything has put the kit's `scripts/`
directory on `sys.path`. They pass when a worker happens to collect another
module first, so the failure depends on how xdist distributes the run, and a
targeted run (`pytest -n 2 tests/test_derive_stage.py`) errors. Found by
WI-631's build, which had to run the module serially or beside an in-memory
module.

IN SCOPE: put the scripts path in place before any test module's top-level
kit import (the shared conftest, or the modules' own preamble as their
neighbours do), and check whether other modules import `kitlib` the same way.

## Done-when

- `python -m pytest -q -n 2 tests/test_derive_stage.py` and the same for
  `tests/test_phase_rule.py` collect and pass on their own.
- The commit bar passes.
