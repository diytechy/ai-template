# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. Only what happens **next**
lives here; the spec/backlog and per-thread design history live in
[IMPROVEMENT_PLAN.md](../IMPROVEMENT_PLAN.md) (its thread `Status:` blocks and
WI-1.x log). The **gate-walk** record for the kit's self-adoption (Thread 47 —
sign-offs, verdicts) is [log.md](log.md).

- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) — this repo
  has no scaffolded `docs/process.md`; the masters are the reference.
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Bar:** `python -m pytest -q` and
  `python project-trajectory/scripts/check_docs.py --root . --stale` green
  before every commit — this repo's standing gate. **The kit's own
  `SN→SR→LLR→TC` spine is self-adopted** (Thread 47): `docs/gate` is at **G3** —
  `check.py --gate G3` (format · lint · tests+coverage ≥80% · traceability ·
  privacy · doc-nav · perf · flows · trajectory · arch-map · trajectory-map) is
  the full bar, and CI's `gate` job runs it. The `trajectory` + `trajectory-map`
  steps now run on **real data** — the meta-repo dogfoods its own trajectory layer
  (Thread 52 P4). Design history stays in the plan threads; the gate-walk record is
  `docs/log.md`.
- **Plan state:** **Thread 47 complete** — self-adoption phases 1–7 landed
  2026-07-07; meta-repo at **G3** (SN=22 SR=38 LLR=35 TC=38, 0 orphans;
  `check.py --gate G3` PASS; product coverage ~91%). **G3 human-ratified
  2026-07-07 and re-attested 2026-07-09** over the SR-037/038 spine change
  (Peter Johnson, `docs/log.md`). **Thread 50**
  (trace.py SR/LLR citation-coherence check) landed; latest post-plan WIs
  **WI-1.44** (the AXES schema bundle: Workstream + `~` soft edges + the CMP-###
  component layer + MOD→REPO — see the plan entry + ADOPTING §6 recipe) and
  **WI-1.45** (review F2: the shipped pre-commit hook now runs the
  `trajectory-map` freshness step — stale dashboards block at commit, not
  first in CI) and **WI-1.46** (review F4–F8 closure: iterative graph walks,
  the guarded sibling import, and the doc-wording nits — the review is now
  fully resolved).
  **Thread 52 COMPLETE 2026-07-08** (all 4 phases) — the opt-out trajectory/
  work-items layer: `work-items.csv` registry + `check_trajectory.py` +
  `gen_trajectory.py` (offline SVG dashboard) + PROCESS_OPTIONS/README docs.
  **Dogfooded (P4):** the meta-repo carries its own 42-WI
  `docs/requirements/work-items.csv` + generated `docs/trajectory.html`
  (Execution 85%, Definition 100%), gate-green on real data. The **ratified
  design notes** behind WI-1.44 sit at root:
  [`AXES_AND_WORKSTREAMS.md`](../AXES_AND_WORKSTREAMS.md) (static structure,
  iter-9) + [`AGENT_ROLES.md`](../AGENT_ROLES.md) (dynamic layer, R1–R6).
- **Open items:**
  - **Needs <human>**: _(none)_ — **G3 re-attested 2026-07-09** over the
    SR-037/038 spine change (Peter Johnson, `docs/log.md`; F1 fully closed).
    Verification basis: 38/38 SRs mechanized, 0 attested.
  - **In flight:** _(none)_ — **WI-1.43 (F1) + WI-1.44 (schema bundle) +
    WI-1.45 (F2 hook step) + WI-1.46 (F4–F8 closure) landed complete
    2026-07-09** (on `MultiRepoSupport`, **not pushed** — push decision is the
    owner's, see Next action). **THREAD_52_REVIEW.md is now fully resolved
    (F1–F8).**
  - **Queued (next):** the Next-action list below (owner DAG data-pass,
    WI-039, the AGENT_ROLES build calls).
  - **Deferred (backlog):** **Thread 53** — `check_dupes.py` mechanical
    anti-duplication (upstream gilbert; strong candidate, unscheduled). **Thread 51**
    — a first-class TC test-evidence column (ruling pending). **WI-1.27** —
    coordinator working-tree stash/rollback on a hard-killed session
    (owner-deferred 2026-07-05: rely on fresh-session reconciliation).
- **Next action:** **F1 CLOSED** (WI-1.43 + owner re-attestation 2026-07-09,
  `docs/log.md`) and the **schema bundle LANDED (WI-1.44, 2026-07-09)** — the
  [`AXES_AND_WORKSTREAMS.md`](../AXES_AND_WORKSTREAMS.md) iter-9 ratified design
  as one migration event: `Track`→`Workstream` + hard/soft (`~`) predecessor
  edges (F3's schema half), the CMP-### component layer (+ `Component` tags),
  `MOD-###`→`REPO-###` (all never-breaking; ADOPTING §6 has the recipe). **The
  adversarial Thread-52 review is now fully closed** — F1/F2 earlier, and
  **WI-1.46 landed F4–F8 2026-07-09**: iterative `_cycles` + `_dag_ranks` (no
  more `RecursionError` on a deep DAG; the icicle is bounded-by-construction and
  documented), the guarded sibling import + `conftest.load_script` shim (F5(a)),
  and the F6/F7 doc-wording nits; F8 closed by ruling (no code). **The queued
  backlog is now ingest-audited (2026-07-09)** — every queued WI row names its
  spec-of-record and readiness state: **ingest-ready now** = WI-034 (Thread 48
  OKF export, rulings recorded in-thread), WI-035 (Thread 49 doc-currency +
  the F1 deeper-thread rider), WI-039 (`PROJECT_STATE.html`, AXES ratified spec
  — one Q10 migration micro-call to confirm at ingest), **WI-042** (the
  dynamic-layer build, [`AGENT_ROLES.md`](../AGENT_ROLES.md) "Remaining open":
  `docs/review-policy` + `REVIEW-A`/`REVIEW-B` dispatch + `AGENT_CMD_MAP`, the
  status-size guard micro-call, `--prompt-map` deferred); **blocked on an owner
  ruling** = WI-036 (Thread 51 TC-evidence column, 3 questions listed
  in-thread), WI-037 (Thread 53 `check_dupes`, threshold/allowlist policy).
  Now open, in rough order: **owner data-pass on the 42-WI DAG edges** (demote
  remaining narrative edges to `~`; F3's data half); **WI-042** or **WI-039**
  (both unblocked); **push decision outstanding** (`MultiRepoSupport` is
  local-only). Optional milestones: **G-Release** walk; rule **Thread 51** /
  **Thread 53** to unblock WI-036/037.

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
