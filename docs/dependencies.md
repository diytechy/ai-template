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
- **`kit`** — not a Python import: external CONTENT vendored into
  `project-trajectory/` and shipped to every adopter (`Kind=skill` today; the
  tier is content-shaped, not code-shaped, so it takes its own name rather
  than overloading `shipped`). Same discipline as the others — what it
  replaces, why hand-authoring the equivalent is worse, and the ruling that
  admitted it — plus the license and the pinned source commit a copy demands.

## Declared dependencies

| Name | Kind | Tier | Replaces | Why hand-rolling is worse | Ruled |
|---|---|---|---|---|---|
| git | system | shipped | — (substrate) | The process *is* git-shaped: diffable registries, append-only log, reviewed Status-change commits, branch-per-traincar. Named in PROCESS.md intro. | RULING-1, 2026-07-28 |
| gh | system | coordinator | A bespoke forge client | Forge-mode backend only (dormant until enabled): PR create/checks/review/merge against GitHub. The local integrator needs no forge at all. | RULING-2, 2026-07-28 |
| pip-audit | python | coordinator | Ad-hoc/manual advisory lookups against requirements-dev.txt | Cross-checks the installed dev/CI toolchain against the PyPA Advisory Database + OSV automatically, on a schedule, instead of relying on someone remembering to look — the gap that let GHSA-6w46-j5rx-g56g (pytest < 9.0.3) sit unnoticed in a compatible-release range that excluded the fix. Runs only in `.github/workflows/sca.yml`, never forced on an adopter. | WI-480, 2026-08-20 (repo-review-2026-08-19 M-11) |
| uv | python | coordinator | pip-tools (`pip-compile`) or a hand-resolved lock | A single fast resolver generates the hash-pinned, `--universal` (cross-OS) CI lock deterministically, avoiding a second resolver dependency on top of pip; already the tool `scripts/dev-setup.sh`'s `offer_python` borrows if a contributor has it. Runs only in `.github/workflows/lock-check.yml`, never forced on an adopter. | WI-480, 2026-08-20 (repo-review-2026-08-19 L-04) |
| antidote | skill | kit | A hand-authored root-cause-vs-patch review skill | `project-trajectory/skills/antidote/SKILL.md`, vendored verbatim (MIT license, [Avtr99/antidote](https://github.com/Avtr99/antidote) commit `8e0350e3d86df36852d56ad0a502376e24de870c`, upstream v1.1.0) from a source that already states the per-fix half of this repo's own consolidation doctrine (PROCESS.md §3) — hand-authoring an equivalent duplicates content that already exists, reviewed, under a compatible license. Pure prompt: no scripts, no network calls, no dependencies of its own (verified by reading it whole before vendoring). Materializes to every adopter (`scope: kit`, `domains: [any]`) via the existing skill fan-out (`skills/README.md`), the same mechanism every other shipped skill uses. | OI-58, 2026-08-22 (WI-507) |

(Dev-tooling this meta-repo's own test suite uses — pytest, pytest-xdist,
ruff — is outside this ledger's scope: it governs what the **kit scripts**
import, not what the meta-repo's harness runs; downstream, those tools are the
adopter's own stack choice, per CLAUDE.md. pip-audit and uv above are the
exception the WI-480 grind explicitly asked for: neither is imported by kit
scripts either, but both are new tools this repo's OWN CI now installs, so
they get the same reviewed-row treatment as git/gh above rather than the
parenthetical carve-out pytest/ruff/pytest-xdist/pytest-cov already have.
`antidote` is a further extension of scope, deliberate and narrow: it is not a
Python import at all, but the first EXTERNAL CONTENT the kit vendors into
`project-trajectory/skills/`, and the same "no unargued dependency" discipline
— what it replaces, why hand-rolling is worse, the admitting ruling, plus a
pinned source commit and license — applies to prose an agent will follow as
much as it applies to code an interpreter will run.)
