# ai-template

**PROJECT-VISION:** A reusable starting point for building **maintainable,
requirement-traced projects** with AI agents and humans working from the same
playbook. The goal: code and analytics that stay readable and correct over the
long run, built **test-first** with **explicit approval gates** so you can
trust what ships.

It is **stack-agnostic** with **Python-first reference scripts** — drop it into
any repo and wire the harness to that repo's tooling.

## What's in here

| Path | What it is |
|---|---|
| [`project-trajectory/`](project-trajectory/) | The portable kit: the gated, requirement-traced development process plus all templates and runnable scripts. **This is the thing you copy into new repos.** |
| [`project-trajectory/README.md`](project-trajectory/README.md) | Full contents + rationale for the kit. |
| [`CLAUDE.md`](CLAUDE.md) | Guide for working **in this template repo** (developing the templates themselves). |

The kit's headline pieces:

- **A gated process** ([`PROCESS.md`](project-trajectory/PROCESS.md)) — roles as
  "hats", approval gates (G1→G2→G3→G-Release→G-Final; G-Release only for
  versioned releases), and a verdict protocol.
- **A traceability spine** — `SN → SR → LLR → TC` registries joined by a
  generated matrix that must report **zero orphans** before each gate.
- **Runnable scripts** (stdlib-only Python 3.8+, no pip needed for the kit
  itself): [`check.py`](project-trajectory/scripts/check.py) (the gate- and
  tier-aware harness), [`trace.py`](project-trajectory/scripts/trace.py)
  (traceability), [`check_docs.py`](project-trajectory/scripts/check_docs.py)
  (doc-navigability: broken-link + orphan-doc checks),
  [`check_perf.py`](project-trajectory/scripts/check_perf.py)
  (performance-budget + regression comparator),
  [`check_stubs.py`](project-trajectory/scripts/check_stubs.py)
  (optional, warn-first no-stub/substance detector for the G3 criterion),
  [`gen_arch_map.py`](project-trajectory/scripts/gen_arch_map.py)
  (the AST code map — summaries, dependencies, `Implements:` back-links — plus
  a generated Mermaid dependency diagram, routed into `architecture.md` and/or
  `AGENTS.md`/`CLAUDE.md`),
  [`gen_release_checklist.py`](project-trajectory/scripts/gen_release_checklist.py)
  (the human release checklist),
  [`gen_cases.py`](project-trajectory/scripts/gen_cases.py) (boundary-aware,
  pairwise test-case combinations), and
  [`bootstrap.py`](project-trajectory/scripts/bootstrap.py) (scaffold a new repo).
  Cross-platform `setup`/`check` launchers (`.sh` + `.ps1`) ship for Linux/macOS
  and Windows.
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
at it), `docs/` (process, status, architecture, interfaces, the registries),
`scripts/` (the harness), `.github/workflows/check.yml`, and empty
`src/`/`tests/`. Then:

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

See [`project-trajectory/README.md`](project-trajectory/README.md) for the full
tour and the tuning knobs (`COVERAGE_THRESHOLD`, `MAX_ROUNDS`, dropping hats for
small projects).
