+++
id = "WI-480"
title = "Dev-toolchain currency: qualify pytest 9.0.3+, add scheduled Python SCA, and generate a reproducible CI lock (repo review 2026-08-19 M-11, L-04)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

`requirements-dev.txt` pins `pytest~=8.3` (resolved 8.4.2 on this tree,
verified 2026-08-19), and GHSA-6w46-j5rx-g56g is fixed only in pytest 9.0.3+ —
the compatible-release range EXCLUDES the patched line, so the constraint can
retain the advisory indefinitely. Honest severity per the review: development-
only, Unix multi-user `/tmp` preconditions, moderate (CVSS 6.8) — not a
production exposure (the shipped runtime is stdlib-only), but CI/developer
machinery, and the structural point stands: no Dependabot/Renovate/pip-audit/
OSV workflow exists, and the weekly floating-latest canary is a compatibility
check, not a vulnerability scanner.

Scope: (1) qualify pytest 9.0.3+ against the suite and move the constraint
after it passes; (2) add a scheduled Python SCA workflow — if that brings a
new dev tool in, it enters via a reviewed row in `docs/dependencies.md`
stating what it replaces and why, per the ledger rule; (3) L-04: keep the
human-maintained compatible ranges, but generate a hash-pinned CI lock per
supported Python and refresh it automatically after the canary/SCA pass, so a
historical failure's exact environment is reproducible. Keep the full-SHA
Action pins and isolated npm tooling exactly as they are (review P-02).
