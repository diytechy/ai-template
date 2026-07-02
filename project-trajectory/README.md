# Project Trajectory Template

A portable, **stack-agnostic** kit for taking a project from brief (or draft)
to an accepted, maintainable deliverable via a **gated, requirement-traced**
process — with modular/deduplicated code, testable chunks, and explicit
attention to end-user usability and corner cases.

It encodes a key lesson: the value is in the **artifacts, gates, and role
discipline** — not in spawning many agents. One driver wears the role "hats" in
continuous context; a separate reviewer is summoned only for high-risk pre-gate
audits.

## Contents

| File | Use |
|---|---|
| `KICKOFF_PROMPT.md` | **Paste this into an agent to start.** Fill the PROJECT BRIEF at the bottom first. |
| `AGENTS.template.md` | Agent/contributor guide → copy to the new repo's `AGENTS.md` (the cross-tool standard most agents read). Encodes the readability conventions + points at the process. |
| `CLAUDE.stub.template.md` · `GEMINI.stub.template.md` | Thin stubs → the new repo's `CLAUDE.md` / `GEMINI.md`; each just points at `AGENTS.md` so Claude Code and Gemini (which prefer their own filename) still land on the full guide. |
| `PROCESS.md` | The canonical method's **load-bearing core** → copy to `docs/process.md`. Roles, gates, ID scheme, anti-duplication, verdict protocol, review triage, harness contract; opens with a minimum-profile table. |
| `PROCESS_OPTIONS.md` | The **opt-in layers** the core doc summarizes → copy to `docs/process-options.md`. Phased delivery, lifecycle tags, the §7 boundary notes, the §9 NFR checklist + perf comparator, and the rung-2 multi-module detail — each with an *applies-when*. |
| `STATUS.template.md` | The live blackboard → copy to `docs/status.md`. |
| `ARCHITECTURE.template.md` | One-page overview + generated map → copy to `docs/architecture.md`. |
| `INTERFACES.template.md` | Cross-project contracts (IF-###) → copy to `docs/interfaces.md`. Use only for interlinked projects. |
| `registries/stakeholder-needs.template.md` | SN-### (stakeholder needs + edge cases). |
| `registries/system-requirements.template.csv` | SR-### with measurable acceptance criteria. |
| `registries/low-level-requirements.template.csv` | LLR-### ↔ code. |
| `registries/test-cases.template.csv` | TC-### ↔ requirements. |
| `registries/interfaces.template.csv` | IF-### ↔ cross-project contracts (paired with `INTERFACES.template.md`). |
| `registries/performance-budgets.template.csv` | PB-### quantitative perf/resource budgets (NFRs), off-spine but back-linked to the SR/LLR/Module they bound; owned by the Integration/Coordination hat (process.md §9). Optional, like interfaces. |
| `registries/modules.template.csv` | MOD-### coordinator module registry for the **rare** multi-repo rung (`MULTI_REPO.md` §6): one row per delegated module repo, `DelegatedSRs` back-linking the coordinator SRs it fulfils. Coordinator-only — **not** scaffolded by bootstrap; `trace.py` validates it when present. |
| `scripts/bootstrap.py` | **One command to scaffold a new repo** from this kit (copies templates → `docs/`/`scripts/`/CI, renames, won't clobber). |
| `scripts/check.py` | **The harness.** Runs format · lint · tests · coverage · traceability · arch-map freshness; gate-scoped (`--gate` defaults to the active gate recorded in `docs/gate`, so CI enforces the bar the project is actually at); nonzero on failure. Python-first reference — wire to your stack. |
| `scripts/trace.py` | **Ready-to-use** traceability checker (Python 3, stdlib only): joins the registries, writes `test/report.md` (counts, matrix, a line-reviewable `SN→SR→LLR→TC` text outline, and a small Mermaid `graph LR` colored by orphan/draft state), exits nonzero on orphans (and duplicate/malformed ids) with `--strict`. If an optional `performance-budgets.csv` (PB-###, §9) is present, it also fails when a budget row's `Refs` don't back-link a real SR/LLR/Module. `--html` also writes a dependency-free collapsible `test/report.html` map that scales to any size. `--phase v1` scopes the G3 Verified criterion for phased roadmaps (out-of-phase SRs reported as explicitly deferred); `--no-placeholders` (G2+) rejects leftover `-000` rows; `--strict-schema` (G3) checks required fields and the closed `Verification`/`Tier` vocabularies. Called by `check.py`. |
| `scripts/check_flows.py` | Verifies the **authored "Runtime flows"** section in `architecture.md` (required from G2): diagrams present, every cited SR/LLR id real — so reviewers verify *behavior* (concurrency, ordering) from sequence diagrams, not CSV rows. Called by `check.py` at G2/G3. |
| `scripts/check_docs.py` | **Doc navigability** check (Python 3, stdlib only): parses the link graph across `docs/` + root `*.md` and **fails on broken intra-repo links** (missing file or `#anchor`), **warns on orphan docs** (unreachable from an entry root), and with `--stale` (git-gated) on docs frozen beside churning code. Keeps the hand-written doc map honest like `gen_arch_map.py` keeps the code map honest (process.md §3). Called by `check.py` from G1. |
| `scripts/check_perf.py` | **Performance-budget comparator** (Python 3, stdlib only, metric-agnostic): compares a product-emitted `perf-metrics.json` against `performance-budgets.csv` (PB-###) and a committed `perf-baseline.json` — **absolute** breach vs `Budget` and **regression** vs baseline ± `Tolerance`, warn-vs-fail per the row's `Gate`, tier-scoped — and writes the gitignored `perf-report.md`. `--update-baseline` accepts a move (commit its diff in the same PR). The kit owns the *comparison*; the project wires the *measurement* (process.md §9). Called by `check.py` at G3 (absent metrics skip). |
| `scripts/check_stubs.py` | **No-stub / substance** tripwire for the G3 criterion (process.md §4): lists public symbols whose body is a stub (`pass`/`...`/`raise NotImplementedError`/bare `return None`/docstring-only), writing the gitignored `stub-report.md`. Stdlib, but **product-layer and warn-first** (exit 0 unless `--strict`) — a stub's shape is language-specific, so it ships like the perf *meters*: opt-in, **not** wired into `check.py`'s required floor. Informs the human/LLM G3 Inspection; a non-Python stack swaps or drops it. |
| `scripts/gen_arch_map.py` | Generates the **code map** from the source AST — per-module summary, internal dependencies, and public symbols with `Implements:` back-links — plus a Mermaid **dependency diagram** (rendered natively by GitHub/VS Code; no toolchain). Routes into `architecture.md` and/or `AGENTS.md`/`CLAUDE.md` (repeatable `--doc`). `--flow <entry>` also renders an orchestrator's ordered call sequence (the high-level flow); `--check` fails if stale. |
| `scripts/gen_release_checklist.py` | Generates the human **release checklist** for G-Release from the registries (every Demonstration/Manual/Inspection SR, Release-tier/manual TC, SN acceptance intent, provided interface) as back-linked tick-boxes. |
| `scripts/gen_cases.py` | Expands an SR's input **dimensions** (`Permutations`) into boundary-aware test combinations — full / **pairwise (all-pairs)** / boundary-corners — so tests exercise the input space without the full Cartesian blow-up. |
| `scripts/setup.{sh,ps1}` · `scripts/check.{sh,ps1}` | Cross-platform launchers: one-command venv + dependency setup, and a thin wrapper over `check.py`, for Linux/macOS and Windows. |
| `onboard.template.{sh,command,cmd}` | **Stage-0 onboarder** (one readable, double-clickable entry point per platform) → `scripts/onboard.*`. Consent-first: explains itself, native folder picker, ensures git, HTTPS-clones, then an end banner naming the checkout dir + the "point an AI agent here" handoff, and hands off to `dev-setup`. Fill in your clone URL; optionally serve it as a Release asset. The zero-to-running rung of the onboarding ladder (process.md §7). |
| `dev-setup.template.{sh,ps1}` | **Developer-workstation** setup → `scripts/dev-setup.*`. Detect-and-report by default (`--check`); `--baseline`/`--full` install consent-first. `--profile code` vs `--profile domain` (non-code contributors) with an EDIT-FOR-YOUR-STACK/DOMAIN block like `check.py`. Provisions what a *human* needs (runtime, git, an **offline** Mermaid renderer) — distinct from `setup.{sh,ps1}` (the product toolchain). |
| `hooks/pre-commit` | Agent-neutral **process floor** → copied to `.githooks/pre-commit`; `setup.{sh,ps1}` enable it via `git config core.hooksPath .githooks`. One POSIX hook (works on Git for Windows too) running the fast, always-valid checks: code-map freshness + id integrity (`trace.py --strict-integrity`) (+ ruff format on staged files if installed). Orphan strictness is gate-scoped — the hook never blocks a legitimate early-stage commit; the full gate bar stays in `check.py`/CI. |
| `agent-hooks/` | **Optional** per-agent hook configs (`claude.settings.json`, `gemini.settings.json`) that mirror the git hook for earlier feedback. Not wired by bootstrap; the git hook + CI are the source of truth (see `agent-hooks/README.md`). |
| `pytest.ini` | Registers the `smoke`/`full`/`release` test-tier markers the harness selects with `--tier` (unmarked tests run in `full`+`release`). |
| `gitignore.template` | Minimal `.gitignore` for the new repo (venv, tool caches, the regenerated trace report + HTML map). |
| `ci/check.yml` | Reference GitHub Actions workflow → copy to `.github/workflows/check.yml`. Runs the same `check.py`. |
| `EXAMPLE.md` | A fully worked SN→SR→LLR→TC chain to copy the pattern from (incl. a multi-module §9 and a multi-repo §10 sketch). |
| `MULTI_REPO.md` | **Design doc** for the rare multi-repo rung: how the spine extends across separate repos under a coordinator (SR-tier delegation, interface catalog, assemblies-as-config, mechanical gate aggregation). A design — the heavy cross-repo tooling is deferred. Reference doc (like `EXAMPLE.md`); not scaffolded. |
| `ADOPTING.md` | **Retrofit guide** for dropping the kit into an *existing* repo (code, history, CI, non-Python stacks): resolving bootstrap collisions, rewiring product steps, porting-or-explicitly-dropping the Python-reference generators (never a vacuous pass), and backfilling requirements from the boundary outward. Reference doc; not scaffolded. |

## How to use

1. **Scaffold:** from this kit, run
   `python scripts/bootstrap.py --dest /path/to/new/repo` (add `--dry-run` to
   preview). This copies the templates into `docs/`, `scripts/`, `AGENTS.md`
   (plus `CLAUDE.md`/`GEMINI.md` stubs), and CI, renaming `*.template.*` to
   working names.
   *(Manual alternative: copy this folder in and rename by hand. Adopting into
   an **existing** repo — code, CI, a non-Python stack? See `ADOPTING.md`.)*
   If `python` is absent or Python 2, use `python3` (Linux/macOS) or `py`
   (Windows); the kit needs Python 3.8+.
2. **Brief:** fill the **PROJECT BRIEF** in the new repo's `AGENTS.md` and
   `docs/status.md`. To drive it conversationally instead, paste
   `KICKOFF_PROMPT.md` (brief filled) into your agent.
3. **Wire the harness to your stack:** edit the step list `scripts/check.py`'s
   `steps()` returns (and the `SRC`/`TESTS`/tool names in its "EDIT FOR YOUR
   STACK" block) for your toolchain (the reference uses `ruff`/`pytest`);
   `trace.py` and `gen_arch_map.py` are stdlib-only.
4. The agent runs the gates **G1 → G2 → G3 → G-Release → G-Final** (G-Release
   only for versioned releases), pausing for your approval at each, with
   `python scripts/check.py` as the bar.

## The core ideas (why it produces sustainable code)

- **Traceability:** `SN → SR → LLR → TC`, joined by a generated matrix that must
  report **zero orphans**. Every line of intent is traceable to a need and a test.
- **Single source of truth + decomposition (not paraphrase):** facts live once
  and are referenced by ID; children add detail. This is what keeps docs and code
  from rotting into contradiction.
- **Modularity & dedup:** shared logic in one place; pure testable cores split
  from I/O/GUI shells; one-page architecture, generated so it can't drift.
- **Testability:** measurable acceptance criteria; tests cite requirement IDs;
  coverage threshold; a harness that runs locally and in CI.
- **Usability & corner cases:** a standing end-user lens for setup/first-run,
  failure modes, safety, automation/never-block, and honest docs.
- **Honest gates:** machine-checkable criteria where possible; everything else is
  explicitly classified Demonstration / Manual / Inspection — nothing hand-waved.

## Tuning knobs

- `COVERAGE_THRESHOLD` and `MAX_ROUNDS` in `PROCESS.md`.
- Drop a hat/gate for tiny projects (e.g. skip UX for a library); keep the
  SN→SR→LLR→TC spine.
- Scale review depth to risk — don't gate a rename like you'd gate a crypto path.
- Scale *structure* to scope: one module in one repo is the default; a repo can
  host several modules on the same spine (grouped by `Module`/`Area`, with an
  integration TC per seam), and multi-repo under a coordinator is a rare, later
  step — climb the ladder only when scope forces it (process.md §10; the
  coordinator model is `MULTI_REPO.md`, a design with the tooling deferred).
