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

- **Bar:** `python -m pytest -q -n auto -m smoke` (the fast per-commit smoke
  tier — ~47 s / 531 cases; full unfiltered suite ~66 s / 684 at
  slice/campaign close) and
  `python project-trajectory/scripts/check_docs.py --root . --stale` green
  before every commit — this repo's standing gate. The kit's own
  `SN→SR→LLR→TC` spine is self-adopted and the gate is **derived**
  (`scripts/derive_gate.py`): with **phase v2 verified** (both v2 SRs
  `Verified` 2026-07-13) the runnable `docs/gate` reads a uniform **G3** (basis
  `per-phase=(default)=G3;v2=G3`); the full bar is
  `check.py --gate G3 --phase v1,v2` (incl. the `derived-gate` freshness step),
  and CI runs the derived gate on real data (the meta-repo dogfoods its own
  trajectory + OKF + derived-gate layers).
- **Plan state:** v1 spine at **G3** (re-attested 2026-07-12, all-mechanized;
  the derived-gate campaign added **SR-049**, a mechanized Test SR, which
  **rides a pending re-attestation** — Needs \<human> above); **phase v2 now at
  G3** — SR-050/SR-051 (the dashboard views, `Phase=v2`) ratified `Planned` by
  the G1 LLM-gate review, decomposed to LLR-051/052 + TC-051/052 by the
  `[v2]-[g2]` batch, then both **Verified by their dev slices** (SR-050 by the
  Process tab 2026-07-12; **SR-051 by the tiered drill-down views 2026-07-13**,
  `Test`, TC-052's 9 pinned pytest nodes). The whole v2 spine cut + the v2 → G3
  advance **rides the owner's queued single-ratify sitting** (Needs \<human>
  below). Spine **SN=24
  SR=51 LLR=52 TC=52, 0 orphans**, 52 declared interface seams, 5 declared components
  (the meta's own How-SW top view is now 24 modules → 5 top-level components, 0
  uncontained). The
  dashboard is the root [`PROJECT_STATE.html`](../PROJECT_STATE.html). Session
  history: [log.md](log.md).
- **Unattended layer (enabled 2026-07-12; cross-provider + owner re-lineup same
  day):** the kit's walk-away loop is wired for a managed, consent-explicit run —
  `docs/gate-policy` = **`single-ratify`** (one human attest per phase batch;
  register [gate-policy.md](gate-policy.md)), managed routing ON via
  `docs/agents-enabled`: **6 pair rows / 2 families** in `docs/agents.csv` —
  `ANTHROPIC` **Fable/Opus/Sonnet = strong/medium/quick** via the claude CLI
  (Env pins `CLAUDE_CODE_EFFORT_LEVEL=high`) and `OPENAI` GPT-5.6
  **Sol/Terra/Luna = strong/medium/quick** via the opencode CLI. Tier
  vocabulary renamed **`weak`→`quick`** (kit-wide; legacy `weak` reads as
  `quick`, never-breaking). Reviews route **cross-family** (build=fable →
  REVIEW-A=terra; same-family is the degraded-legal fallback). Both CLIs are
  **installed + signed in** (claude 2.1.207 on PATH; opencode OpenAI oauth);
  dev-setup names them and `--install` offers each individually. Failure
  context rides the registry `Notes` (echoed at preflight, cooldown, and the
  no-routable page). `docs/run-phase` = `BUILD`, `docs/guardrails-policy` =
  `off` (no core vendored here — reason in the file), launcher twins' fallback
  maps re-pointed (strong=claude-fable-5; BUILD + reviews=opus since the
  owner's 2026-07-12-evening dial turn — `AGENT_TIER_MAP` empty, so BUILD
  rides the engine's medium default with tier-up-never-down escalation as the
  re-raise; the first live run had spent 78% of wall time in strong-tier
  BUILDs). No spine change — **derived gate stays G3**. **Live-verified
  through the loop's own machinery (run_session): 5/6 models replied** —
  fable/opus/sonnet (effort env merged) + sol/terra; **gpt-5.6-luna hangs
  today** (id valid in opencode's catalog; 2 attempts, zero output — the loop
  degrades to TIMEOUT→cooldown and quick still routes sonnet; retry later or
  rule an alternate id). **Found + fixed 2026-07-12 evening — the Windows
  CLI-shim spawn defect:** the coordinator's spawn of the OPENAI rows failed
  on Windows (`[WinError 2]`, sessions 002/005 — bare `opencode` resolves as
  a `.cmd` shim for `shutil.which` but not for CreateProcess), so that run's
  REVIEW-A silently ran same-family; `run_session` now which-resolves
  `argv[0]` on Windows and the terra spawn is live-verified green (the fix's
  WI row + spec are the record; session entry in [log.md](log.md)).
  **Watch the next unattended run's index**: REVIEW-A should route
  `gpt-5.6-terra` with no ERROR row — that closes the fix's last done-when.
