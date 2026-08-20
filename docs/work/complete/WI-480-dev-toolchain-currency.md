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

## Deliverable

Qualified pytest 9.0.3+ against the full suite in a THROWAWAY venv — the
identical pass/fail set as the pinned 8.4.2 (2624 passed / 13 skipped; the
two failures both runs shared were a pre-existing WI-466 golden gap, fixed
separately at 74c20704) — then moved `requirements-dev.txt` to
`pytest>=9.0.3,<10` with the GHSA, the measurement, and the method recorded
in the constraint's comment, closing GHSA-6w46-j5rx-g56g. Added
`.github/workflows/sca.yml` (weekly `pip-audit`, non-gating; verified
locally catching the pytest advisory pre-bump and clean post-bump) and
`.github/workflows/lock-check.yml` (triggered after canary/SCA, regenerates
the hash-pinned `uv`-generated locks for both supported Pythons and FAILS
LOUDLY on staleness rather than auto-committing — the auto-commit reading
was deliberately refused under `push = "human"` and the staged-divergence
precedent), with `requirements-dev-lock-{3.11,3.x}.txt` committed as the
initial reproducible record (deterministic regeneration verified;
the 3.x lock was resolved on local 3.12 and is expected to flag stale on
its first CI run — the mechanism working). `pip-audit` and `uv` entered
`docs/dependencies.md` as reviewed coordinator-tier rows. Post-bump smoke
settled at 53.6s (first warm-up runs spiked to 69–105s; the ~56s headroom
finding stands banked).

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
