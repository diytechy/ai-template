+++
id = "WI-301"
title = "Toolchain prereq preflight - a below-floor interpreter must be named ONCE and loudly, not surface as ~50 opaque agent_loop reds"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 298
+++

## Deliverable

Landed 2026-07-25. tests/test_prereq_toolchain.py (two hard failures: the RUNNING interpreter, which seed_venv builds fixture venvs from, and the ROOT ./.venv, which agent_dispatch._harness_floor_failures probes - distinct preconditions) + conftest floor helpers (declared_python_floor/floor_shortfall/skip_below_floor) reading agent_common.MIN_PYTHON and agent_common.interpreter_version rather than restating the floor, + a controller-only pytest_sessionstart banner, + skip guards at the two real dependencies (seed_venv; the dev-setup --install test). Measured on a CLT-Python 3.9.6 .venv: 49 failed/1436 passed/3 skipped -> 2 failed/1381 passed/107 skipped. Module re-tiered to SLOW_MODULES on the test_session_stdin precedent - it is designed to red below the floor, so leaving it in the commit bar would make that bar unpassable on the machine needing the fix; the banner still fires in the smoke tier, so only the hard stop moves to close/CI.
