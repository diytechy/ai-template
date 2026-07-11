# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. Only what happens **next**
lives here; the **WI registry** is
[work-items.csv](requirements/work-items.csv) and the **session/gate record** is
[log.md](log.md). The kit's per-thread **design history** (thread `Status:`
blocks + the WI-1.x log) is archived at
[archive/IMPROVEMENT_PLAN.md](archive/IMPROVEMENT_PLAN.md) — context, not a
working surface.

- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) — this repo
  has no scaffolded `docs/process.md`; the masters are the reference.
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Bar:** `python -m pytest -q` and
  `python project-trajectory/scripts/check_docs.py --root . --stale` green
  before every commit — this repo's standing gate. **The kit's own
  `SN→SR→LLR→TC` spine is self-adopted** (Thread 47): `docs/gate` is at **G3**
  — `check.py --gate G3` (12 steps; the `okf` freshness step joined 2026-07-10)
  is the full bar and CI's `gate` job runs it, on **real data** (the meta-repo
  dogfoods its own trajectory + OKF layers). Design history: the plan threads;
  gate-walk record: [log.md](log.md).
- **Plan state:** meta-repo at **G3**, spine **SN=22 SR=43 LLR=40 TC=43, 0
  orphans**, 43/43 SRs mechanized. Latest batch: the **ClaudeGuardChecks
  integration, Phases 1–5** (WI-045…049, owner-directed, review deferred) —
  the working-agreement distill, the guardrails reference-upstream pointer, the
  enforcement-audit discipline + `stdlib-only` promoted to a test (SR-034), and
  the subagent spawn gate (**SR-043**). The prior 2026-07-10 grind
  (WI-1.47…1.54) + its triage are in [log.md](log.md) and
  [work-items.csv](requirements/work-items.csv). **`IMPROVEMENT_PLAN.md` is now
  archived** ([archive/IMPROVEMENT_PLAN.md](archive/IMPROVEMENT_PLAN.md)) — the
  live homes are this file, `work-items.csv`, and `log.md`. Dogfood registry:
  **51 WIs, 50 done + WI-033 active**; the dashboard is the root
  [`PROJECT_STATE.html`](../PROJECT_STATE.html).
- **Open items:**
  - **Needs <human> (the run is paused on these):**
    1. **G3 re-attestation** — one sitting now covers the 2026-07-10 grind
       (SR-039…042 added, SR-038 extended, the B1 SN-Refs correction) **and**
       this batch (SR-034 text Inspection→Analysis; new **SR-043**). *Mandatory*:
       a Verified SR's text changed and a new SR joined the spine ([log.md](log.md)).
    2. **Push decision** — `MultiRepoSupport` is local-only (~46 commits).
    3. **F3 data-pass** on the 48-WI DAG edges (demote narrative edges to
       `~`) — owner's mapping call, unchanged.
    4. **Phase 2 sibling-repo ruling** — enrich the guardrails upstream
       (`FableClaudeMDForOpus`) in place vs. a new curated repo, then execute
       the deferred content enrichment (spec:
       [`docs/archive/INTEGRATION_PLAN.md`](archive/INTEGRATION_PLAN.md) Phase 2).
    5. **Review the Phases 1–4 batch** (owner-directed, review deferred).
  - **In flight:** _(none)_ — the queue is empty.
  - **Recently landed:** the **2026-07-10 late batch (WI-050…052, no spine
    change)** — the root-README registry/artifact map + the PROCESS.md §5
    **change-intake flow** (the defect-routing chart), the fresh-Mac dev-setup
    honesty fixes + `dev-setup.template.command` rung, and the pytest-cov 7
    subprocess-coverage re-wire (29%→91%; also heals the CI `check` job). Before
    it, the **ClaudeGuardChecks integration Phases 1–5**
    (WI-045…049, 2026-07-10; SR-034 promoted + new SR-043 ride the
    re-attestation; its spec-of-record `INTEGRATION_PLAN.md` copied into
    `docs/archive/` so no citation points outside this repo) and, before it,
    **OKF Layer B2** (WI-1.54).
  - **Deferred (backlog):** **WI-1.27** coordinator stash/rollback
    (owner-deferred 2026-07-05); OKF **Layer B1** (intrusive doc-frontmatter,
    behind a future flag); the **Q1 rider ruling** (a warn-first `--untraced`
    tier — recommendation recorded in WI-1.50's entry); the committed-composites
    freshness design (deferred with reasoning, WI-1.50); the AXES §12
    residual items — `consumes`/effort schema, a typed-IF contract check,
    edge-vocabulary unification, the swBlock/CMP drift check, cyclic-graph
    rendering (all gated on real need; see
    [`docs/archive/AXES_AND_WORKSTREAMS.md`](archive/AXES_AND_WORKSTREAMS.md) §12).
- **Next action:** the **owner sitting** — re-attest G3 per [log.md](log.md),
  rule on push (~48 commits), rule on the Phase 2 sibling-repo target, and
  review the Phases 1–5 batch. After that the frontier is open: G-Release walk,
  the F3 edge data-pass, the **working-surface SSOT + architecture-connectivity
  restructure** (**S0–S8 fully ruled 2026-07-10**, including the S8
  heterogeneous-implementer/reviewer addition — ready to schedule as one
  campaign bundled with the re-attestation:
  [specs/working-surface-and-architecture-restructure.md](specs/working-surface-and-architecture-restructure.md)),
  or new scope (which needs a plan/WI entry first).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/` — nothing to double-click
  launch); no scaffolded `docs/process.md` (the masters live in
  `project-trajectory/`). *(The SN-spine non-goal was **lifted by Thread 47** —
  the kit now traces itself; its registries live in `docs/requirements/` +
  `docs/test/`, distinct from the shipped `project-trajectory/registries/`
  templates.)*
