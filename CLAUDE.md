# CLAUDE.md — Working in this template repo

This repo is a **meta-project**: its product is the reusable kit in
[`project-trajectory/`](project-trajectory/) that *other* repos copy in to run a
gated, requirement-traced development process. So work here improves templates
and scripts, not a downstream application.

> Looking for the agent guide that ships **to** new projects? That's
> [`project-trajectory/CLAUDE.template.md`](project-trajectory/CLAUDE.template.md).
> Don't confuse the two: this file governs editing the kit; that one governs
> using the kit.

---

## What we're optimizing for

The kit exists to make downstream code **maintainable and trustworthy**:
readable for humans and agents alike, deeply tested, and advanced only through
explicit approval gates. Every change here should make that easier to achieve in
a real project — or get out of the way.

## Principles for editing the kit

- **Dogfood the philosophy.** The templates preach single-source-of-truth,
  decompose-don't-paraphrase, and generated-not-hand-maintained. Hold the kit to
  the same bar: don't restate a rule in five files — state it in
  [`PROCESS.md`](project-trajectory/PROCESS.md) and link to it.
- **Keep scripts stdlib-only and cross-platform.** The kit's own scripts
  (`trace.py`, `check.py`, `gen_arch_map.py`, `bootstrap.py`) must run on a clean
  Python 3.8+ with no pip installs, on Windows and POSIX. Tools a *downstream*
  project needs (ruff, pytest) are theirs to install; the kit must not require
  them to run its own checks.
- **Stack-agnostic core, Python-first reference.** The process and ID scheme are
  language-neutral; concrete harness commands are Python examples clearly marked
  as "swap for your stack."
- **Templates must stay copy-ready.** A `*.template.*` file should produce
  something sensible the moment it's copied and filled — example/placeholder rows
  end in `-000` so `trace.py` ignores them.
- **Self-test before claiming done.** After changing a script, run
  `python -m pytest -q` — the suite in `tests/` bootstraps a temp scaffold and
  exercises every script end-to-end — and paste the real output. Never report a
  green you didn't produce.
- **Edit conservatively.** This is a foundation many projects inherit; prefer the
  smallest change that fixes the problem, and flag anything that would force
  downstream repos to migrate.

## Repo map

- [`project-trajectory/PROCESS.md`](project-trajectory/PROCESS.md) — canonical
  method (roles, gates, IDs, anti-duplication, design-time runtime flows). The
  source of truth other docs link to.
- `project-trajectory/*.template.md` + `registries/*.template.*` — the artifact
  formats copied into a new repo's `docs/`.
- `project-trajectory/scripts/` — runnable kit scripts (see "stdlib-only" above).
- `project-trajectory/ci/check.yml` — reference CI that runs the same harness.
- [`project-trajectory/EXAMPLE.md`](project-trajectory/EXAMPLE.md) — the worked
  UN→SR→LLR→TC chain; keep it in sync with the registry column headers (a test
  asserts its `Permutations` snippets parse with `gen_cases.py`).
- `tests/` — the kit's own pytest suite (meta-repo dev tooling; the stdlib-only
  rule applies to the kit scripts, not to testing them). CI:
  `.github/workflows/test.yml` runs it on Linux + Windows, Python 3.8 + latest.

## Communication style

Direct and concrete; explain the *why* before the *how*; surface trade-offs and
uncertainty honestly; ask before anything irreversible. Prefer the simplest
thing that works and say so when a request looks over-engineered for its need.
