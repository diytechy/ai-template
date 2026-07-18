"""Auto-start coverage in the subprocesses the meta-repo self-tests spawn.

Python imports `sitecustomize` at interpreter startup if it is on the path.
`tests/conftest.run_py` puts *this* directory on the subprocess `PYTHONPATH`
(only when pytest-cov is measuring the parent) and sets `COVERAGE_PROCESS_START`,
so each child that runs a kit script records coverage too. `process_startup()`
is a no-op unless `COVERAGE_PROCESS_START` is set, so this file is inert in any
other context. (IMPROVEMENT_PLAN.md Thread 47 phase 6.)
"""

import coverage

coverage.process_startup()
