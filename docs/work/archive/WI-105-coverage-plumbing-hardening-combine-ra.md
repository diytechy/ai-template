+++
id = "WI-105"
title = "Coverage plumbing hardening - combine race + debris + lost subprocess data (M9/L1)"
workstream = "scripts"
needs = ["WI-104"]
order = 104
+++

## Deliverable

WI-105 (2026-07-13): coverage-plumbing hardening (the 2026-07-12b review's M9/L1). Empirically confirmed WI-104's toolchain pin is the PRIMARY M9/L1 remedy - on the pinned toolchain (pytest-cov 5.0.0 / coverage 7.6.1 on the 3.8 floor; ~=7 on 3.9+) the full suite measures a clean 91.23% (vs the degraded ~82% the old-local pytest-cov 4.1.0 combine race produced), leaves ZERO .coverage.* debris at root, and pytest-cov erases stale parallel files at session start (verified: a seeded stale .coverage.* file was consumed by the next measured run), so the combine race + debris loop do not reproduce and an aborted run self-heals. Added the one MISSING safety net: raised docs/stack.ini [coverage] threshold 80 -> 85, turning a renewed silent subprocess-coverage loss (~91% -> ~82%) into a gate RED instead of passing on '1.83 points of plumbing luck' (mechanizes the review's suggestion 4); ~6 pts headroom on both pinned Pythons, and check.py propagates it via --cov-fail-under (an UNPINNED toolchain now fails here at ~82%, the intended nudge to dev-setup --install). Recorded the closure + pinned-toolchain requirement in .coveragerc, and DECLINED the structural alternative (point subprocess children at a dedicated data dir to unshare the glob): pytest-cov's session-end combine only merges parallel files beside its own datafile, so a separate dir needs an explicit combine step that risks dropping the subprocess coverage the 91% depends on - a poor trade once the pin makes the shared-glob path clean. Meta-only (docs/stack.ini + .coveragerc); NO kit-shipped file changed (the shipped check.py default COVERAGE_THRESHOLD=80 is untouched). Verified on the pinned venv: full suite 695 passed/3 skipped at 91.23% >= 85 (exit 0, 0 debris), smoke 543 passed, check_docs --stale OK.
