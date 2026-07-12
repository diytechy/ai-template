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
- **Plan state:** meta-repo at **G3** (re-attested 2026-07-12, all-mechanized;
  the in-flight derived-gate campaign adds **SR-049**, a mechanized Test SR, which
  **rides a pending re-attestation** at campaign close), spine **SN=24 SR=49
  LLR=50 TC=50, 0 orphans**, 51 declared interface seams, 5 declared components
  (the meta's own How-SW top view is now 24 modules → 5 top-level components, 0
  uncontained). The
  dashboard is the root [`PROJECT_STATE.html`](../PROJECT_STATE.html). Session
  history: [log.md](log.md).
- **Open items:**
  - **Needs \<human> (the run is paused on these):**
    1. **Push decision** — `MultiRepoSupport` is local-only (~48 commits).
    *(Former items 3–5 resolved 2026-07-12 — the WI-DAG soft-edge sweep,
    the already-made sibling-repo ruling, and the guardrails-batch review;
    see [log.md](log.md). The 2026-07-12 deep-review items are ruled and filed
    as backlog WI-078…082 below.)*
  - **External follow-up (tracked upstream, not this repo's work):** the
    guardrails content enrichment (`JUDGMENT.md` playbook + CONTEXT-class rules
    + the `Verified:` greppable claim vocabulary) is **owner-ruled to live in
    `TheColliny/FableClaudeMDForOpus`** and pulled downstream via the vendoring
    layer (`check_vendored.py`); nothing to build in this kit repo. Rationale:
    [archive/INTEGRATION_PLAN.md](archive/INTEGRATION_PLAN.md) Phase 2.
  - **In flight:** _(none)_ — all four 2026-07-11 batches are **closed and
    archived**: the campaign-binning · parallel-tests · resume-hardening
    batch (the `Campaign` grouping column + the campaign-binned When-view
    DAG · pytest-xdist parallel execution, ~6× plain and ~4.6× at the gate ·
    the dirty-tree reconcile surface at loop start, stale-lock verified safe;
    [archive/specs/campaign-binning-parallel-tests-resume-hardening.2026-07-11.md](archive/specs/campaign-binning-parallel-tests-resume-hardening.2026-07-11.md)),
    the owner-feedback batch
    ([archive/specs/owner-feedback-2026-07-11.md](archive/specs/owner-feedback-2026-07-11.md)),
    the capability-expansion campaign
    ([archive/specs/capability-expansion.2026-07-11.md](archive/specs/capability-expansion.2026-07-11.md)),
    and the working-surface + architecture campaign
    ([archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md)).
    Every spine-toucher bundles into the one pending G3 re-attestation above.
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
    - **WI-078** — wire `[step:dupes]` + a `docs/dupes-allow` census (the F5
      bound). Owner-ruled 2026-07-12 (deep-review option (b)): gate *new*
      duplication over an allowlist that **is** the census; keep every script
      independently copy-able (reject the shared helper module). The allowlist
      machinery already exists in `check_dupes.py` — only the `stack.ini` step
      and the populated allowlist remain. Ready; scheduled behind the owner
      sitting. Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §1
      M2/M6.
    - **WI-079** — strip archive-anchor citations on scaffold. Owner-ruled
      2026-07-12: `bootstrap.py` drops the trailing `(REVIEW_*/THREAD_*)`
      provenance suffixes as it copies scripts downstream — provenance stays
      here, downstream gets the copy-ready comment. Lowest-value of the batch;
      accept-and-document is the recorded fallback if the transform isn't cheap.
      Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §1
      M7.
    - **WI-080** — decompose `agent_loop.py:main()` (~1,015 lines / ~500-line
      loop body) behind unit-testable seams. Owner-ruled 2026-07-12: approved as
      its own `main-decomposition` campaign, **test-seams-first** and
      behavior-preserving; the highest-value / highest-risk item, sequenced
      after the owner sitting. Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §3
      H1.
    - **WI-081** — decompose `trace.py:main()` (~640 lines; extract
      `render_report`). Follow-on to WI-080 (soft edge), same shape / less
      urgent (most-copied artifact, so its churn ships widest); the
      `parse_model_map`→`parse_map` rename (L3) folds into whichever refactor
      lands first. Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §3
      M1/L3.
    - **WI-082** — decompose `bootstrap.py:main()` (~390 lines). Owner-ruled
      2026-07-12: left deferred **indefinitely** — milder (honest sequential
      scaffolding), lowest urgency of the three. Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §3
      M5.
    - _(The derived-gate campaign's remaining slices are no longer deferred — the
      campaign is in flight; the live slice list is in **Next action** below.)_
- **Next action — phase v2 (new scope; branch `derived-gate-model` for the gate
  redesign).** A resume session picks up here:
  1. **Derived-gate campaign — RATIFIED, in flight (this branch).** The design
     ([specs/derived-gate-model.md](specs/derived-gate-model.md)) is ratified and
     the foundation slices have landed — the `Draft` artifact state + exemption in
     `trace.py`, SN section-as-state maturity, **`scripts/derive_gate.py`** (the
     gate computed from artifact states, cached to `docs/gate` with a `--check` rot
     guard; the meta reads G3), and **`check.py` now consuming the derived gate**
     (a `derived-gate` freshness step at every gate + the pre-commit floor;
     derive_gate traced into the meta spine as SR-049), and the **phase archetype
     + phase-drop detector** in `check_trajectory` (the `[phase]-[g*]` anchor + the
     "open a new phase-gate WI" warn, all warn-first, vacuous on the single-phase
     meta), and the **ratification workflow** (the `gate-advance` skill +
     `gate-policy`: ratification is now a reviewed `Status`-change commit, and
     `docs/gate` is generated), and the **process-doc rewrite** (PROCESS_OPTIONS
     "Derived gate model" section + reconciled Phased-delivery; PROCESS.md §4/§7
     minimal mechanism edits, **+785 B flagged**, baseline re-stamped 59,638).
     Remaining: **WI-096** migration + dogfood — regenerate the meta `docs/gate` to
     the derived form, prove derived == G3, migrate `gate.template`, the ADOPTING
     recipe, and retire the last hand-set-gate references. Runs under today's
     monolithic gate; once it lands, phase v3+ uses the derived gate.
  2. **Dashboard views re-enter at G1 as new-SR WIs — WI-085**
     ([spec](specs/WI-085.md)) **and WI-087** ([spec](specs/WI-087.md)). Draft
     each a new `SR` (under `SN-021`/`SN-010`, `Phase=v2`; the reviewer
     consistency sweep flags contradictions), **STOP and page the owner to sign
     off** (§4 G1 review, [log.md](log.md)), then G2→G3 under
     `check.py --gate G3 --phase v1`.
  3. **The rest of the backlog needs no new SR — proceed at G3:** WI-078
     (dupes-gate), then `main-decomposition` (WI-080 → WI-081), then WI-079.
  Remaining owner item: the **push decision** above.

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
