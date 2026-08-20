# CLAUDE.md — Working in this template repo

This repo is a **meta-project**: its product is the reusable kit in
[`project-trajectory/`](project-trajectory/) that *other* repos copy in to run a
gated, requirement-traced development process. So work here improves templates
and scripts, not a downstream application.

> Looking for the agent guide that ships **to** new projects? That's
> [`project-trajectory/AGENTS.template.md`](project-trajectory/AGENTS.template.md)
> (scaffolds to `AGENTS.md`, with thin `CLAUDE.md`/`GEMINI.md` stubs pointing at
> it). Don't confuse the two: this file governs editing the kit; that one governs
> using the kit.

> **`OWNER_SCRATCHPAD.md` is owner-only** — never read, cite, or act on it. It
> holds the human owner's free-form notes; the working surfaces are
> `docs/status.md`, the registries, and `docs/log.md`.

---

## What we're optimizing for

The canonical purpose statement is the `PROJECT-VISION:` tag opening the root
[README.md](README.md) — the same one-home pattern the kit ships downstream.
In short: the kit exists to make downstream code **maintainable and
trustworthy** — readable for humans and agents alike, deeply tested, and
advanced only through explicit approval gates. Every change here should make
that easier to achieve in a real project — or get out of the way.

## Principles for editing the kit

- **Dogfood the philosophy.** The templates preach single-source-of-truth,
  decompose-don't-paraphrase, and generated-not-hand-maintained. Hold the kit to
  the same bar: don't restate a rule in five files — state it in
  [`PROCESS.md`](project-trajectory/PROCESS.md) and link to it.
- **Keep scripts stdlib-preferred and cross-platform; dependencies need a
  ledger row.** The kit's own scripts run on a clean Python 3.11+ on Windows
  and POSIX, and today import stdlib only. The rule is "no *unargued*
  dependencies," not "no dependencies": a genuinely better tool may enter via a
  reviewed row in [`docs/dependencies.md`](docs/dependencies.md) — stating what
  it replaces and why — enforced by `tests/test_dependency_ledger.py`. Shipped
  checks stay stdlib-*preferred* (a dependency there forces every adopter to
  install it — rare, ideally never). Tools a *downstream* project needs (ruff,
  pytest) are theirs to install; the kit must not require them to run its own
  checks.
- **Stack-agnostic core, Python-first reference.** The process and ID scheme are
  language-neutral; concrete harness commands are Python examples clearly marked
  as "swap for your stack."
- **Templates must stay copy-ready.** A `*.template.*` file should produce
  something sensible the moment it's copied and filled — example/placeholder rows
  end in `-000` so `trace.py` ignores them. A token the kit *mandates* into an
  adopter's cell must mean something in **their** repo: a marker naming one of
  this repo's own rulings cites a record they can never read.
- **Don't let this repo drift from the template it ships.** VALUES may diverge
  between the kit's template and this repo's own instance (owner dials, filled
  registry rows, enabled sets); STRUCTURE must not (schema headers, launcher
  command contracts, declared-section shapes) — `tests/test_dogfood_sync.py`
  enforces it.
- **Self-test before claiming done.** The per-commit bar is the fast **smoke**
  tier (`python -m pytest -q -n auto -m smoke`) — budgeted at **60 s** wall in
  [`docs/stack.ini`](docs/stack.ini) and enforced in CI by
  `scripts/check_smoke_budget.py`; **measured 2026-08-20 on this box: 54.9 /
  64.0 / 55.7 s over three warm runs — one of them past the 60 s ceiling.** One
  box is one data point and the budget is not moved to fit it. Run the **full**
  unfiltered suite (`python -m pytest -q -n auto`, ~6 min) before claiming a
  WI/slice done, at phase close, and after a broad script change — it
  bootstraps a temp scaffold and exercises every script end-to-end. Paste the
  real output; never report a green you didn't produce. (Commit bar vs gate bar,
  and what the smoke tier drops: the `session-protocol` skill §3.)
- **Edit conservatively.** This is a foundation many projects inherit; prefer the
  smallest change that fixes the problem, and flag anything that would force
  downstream repos to migrate.

## Repo map

Entry points only — read the directories for the rest.

- **Method:** [`PROCESS.md`](project-trajectory/PROCESS.md) (the load-bearing
  core) + [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) (opt-in
  layers, each with an *applies-when*). Keep §-numbering stable — `§N`
  cross-refs pervade the kit.
- **The shipped kit:** everything under `project-trajectory/` — the
  `*.template.*` artifact formats and blank `registries/` an adopter fills,
  `scripts/`, `skills/`, `ci/`, and the reference docs `EXAMPLE.md` /
  `ADOPTING.md` / `MULTI_REPO.md`. A `scope: this-repo` skill maintains *this*
  repo (dogfooded into `.claude/skills/`): change a convention here, update its
  skill.
- **The kit's own, filled spine** — not to be confused with those blank forms:
  `docs/requirements/`, `docs/test/`, `docs/work/`, `docs/stack.ini`,
  `docs/runtime-flows.md` (the authored Runtime flows; the structural
  architecture is derived into the dashboard — WI-455), the
  derived `docs/gate` (never hand-set), and the generated root
  [`PROJECT_STATE.html`](PROJECT_STATE.html) (`python
  project-trajectory/scripts/gen_trajectory.py`). The traced "product" is
  `project-trajectory/scripts` + `tests/`; the self-application boundary is **no
  *product* launch** — an actions-menu launcher is in scope, `run.*` product
  launchers are not.
- **Working surfaces:** [`docs/status.md`](docs/status.md), forward-only — what
  happens **next** — and `docs/log.md`, what happened. Root
  `agent-resume.{cmd,sh,command}` run
  `project-trajectory/scripts/agent_loop.py --root .`, resuming from
  `docs/status.md` under the policies declared in
  [`docs/process.toml`](docs/process.toml): every spine tier is human-held and
  `push = "human"`.
- **Reference, not working surfaces:**
  [`docs/registry-machinery-reference.md`](docs/registry-machinery-reference.md)
  (what the scripts enforce on the spine, field by field),
  [`docs/enforcement-audit.md`](docs/enforcement-audit.md) (each rule mapped to
  its strongest enforcer, gaps included), and
  [`docs/archive/`](docs/archive/README.md) (design history; root stays
  live-only).
- **`tests/`** — the kit's own pytest suite; the stdlib rule covers the kit
  scripts, not testing them. `.github/workflows/test.yml` runs it on Linux +
  Windows (Python 3.11 + latest) and macOS.

## Communication style

Direct and concrete; explain the *why* before the *how*; surface trade-offs and
uncertainty honestly; ask before anything irreversible. Prefer the simplest
thing that works and say so when a request looks over-engineered for its need.
Don't change unrelated code; when you spot a design smell, surface it as a
separate finding rather than fixing it inline. (The shipped guide states the
full version — `project-trajectory/AGENTS.template.md` "Working agreement".)
