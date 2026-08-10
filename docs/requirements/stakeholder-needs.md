# Stakeholder Needs (SN-###) — the kit meta-repo

Every need below serves the [PROJECT-VISION](../../README.md#vision) — a
*reusable starting point for building maintainable, requirement-traced projects
with AI agents and humans working from the same playbook*. The G1 consistency
review checks each row against it: a need serving no part of the vision is scope
creep; a need contradicting it is a finding.

**What this file is.** The kit's *self-adoption* Stakeholder Needs (Thread 47):
the "product" is the kit under `project-trajectory/`, and its stakeholders are
the people and agents who adopt, run, and maintain it. These are the kit's
**own** needs — distinct from the `stakeholder-needs.template.md` it ships to
adopters. Engineering translations live in `system-requirements.csv` (referenced
by `SN-Refs`), authored in Thread 47 phase 3. Priority: **M**=Must · **S**=Should
· **C**=Could.

## Core needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent (how we'd know it's met) |
|---|---|---|---|---|
| SN-001 | A team can drop the kit into a new or existing repo and get a working gated, requirement-traced process without hand-building the tooling. | It is the kit's reason to exist — a *reusable starting point*. | M | `bootstrap.py --dest <repo>` produces a scaffold whose harness runs green out of the box; a re-sync onto an existing repo never clobbers the repo's own files. |
| SN-002 | The trace from need → requirement → design → test is **mechanically verified**, not manually asserted: every requirement links to a need and a test before a gate. | *Requirement-traced … trust what ships*; a hand-maintained trace rots. | M | `trace.py --strict` reports **zero orphans** across the joined `SN→SR→LLR→TC` spine; a malformed/duplicate id fails at any stage. |
| SN-003 | The kit is **stack-agnostic** — a non-Python project uses it by re-pointing the harness at that stack's tools, with Python only as the reference. | *Stack-agnostic with Python-first reference scripts.* | M | The toolchain is declared once in `docs/stack.ini`; a stack swap edits that file, not a kit script; a non-Python bootstrap profile omits Python-only artifacts. |
| SN-004 | Progress advances only through **explicit approval gates** (G1→G2→G3→…), and a gate passes only when its mechanical bar is met. | *Explicit approval gates so you can trust what ships.* | M | `check.py --gate GN` enforces that gate's required steps; a missing required tool **fails**, never silently skips. |
| SN-005 | AI agents and humans work from the **same playbook**, with the process enforced **agent-neutrally** (git hooks + CI), not by trusting any one agent. | *AI agents and humans working from the same playbook*; enforcement can't depend on which agent showed up. | M | The enforcement floor is git + CI running the *same* harness a human runs; per-agent configs only mirror it, never replace it. |
| SN-006 | An agent can run **unattended** and resume from repo text alone; such a run never blocks on a prompt and fails clearly. | Agents develop here; a walk-away run must be safe and resumable. | S | `agent_loop.py` resumes from `docs/status.md`, exits a **typed code** at each end state, and a preflight refuses a broken footing (no agent CLI, not a git repo, private author under privacy-check) rather than hanging. |
| SN-007 | The kit's **own** changes stay traceable and tested — a change to a script is covered by a test exercised end-to-end against a real scaffold. | The kit is a foundation many repos inherit; a regression here propagates downstream. (This need is what Thread 47 makes first-class.) | M | The suite bootstraps a temp scaffold and runs every script; `pytest -q` green is required before each change lands. |
| SN-008 | Gates are **honest** — a green never hides a skipped check, a stub, or an unmet criterion. | *Trust what ships*; a false green is worse than a red. | M | `check.py` **fails** (not skips) on a missing required tool — the explicitly-requested `--lenient` local mode is the one sanctioned degrade to SKIP (SR-006), never a CI/gate default; the no-stub detector and the privacy/secrets floor run at their declared gate. |
| SN-009 | A committed **secret or private identity** is caught before it publishes, in **every** repo, without extra setup. | Trust + safety; a leaked key or PII is near-irreversible once pushed. | M | `check_privacy.py`'s always-on secrets floor scans every commit's staged diff, message, and outgoing range; the privacy gate adds PII/identity classes when the `privacy_check` dial is on. |
| SN-010 | Documentation stays **navigable and honest** — links resolve, the vision is declared once, and generated views cannot silently rot. | *Readable and correct over the long run.* | S | `check_docs.py` fails on a broken intra-repo link or a missing `PROJECT-VISION` tag; every generated artifact carries a `--check` freshness contract. |
| SN-011 | The kit's scripts run on a **clean Python 3.11+ with minimal, argued dependencies** — stdlib by default, a non-stdlib dependency admitted only through a reviewed ledger row — on Windows and POSIX (and macOS). | Portability — the kit must not impose an *unargued* dependency stack on a downstream repo to run its checks. But a blanket "no dependencies" rule is itself a design constraint: it can force a worse hand-rolled alternative than a well-chosen tool, so the bar is **argument, not abstinence** (owner RULING-3, 2026-07-28). | M | Every non-stdlib import in the kit's scripts is declared as a row in `docs/dependencies.md` naming what it replaces, why hand-rolling is worse, and the ruling that admitted it — `tests/test_dependency_ledger.py` fails the suite on an undeclared import; checks an adopter runs (`shipped` tier) stay stdlib-*preferred*, since a dependency there forces every adopter to install it; the CI matrix is green on Linux + Windows + macOS. |
| SN-012 | The process is **right-sized**, not ceremony for its own sake — small changes stay cheap, and heavy layers are opt-in. | An over-heavy process is abandoned; adoption depends on proportionality. | S | Opt-in layers (perf, guardrails, unattended, parallel tracks, OKF export) cost a repo that doesn't use them nothing; the proportionality doctrine governs LLR/TC granularity. |
| SN-023 | A reviewer can see the project's progress **and how its parts connect** from one dashboard-like file. | *Readable and correct over the long run*; the relationships between the parts (which module talks to which, over what contract) are as much of the project's truth as its requirement tree, and scattering them hides architectural drift. | S | The root `PROJECT_STATE.html` renders both the roadmap/decomposition **and** the declared interface graph; every module in the arch-map inventory is a declared `IF-###` interface endpoint or an explicit source/sink, checked mechanically (warn-first). |
| SN-024 | Subjective/perceptual acceptance — a realistic-looking render, an artifact comparison with no crisp measurable interface — is adjudicated by an **independent critical eye against a written rubric**, never by the session that authored the artifact. | *Trust what ships*; an implementer session cannot judge its own output, and a lax test case lets awkward work ship because nothing gave it the critical eye — another agent wearing a different hat must say *where and why* it isn't good enough and drive rework. | S | A `Verification=Critique` requirement is judged by a fresh, family-heterogeneous critique session against a `docs/rubrics/` rubric derived from the SN/SR intent (not the possibly-lax TC); the verdict cites numbered rubric anchor ids, bounded iteration drives rework, and the loop escalates to the human on budget exhaustion. |
| SN-025 | A **single command from the repo root** (`agent-resume`) lets a configured LLM agent implement toward the vision — fully autonomously where enabled — with no human curating what comes next. | Walk-away autonomy is the whole promise of the unattended layer: if a human must hand-maintain a next-step pointer, the loop is attended in practice and the pointer rots against the registry it paraphrases. Extends SN-006 (a *resumable* unattended run) into a *self-directing* one. | S | A plain launch derives what to do next from the tracked WI DAG plus Git — never from prose or a hand-maintained pointer (the `docs/next-wi` file this need made unnecessary, retired by WI-180) and never from predefined tracks; the ready frontier is ordered deterministically, so two readers of the same registry dispatch the same work; the status surface a human reads is generated, never hand-copied. |
| SN-026 | **Several LLM families are configurable** — selected per job and per capability level — and work that benefits from an independent second opinion is automatically routed to a *different* family wherever that is configured. | One family is a single point of both failure and bias: an outage, a retired model or an expired auth stalls the whole loop, and a reviewer drawn from the implementer's own family shares its blind spots — so a same-family review reads like corroboration while adding little. Declaring the families and levels in a registry, rather than hard-coding one vendor, is also what keeps the kit vendor-neutral as models turn over. | S | `docs/agents.csv` declares (family × model × tier) pair-rows and `docs/agents-enabled` is the consent surface whose presence turns managed selection on; the coordinator resolves a row per in-process phase and tier, prefers a cross-family draw for the reviewer, critic and planner-pair sessions, degrades to the *documented* same-family mode when only one family is routable rather than silently skipping the second opinion, and logs every selection before launch — never a silent model swap. |
| SN-027 | Ready work **fans out across bounded parallel lanes**, while mutation of the integration branch stays **serialized and gated**. | Throughput: the WI DAG already encodes what may proceed, so a frontier that advances one item at a time idles for no reason. But parallel *integration* is precisely how a reviewed process ships an unreviewed tree — so the fan-out must narrow back to a single serialized, gated seam before anything lands. | S | A launch with independent ready WIs runs up to the configured worker ceiling (default 2) concurrently in isolated worktrees; every finished branch lands through one serial, fail-closed integrator that runs the declared bar on the composed tree; `--jobs 1` preserves the serial semantic; a declared pause stops claiming and drains what is already in flight; a crash at any lifecycle boundary recovers from Git history alone, without double-assignment or half-integrated authoritative state. Spec of record: `docs/archive/specs/parallel-wi-dispatch.2026-07-20.md` + `docs/concurrency-restructure.md`. |
| SN-028 | **Every policy dial has one home** — a single hand-edited, machine-read file — and a repo that declares the same dial twice is REFUSED rather than resolved by precedence. | The dials had accreted into ~10 one-word files under `docs/`, an idiom that was never ruled: it was held in place by the git hooks' pure-sh parse (a Python-less box must still fail closed on a declared privacy gate) and by a 3.8 floor with no `tomllib`. Both reasons are spent. Scattering costs an owner one file per question and a reader five ad-hoc parsers; worse, two sources for one dial is exactly the state where two readers disagree about the same policy, and a precedence rule makes that disagreement invisible instead of loud. | S | `docs/process.toml` holds every process dial under bare `[section]` headers, one `key = value` per line; the SHAPE is checked rather than conventional, because two grammars read the file (`tomllib` and the hooks' sh) and every shape only one of them understands is a silent flip of a security gate; the two readings are pinned equal over a table of adversarial files; a legacy one-word file still present alongside its key is a REFUSAL naming both, and `bootstrap.py --migrate-config` (run by bootstrap and by the documented re-sync) converts and deletes the legacy files so an adopter never meets that refusal un-aided; a wrong-typed or out-of-range dial is refused, never defaulted. |


