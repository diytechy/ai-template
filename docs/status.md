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
  2026-07-07** (Peter Johnson, `docs/log.md`); **the 2026-07-09 SR-037/038 spine
  change (F1 fix, WI-1.43) awaits re-attestation** — see log.md. **Thread 50**
  (trace.py SR/LLR citation-coherence check) landed; latest post-plan WI **WI-1.43**.
  **Thread 52 COMPLETE 2026-07-08** (all 4 phases) — the opt-out trajectory/
  work-items layer: `work-items.csv` registry + `check_trajectory.py` +
  `gen_trajectory.py` (offline SVG dashboard) + PROCESS_OPTIONS/README docs.
  **Dogfooded (P4):** the meta-repo carries its own 37-WI
  `docs/requirements/work-items.csv` + generated `docs/trajectory.html`
  (Execution 86%, Definition 100%), gate-green on real data.
- **Open items:**
  - **Needs <human>**: **G3 re-attestation for the SR-037/038 spine change**
    (WI-1.43, the F1 fix — owner authorized the change 2026-07-09; the mechanized
    bar was re-run and PASSes; a one-line sign-off in `docs/log.md` closes it).
    Verification basis: 38/38 SRs mechanized, 0 attested.
  - **In flight:** _(none)_ — **Thread 52 landed complete 2026-07-08** (commits
    `07fd10f`/`6fa3236`/`49a5cf8` + P4; on `MultiRepoSupport`, not pushed).
  - **Queued (next):** _(none scheduled)_
  - **Deferred (backlog):** **Thread 53** — `check_dupes.py` mechanical
    anti-duplication (upstream gilbert; strong candidate, unscheduled). **Thread 51**
    — a first-class TC test-evidence column (ruling pending). **WI-1.27** —
    coordinator working-tree stash/rollback on a hard-killed session
    (owner-deferred 2026-07-05: rely on fresh-session reconciliation).
- **Next action:** **F1 is RESOLVED (WI-1.43, 2026-07-09)** — SR-037/038 +
  LLR-034/035 + TC-037/038 landed, G3 re-run PASS; **owner re-attestation pending**
  (`docs/log.md`). Then, per the ratified design notes
  ([`AXES_AND_WORKSTREAMS.md`](../AXES_AND_WORKSTREAMS.md) iter-9 +
  [`AGENT_ROLES.md`](../AGENT_ROLES.md)): the **one-bump schema bundle** (CMP
  registry + `Component` tags + `Track`→`Workstream` + hard/soft `kind` +
  `MOD→REPO` + resync scaffolding — F3's dogfood-DAG cleanup rides along).
  Remaining review findings: **F2 (MEDIUM)** — `trajectory.html` staleness
  caught only in CI, not the pre-commit hook — and F4–F8 (see
  [`THREAD_52_REVIEW.md`](../THREAD_52_REVIEW.md)). Push decision outstanding
  (`MultiRepoSupport` is local-only). Optional milestones: **G-Release** walk;
  rule **Thread 51** / schedule **Thread 53**.

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
