# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is **forward-only**:
only what happens **next** lives here. The **WI registry** is
[work-items.csv](requirements/work-items.csv) (each WI's backward-looking
`Deliverable` records what shipped) and the **session/gate record** is
[log.md](log.md). The kit's per-thread **design history** is archived at
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
  before every commit — this repo's standing gate. The kit's own
  `SN→SR→LLR→TC` spine is self-adopted: `docs/gate` is at **G3**;
  `check.py --gate G3` (12 steps) is the full bar and CI runs it on real data
  (the meta-repo dogfoods its own trajectory + OKF layers).
- **Plan state:** meta-repo at **G3**, spine **SN=23 SR=44 LLR=42 TC=44, 0
  orphans**. The dashboard is the root
  [`PROJECT_STATE.html`](../PROJECT_STATE.html). Session history: [log.md](log.md).
- **Open items:**
  - **Needs \<human> (the run is paused on these):**
    1. **G3 re-attestation** — one sitting covers the accumulated spine changes
       still awaiting sign-off: `SR-034` text (Inspection→Analysis), the added
       `SR-039…SR-043`, the extended `SR-038`, the **`SR-037` text change** (the
       SSOT coherence + SpecRef rules), and now **`SN-023` + `SR-044`** (the
       declared-interface connectivity layer, new SN→SR). *Mandatory*: Verified
       SR text changed and new SN/SRs joined the spine ([log.md](log.md)).
    2. **Push decision** — `MultiRepoSupport` is local-only (~48 commits).
    3. **WI-DAG edge data-pass** — demote the narrative predecessor edges in
       `work-items.csv` to soft `~` edges (which edges are real technical
       blockers vs. authored ordering is the owner's mapping call).
    4. **Sibling-repo ruling** — enrich the guardrails upstream
       (`FableClaudeMDForOpus`) in place vs. a new curated repo, then execute
       the deferred content enrichment (spec:
       [archive/INTEGRATION_PLAN.md](archive/INTEGRATION_PLAN.md) Phase 2).
    5. **Review the owner-directed guardrails-integration batch** (built with
       review deferred; see [log.md](log.md)).
  - **In flight — the working-surface + architecture-connectivity campaign**
    (spec:
    [specs/working-surface-and-architecture-restructure.md](specs/working-surface-and-architecture-restructure.md),
    fully ruled). The SSOT-mechanize, meta-compliance and
    architecture-connectivity-mechanize slices landed (see [log.md](log.md)); the
    spine-touchers bundle into the pending re-attestation (the campaign ruling).
    Remaining:
    - **WI-057** — meta-repo interface authoring: write the kit's own `IF-###`
      seams so its architecture view shows the real system. **Driver:** the
      connectivity layer is now live and the meta repo emits one
      *"connectivity undeclared"* warn (20 arch-map modules, zero IF rows) at the
      hook and G3 — expected and non-blocking; WI-057 authors the rows that
      resolve it.
    - **WI-058** — cross-agent skill sync (checked fan-out from one source).
    - **WI-059** — heterogeneous implementer/reviewer scheduling (sequenced
      last, detachable).
  - **Deferred (backlog — first-class `deferred` WI rows, each with its
    reason):**
    - **WI-060** — coordinator working-tree stash/rollback between sessions
      (owner-deferred 2026-07-05; the clean-exit path has no inter-session
      residue handling yet).
    - **WI-061** — OKF source-doc frontmatter mutation behind a flag
      (intrusive to the source docs; parked until a real consumer earns it).
    - **WI-062** — `check_doc_refs` warn-first untraced-path tier (the
      recommendation is recorded; the meta-repo is a pathological case, so it
      stays filed until it earns wiring).
    - **WI-063** — committed-composite artifact freshness gating (deferred with
      reasoning: the gitignored composites carry no `--check`).
    - **WI-064** — the AXES component/interface residual schema and graph
      extensions (`consumes`/effort schema, a typed-IF contract check,
      edge-vocabulary unification, the swBlock/CMP drift check, cyclic-graph
      rendering — all deferred-on-need).
- **Next action:** continue the campaign — **WI-057** (author the meta repo's own
  `IF-###` seams, resolving the live *"connectivity undeclared"* warn), then
  **WI-058**, **WI-059**. The owner sitting (the re-attestation, push ruling,
  sibling-repo target, batch review) follows the campaign close. After that: the
  G-Release walk, the WI-DAG edge data-pass, or new scope (which needs a plan/WI
  entry first).

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
