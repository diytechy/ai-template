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
  privacy · doc-nav · perf · flows · arch-map) is the full bar, and CI's `gate`
  job runs it. Design history stays in the plan threads; the gate-walk record is
  `docs/log.md`.
- **Plan state:** **Thread 47 complete** — self-adoption phases 1–7 landed
  2026-07-07; meta-repo at **G3** (SN=22 SR=36 LLR=33 TC=36, 0 orphans;
  `check.py --gate G3` PASS; product coverage ~91%). **G3 human-ratified
  2026-07-07** (Peter Johnson, `docs/log.md`; G1+G2+G3 all ratified). **Thread 50**
  (trace.py SR/LLR citation-coherence check) landed; latest post-plan WI **WI-1.42**.
  **Thread 52 Phase 1 landed 2026-07-07** — the work-items registry +
  `check_trajectory.py` validator + the opt-out `trajectory` gate step.
- **Open items:**
  - **Needs <human>**: _(none)_ — **G3 ratified 2026-07-07** (`docs/log.md`); the
    mechanized bar was met and reproduced, the owner signed off on the basis of
    spot checks + four adversarial review passes (findings resolved). Verification
    basis: 36/36 SRs mechanized, 0 attested.
  - **In flight:** **Thread 52** — Trajectory / work-items layer (upstreaming
    gilbert WB19 · D19-6). **Phases 1–3 landed 2026-07-07**: **P1** the
    `work-items.csv` registry + `check_trajectory.py` validator + the opt-out
    `trajectory` gate step; **P2** `gen_trajectory.py` → a fully-offline
    `docs/trajectory.html` (SVG icicle + **plain-SVG layered DAG in Python**, no
    CDN) + the `trajectory-map` freshness gate ({G3}); **P3** the PROCESS_OPTIONS
    "Trajectory / work-items layer" section + STATUS convention + README
    kit-contents (PROCESS.md/AGENTS byte-flat). **Phase 4 remains** — dogfood:
    decompose this plan into a real `work-items.csv` by track + generate the kit's
    own dashboard. Phase-0 rulings (Peter 2026-07-07) stand.
  - **Queued (next):** _(none new — Thread 52 phases 2–4 are the active work; see
    Next action)_
  - **Deferred (backlog):** **Thread 53** — `check_dupes.py` mechanical
    anti-duplication (upstream gilbert; strong candidate, unscheduled). **Thread 51**
    — a first-class TC test-evidence column (ruling pending). **WI-1.27** —
    coordinator working-tree stash/rollback on a hard-killed session
    (owner-deferred 2026-07-05: rely on fresh-session reconciliation).
- **Next action:** **Thread 52 Phase 4** — **dogfood the layer (ruling C).** Author
  `docs/requirements/work-items.csv` for the kit itself: map the landed Threads +
  `WI-1.x` into `WI-###` rows organized **by track** (e.g. `scripts`,
  `docs/process`, `self-adoption`, `unattended`) with predecessors + SR-refs;
  reconcile with the existing Thread/`WI-1.x` numbering (**map, don't renumber
  blindly** — likely coexist: the CSV is the machine-readable execution registry
  beside the prose plan). Then generate the kit's own `docs/trajectory.html` and let
  the `trajectory` + `trajectory-map` gate steps go green on **real** data (vacuous
  today). Owner accepts this is a deep reshuffle — stage it LAST, now that the
  tooling (P1–P3) validates it. Read the **Thread 52** spec in `IMPROVEMENT_PLAN.md`
  (Phase-0 ruling C). Other milestones stay optional: **G-Release** walk, or
  **Thread 48/49**.

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
