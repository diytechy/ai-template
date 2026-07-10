# ai-template

<a id="vision"></a>
**PROJECT-VISION:** A reusable starting point for building **maintainable,
requirement-traced projects** with AI agents and humans working from the same
playbook. The goal: code and analytics that stay readable and correct over the
long run, built **test-first** with **explicit approval gates** so you can
trust what ships.

It is **stack-agnostic** with **Python-first reference scripts** — drop it into
any repo and wire the harness to that repo's tooling (SN-003).

## What's in here

| Path | What it is |
|---|---|
| [`project-trajectory/`](project-trajectory/) | The portable kit: the gated, requirement-traced development process plus all templates and runnable scripts. **This is the thing you copy into new repos.** |
| [`project-trajectory/README.md`](project-trajectory/README.md) | Full contents + rationale for the kit. |
| [`CLAUDE.md`](CLAUDE.md) | Guide for working **in this template repo** (developing the templates themselves). |

## The kit's headline pieces

- **A gated process** ([`PROCESS.md`](project-trajectory/PROCESS.md)) — roles as
  "hats", approval gates (G1→G2→G3→G-Release→G-Final; G-Release only for
  versioned releases), and a verdict protocol; each gate's bar **fails, never
  silently skips** (SN-004, SN-008).
- **A traceability spine** — `SN → SR → LLR → TC` registries joined by a
  generated matrix that must report **zero orphans** before each gate (SN-002).
