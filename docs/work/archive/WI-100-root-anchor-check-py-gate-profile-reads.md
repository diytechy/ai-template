+++
id = "WI-100"
title = "Root-anchor check.py gate/profile reads or fail loudly off-root (M2)"
workstream = "scripts"
order = 99
+++

## Deliverable

check.py's docs/gate + docs/stack.ini + docs/architecture.md reads are CWD-relative (unlike the sibling scripts' --root), so running it off the repo root silently fell back to the built-in commands + gate `all` — a different, weaker plan, not an error. Took the review's loud-fail option (the WI title's "or fail loudly"): main() now refuses to run when no docs/ dir sits at CWD, naming the cwd. Smallest fix that closes the silent divergence, no new inherited flag/chdir semantics for downstream check.py. Added tests/test_check_harness.py::test_off_root_fails_loudly. No spine change (G3). Full suite 701 passed.
