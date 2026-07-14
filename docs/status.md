# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is **forward-only**:
only what must happen **next** lives here. Everything backward-looking has a
home elsewhere — don't restate it here:

- **What shipped / verdicts / session record:** [log.md](log.md).
- **Owner decision briefs:** [open-items.md](open-items.md) — one `## OI-N`
  section per pending decision (blast radius, options, recommendation); a
  ruling appends to the log's Decisions and the section is removed.
- **The WI registry (every backlog + deferred item, with its reason):**
  [work-items.csv](requirements/work-items.csv) — the dashboard is the root
  [`PROJECT_STATE.html`](../PROJECT_STATE.html).
- **Design history:** [archive/](archive/README.md).
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) (this repo has
  no scaffolded `docs/process.md`; the masters are the reference).
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Active gate:** runnable **G2** (derived — `scripts/derive_gate.py`;
  per-phase `(default)=G3;v2=G3;v3=G2`, cached to [`docs/gate`](gate)) —
  **phase v3 (dashboard-ux) is decomposed to G2** (the `[v3]-[g2]` batch,
  log.md 2026-07-14): each v3 SR owns its LLR+TC, the three Critique rows own
  their `docs/rubrics/dashboard-*.md` rubrics. **Phase v2 is at G3**
  (SR-051/LLR-052/TC-052 Verified); the intake/human-decision loop panels shipped
  2026-07-14 (SR-055/LLR-056/TC-056 Verified) and the decomposition render polish
  shipped 2026-07-14 (SR-056/LLR-057/TC-057 Verified — right-sized columns,
  explicit containment arrows, persistent hover). v3 stays G2 until the remaining
  dev slice (WI-144) lands. Spine self-adopted:
  **SN=24 SR=56 LLR=57 TC=57** (orphans=0 — the post-g1 window is closed),
  52 seams, 5 components.
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~72 s) and
  `check.py` at the derived gate (now **G2**; its `trajectory` step gains
  `--strict`, so status.md must stay current — closed WI ids leave, open ones are
  named). The whole spine rejoins `--gate G3` when the remaining v3 dev slice
  (WI-144) re-verifies.
- **Run-state:** [run-state](run-state) holds the declared value (don't
  paraphrase it here); when it reads NEEDS-HUMAN its `ask:` line is the
  canonical one-line summary the stop banner headlines.

- **Open items** _(one bullet per item; `OI-N` ids are stable and never
  renumbered):_
  - **Needs \<human>** _(ratification history — including the 2026-07-14 sitting
    that ratified the `[v3]-[g2]` batch and the research-knowledge spec — lives
    in [log.md](log.md) Decisions; under `single-ratify` the loop does **not**
    pause on the items below. Depth per item in
    [open-items.md](open-items.md):_
    - **OI-3** — **push decision** (git-checked: `origin` exists, this branch
      tracked, ~10 unpushed commits — not "48 local-only"); rec: push.
    - **OI-4** — rule **WI-097** (LICENSE + public/private intent); no rec —
      needs the owner's intent.
    - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 campaigns
      of medium-BUILD evidence.
    - **OI-11** — disposition the **session-038 REVIEW-A** [MAJOR] (the
      decomposition containment-arrow reading against SR-056); verified a
      spec-interpretation call (the layer-swap drill renders one containment edge
      per descendable block, which the code satisfies); rec: accept — the fresh
      042 critique did **not** re-raise arrow legibility. Depth in
      [open-items.md](open-items.md).
    - **OI-12** — disposition the **042 CRITIQUE** (7 findings,
      CHANGES-REQUESTED) against the SR-052/053/054 rubrics; rec: accept the
      contrast/dead-panel/legend/glyph/grouping fixes as WI-144's remaining build
      work (they meet already-ratified rubrics), and ratify the new **U5**
      uniformity anchor + phase-hue palette de-collision + the 3 TC-HARDEN
      change-intake cases at the phase-g2 close. Depth in
      [open-items.md](open-items.md).
- **Queued (v3 dev slices, owner intake 2026-07-13** —
  [specs/owner-intake-2026-07-13.md](specs/owner-intake-2026-07-13.md)):_ **live**,
  running G2→G3 in series. The SR-051-rev interface-wired descend-a-layer render,
  the Process-tab intake + human-decision loop panels (SR-055), and the SR-056
  decomposition render polish (with OI-10 folded) all **shipped** (log.md
  2026-07-14; phase v2 at G3). Remaining:
  **WI-144** (dashboard UI-quality pass + the SR-052/053/054 Critique rows — the
  campaign-closing slice that arms SR-047's critique loop and runs the full gate
  bar at close)._
- **Queued (research-knowledge campaign, OI-9 §8** —
  [specs/research-knowledge.md](specs/research-knowledge.md)):_ filed at the
  2026-07-14 ratification — **WI-152** (knowledge home) · **WI-153** (trace.py
  ref integrity + knowledge⇒component coupling) · **WI-154** (process text) ·
  **WI-155** (dogfood packs + the seed prompt→image research WI, `BuildTier=
  strong`) · **WI-156** (kit-provisioned pack library) · **WI-157** (skills
  domains filter); **WI-158** deferred (OKF pack export). Sequence after the v3
  slices unless the owner reorders `docs/next-wi`._
- **Queued (owner intake 2026-07-14** — triage + answers:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)):_
  **WI-146** (ratification tree view + brief lint) · **WI-147** (graceful
  pause) · **WI-148** (weekday blackout window) · **WI-149** (lowest-gate-first
  advisory) · **WI-150** (planner-assigned BuildTier) · **WI-151** (throughline
  pointer) · **WI-110** re-queued (owner directive: opus BUILD effort → xhigh,
  verified via the iteration-index s/turn telemetry). Their sitting-gate
  predecessor is now satisfied (the sitting closed); sequence after the v3
  slices unless the owner reorders `docs/next-wi`._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus`, pulled downstream
  via the vendoring layer — nothing to build here.
- **Next action:** **WI-144 — dashboard UI-quality pass, build round 1**
  ([next-wi](next-wi)). The fresh provider-heterogeneous **042 CRITIQUE**
  (SR-047's loop, armed for the first time) returned **CHANGES-REQUESTED — 7
  findings** against `PROJECT_STATE.html` vs the SR-052/053/054 rubrics (2
  BLOCKER: a dead When-tab detail panel + sub-4.5:1 label contrast; 4 MAJOR; 1
  MINOR) + 3 TC-HARDEN change-intake proposals — filed as **OI-12**
  ([open-items.md](open-items.md)). Disposition split: the contrast /
  dead-panel / How-legend / status-glyph / knowledge-grouping fixes meet the
  **already-ratified** rubrics (build work, provisional per the OI-8
  amendments-are-future-WIs note); the new **U5** uniformity anchor + phase-hue
  palette de-collision, and the 3 TC-HARDEN cases, are **owner-gated** (a rubric
  amendment + change-intake). WI-144 stays **open** (critique CHANGES-REQUESTED);
  it re-critiques **fresh** after the build round (never self-adjudicated).
  [run-state](run-state) is **RUNNING**. Once WI-144 closes it rejoins the whole
  spine to G3; then the owner-intake WIs (WI-146…151, WI-110) and the
  research-knowledge campaign (WI-152…157). OI-3 (push), OI-4 (LICENSE), OI-7
  (cadence), OI-12 (critique disposition) block nothing under `single-ratify` and
  can be ruled any time. The deferred `main-decomposition` campaign
  (**WI-080→WI-081**) stays parked (`deferred`, not queued).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