- **Open items:**
  - **Needs \<human> (the owner queue — human-only calls; under the declared
    `single-ratify` gate authority the loop does NOT pause on these — it
    continues independent backlog work per Next action and pages only when
    nothing actionable remains):**
    1. **Push decision** — `MultiRepoSupport` is local-only (~48 commits); the
       `derived-gate-model` branch adds the derived-gate campaign on top.
    2. **G3 re-attestation** — the derived-gate campaign added **SR-049** (derived
       gate from artifact states; a new Verified `Test` SR) to the ratified spine,
       and the meta's `docs/gate` is now the **derived** G3. The mechanized bar is
       met (derived gate reads G3; all-mechanized: 46 Test · 2 Analysis · 1
       Inspection · 0 Attest); the owner's attested sign-off over the SR-049 spine
       cut + the gate-model change is outstanding. See [log.md](log.md).
       *(The **whole phase-v2 spine cut** — SR-050 Verified 2026-07-12 by the
       process-view slice, **SR-051 Verified 2026-07-13 by the tiered
       drill-down views**, taking v2 → G3 — bundles into the same sitting.)*
    3. **Single-ratify enablement review (the single attest)** — moving
       `docs/gate-policy` from `attended` to `single-ratify` (the unattended
       layer's gate authority) is, by the policy file's own rule, a change whose
       landing commit *is* the reviewed commit the owner accepts. Review that
       enablement commit; until then [gate-policy.md](gate-policy.md) stands
       DRAFT. (Config only — it governs WHO makes a ratifying commit, not what
       the derived gate computes.)
    4. **v2 batch ratification (due — the `[v2]-[g2]` close landed 2026-07-12;
       both v2 dev slices have since shipped and Verified their SRs, so the whole
       v2 arc through G3 is now one sitting)** — SR-050/SR-051
       were ratified `Draft`→`Planned` by the G1 LLM-gate review, decomposed
       (LLR-051/052 + TC-051/052) by the G2 batch, and then Verified by the two
       dev slices, with **provisional rulings** the owner accepts or amends at
       the single sitting: the tiered-drill-down slice's four open questions —
       now **implemented as
       ruled** (tier composition Phase ⊃ Workstream ⊃ WI with Campaign kept as the
       bottom-tier campaign container; grouping-primary phase encoding + per-phase
       color accent; in-place `<details>`-style expand, no zoom navigation; the
       > 3 rule governs start-collapsed with `TOP_VIEW_MAX = 10` unchanged) — and
       the process view's generated-first render mode (Test TC; Critique only on a
       static fallback). Verdicts + rationale: [log.md](log.md).
    5. **Review-cadence proposal (owner-raised 2026-07-12 evening, ruling
       pending — queued as a decision record, the loop does not act on it):**
       **WI-123** ([specs/WI-123.md](specs/WI-123.md)) — campaign-close 2×
       adversarial review cadence instead of per-slice. Recorded
       recommendation: rule only after ≥ 2 campaigns of medium-BUILD evidence
       (per-slice reviews are the escalation sensor the BUILD-tier relax above
       leans on). *(Its sibling proposal — the smoke-tier commit bar — was
       owner-directed and **implemented 2026-07-13**; the commit bar is now
       `pytest -q -n auto -m smoke`, full suite at close — see the Bar line
       above and log.md.)* *(The other sibling — per-WI routing hints — was
       likewise **implemented 2026-07-13**: an optional `BuildTier` column on
       `work-items.csv` plus a driver-maintained `docs/next-wi` the managed
       coordinator reads to set a BUILD session's starting tier, with
       tier-up-never-down still winning after the pin; the proposed
       plan-required flag folded into `SpecRef` semantics rather than a new
       column — see PROCESS_OPTIONS "Unattended operation" and log.md.)*
    *(Earlier items 3–5 resolved 2026-07-12 — the WI-DAG soft-edge sweep,
    the already-made sibling-repo ruling, and the guardrails-batch review;
    see [log.md](log.md). The 2026-07-12 deep-review items are ruled and filed
    as backlog WI-080…082 below.)*
  - **External follow-up (tracked upstream, not this repo's work):** the
    guardrails content enrichment (`JUDGMENT.md` playbook + CONTEXT-class rules
    + the `Verified:` greppable claim vocabulary) is **owner-ruled to live in
    `TheColliny/FableClaudeMDForOpus`** and pulled downstream via the vendoring
    layer (`check_vendored.py`); nothing to build in this kit repo. Rationale:
    [archive/INTEGRATION_PLAN.md](archive/INTEGRATION_PLAN.md) Phase 2.
  - **Phase v2 — COMPLETE (2026-07-13, at G3).** Both dev slices shipped: the
    process-view slice (the Process tab, SR-050 Verified 2026-07-12) and the
    tiered drill-down views (SR-051 Verified 2026-07-13); the pre-dev batch
    (`[v2]-[g1]` + `[v2]-[g2]`) closed 2026-07-12. The derived gate now reads a
    uniform G3; the whole v2 spine cut rides the owner sitting above. (All four 2026-07-11 batches are
    **closed and archived**: the campaign-binning · parallel-tests · resume-hardening
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
    Every spine-toucher bundles into the one pending G3 re-attestation above.)
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
      lands first — as does the second review's M8 (index-dict the quadratic
      report joins; [repo-review-2026-07-12b.md](repo-review-2026-07-12b.md)).
      Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §3
      M1/L3.
    - **WI-082** — decompose `bootstrap.py:main()` (~390 lines). Owner-ruled
      2026-07-12: left deferred **indefinitely** — milder (honest sequential
      scaffolding), lowest urgency of the three. Spec:
      [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md) §3
      M5.
    - **WI-108** — flaky `test_hook_honors_kit_scripts_dir_override` under max
      parallel + coverage: a subprocess-heavy hook-integration test that failed 1×
      in 8 full-suite gate runs and was **unreproducible** in 6 targeted re-runs
      (incl. oversubscription) — the derived-gate feature is not implicated (its
      own tests are deterministic). Deferred until it recurs often enough to
      reproduce (and therefore verify a fix against); the candidate hardening
      (xdist `loadgroup` grouping of the hook tests) is recorded, not applied
      blind. Spec: [specs/WI-108.md](specs/WI-108.md).
    - **WI-110** — effort-level selection for agent sessions (owner-filed
      2026-07-12 at the cross-provider sitting): the static
      `CLAUDE_CODE_EFFORT_LEVEL=high` pin landed; deferred are the `xhigh`
      ("very high") live experiment, a per-phase `AGENT_EFFORT_MAP` sibling of
      the tier map, and computed selection (evidence-gated — see the un-defer
      triggers). Spec: [specs/WI-110.md](specs/WI-110.md).
    - _(The derived-gate campaign landed 2026-07-12; its one open item is the
      owner G3 re-attestation, in **Needs \<human>** above.)_
  - **Queued (deep-review-b remediation, filed 2026-07-12 — awaiting owner
    triage/sequencing; findings + risk notes:
    [repo-review-2026-07-12b.md](repo-review-2026-07-12b.md)):**
    - **WI-097** — LICENSE decision + file (**needs the owner**: which license,
      and whether the kit is headed public; the report's H3).
    - **WI-098** — thin history-provenance comments in the kit masters (H4;
      the strip-at-scaffold precedent shipped 2026-07-13, so this masters-comment
      question now stands on its own — and could absorb the design-doc citations
      `AGENT_ROLES`/`IMPROVEMENT_PLAN` the scaffold-strip left in scope).
    - **WI-103** — PROCESS_OPTIONS byte budget + applies-when index table (M5;
      any doc *split* additionally needs an owner taste ruling — so this one is
      owner-taste-gated, not an autonomous cheap pick). *(The M1 rule-set-sync
      meta test, the M2 off-root loud-fail guard, the M3 Status-casing rule
      (unified case-insensitive + stated once in §4), and the M4/L7
      gen_trajectory hygiene — one module-level `esc` + a `<title>` tooltip on
      every SVG node — all landed 2026-07-13; records in log.md + registry
      Deliverables.)*
    - _(Not filed, deliberately: L5 commit-subject length — accept, or it needs
      a commit-msg check to be a backed rule; L6 template-cell manuals — an
      owner taste ruling on a deliberate design, medium churn to shipped
      templates; M8/L3 fold into WI-081/WI-080 as noted above.)_
- **Next action — Needs <human> (branch `derived-gate-model`; `docs/next-wi` =
  WI-123).** Rule the queued review-cadence proposal in
  [specs/WI-123.md](specs/WI-123.md): accept its evidence-gated deferral,
  adapt it, or authorize implementation. No autonomous queued WI remains
  (WI-097/098/103 each needs an owner ruling). The coordinator
  must stop in `NEEDS-HUMAN` until this decision creates actionable scope.
  1. **Derived-gate campaign — LANDED (this branch).** The design
     ([specs/derived-gate-model.md](specs/derived-gate-model.md)) is ratified and
     the whole 8-slice campaign has shipped: the `Draft` artifact state + trace
     exemption, SN section-as-state maturity, `scripts/derive_gate.py` (the gate
     computed from artifact states + cached to `docs/gate` with a `--check` rot
     guard), `check.py` consuming the derived gate (the `derived-gate` freshness
     step + pre-commit floor), the `[phase]-[g*]` archetype + phase-drop detector,
     the ratification workflow (`gate-advance` skill + `gate-policy`; ratification
     = a reviewed `Status`-change commit), the process-doc rewrite (PROCESS_OPTIONS
     "Derived gate model" + PROCESS.md §4/§7, **+785 B flagged**, baseline 59,638),
     and the migration + dogfood (the meta's own `docs/gate` is now the **derived**
     G3; `derive_gate --check` full-basis-passes). The **one open item** is the
     owner **G3 re-attestation** over the SR-049 spine cut (Needs \<human> above).
     Phase v3+ now uses the derived gate: draft new SN/SR in the live spine, and
     the derived gate follows.
     *(The unattended-enablement step landed 2026-07-12 — the managed-routing
     consent layer + `single-ratify` gate authority; see the Unattended-layer
     bullet under Current State and its single-attest item in Needs \<human>.)*
  2. **Phase v2 dev slices — BOTH DONE (v2 at G3).** The process-view slice
     closed 2026-07-12 (the Process tab, `process_panel()` per LLR-051, TC-051's
     7 nodes, SR-050 `Verified`, seam IF-052). The **tiered drill-down slice
     closed 2026-07-13**: `when_view()`/`_wi_phases()` + the shared
     `_campboxes`/`_wi_row`/`_wi_table` helpers give the When roadmap a
     phase ⊃ workstream ⊃ WI hierarchy (collapse at > 3 local members, campaign
     bottom tier, per-phase color accent, per-tier aggregated edges) and the
     How-SW view an expand-at-≤3/collapse-at->3 top view; LLR-052 `Implemented`,
     TC-052 `Verified` (9 pinned nodes), **SR-051 `Verified`**. The close
     regenerated the gate (v2 → G3) and passed `check.py --gate G3 --phase v1,v2`
     (14/14). Spec archived under `docs/archive/specs/` (path in the WI row's
     Deliverable). The v2 spine cut rides the owner single-ratify sitting above.
   3. **The rest of the backlog needs no new SR — proceed at G3 after the owner
      ruling above.** The dev-toolchain pin, the coverage-plumbing hardening, the
     **dupes-gate + census** (the M2/M6 census wired as `docs/stack.ini`
     `[step:dupes]` over the `docs/dupes-allow` allowlist — new copy-paste
     between an unlisted file-pair now fails G3), the **scaffold-strip of the
     archive-anchor review citations** (`bootstrap.strip_provenance` drops the
     `(REVIEW_*/THREAD_*)` provenance from scripts as it copies them, so a
     downstream reader inherits no dangling `docs/archive/` pointer — deep-review
     M7), the **M1 rule-set-sync meta test** (`tests/test_rule_sync.py` pins
     `trace.LLR_EXEMPT`/`derive_gate.LLR_EXEMPT` and the `is_draft`/`sn_draft_ids`
     *policy* predicates equal, so the orphan report and the derived gate can't
     silently disagree — trace.py's inline exempt literal became a named constant),
     the **M2 off-root loud-fail guard** (`check.py`'s `main()` now
     refuses to run when no `docs/` dir sits at CWD, so its CWD-relative gate/
     profile/arch reads can't silently fall back to the built-in commands + gate
     `all`; the loud-fail option over a new inherited `--root`+chdir flag), and
     the **M3 Status-casing rule** (`is_verified()` now mirrors `is_draft()` —
     both magic Status values matched case-insensitively, the non-breaking
     unification — pinned equal across trace.py/derive_gate.py by
     `test_rule_sync`, with the one rule stated once in PROCESS.md §4), and the
     **M4/L7 gen_trajectory hygiene** (the 7 duplicated per-function `esc`
     closures collapsed to one module-level `esc`, and a `<title>` hover/a11y
     tooltip added to every SVG node across all four view emitters)
     all landed 2026-07-13 (records in log.md + registry Deliverables).
      **`main-decomposition` (WI-080 → WI-081) is the highest-value next step but
      is sequenced *behind the owner sitting*** (highest-risk, behavior-preserving,
      test-seams-first). WI-103 (PROCESS_OPTIONS
     byte budget + applies-when index) is owner-taste-gated (its doc split needs
     a ruling); WI-097/098 are owner-gated; the owner's triage/sequencing is
     welcome but does not block the cheap picks.
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
