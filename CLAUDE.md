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
  ledger row.** The kit's own scripts (`trace.py`, `check.py`,
  `gen_arch_map.py`, `bootstrap.py`) run on a clean Python 3.11+ on Windows
  and POSIX, and today import stdlib only. The rule is "no *unargued*
  dependencies," not "no dependencies" (owner ruling 2026-07-28,
  `docs/concurrency-restructure.md` §1.3): a genuinely better tool may enter
  via a reviewed row in [`docs/dependencies.md`](docs/dependencies.md) —
  stating what it replaces and why — enforced by
  `tests/test_dependency_ledger.py`. Shipped checks stay stdlib-*preferred*
  (a dependency there forces every adopter to install it — rare, ideally
  never). Tools a *downstream* project needs (ruff, pytest) are theirs to
  install; the kit must not require them to run its own checks.
- **Stack-agnostic core, Python-first reference.** The process and ID scheme are
  language-neutral; concrete harness commands are Python examples clearly marked
  as "swap for your stack."
- **Templates must stay copy-ready.** A `*.template.*` file should produce
  something sensible the moment it's copied and filled — example/placeholder rows
  end in `-000` so `trace.py` ignores them.
- **Don't let this repo drift from the template it ships.** VALUES may diverge
  between the kit's template and this repo's own instance (owner dials, filled
  registry rows, enabled sets); STRUCTURE must not (schema headers, launcher
  command contracts, declared-section shapes) — `tests/test_dogfood_sync.py`
  enforces it.
- **Self-test before claiming done.** The per-commit bar is the fast **smoke**
  tier (`python -m pytest -q -n auto -m smoke`, ~3.3 min); run the **full**
  unfiltered suite (`python -m pytest -q -n auto`, ~4.2 min) before claiming a
  WI/slice done, at phase close, and after a broad script change — it
  bootstraps a temp scaffold and exercises every script end-to-end. Paste the
  real output; never report a green you didn't produce. (Commit bar vs gate bar,
  and what the smoke tier drops: the `session-protocol` skill §3.)
- **Edit conservatively.** This is a foundation many projects inherit; prefer the
  smallest change that fixes the problem, and flag anything that would force
  downstream repos to migrate.

## Repo map

- [`project-trajectory/PROCESS.md`](project-trajectory/PROCESS.md) — canonical
  method, **load-bearing core** (roles, gates, IDs, anti-duplication, design-time
  runtime flows). The source of truth other docs link to. Its companion
  [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) holds the **opt-in
  layers** (phased delivery, lifecycle tags, §7 boundary notes, §9 NFR/perf, the
  rung-2 multi-module detail), each with an *applies-when*. Both are scaffolded
  (`docs/process.md` + `docs/process-options.md`); keep §-numbering stable when
  editing — `§N` cross-refs pervade the kit.
- `project-trajectory/*.template.md` + `registries/*.template.*` — the artifact
  formats copied into a new repo's `docs/`.
- `project-trajectory/scripts/` — runnable kit scripts (see "stdlib-only" above).
- `project-trajectory/skills/` — agent-neutral **skills** (opt-in accelerators):
  one `<name>/SKILL.md` with an applicability schema; `scope: kit` skills ship +
  materialize downstream, `scope: this-repo` ones maintain *this* template and are
  dogfooded into [`.claude/skills/`](.claude/skills/). `gen_skills_index.py`
  regenerates `skills/INDEX.csv`; `bootstrap.py --agents` materializes them (see
  `project-trajectory/skills/README.md`). When you change *this* repo's
  conventions, update the matching `this-repo` skill too.
- `project-trajectory/ci/check.yml` — reference CI that runs the same harness.
- [`project-trajectory/EXAMPLE.md`](project-trajectory/EXAMPLE.md) — the worked
  SN→SR→LLR→TC chain; keep it in sync with the registry column headers (a test
  asserts its `Permutations` snippets parse with `gen_cases.py`).
