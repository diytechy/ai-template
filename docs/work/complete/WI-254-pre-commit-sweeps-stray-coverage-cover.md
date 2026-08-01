+++
id = "WI-254"
title = "Pre-commit sweeps stray .coverage/.coverage.* residue from the repo root (meta-repo wrapper hook only - shipped kit hook untouched, no downstream change) (2026-07-20 owner directive)"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 251
+++

## Deliverable

Meta-repo .githooks/pre-commit wrapper now sweeps .coverage + .coverage.* (pytest-cov -n auto shards; thousands had accumulated) from the repo root before delegating to the shipped floor - exact top-level names only, gitignored residue only, kit hook untouched (no downstream change). Proven live: first firing cleared the backlog to zero. 109-REVIEW-A APPROVE (rm scope verified: .coveragerc-style config unmatched, index untouched).
