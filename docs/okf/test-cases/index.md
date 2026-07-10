---
type: "Index"
title: "test-cases"
description: "tier index"
tags: []
resource: "generated"
---

# test-cases — index

| id | summary |
|---|---|
| [TC-001](TC-001.md) | Run the trace suite; a linked chain is orphan-free and an injected orphan fails --strict. |
| [TC-002](TC-002.md) | Run the registry-checks suite; duplicate/malformed ids and mis-columned rows fail --stric… |
| [TC-003](TC-003.md) | Run the registry-checks suite; leftover -000 rows and empty/out-of-vocab fields are flagg… |
| [TC-004](TC-004.md) | Run the acceptance-criteria advisory suite; an unpinned comparative warns without changin… |
| [TC-005](TC-005.md) | Run the off-spine registry suites; back-link findings fire and -000 rows are ignored. |
| [TC-006](TC-006.md) | Run the check-harness suite; gate steps run and a missing required tool fails with SKIP(m… |
| [TC-007](TC-007.md) | Run the stack-profile suite; commands and tiers/coverage/arch-map resolve from stack.ini. |
| [TC-008](TC-008.md) | Run the stack-profile suite; malformed/non-integer/missing-binary profiles fail loudly. |
| [TC-009](TC-009.md) | Run the profile suite; a non-Python profile omits Python-only files and seeds files-mode … |
| [TC-010](TC-010.md) | Run the bootstrap suite; a fresh scaffold's harness runs green. |
| [TC-011](TC-011.md) | Run the bootstrap suite; a re-run leaves existing files unchanged, --force overwrites, an… |
| [TC-012](TC-012.md) | Run the check-docs suite; a broken link or missing vision tag fails --stale. |
| [TC-013](TC-013.md) | Run the check-flows suite; a conformant flow passes and a malformed one fails. |
| [TC-014](TC-014.md) | Run the check-perf suite; a within-tolerance metric passes and a regression fails. |
| [TC-015](TC-015.md) | Run the perf-budgets suite; an unresolvable or empty PB Refs is a finding. |
| [TC-016](TC-016.md) | Run the check-stubs suite; a stub at the declared gate fails and clean source passes. |
| [TC-017](TC-017.md) | Run the check-privacy suite; a staged secret is blocked with privacy-check off. |
| [TC-018](TC-018.md) | Run the check-privacy suite; PII/identity classes fire only with privacy-check on and hon… |
| [TC-019](TC-019.md) | Run the pre-commit-hook suite; a failing integrity/secrets check blocks the commit. |
| [TC-020](TC-020.md) | Run the pre-push-hook suite; a secret/identity in the push range blocks the push. |
| [TC-021](TC-021.md) | Run the hook suites' python-probe cases; a missing/aliased python3 reports clearly withou… |
| [TC-022](TC-022.md) | Run the check-vendored suite; a drifted vendored copy is a finding. |
| [TC-023](TC-023.md) | Run the gen-arch-map suite; --check fails on a stale map and regeneration rewrites only t… |
| [TC-024](TC-024.md) | Run the gen-cases suite; the spec grammar expands to the expected case set. |
| [TC-025](TC-025.md) | Run the skills-index suite; INDEX.csv regenerates from the SKILL.md frontmatter. |
| [TC-026](TC-026.md) | Run the agent-loop suite; the loop resumes from status.md headless without blocking. |
| [TC-027](TC-027.md) | Run the agent-loop suite; preflight exits a typed code on a non-git dir / missing CLI / p… |
| [TC-028](TC-028.md) | Run the agent-loop suite; a zero-commit repo is guarded and an all-ERROR region reads as … |
| [TC-029](TC-029.md) | Run the tracks suite; a dead lock holder releases and the next run acquires the lock. |
| [TC-030](TC-030.md) | Run the tracks suite; a second coordinator on a held lock is refused. |
| [TC-031](TC-031.md) | Run the gate-policy and push-policy suites; each reader returns the first declared line. |
| [TC-032](TC-032.md) | Run the onboard/dev-setup suite; the scaffolded scripts run to a green setup and dev-setu… |
| [TC-033](TC-033.md) | Run gen_release_checklist.py over a warn-tier PB budget; assert the generated checklist l… |
| [TC-034](TC-034.md) | Inspect that no kit script imports a third-party package (stdlib-only). |
| [TC-035](TC-035.md) | Analyze the CI matrix result across Linux/Windows/macOS x Python 3.8/latest. |
| [TC-036](TC-036.md) | Inspect a re-sync done per ADOPTING.md section 6 against the docs/kit-version diff — kit-… |
| [TC-037](TC-037.md) | Run the trajectory-validator suite; a well-formed registry passes, and a malformed WI id,… |
| [TC-038](TC-038.md) | Run the dashboard suite; the generated root HTML is one offline file (no external hosts/C… |
| [TC-039](TC-039.md) | Run the check-dupes suite; a seeded copy-pasted helper fails naming both file:line locati… |
| [TC-040](TC-040.md) | Run the agent-loop suite; a REVIEW-B-mapped phase invokes the second fake CLI and not the… |
| [TC-041](TC-041.md) | Run the doc-refs suite; a dangling path warns then gates under --strict, non-path backtic… |
| [TC-042](TC-042.md) | Run the gen-okf suite; typed linked concepts generate, regeneration is byte-stable, --che… |
