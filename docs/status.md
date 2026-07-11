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
  `check.py --gate G3` (13 steps) is the full bar and CI runs it on real data
  (the meta-repo dogfoods its own trajectory + OKF layers).
- **Plan state:** meta-repo at **G3**, spine **SN=23 SR=46 LLR=47 TC=47, 0
  orphans**, 49 declared interface seams. The dashboard is the root
  [`PROJECT_STATE.html`](../PROJECT_STATE.html). Session history: [log.md](log.md).
- **Open items:**
  - **Needs \<human> (the run is paused on these):**
    1. **G3 re-attestation** — one sitting covers the accumulated spine changes
       still awaiting sign-off: `SR-034` text (Inspection→Analysis), the added
       `SR-039…SR-043`, the extended `SR-038`, the **`SR-037` text change** (the
       SSOT coherence + SpecRef rules), **`SN-023` + `SR-044`** (the
       declared-interface connectivity layer, new SN→SR), the **`SR-025`
       text change** (extended to the checked per-agent skill fan-out; +LLR-043/
       TC-045), and now the **new `SR-045`** under `SN-006`/`SN-016` (the S8
       heterogeneous implementer/reviewer scheduling layer; +LLR-044/045/046 +
       TC-046 + IF-044…047), **its text since extended by the pair-row registry
       slice** (pair-row identity/access split, Family-keyed heterogeneity,
       version-less newest resolution, per-pair `Env`; +LLR-044/045 text), and
       now the **new `SR-046`** under `SN-001` (the
       run capability menu / launcher surface; +LLR-047 + TC-047), and now the
       **new `SN-024` + `SR-047`** under `SN-024`/`SN-006` (the subjective-quality
       critique loop / `Critique` verification value; +LLR-048 + TC-048).
       *Mandatory*: Verified SR text changed and new SN/SRs joined the spine
       ([log.md](log.md)).
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
  - **In flight — the capability-expansion campaign** (spec:
    [specs/capability-expansion.md](specs/capability-expansion.md), fully
    ruled + scheduled 2026-07-11, bundled with the pending re-attestation):
    - **WI-070** — `PROJECT_STATE.html` OKF knowledge tab (the bundle's
      first real consumer; extends the dashboard SR).
    **Next up: WI-070** (the C4 OKF knowledge tab). The C3 pair-row agent
    registry just landed (Family/Model/Version identity vs CmdTemplate/Env
    access, one row = one model×route pair; version-less newest-in-line
    resolution; Family-keyed heterogeneity; per-pair Env merged into the launch;
    account/router rows; SR-045 text extended, riding the re-attestation). The
    prior working-surface + architecture campaign
    is closed and archived
    ([archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md));
    all spine-touchers bundle into the one pending re-attestation.
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
    - **WI-065** — reconcile the `Verifies` vocabulary between `trace.py` and
      the seam-TC-citation scan (spec: [specs/WI-065.md](specs/WI-065.md);
      deferred until a seam actually needs `Active` status — every current
      seam is `Stable`).
- **Next action:** execute the capability-expansion campaign in order —
  **WI-070** next (the C3 pair-row registry just landed), the campaign's last
  slice. The **owner sitting** follows
  the campaign close: one G3 re-attestation over every accumulated spine
  change (both campaigns), the push ruling, the sibling-repo target, and the
  deferred batch review. After that: the G-Release walk, the WI-DAG edge
  data-pass, or new scope (which needs a plan/WI entry first).

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
