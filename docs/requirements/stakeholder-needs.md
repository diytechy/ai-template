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
| SN-008 | Gates are **honest** — a green never hides a skipped check, a stub, or an unmet criterion. | *Trust what ships*; a false green is worse than a red. | M | `check.py` **fails** (not skips) on a missing required tool; the no-stub detector and the privacy/secrets floor run at their declared gate. |
| SN-009 | A committed **secret or private identity** is caught before it publishes, in **every** repo, without extra setup. | Trust + safety; a leaked key or PII is near-irreversible once pushed. | M | `check_privacy.py`'s always-on secrets floor scans every commit's staged diff, message, and outgoing range; the privacy gate adds PII/identity classes when `docs/privacy-check` is on. |
| SN-010 | Documentation stays **navigable and honest** — links resolve, the vision is declared once, and generated views cannot silently rot. | *Readable and correct over the long run.* | S | `check_docs.py` fails on a broken intra-repo link or a missing `PROJECT-VISION` tag; every generated artifact carries a `--check` freshness contract. |
| SN-011 | The kit's scripts run on a **clean Python 3.8+ with no pip installs**, on Windows and POSIX (and macOS). | Portability — the kit must not impose its own dependency stack on a downstream repo to run its checks. | M | Every kit script is stdlib-only; the CI matrix is green on Linux + Windows + macOS. |
| SN-012 | The process is **right-sized**, not ceremony for its own sake — small changes stay cheap, and heavy layers are opt-in. | An over-heavy process is abandoned; adoption depends on proportionality. | S | Opt-in layers (perf, guardrails, unattended, parallel tracks, OKF export) cost a repo that doesn't use them nothing; the proportionality doctrine governs LLR/TC granularity. |
| SN-023 | A reviewer can see the project's progress **and how its parts connect** from one dashboard-like file. | *Readable and correct over the long run*; the relationships between the parts (which module talks to which, over what contract) are as much of the project's truth as its requirement tree, and scattering them hides architectural drift. | S | The root `PROJECT_STATE.html` renders both the roadmap/decomposition **and** the declared interface graph; every module in the arch-map inventory is a declared `IF-###` interface endpoint or an explicit source/sink, checked mechanically (warn-first). |
| SN-024 | Subjective/perceptual acceptance — a realistic-looking render, an artifact comparison with no crisp measurable interface — is adjudicated by an **independent critical eye against a written rubric**, never by the session that authored the artifact. | *Trust what ships*; an implementer session cannot judge its own output, and a lax test case lets awkward work ship because nothing gave it the critical eye — another agent wearing a different hat must say *where and why* it isn't good enough and drive rework. | S | A `Verification=Critique` requirement is judged by a fresh, provider-heterogeneous critique session against a `docs/rubrics/` rubric derived from the SN/SR intent (not the possibly-lax TC); the verdict cites numbered rubric anchor ids, bounded iteration drives rework, and the loop escalates to the human on budget exhaustion. |

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
| SN-017 | Runtime | The coordinator is killed / power-lost mid-session | The per-worktree lock is a kernel advisory lock the OS releases on death, so the next run is **not wedged** (no stale-pid file). *(tests/test_agent_loop_tracks.py — lock auto-release)* |
| SN-018 | Runtime | A second coordinator is launched in the same checkout | It is **refused** rather than risking a two-writer race. *(tests/test_agent_loop_tracks.py — lock mutual exclusion)* |
| SN-019 | Runtime | A repo with **no commits yet** (HEAD absent) | The coordinator's rev-parse guard does not crash the loop. *(tests/test_agent_loop.py::test_zero_commit_repo_is_guarded)* |
| SN-020 | Runtime | The agent CLI / model errors before doing work (retired model, expired auth) | The session is logged `ERROR` and an all-`ERROR` stall is reported as an **unavailable agent**, not a work stall. *(tests/test_agent_loop.py — error region)* |
| SN-021 | Runtime | A generated artifact (arch map, trace view) drifts from its source | Its `--check` fails at the gate — a stale generated doc is a red, not a silent rot (SN-010). |
| SN-022 | Runtime | A committed example row / placeholder is left in a registry at a gate | `--no-placeholders` flags a leftover `-000` row from G2 on; a fresh scaffold stays green until it claims a gate. |
