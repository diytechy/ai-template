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
  ship for Linux/macOS and Windows. The **authoritative per-script table**
  (one home, one row per script) is the kit README:
  [`project-trajectory/README.md`](project-trajectory/README.md). Headliners:
  [`check.py`](project-trajectory/scripts/check.py) (the gate- and tier-aware
  harness) and [`trace.py`](project-trajectory/scripts/trace.py) (the
  traceability join) anchor the floor;
  [`check_docs.py`](project-trajectory/scripts/check_docs.py) keeps the docs
  navigable and this README need-cited (SN-010);
  [`check_privacy.py`](project-trajectory/scripts/check_privacy.py) gives every
  repo a secrets floor plus the opt-in PII/identity gate (SN-009); and
  [`bootstrap.py`](project-trajectory/scripts/bootstrap.py) scaffolds a new
  repo in one command (SN-001). The generated views these produce — including the
  single root `PROJECT_STATE.html` that shows progress **and** how the parts
  connect (the declared `IF-###` interface graph, SN-023) — are listed under
  "The registries & trace artifacts" below.

- **Unattended agent operation** (SN-006):
  - Root `agent-resume.*` launchers boot an agent session at the declared
    tier, or the walk-away coordinator loop
    ([`agent_loop.py`](project-trajectory/scripts/agent_loop.py)).
  - Fresh headless sessions resume from `docs/status.md` until
    `docs/run-state` reaches an end state.
  - A per-phase model map (`docs/run-phase`), reactive rate-limit backoff, a
    stall guard, and tracked per-session logs in `docs/iteration/`.
  - Optional **heterogeneous scheduling** — when `docs/agents-enabled` opts in,
    a committing build schedules separate fresh **reviewer** sessions (redacted
    of the implementer's self-assessment), with the model chosen from the
    `docs/agents.csv` enable-list by tier + provider heterogeneity + cooldown,
    a mechanical substance scorer, and a fixed **win-stay/lose-shift**
    escalation policy (degraded availability — one provider — is legal); absent
    the enable-list, behavior is unchanged (see
    [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) "Unattended
    operation").
  - Optional **subjective-quality critique loop** — a `Verification=Critique`
    requirement's perceptual acceptance is judged by a fresh, provider-
    heterogeneous **critic** against a written [`docs/rubrics/`](project-trajectory/rubrics/README.template.md)
    rubric (numbered good/bad anchors, derived from the SN/SR intent, never the
    authoring session), iterating rework toward the bar and escalating on budget
    exhaustion; a lax-TC ratchet keeps the fix landing in the chain (SN-024).
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
- **An agent guide template**
  ([`AGENTS.template.md`](project-trajectory/AGENTS.template.md)) that encodes
  our readability/maintainability conventions and points agents at the
  process. It scaffolds to `AGENTS.md` (the cross-tool standard), with thin
  `CLAUDE.md`/`GEMINI.md` stubs pointing back at it.

## The registries & trace artifacts — one map

The process stores every durable fact as **one registry row**, referenced
everywhere else by id ([`PROCESS.md`](project-trajectory/PROCESS.md) §2–§3);
anything visual or navigable is a **generated view** of those rows, never a
second home for them. Four registries form the required **spine**; the rest are
optional layers a project adopts only when its scope earns them. How an
ambiguously-reported problem routes *into* these tiers — coverage gap vs.
requirement gap, then scoping via new IF/CMP/PART rows — is the
**change-intake flow**, charted in
[`PROCESS.md`](project-trajectory/PROCESS.md) §5.

```mermaid
graph LR
  subgraph spine["The spine — joined by trace.py; zero orphans to pass a gate"]
    SN["SN-### need"] --> SR["SR-### requirement"]
    SR --> LLR["LLR-### design"]
    LLR --> TC["TC-### test"]
  end
  subgraph off["Off-spine layers — optional; id-integrity-checked when present"]
    WI["WI-### work item"]
    IF["IF-### interface"]
    PB["PB-### perf budget"]
    PART["PART-### purchased part"]
    ASSET["ASSET-### binary asset"]
    CMP["CMP-### component"]
    REPO["REPO-### delegated repo"]
  end
  WI -- "SR-Refs" --> SR
  IF -- "SR-Refs" --> SR
  PB -- "Refs" --> SR
  REPO -- "DelegatedSRs" --> SR
  PART -- "IF-Ref" --> IF
  ASSET -- "Refs" --> LLR
  LLR -. "Component tag" .-> CMP
  IF -. "Component tag" .-> CMP
  ASSET -. "Component tag" .-> CMP
  PART -. "Component tag" .-> CMP
```

### The spine — required, every project

| Registry | Ids | What it does |
|---|---|---|
| [`stakeholder-needs`](project-trajectory/registries/stakeholder-needs.template.md) | `SN-###` | Why the project exists — one need per row, in the stakeholder's words. The root every other row must trace back to. |
| [`system-requirements`](project-trajectory/registries/system-requirements.template.csv) | `SR-###` | One testable *shall*-statement per row, with measurable acceptance criteria and input `Permutations` for test design; cites the `SN` it serves. |
| [`low-level-requirements`](project-trajectory/registries/low-level-requirements.template.csv) | `LLR-###` | The design decomposition — pins an SR onto real code (`Module` + `CodeSymbol`). Adds detail; never paraphrases its parent. |
| [`test-cases`](project-trajectory/registries/test-cases.template.csv) | `TC-###` | Verifies SR/LLR ids, classified by `Method` (Test / Demonstration / Inspection / Attest) and `Tier`; written failing-first at G2. |

[`trace.py`](project-trajectory/scripts/trace.py) joins the four tiers into the
traceability matrix (`docs/test/report.md`; `--html` adds a collapsible map) and
fails the gate on any orphan, duplicate, or malformed id (SN-002).

### Off-spine registries — optional layers

Each lives off the joined spine (an absent or placeholder-only file costs
nothing) but back-links into it, so `trace.py` / `check_trajectory.py`
integrity-check the ids the moment real rows exist.

| Registry | Ids | What it does — and why it exists |
|---|---|---|
| [`interfaces`](project-trajectory/registries/interfaces.template.csv) | `IF-###` | One **directed seam** per row — this side ↔ a counterpart, the shared contract in one testable line, versioned. Endpoints are **primitives** (a repo or module, a physical mating surface) — never components; a component's interface set is *derived*, below. Every interface is backed by an SR and a contract test ([`PROCESS.md`](project-trajectory/PROCESS.md) §8). |
| [`performance-budgets`](project-trajectory/registries/performance-budgets.template.csv) | `PB-###` | Quantitative NFR budgets (latency, RAM, artifact size) that behavior tests can't express; `check_perf.py` compares emitted metrics against budget + baseline (§9). |
| [`procurement`](project-trajectory/registries/procurement.template.csv) | `PART-###` | Parts the project **buys rather than builds** (motor, board, camera): vendor, cost, status, quantity. The owning `IF-###` row is each part's owner-of-record. |
| [`assets`](project-trajectory/registries/assets.template.csv) | `ASSET-###` | The facts *about* an un-diffable binary (art, music, CAD, voice): provenance (AI-content disclosure), license, attribution, contract link, location + hash. |
| [`components`](project-trajectory/registries/components.template.csv) | `CMP-###` | The durable **set-grained** home for knowledge + lifecycle — a subsystem, "the left arm", a package group. It exists because no finer tier can hold either: an IF is one seam, a workstream is mutable by design, and an LLR *is* the thing a rewrite replaces — while `State`/`SupersededBy` carry identity across the rewrite. **Structure is derived, never authored**: membership is a `Component` tag on LLR/IF/ASSET/PART rows; an IF with both endpoints inside a CMP is *internal*, with one endpoint inside it is that CMP's *boundary*. (Ratified design: [`AXES_AND_WORKSTREAMS.md`](docs/archive/AXES_AND_WORKSTREAMS.md); live spec: [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) "Component layer".) |
| [`work-items`](project-trajectory/registries/work-items.template.csv) | `WI-###` | The execution DAG — *when/how* atop the spine's *what*: each WI delivers SRs, belongs to a workstream, and depends on predecessors (a bare id blocks; a `~`-prefixed id only orders). Validated by `check_trajectory.py`; rendered into `PROJECT_STATE.html`. |
| [`repos`](project-trajectory/registries/repos.template.csv) | `REPO-###` | Coordinator-only, for the rare multi-repo rung: one row per delegated repo plus the coordinator SRs it fulfils ([`MULTI_REPO.md`](project-trajectory/MULTI_REPO.md) §6). |

*(Under the parallel-tracks layer,
[`id-blocks`](project-trajectory/registries/id-blocks.template.md) additionally
reserves per-track `SN`/`SR` hundreds-blocks so concurrent drafts never mint the
same id.)*

*(Spine-touching work batches as a **campaign** so one owner sitting re-attests
the whole batch, with the gate cadence riding the same convention — see
[`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) "Campaign ruling".)*

### The generated trace artifacts — views, never sources of truth

Each is regenerated from the registries or source and freshness-gated
(`--check` byte-compares), so it cannot drift from what it depicts:

| Artifact | Generator | Shows |
|---|---|---|
| `docs/test/report.md` / `.html` | `trace.py` | The traceability matrix: counts, the `SN→SR→LLR→TC` outline, orphans and draft rows colored. |
| `docs/architecture.md` code map | `gen_arch_map.py` | Per-module summary, Mermaid dependency diagram, `Implements:` back-links — beneath the hand-written one-page overview and the authored runtime flows `check_flows.py` verifies. |
| root `PROJECT_STATE.html` | `gen_trajectory.py` | The offline dashboard: spine icicle, WI DAG, module map, an OKF knowledge-graph tab (when `docs/okf/` exists), definition/execution meters, a git-derived as-of stamp. |
| `docs/okf/` | `gen_okf.py` | The same graph exported as an Open Knowledge Format bundle — consumed by the dashboard's Knowledge tab. |
| `docs/release-checklist.md` | `gen_release_checklist.py` | Every human-verified item (Demonstration / Manual / Inspection SRs, Release-tier TCs) as back-linked tick-boxes for G-Release. |

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
- root `run.*` / `agent-resume.*` launchers (shipped inert until you wire them —
  a `[run]` section in `docs/stack.ini` for `run.*`, `AGENT_CMD` for
  `agent-resume.*`)
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
