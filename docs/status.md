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

- **Active gate:** runnable **G3** (derived — `scripts/derive_gate.py`; per-phase
  `(default)=G3;v2=G3;v3=G3`, cached to [`docs/gate`](gate)) — **the whole spine
  is back at G3** (2026-07-15): the v3 dashboard-ux campaign closed when its final
  UI-quality slice passed the **owner's manual critique** APPROVE
  ([reviews/074-CRITIQUE.md](reviews/074-CRITIQUE.md)), moving SR-052/053/054 →
  Verified. Spine: **SN=24 SR=56 LLR=57 TC=57** (orphans=0), 52 seams, 5
  components.
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~72 s) and
  `check.py` at the derived gate (now **G3** — its `trajectory` step runs
  `--strict` and the G3-only `lint` / `dupes` / `--require-verified` steps are
  live, so status.md must stay current: closed WI ids leave, open ones are named).
- **Run-state:** [run-state](run-state) holds the declared value (don't
  paraphrase it here); when it reads NEEDS-HUMAN its `ask:` line is the
  canonical one-line summary the stop banner headlines.

- **Open items** _(one bullet per item; `OI-N` ids are stable and never
  renumbered):_
  - **Needs \<human>** _(ratification history — including the 2026-07-14 sitting
    that ratified the `[v3]-[g2]` batch and the research-knowledge spec — lives
    in [log.md](log.md) Decisions; `docs/gate-policy` is now **`autonomous`**
    (owner directive 2026-07-15) so the loop does **not** pause on the items
    below. Depth per item in [open-items.md](open-items.md):_
    - **OI-3** — **push decision** (git-checked: `origin` exists, this branch
      tracked, ~10 unpushed commits — not "48 local-only"); rec: push.
    - **OI-4** — rule **WI-097** (LICENSE + public/private intent); no rec —
      needs the owner's intent.
    - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 campaigns
      of medium-BUILD evidence.
- **v3 dashboard-ux campaign — COMPLETE** (owner intake 2026-07-13). All slices
  shipped; the closing UI-quality slice (SR-052/053/054 Critique) passed the
  owner's manual critique 2026-07-15 and the spine rejoined G3. A follow-up render
  slice (**WI-165**, Process-tab circular loops) is now unblocked, and **WI-159**
  (Knowledge-tab density) stays deferred — both future graphic-breakdown
  iterations the owner flagged._
- **Queued (research-knowledge campaign, OI-9 §8** —
  [specs/research-knowledge.md](specs/research-knowledge.md)):_ filed at the
  2026-07-14 ratification — **WI-152** (knowledge home) · **WI-153** (trace.py
  ref integrity + knowledge⇒component coupling) · **WI-154** (process text) ·
  **WI-155** (dogfood packs + the seed prompt→image research WI, `BuildTier=
  strong`) · **WI-156** (kit-provisioned pack library) · **WI-157** (skills
  domains filter); **WI-158** deferred (OKF pack export). The owner **greenlit**
  this campaign (2026-07-15) to **follow the off-spine backlog automatically** —
  no stop in between; the DAG sequences it (WI-152 first, its ratification-sitting
  predecessor already done)._
- **Queued (owner intake 2026-07-14** — triage + answers:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)):_
  All owner-intake WIs are complete — the loop worked them in id order after the
  2026-07-14 sitting._
- **Queued (owner intake 2026-07-14b** — 4 items, triage + answers:
  [specs/owner-intake-2026-07-14b.md](specs/owner-intake-2026-07-14b.md); item 1
  — the codex-CLI swap + Sol builder preference — was executed at intake as a
  dial turn, Decisions log; its per-phase preference follow-up is complete):_
  **WI-162** (parallel WI dispatch across lanes — design spec, strong) · **WI-163** (per-WI critique
  budget dial: `inf`-until-APPROVE | `block`-on-exhaust) · **WI-164**
  (optimization-methodology research — joins the research-knowledge campaign
  behind WI-152) · **WI-165** (Process-tab circular loops, SR-055 — **now
  unblocked**, the v3 campaign closed) · **WI-166** (`dev-setup.template.cmd` Windows double-click rung —
  the meta shim + codex dev-setup rows already shipped at the intake follow-up,
  log.md). Codex **Sol builds are now live** (`codex` on PATH + logged in
  2026-07-15)._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-159** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** **the loop resumes under `autonomous`** — the v3 campaign
  closed (spine at G3), so the DAG-actionable off-spine backlog is next:
  **WI-163** (critique-budget dial) → **WI-166** (`dev-setup.template.cmd`) →
  **WI-162** (parallel-dispatch spec) → **WI-165** (Process circular loops) →
  **WI-167** (tripwire path coverage — filed by the 076 design-check, which
  ruled GRIND-THROUGH on the WI-161 review-path tripwire page,
  [reviews/076-DESIGN-CHECK.md](reviews/076-DESIGN-CHECK.md));
  `docs/next-wi` is pointed at **WI-163**.
  The `docs/pause` hold is lifted at this close. **After the backlog the loop
  flows into the research-knowledge campaign** (WI-152…157 + WI-164)
  automatically — the owner greenlit it 2026-07-15; only the deferred
  `main-decomposition` (WI-080→WI-081) stays parked. Codex Sol builds are live.
  Round-by-round evidence → [log.md](log.md), not here.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
