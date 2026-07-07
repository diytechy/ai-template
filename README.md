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

The kit's headline pieces:

- **A gated process** ([`PROCESS.md`](project-trajectory/PROCESS.md)) — roles as
  "hats", approval gates (G1→G2→G3→G-Release→G-Final; G-Release only for
  versioned releases), and a verdict protocol; each gate's bar **fails, never
  silently skips** (SN-004, SN-008).
- **A traceability spine** — `SN → SR → LLR → TC` registries joined by a
  generated matrix that must report **zero orphans** before each gate (SN-002).
- **Runnable scripts** (stdlib-only Python 3.8+, no pip needed for the kit
  itself — SN-011): [`check.py`](project-trajectory/scripts/check.py) (the gate- and
  tier-aware harness), [`trace.py`](project-trajectory/scripts/trace.py)
  (traceability), [`check_docs.py`](project-trajectory/scripts/check_docs.py)
  (doc-navigability: broken-link + orphan-doc checks, plus the README
  `PROJECT-VISION:` tag + the **opt-out** README need-coverage guard, and
  `--stale` — SN-010),
  [`check_flows.py`](project-trajectory/scripts/check_flows.py)
  (the authored runtime-flows section: diagrams present, cited ids real),
  [`check_perf.py`](project-trajectory/scripts/check_perf.py)
  (performance-budget + regression comparator),
  [`check_stubs.py`](project-trajectory/scripts/check_stubs.py)
  (optional, warn-first no-stub/substance detector for the G3 criterion),
  [`check_privacy.py`](project-trajectory/scripts/check_privacy.py)
  (a deterministic **secrets floor** for committed keys/tokens in every repo,
  opt-out via `docs/secrets-scan`, plus privacy/PII classes — author email,
  content, and commit messages — gated on the `docs/privacy-check` toggle —
  SN-009),
  [`gen_arch_map.py`](project-trajectory/scripts/gen_arch_map.py)
  (the AST code map — summaries, dependencies, `Implements:` back-links — plus
  a generated Mermaid dependency diagram, routed into `architecture.md` and/or
  `AGENTS.md`/`CLAUDE.md`),
  [`gen_release_checklist.py`](project-trajectory/scripts/gen_release_checklist.py)
  (the human release checklist),
  [`gen_cases.py`](project-trajectory/scripts/gen_cases.py) (boundary-aware,
  pairwise test-case combinations), and
  [`bootstrap.py`](project-trajectory/scripts/bootstrap.py) (scaffold a new repo —
  SN-001).
  Cross-platform `setup`/`check` launchers (`.sh` + `.ps1`) ship for Linux/macOS
  and Windows.
- **Unattended agent operation** (SN-006) — root `agent-resume.*` launchers boot an
  agent session at the declared tier, or the walk-away coordinator loop
  ([`agent_loop.py`](project-trajectory/scripts/agent_loop.py)): fresh headless
  sessions resume from `docs/status.md` until `docs/run-state` reaches an end
  state, with a per-phase model map (`docs/run-phase`), reactive rate-limit
  backoff, a stall guard, tracked per-session logs in `docs/iteration/`, and
  optional **tier-conditional guardrails** (`docs/guardrails-policy` injects a
  vendored discipline core into weaker-tier sessions; drift-checked by
  `check_vendored.py`).
  Consent is explicit and governed by one-word declared-policy files scaffolded
  into `docs/`: `gate-policy` (who advances gates), `push-policy` (who may
  push), and `privacy-check` (the PII/identity privacy gate — a `true`/`false`
  toggle enforced by the git hooks + `check_privacy.py`).
- **Agent-neutral skills and hooks** (SN-005) — opt-in skills
  ([`skills/`](project-trajectory/skills/)) materialized per agent by
  `bootstrap.py --agents`, and git hooks
  ([`hooks/`](project-trajectory/hooks/)): a fast `pre-commit` process floor
  and a `pre-push` privacy backstop for privacy-checked repos.
- **Cross-project support** — an [`IF-###` interfaces registry](project-trajectory/INTERFACES.template.md)
  for projects that interlink, so shared contracts stay traceable and versioned.
- **An agent guide template** ([`AGENTS.template.md`](project-trajectory/AGENTS.template.md))
  that encodes our readability/maintainability conventions and points agents at
  the process. It scaffolds to `AGENTS.md` (the cross-tool standard), with thin
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