## Draft needs (unratified)

The 2026-08-08 mechanized-loop program
(`docs/plan-2026-08-08-mechanized-loop.md`) was built against five needs;
the one still below is all the P0 sitting has left to rule on. The other
four were dispositioned on 2026-08-10 — one attested into Core needs, three
ruled **mis-levelled** and demoted to the requirement tier, their ids
retired and never re-minted. Each ruling is recorded in
[`log.md`](../log.md)'s Decisions section, **not here**: a prose `SN-###`
token anywhere in this file joins the id universe, and one written under
this heading reads as a Draft row. It sits here,
not in Core needs, for one reason: **ratification is the owner's act**, and
that program's own §10 reserves it for the P0 sitting. The machinery says
so rather than trusting the prose — a Draft SN reads G0, so the derived
gate DROPS while these are unratified, which is exactly the "a new phase is
due" signal `docs/gate` exists to give.

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent (how we'd know it's met) |
|---|---|---|---|---|
| SN-029 | **An autonomous run gets as far as it honestly can.** Once triggered, the coordinator stops for a human judgement only when the declared ratification level reserves that tier for a human, when a round cannot converge on its own, or when requirement/test documentation is introduced or amended such that the gate drops below what automation is permitted to attest. | The unattended layer only pays for itself if a walk-away run actually walks away — so what stops it must be exactly the set of judgements the owner reserved, and nothing else. The three-value gate-authority enum (`attended` / `single-ratify` / `autonomous`) could not express "TCs are human-held but LLRs are not", which is the distinction an owner actually wants to dial; four independent tables each re-interpreted the same word, each with its own fail-safe direction. And "has this been ratified?" was answered by walking git for the newest commit where a row read `Verified` — sound only while every amendment flips its row in the same commit, which is precisely the sanctioned path the amendment detector deliberately ignores. So the blessed way to amend an attested requirement was invisible to every consumer, and a stakeholder need had no anchor at all (an SN has no Status cell). | S | A cumulative 0-4 level names the highest tier a human still ratifies, compared against a separately derived SPINE STAGE (which tier is in process) with a declared mapping to the harness gate; every failure direction — an unreadable stage, an out-of-range level, a wrong-typed dial — resolves toward MORE human involvement, because the failure that matters is a machine ratifying something a human meant to hold; each acceptance is anchored ON THE ACCEPTED ARTIFACT'S OWN ROW — the commit whose tree carries the accepted text, plus a digest of that row's normative cells — never in a second registry keyed on the same artifact; and text that has moved away from what was accepted surfaces regardless of any Status movement, which is the one signal the sanctioned amend-and-flip path would otherwise hide — so an AMENDED requirement drops the derived stage exactly as a newly introduced one does. |