- **Runnable scripts** — stdlib-only Python 3.8+, no pip needed for the kit
  itself (SN-011). Cross-platform `setup`/`check` launchers (`.sh` + `.ps1`)
  ship for Linux/macOS and Windows. Full detail:
  [`project-trajectory/README.md`](project-trajectory/README.md).

  | Script | Purpose |
  |---|---|
  | [`check.py`](project-trajectory/scripts/check.py) | Gate- and tier-aware harness |
  | [`trace.py`](project-trajectory/scripts/trace.py) | Traceability matrix (join + orphan check) |
  | [`check_docs.py`](project-trajectory/scripts/check_docs.py) | Doc navigability: broken links, orphan docs, `PROJECT-VISION` tag, opt-out README need-coverage, `--stale` (SN-010) |
  | [`check_flows.py`](project-trajectory/scripts/check_flows.py) | Runtime-flow diagrams present, cited ids real |
  | [`check_perf.py`](project-trajectory/scripts/check_perf.py) | Performance-budget + regression comparator |
  | [`check_stubs.py`](project-trajectory/scripts/check_stubs.py) | Optional, warn-first: no-stub/substance detector (G3) |
  | [`check_dupes.py`](project-trajectory/scripts/check_dupes.py) | Optional: copy-paste detector (opt in via `[step:dupes]`) |
  | [`check_doc_refs.py`](project-trajectory/scripts/check_doc_refs.py) | Optional, warn-first: prose-rot detector (dead paths, broken `sym:module.name` refs) |
  | [`check_privacy.py`](project-trajectory/scripts/check_privacy.py) | Secrets floor for every repo, opt-out via `docs/secrets-scan`; PII/identity classes gated on `docs/privacy-check` (SN-009) |
  | [`gen_arch_map.py`](project-trajectory/scripts/gen_arch_map.py) | AST code map + Mermaid dependency diagram, routed into `architecture.md`/`AGENTS.md`/`CLAUDE.md` |
  | [`gen_release_checklist.py`](project-trajectory/scripts/gen_release_checklist.py) | Generated human release checklist |
  | [`gen_cases.py`](project-trajectory/scripts/gen_cases.py) | Boundary-aware, pairwise test-case combinations |
  | [`check_trajectory.py`](project-trajectory/scripts/check_trajectory.py) + [`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py) | Opt-out work-items layer: validates the execution DAG, renders the offline root `PROJECT_STATE.html` dashboard |
  | [`gen_okf.py`](project-trajectory/scripts/gen_okf.py) | Traceability graph as an Open Knowledge Format bundle (opt-out via `docs/okf-export`); the kit's own is [docs/okf/index.md](docs/okf/index.md) |
  | [`bootstrap.py`](project-trajectory/scripts/bootstrap.py) | Scaffold a new repo (SN-001) |

- **Unattended agent operation** (SN-006):
  - Root `agent-resume.*` launchers boot an agent session at the declared
    tier, or the walk-away coordinator loop
    ([`agent_loop.py`](project-trajectory/scripts/agent_loop.py)).
  - Fresh headless sessions resume from `docs/status.md` until
    `docs/run-state` reaches an end state.
  - A per-phase model map (`docs/run-phase`), reactive rate-limit backoff, a
    stall guard, and tracked per-session logs in `docs/iteration/`.
  - Optional **tier-conditional guardrails** — `docs/guardrails-policy`
    injects a vendored discipline core into weaker-tier sessions, drift-checked
    by `check_vendored.py`.
  - Consent is explicit via one-word declared-policy files scaffolded into
    `docs/`: `gate-policy` (who advances gates), `push-policy` (who may push),
    and `privacy-check` (the PII/identity gate, enforced by the git hooks +
    `check_privacy.py`).
- **Agent-neutral skills and hooks** (SN-005):
  - Opt-in skills ([`skills/`](project-trajectory/skills/)), materialized per
    agent by `bootstrap.py --agents`.
  - Git hooks ([`hooks/`](project-trajectory/hooks/)): a fast `pre-commit`
    process floor and a `pre-push` privacy backstop for privacy-checked repos.
- **Cross-project support** — an
  [`IF-###` interfaces registry](project-trajectory/INTERFACES.template.md)
  for projects that interlink, so shared contracts stay traceable and versioned.
- **An agent guide template**
  ([`AGENTS.template.md`](project-trajectory/AGENTS.template.md)) that encodes
  our readability/maintainability conventions and points agents at the
  process. It scaffolds to `AGENTS.md` (the cross-tool standard), with thin
  `CLAUDE.md`/`GEMINI.md` stubs pointing back at it.

## Quick start — bootstrap a new project

```bash
# From inside this template repo:
python project-trajectory/scripts/bootstrap.py --dest /path/to/your/new/repo

# Preview without writing:
python project-trajectory/scripts/bootstrap.py --dest /path/to/repo --dry-run

# Setting up for an agent? Also materialize its skills (asks if run interactively):
python project-trajectory/scripts/bootstrap.py --dest /path/to/repo --agents claude
```

> **Which `python`?** Needs 3.8+. If `python` is missing or points at Python 2,
> use `python3` (Linux/macOS) or the `py` launcher (Windows). On a fresh macOS,
> the first `python3` may prompt to install the Command Line Tools — accept it
> (or run `xcode-select --install`), which also provides `git`.

This scaffolds:
- `AGENTS.md` (the agent guide; `CLAUDE.md`/`GEMINI.md` stubs point at it)
- `docs/` — process, status + log + plan, architecture, interfaces, the
  registries, and the declared-policy files (`gate`, `gate-policy`,
  `push-policy`, `privacy-check`)
- `scripts/` — the harness
- root `run.*` / `agent-resume.*` launchers (shipped inert until you fill
  their command slots)
- `.github/workflows/check.yml`, and empty `src/`/`tests/`

Then:

1. Fill the **PROJECT BRIEF** in the new repo's `AGENTS.md` and `docs/status.md`.
2. Install the harness tooling for your stack (Python reference: `ruff pytest
   pytest-cov`). Commands are declared once in `docs/stack.ini` — a
   non-Python stack edits that one file.
3. Start **gate G1** — see the new repo's `docs/process.md`.

### Or kick off with an agent

If you'd rather drive it conversationally, open
[`project-trajectory/KICKOFF_PROMPT.md`](project-trajectory/KICKOFF_PROMPT.md),
fill the brief at the bottom, and paste it into your agent. It will scaffold the
same artifacts and run the gates with you.

## Why this produces sustainable code

- **Traceability** — every line of intent ties back to a stakeholder need and
  forward to a test; orphans are caught mechanically.
- **Test-driven** — the G2 test case for each requirement is written as a
  *failing* test before the code that satisfies it (red → green → refactor), so
  implementation is pulled by the spec, not retrofitted to it.
- **Single source of truth** — facts live once and are referenced by id, so docs
  and code can't quietly contradict each other.
- **Modularity & dedup** — pure cores split from I/O shells; shared logic in one
  place; a one-page, generated architecture map that can't drift.
- **Honest gates** — machine-checkable where possible; everything else is
  explicitly classified, never hand-waved.

> **Generate vs. measure.** This kit *generates* legibility (traced spine,
> committed code map, gates). *Measuring* legibility over time — AI-readiness
> or complexity/churn dashboards — is a separate, optional, downstream concern
> ([`PROCESS.md`](project-trajectory/PROCESS.md) §7).

> **Spec vs. runtime harness.** This kit is a portable process *spec*. A
> turnkey, tool-specific agent-runtime harness (an installed engine with its
> own gates/subagents) is different, optional, downstream tooling that can run
> *with* a repo built from this kit — never a dependency of it
> ([`PROCESS.md`](project-trajectory/PROCESS.md) §7).

> **Project scale.** One module in one repo is the default. A larger repo can
> host several modules on the same spine (grouped by `Module`/`Area`,
> module-scoped review, an integration TC at each seam); a multi-repo split
> under a coordinator is a rarer, heavier step, taken only when modules need
> independent versioning/release
> ([`PROCESS.md`](project-trajectory/PROCESS.md) §10; coordinator design:
> [`MULTI_REPO.md`](project-trajectory/MULTI_REPO.md)).

> **Onboarding ladder.** `Stage 0` (get git + the repo) → `dev-setup`
> (workstation: runtime, git, an offline Mermaid renderer) → `setup` (product
> toolchain) → `check` (the gates) — each rung optional, readable, and
> consent-first. The kit scaffolds a per-platform Stage-0 `onboard` script
> (native folder picker + an AI-agent handoff for non-coders) and a tiered
> `dev-setup` ([`PROCESS.md`](project-trajectory/PROCESS.md) §7).

## Built with the kit (self-adoption)

This repo eats its own dog food: the kit is developed **using the kit's own
process**, traced by its own `SN→SR→LLR→TC` spine and gated by its own
[`check.py`](project-trajectory/scripts/check.py).

- Every capability above cites the
  [stakeholder need](docs/requirements/stakeholder-needs.md) it realizes;
  `check_docs.py`'s **opt-out** need-coverage guard keeps that honest — every
  Must/Should need must be cited somewhere in this README, so a requirements
  change mechanically ages it (no delimiter markers; any `SN-###` counts).
- Two needs have no headline bullet of their own — the meta-repo's own:
  **SN-007**, the kit's own changes stay traced and tested (the suite
  exercises every script end-to-end against a real scaffold), and **SN-012**,
  the process stays right-sized (perf, guardrails, unattended, and
  parallel-tracks layers cost a repo that doesn't use them nothing).
- The meta-repo's needs, requirements, and tests live under
  [`docs/requirements/`](docs/requirements/) + [`docs/test/`](docs/test/) —
  distinct from the blank templates the kit *ships*.
- It currently passes its own gates at **G3** (gate-walk record:
  [`docs/log.md`](docs/log.md)).

### The gates at a glance

What each approval gate certifies — full criteria in
[`PROCESS.md`](project-trajectory/PROCESS.md) §4:

- **G1 — Requirements/UX/Constraints.** Needs + requirements are complete,
  measurable, and consistent with the vision; every requirement links a need;
  usability/doc needs, constraints, and non-goals are captured.
- **G2 — Decomposition & test coverage.** Every requirement decomposes to design
  (LLR) and a test (TC), each TC written **failing-first**; zero trace orphans;
  no placeholder rows; key runtime flows diagrammed.
- **G3 — Implementation.** Code is written **test-first** and passes the full
  harness: format/lint, full test tier, coverage ≥ threshold, schema, every
  in-scope requirement `Verified`, no stubs.
- **G-Release — Release readiness** *(per release)*. The release test tier
  passes; the generated release checklist is completed and signed; version
  bumped; changelog + interface versions updated.
- **G-Final — Acceptance.** A human exercises the real product (including
  manual/demonstration items) and approves.

See [`project-trajectory/README.md`](project-trajectory/README.md) for the full
tour and the tuning knobs (`COVERAGE_THRESHOLD`, `MAX_ROUNDS`, dropping hats for
small projects).
