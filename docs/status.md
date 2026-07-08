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
    gilbert WB19 · D19-6). **Phase 1 landed 2026-07-07**:
    `registries/work-items.template.csv` + `scripts/check_trajectory.py` (stdlib
    validator — acyclic DAG, resolvable predecessors, SR-ref warn, id integrity)
    + the **opt-out `trajectory` check.py step** ({G2,G3}, vacuous on a
    placeholder-only/absent registry, `docs/trajectory-check: off` silences it).
    **Phases 2–4 remain** (offline SVG dashboard · PROCESS_OPTIONS/docs · dogfood
    reshuffle). Phase-0 rulings (Peter 2026-07-07) stand: **(A)** plain-SVG DAG in
    Python, **(B)** opt-out, **(C)** dogfood this plan as work-items by track.
  - **Queued (next):** _(none new — Thread 52 phases 2–4 are the active work; see
    Next action)_
  - **Deferred (backlog):** **Thread 53** — `check_dupes.py` mechanical
    anti-duplication (upstream gilbert; strong candidate, unscheduled). **Thread 51**
    — a first-class TC test-evidence column (ruling pending). **WI-1.27** —
    coordinator working-tree stash/rollback on a hard-killed session
    (owner-deferred 2026-07-05: rely on fresh-session reconciliation).
- **Next action:** **Thread 52 Phase 2** — the **offline dashboard**. Port the SVG
  **icicle** ~as-is from gilbert; **build the plain-SVG layered DAG** (Phase-0 ruling
  A: topological rank → crossing-reduction → coordinate assignment → SVG with a few
  lines of inline vanilla JS, **no CDN**); a vision header + definition/execution
  %-meters; one self-contained `docs/trajectory.html`. Add a `--check` **freshness**
  contract (regenerate-in-memory + byte-compare, like `gen_arch_map --check`) wired
  into the generated-artifact freshness gate; the renderer **reuses
  `check_trajectory.py`'s validation** (single source). Tests: deterministic
  generation; stale html trips `--check`. Read the **Thread 52** spec in
  `IMPROVEMENT_PLAN.md` (Phase-0 rulings baked in — don't re-litigate). Reference:
  gilbert `scripts/gen_trajectory.py` (`c:\Projects\gilbert`, kit-version 767487c) —
  **adapt, don't copy** (its DAG is CDN Cytoscape; ruling A forbids that — build the
  SVG DAG in Python). Other milestones stay optional: **G-Release** walk, or
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