## Edge-case expectations

How the kit behaves when things go wrong — the highest-value rows, and (for a
dev-tooling product) mostly **Provision/Startup** and unattended-**Runtime**
failures. Each becomes a measurable SR in phase 3; several map directly to
tests that already exist (noted).

| SN-ID | Lifecycle | Scenario | Expected behavior |
|---|---|---|---|
| SN-013 | Provision | No Python 3 interpreter on PATH (or the Windows Store alias that resolves but exits nonzero) | The git hooks / coordinator **probe by running** a candidate and skip-or-report clearly; they never crash cryptically. |
| SN-014 | Provision | A required harness tool is absent | `check.py` reports `SKIP(missing)` and **fails the gate** — a missing tool is never a silent pass (SN-008). |
| SN-015 | Startup | The working directory is not a git repository | The coordinator preflight reports "not a git repo" and exits nonzero; it never hangs. |
| SN-016 | Startup→Runtime | An unattended run must never block on a prompt at launch **or mid-run** | `agent_loop.py` runs headless (stdin closed); a rate limit backs off, a stall aborts to protect the budget — the loop is never wedged by a prompt. |
| SN-017 | Runtime | The coordinator is killed / power-lost mid-session | The per-worktree lock is a kernel advisory lock the OS releases on death, so the next run is **not wedged** (no stale-pid file). *(tests/test_agent_loop.py::test_lock_auto_released_when_holder_dies)* |
| SN-018 | Runtime | A second coordinator is launched in the same checkout | It is **refused** rather than risking a two-writer race. *(tests/test_agent_loop.py::test_lock_excludes_a_second_process)* |
| SN-019 | Runtime | A repo with **no commits yet** (HEAD absent) | The coordinator's rev-parse guard does not crash the loop. *(tests/test_agent_loop.py::test_zero_commit_repo_is_guarded)* |
| SN-020 | Runtime | The agent CLI / model errors before doing work (retired model, expired auth) | The session is logged `ERROR` and an all-`ERROR` stall is reported as an **unavailable agent**, not a work stall. *(tests/test_agent_loop.py — error region)* |
| SN-021 | Runtime | A generated artifact (arch map, trace view) drifts from its source | Its `--check` fails at the gate — a stale generated doc is a red, not a silent rot (SN-010). |
| SN-022 | Runtime | A committed example row / placeholder is left in a registry at a gate | `--no-placeholders` flags a leftover `-000` row from G2 on; a fresh scaffold stays green until it claims a gate. |

## Non-goals

Explicit scope boundaries — what the kit deliberately does **not** do, recorded
so a later contributor treats them as decisions, not oversights (G1 requires
non-goals to be captured; [PROCESS.md](../../project-trajectory/PROCESS.md) §4).

- **NG-1 · Internationalization / localization.** The kit's display strings,
  CLI output, policy tokens, status vocabulary, registry headers, and parsers
  are English-only by design. The product is a developer-process kit whose
  audience and machine vocabulary are English; externalizing strings would add
  cost with no stakeholder need behind it (recorded from the
  [repo-review-2026-07-22](../repo-review-2026-07-22.md) L-4 finding). If
  localization ever becomes a requirement, first separate the **display**
  strings from the stable **machine** tokens — policy names, status values,
  registry column headers — before translating anything: those tokens are
  contracts, not prose, and must not move with a locale.