- [`project-trajectory/MULTI_REPO.md`](project-trajectory/MULTI_REPO.md) — the
  **design** doc for the rare multi-repo coordinator rung (a reference doc like
  `EXAMPLE.md`, not scaffolded); the heavy cross-repo tooling is deferred.
- [`project-trajectory/ADOPTING.md`](project-trajectory/ADOPTING.md) — the
  **retrofit** guide for dropping the kit into an existing (possibly
  non-Python) repo; a reference doc like `EXAMPLE.md`, not scaffolded.
- `tests/` — the kit's own pytest suite (meta-repo dev tooling; the stdlib-only
  rule applies to the kit scripts, not to testing them). CI:
  `.github/workflows/test.yml` runs it on Linux + Windows (Python 3.11 + latest)
  and macOS (latest).
- [`docs/status.md`](docs/status.md) + [`docs/process.toml`](docs/process.toml)
  + root `agent-resume.{cmd,sh,command}` — the kit's **unattended layer
  self-applied**: the launchers (wired for Claude, strong tier) run
  `project-trajectory/scripts/agent_loop.py --root .`, resuming from
  `docs/status.md` under the declared policies (this repo runs `human_ratification_through = 0` — loop-held — with `push = "human"` and the privacy gate off).
- **The kit's own `SN→SR→LLR→TC` spine** (Thread 47 self-adoption, *at G3*):
  [`docs/requirements/stakeholder-needs.md`](docs/requirements/stakeholder-needs.md)
  + `system-requirements.csv` + `low-level-requirements.csv` +
  `docs/test/test-cases.csv` + [`docs/architecture.md`](docs/architecture.md)
  (one-page + the G2 Runtime flows) + `docs/gate` + `docs/stack.ini` +
  `docs/log.md` + the `docs/work/` WI spec registry + root `PROJECT_STATE.html`
  (the **Thread 52 trajectory layer, dogfooded** — the kit's own work-item DAG +
  its generated, freshness-gated dashboard; regenerate with
  `python project-trajectory/scripts/gen_trajectory.py` after editing the registry
  or the spine) — the kit **traced with its own process**, its "product" being
  `project-trajectory/scripts` + `tests/`. Keep these **distinct from the
  templates the kit ships** in `project-trajectory/registries/`: those are the
  blank forms an adopter fills; these are the kit's *own, filled* registries.
  (`run.*` launchers stay un-self-applied — a meta-repo has no product to launch.)
- [`docs/enforcement-audit.md`](docs/enforcement-audit.md) — the kit's worked
  **enforcement audit** (dogfooding the `PROCESS_OPTIONS.md` discipline): each
  process/working-agreement rule mapped to its strongest enforcer
  (Harness/Test/Reviewer/Prose), with the honest gaps recorded.
- [`docs/registry-machinery-reference.md`](docs/registry-machinery-reference.md) —
  a **reference doc** (like `EXAMPLE.md`/`ADOPTING.md`, not a working surface):
  what the scripts actually enforce on the `SN→SR→LLR→TC` spine — every field,
  every join rule, how `derive_gate.py` computes the gate from those rows, and
  how that gate then selects the harness steps, test tier and coverage floors.
- [`docs/archive/`](docs/archive/README.md) — the kit's **design history**:
  `IMPROVEMENT_PLAN.md` (the thread specs + WI-1.x log, archived once the live
  homes — `status.md` + `work-items.csv` + `log.md` — superseded it) and its own
  historical inputs (the resolved template review, the adoption field report, the
  mined scratch notes). Not working surfaces; root stays live-only.

## Communication style

Direct and concrete; explain the *why* before the *how*; surface trade-offs and
uncertainty honestly; ask before anything irreversible. Prefer the simplest
thing that works and say so when a request looks over-engineered for its need.
Don't change unrelated code; when you spot a design smell, surface it as a
separate finding rather than fixing it inline. (The shipped guide states the
full version — `project-trajectory/AGENTS.template.md` "Working agreement".)
