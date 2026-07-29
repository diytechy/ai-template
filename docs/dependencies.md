# Dependency ledger

The abuse guard for [concurrency-restructure.md](concurrency-restructure.md)
§1.3 (RULING-3, owner 2026-07-28): **not "no dependencies" — "no unargued
dependencies."** Stdlib is the default everywhere; a non-stdlib dependency in
the kit's own scripts exists only as a row here, and every row states what it
replaces, why hand-rolling is worse, and the ruling that admitted it.
`tests/test_dependency_ledger.py` scans every import in
`project-trajectory/scripts/` against this table and **fails on any Python
import not declared here** — adding a dependency without a reviewed ledger row
is a red suite, by design.

Tiers:

- **`coordinator`** — used by this repo's coordination tooling; installed by
  dev-setup; never forced on an adopter.
- **`shipped`** — imported by a check an adopter runs; forces every adopter to
  install it, so the bar is highest (owner ruling required, expected rare,
  ideally never — stdlib remains *preferred* for shipped checks).
- **`system`** — a binary on PATH, not a Python package; same entry
  discipline.

## Declared dependencies

| Name | Kind | Tier | Replaces | Why hand-rolling is worse | Ruled |
|---|---|---|---|---|---|
| git | system | shipped | — (substrate) | The process *is* git-shaped: diffable registries, append-only log, reviewed Status-change commits, branch-per-traincar. Named in PROCESS.md intro. | RULING-1, 2026-07-28 |
| gh | system | coordinator | A bespoke forge client | Forge-mode backend only (dormant until enabled): PR create/checks/review/merge against GitHub. The local integrator needs no forge at all. | RULING-2, 2026-07-28 |

*No Python-package rows yet — every kit script imports stdlib only. The first
row added here must arrive with its reviewed reason, per the header.*

(Dev-tooling this meta-repo's own test suite uses — pytest, pytest-xdist,
ruff — is outside this ledger's scope: it governs what the **kit scripts**
import, not what the meta-repo's harness runs; downstream, those tools are the
adopter's own stack choice, per CLAUDE.md.)