> **Which `python`?** The kit needs Python 3.8+. These examples say `python`; if
> that name is missing or points at Python 2, use `python3` (usual on Linux/macOS)
> or the `py` launcher (Windows). On a fresh macOS, the first `python3` may prompt
> you to install the Command Line Tools — accept it (or run `xcode-select
> --install`), which also provides `git`.

This scaffolds `AGENTS.md` (the agent guide; `CLAUDE.md`/`GEMINI.md` stubs point
at it), `docs/` (process, status + log + plan, architecture, interfaces, the
registries, and the declared-policy files `gate`, `gate-policy`, `push-policy`,
`privacy-check`), `scripts/` (the harness), the root `run.*` /
`agent-resume.*` launchers (shipped inert until you fill their command slots),
`.github/workflows/check.yml`, and empty `src/`/`tests/`. Then:

1. Fill the **PROJECT BRIEF** in the new repo's `AGENTS.md` and `docs/status.md`.
2. Install the harness tooling for your stack (the Python reference uses
   `ruff pytest pytest-cov`). The commands the harness runs — format, lint,
   test, tiers, coverage — are declared once in the new repo's `docs/stack.ini`;
   a non-Python stack edits that one file.
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

> **Scope — generate vs. measure.** This kit *generates* legibility (the traced
> spine, the committed code map, the gates), so a repo built with it should score
> well by construction. *Measuring* legibility over time — AI-readiness or
> complexity/churn dashboards — is a separate, **optional downstream** concern,
> not a kit dependency (see [`PROCESS.md`](project-trajectory/PROCESS.md) §7).

> **Scope — spec vs. runtime harness.** This kit is a portable process *spec*; a
> turnkey, tool-specific agent-runtime harness (an installed engine with its own
> gates/subagents) is different, optional, downstream tooling that can run *with*
> a repo built from this kit — never a dependency of it (see
> [`PROCESS.md`](project-trajectory/PROCESS.md) §7).

> **Scope — project scale.** **One module in one repo is the default.** A larger
> repo can host several modules on the same spine (sub-trees grouped by
> `Module`/`Area`, module-scoped review by convention, an integration TC at each
> seam); a multi-repo split under a coordinator is a rarer, heavier step taken only
> when modules need independent versioning or release — scale up the escalation
> ladder only when the scope forces it (see
> [`PROCESS.md`](project-trajectory/PROCESS.md) §10; the coordinator model is
> [`MULTI_REPO.md`](project-trajectory/MULTI_REPO.md), a design with the cross-repo
> tooling deferred).

> **Onboarding ladder.** A fresh contributor's path mirrors the lifecycle phases
> one level up — `Stage 0` (get git + the repo) → `dev-setup` (workstation:
> runtime, git, an offline Mermaid renderer) → `setup` (product toolchain) →
> `check` (the gates) — each rung optional, readable, and consent-first. The kit
> scaffolds a per-platform Stage-0 `onboard` script (with a native folder picker
> and an AI-agent handoff for non-coders) and a tiered `dev-setup` (see
> [`PROCESS.md`](project-trajectory/PROCESS.md) §7).

## Built with the kit (self-adoption)

This repo eats its own dog food: the kit is developed **using the kit's own
process**, traced by its own `SN→SR→LLR→TC` spine and gated by its own
[`check.py`](project-trajectory/scripts/check.py). Every capability above cites
the [stakeholder need](docs/requirements/stakeholder-needs.md) it realizes, and
`check_docs.py`'s **opt-out** need-coverage guard keeps that honest — every
Must/Should need must be cited somewhere in this README, so a requirements change
mechanically ages it (no delimiter markers; any `SN-###` counts). The two needs
without a headline bullet are the meta-repo's own: **the kit's own changes stay
traced and tested** (SN-007 — the suite exercises every script end-to-end against
a real scaffold) and **the process stays right-sized** (SN-012 — perf, guardrails,
unattended, and parallel-tracks layers cost a repo that doesn't use them nothing).

The meta-repo's needs, requirements, and tests live under
[`docs/requirements/`](docs/requirements/) + [`docs/test/`](docs/test/) —
distinct from the blank templates the kit *ships* — and it currently passes its
own gates at **G3** (the gate-walk record is [`docs/log.md`](docs/log.md)).

### The gates at a glance

What each approval gate certifies — the full criteria live in
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
