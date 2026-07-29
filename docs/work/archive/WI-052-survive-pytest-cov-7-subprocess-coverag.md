+++
id = "WI-052"
title = "Survive pytest-cov 7 (subprocess coverage)"
workstream = "self-adoption"
order = 51
+++

## Deliverable

Dependency rot (commit 6004004, 2026-07-10): pytest-cov 7 removed the COV_CORE_* env contract; conftest.augment_env keyed on COV_CORE_DATAFILE alone, so every child process ran unmeasured and the coverage floor read 29% vs the 80 bar. Detection now asks the live session (coverage.Coverage.current()) with the env var as legacy fallback; coverage restored to 91%. Failing-first regression test in test_check_harness.py (skips outside a measured run). Also heals the ubuntu CI check job, which pip-installs latest pytest-cov. Wiring provenance: Thread 47 phase 6.
