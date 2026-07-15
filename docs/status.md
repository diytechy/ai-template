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
  per-phase `(default)=G3;v2=G3;v3=G2`, cached to [`docs/gate`](gate)). **Phase
  v3 (dashboard-ux) is decomposed to G2** (the `[v3]-[g2]` batch, log.md
  2026-07-14): each v3 SR owns its LLR+TC; the three Critique rows own their
  `docs/rubrics/dashboard-*.md`. **Phase v2 is at G3** (the intake/decision-loop
  panels + decomposition render polish shipped 2026-07-14). v3 stays G2 until the
  last dev slice (**WI-144**) lands. Spine: **SN=24 SR=56 LLR=57 TC=57**
  (orphans=0), 52 seams, 5 components.
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
  - **The phase-v3 g2-close ratification sitting is DUE** — a batched human touch
    *parallel* to the loop, not a stop: `keep_nondependent` keeps run-state
    RUNNING on the non-dependent owner-intake WIs, and a NEEDS-HUMAN park while
    those queued WIs are actionable is a stale end-state `trajectory --strict`
    rejects. WI-144 is `active` but **paused** — its critique budget is exhausted
    (`AGENT_CRITIQUE_MAX=3`; 042/048/052 CHANGES-REQUESTED on SR-052/053/054). The
    sitting rules **OI-12** (the critique disposition: buildable A4/T4 fixes + the
    owner-gated 3 TC-HARDEN / U5 palette taxonomy) and sequences the queued
    campaigns (owner-intake vs research-knowledge); WI-144 then resumes its final
    build round. (The `[v3]-[g2]` *design* batch was already ratified 2026-07-14
    ([log.md](log.md)); this is the g2-close, not a re-ratification.)
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
    - **OI-11** — session-038 REVIEW-A [MAJOR] (containment-arrow vs SR-056);
      rec: accept — a spec-interpretation call the code satisfies, and the 042
      critique did not re-raise it (subsumed by OI-12).
    - **OI-12** — 042 CRITIQUE (7 findings, CHANGES-REQUESTED) vs the
      SR-052/053/054 rubrics; rec: accept — six rubric-meeting fixes are WI-144
      build work; the **U5** anchor + phase-hue de-collision + 3 TC-HARDEN are
      owner-gated (ratify at phase-g2 close). Depth in [open-items.md](open-items.md).
- **Queued (v3 dev slice, owner intake 2026-07-13** —
  [specs/owner-intake-2026-07-13.md](specs/owner-intake-2026-07-13.md)):_ the
  earlier SR-051-rev / SR-055 / SR-056 slices **shipped** ([log.md](log.md)
  2026-07-14; phase v2 at G3). Remaining: **WI-144** (dashboard UI-quality pass +
  the SR-052/053/054 Critique rows — arms SR-047's critique loop, runs the full
  gate bar at close)._
- **Queued (research-knowledge campaign, OI-9 §8** —
  [specs/research-knowledge.md](specs/research-knowledge.md)):_ filed at the
  2026-07-14 ratification — **WI-152** (knowledge home) · **WI-153** (trace.py
  ref integrity + knowledge⇒component coupling) · **WI-154** (process text) ·
  **WI-155** (dogfood packs + the seed prompt→image research WI, `BuildTier=
  strong`) · **WI-156** (kit-provisioned pack library) · **WI-157** (skills
  domains filter); **WI-158** deferred (OKF pack export). The owner sequences
  this campaign at the g2-close sitting; do not auto-start it._
- **Queued (owner intake 2026-07-14** — triage + answers:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)):_
  **WI-151** (throughline pointer).
  Their sitting-gate predecessor is satisfied (the 2026-07-14 sitting closed), so
  these are the loop's **actionable non-dependent backlog** — the loop works them
  in id order (the ratification-package + graceful-pause + weekday-blackout WIs
  shipped 2026-07-14, see [log.md](log.md)) unless the owner reorders
  `docs/next-wi` at the pending g2-close sitting._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** **WI-151** ([next-wi](next-wi)) — run-state **RUNNING**. The
  loop works the remaining actionable owner-intake WI while WI-144 is paused and
  the g2-close sitting is DUE in parallel (Open items above). Shipped work +
  round-by-round evidence → [log.md](log.md) / OI-12, not here.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
