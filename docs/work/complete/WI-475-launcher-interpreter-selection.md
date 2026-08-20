+++
id = "WI-475"
title = "Launchers accept any runnable python and ignore a valid .venv: prefer the project environment and probe version >= 3.11 before selection (repo review 2026-08-19 H-01)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Every launcher that selects a Python now prefers the repository's `.venv`
and probes each candidate by RUNNING it — once for runnability (the
Store-alias guard) and once for `sys.version_info >= (3, 11)` — refusing
with a list of rejected candidates and reasons when none qualifies: root
`agent-resume.{cmd,sh}` and their shipped templates, plus `check.{sh,ps1}`;
`agent-resume.command` inherits the policy through its `exec` of the `.sh`
twin and now says so (the one honest exception, documented). On Windows the
probe and engine invocations are `call`-prefixed — without it cmd.exe hands
control to a `.cmd` shim python (pyenv-win ships one) and the pre-change
launcher exited 0 having run NOTHING, proven by driving the old launcher
against such a shim. Two real bugs found by executing rather than reading:
PowerShell drops an empty string from a native command line (so a `-c ""`
probe rejected every candidate) and PowerShell 7.4+ turns non-zero native
exits into terminating errors under Stop preference.
`tests/test_launcher_interpreter.py` (27 tests, slow-tiered by the declared
mechanical boundary) executes the selection against fake interpreters that
are the real python with a spoofed version — venv preferred, below-floor
refused AND NAMED, floor-satisfying PATH python taken, stale venv fallen
through, alias stub walked past to `py -3` — replacing the text-inspecting
confidence the review flagged. Verified on a bootstrapped scaffold;
RESYNC_PACK entry `[since 27a65c19]`. Worker full suite: 2621 passed / 13
skipped in 506.88s.

## Context

Confirmed against the tree: `agent-resume.cmd:89-105` probes candidates only
for RUNNABILITY (the Store-alias guard from repo-review 2026-07-21 M-16) —
never for version, and never preferring `.venv` — and the `.sh` launchers and
both shipped templates do the same. `README.md` requires Python 3.11+, and the
kit's scripts import `tomllib` (3.11+). On the review's workspace, ambient
`python` was 3.8.10 while `.venv` held 3.11.9: the advertised one-command
entry point picked the ambient interpreter and `agent_loop.py` died at import
with `ModuleNotFoundError: tomllib`, with a working environment sitting right
there. The existing launcher tests (`tests/test_bootstrap.py`) inspect
launcher TEXT, which is exactly the false confidence the review calls out.

The fix, per the review: prefer the repository's `.venv` interpreter when
present; probe every fallback candidate with `sys.version_info >= (3, 11)`
before selection; on failure emit a diagnostic that LISTS the rejected
candidates and why; apply the same policy to the `check.*` launchers and the
scaffolded templates (root `agent-resume.{cmd,sh,command}` + the
`*.template.*` copies — a scaffold-surface change, so verify by BOOTSTRAPPING
A SCAFFOLD and add the RESYNC entry). Tests must EXECUTE the selection logic
against fake old/new interpreters and against a valid venv plus an invalid
ambient python — not grep the script text.
