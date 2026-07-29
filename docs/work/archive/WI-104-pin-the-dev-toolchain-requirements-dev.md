+++
id = "WI-104"
title = "Pin the dev toolchain (requirements-dev; CI + dev-setup consume) (M6)"
workstream = "scripts"
order = 103
+++

## Deliverable

WI-104 (2026-07-13): pinned the meta-repo's OWN dev toolchain so the same machinery runs everywhere and a tool major can't turn the gate red unrelated to any commit (the 2026-07-12b review's M6). New root requirements-dev.txt with compatible-release (~=) pins for the four tools the self-tests + gate drive - ruff~=0.15.0, pytest~=8.3, pytest-xdist~=3.6, and a Python-gated pytest-cov split (~=7.0 on 3.9+, ~=5.0 on the 3.8 floor, since pytest-cov 6.0 dropped 3.8 - the one irreducible per-Python difference WI-105 must harden across). The kit SCRIPTS stay stdlib-only and nothing ships downstream (project-trajectory/scripts/setup.* + ci/check.yml are the adopter's own templates, untouched). Consumers rewired to install `-r requirements-dev.txt`: both jobs in .github/workflows/test.yml (test + gate) and both meta dev-setup twins (scripts/dev-setup.sh, scripts/dev-setup.ps1); the .command wrapper delegates unchanged. Added .github/workflows/canary.yml - a NON-gating weekly (+ workflow_dispatch) job that installs UNPINNED latest and runs ruff format/lint + the suite, preserving the early-warning that unpinned CI used to give for free so a pin bump is a heads-up, not a surprise red. Verified on the pinned 3.8 resolution in a throwaway venv (pytest 8.3.5, pytest-cov 5.0.0, ruff 0.15.21, xdist 3.6.1, coverage 7.6.1): full suite 695 passed / 3 skipped, ruff format+lint clean, smoke 543 passed, check_docs --stale OK. Hard-edges WI-105 (coverage-plumbing fix, now verifiable on one known toolchain). No spine change, no byte-budgeted file touched.
