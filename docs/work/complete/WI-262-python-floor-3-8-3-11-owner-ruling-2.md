+++
id = "WI-262"
title = "Python floor 3.8 -> 3.11 (owner ruling 2026-07-21; supersedes repo-review-2026-07-21 L-19): one kit-wide floor bump - requirements-dev.txt collapses to a single pytest-cov~=7.0 (the 5.x leg and its CI-unverified subprocess-coverage path dissolve, closing L-19), conftest.py sheds the pytest-cov 5.x branch (WI-105 dual-major plumbing), CI matrix 3.8 cells -> 3.11 (macOS arm64 exclusion may simplify), and the mechanical prose sweep (~15 script docstrings Python 3.8+, CLAUDE.md, READMEs, PROCESS/ADOPTING, stack.ini, test_stdlib_only floor comments, gen_okf.py:576-class scar comments, scripts/dev-setup.{sh,ps1,cmd,command} header comments + install-Python-3.8+ hint strings - no hard gate there, requirements-dev.txt carries the constraint). Rationale recorded: 3.9/3.10 rejected as EOL/EOL-Oct-2026; 3.11 supported to Oct 2027, enables dataclass slots for the queued trace.py refactor (M-7), finer tracebacks, interpreter speedup. DOWNSTREAM MIGRATION FLAG: withdraws the system-Python accommodation for RHEL 9 / Debian 11 (3.9) and Ubuntu 22.04 (3.10) - scripts stay de-facto compatible until 3.11-only syntax lands, but the promise changes; note in ADOPTING/resync"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 259
+++

## Deliverable

Python floor 3.8 -> 3.11 (kit-wide prose+config sweep, supersedes L-19): requirements-dev.txt collapses the pytest-cov Python-gated split to a single pytest-cov~=7.0; conftest.py sheds the pre-7 COV_CORE_DATAFILE branch (keeps the 7.x Coverage.current() path); CI matrix 3.8->3.11; stack.ini + 16 script docstrings + CLAUDE.md/READMEs/PROCESS/dev-setup + the session-protocol skill floor declaration bumped; ADOPTING migration recipe added. Scripts stay de-facto 3.9-runnable (no 3.11-only syntax); full suite 1348 passed, coverage 91.51% (conftest wiring intact). PROCESS.md kept byte-neutral. Requirement spine (SN-011/SR-034/SR-035/architecture overview) deliberately LEFT at 3.8 -> separate requirements-change follow-up WI. Adversarial REVIEW-A CHANGES-REQUESTED f=3 -> MAJOR skill-floor miss + MINOR test comment fixed and re-verified (skill-sync 12/12), SR-035 CI-narrative deferred to the spine WI.
