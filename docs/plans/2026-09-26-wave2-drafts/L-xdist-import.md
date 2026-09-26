+++
id = "WI-@L@"
title = "Make the stage test modules import on their own under xdist"
workstream = "tests"
specref = "tests/conftest.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

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
