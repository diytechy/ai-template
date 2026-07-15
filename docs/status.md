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
  - **WI-144 is browser-blocked — being resolved by an OWNER manual critique
    (2026-07-15, in-chat).** The final build round is implemented and mechanized
    (3 TC-HARDEN + residual A4/T4/U4/U3/U1/U5 fixes; [log.md](log.md)); T2 stays
    deferred → **WI-159**. The one step left is the perceptual `Critique` APPROVE
    of the rendered `PROJECT_STATE.html`; sessions 070-073 each re-hit it with no
    browser backend and stopped, so the owner records the critique directly
    instead. On APPROVE, WI-144 closes and the spine rejoins G3; on CHANGES, a
    build round runs. The loop is `docs/pause`-held during this (run-state stays
    RUNNING per OI-13). **WI-144 is not the loop's only work:** the off-spine
    WI-161/163/166 + the WI-162 spec are DAG-actionable (predecessors done, no
    WI-144 dependency), so `autonomous` has real work to resume onto.
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
  this campaign after WI-144 closes; do not auto-start it._
- **Queued (owner intake 2026-07-14** — triage + answers:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)):_
  All owner-intake WIs are complete — the loop worked them in id order after the
  2026-07-14 sitting._
- **Queued (owner intake 2026-07-14b** — 4 items, triage + answers:
  [specs/owner-intake-2026-07-14b.md](specs/owner-intake-2026-07-14b.md); item 1
  — the codex-CLI swap + Sol builder preference — was executed at intake as a
  dial turn, Decisions log):_ **WI-161** (per-phase model preference knob —
  restores Fable-led PLAN while BUILD keeps Sol) · **WI-162** (parallel WI
  dispatch across lanes — design spec, strong) · **WI-163** (per-WI critique
  budget dial: `inf`-until-APPROVE | `block`-on-exhaust) · **WI-164**
  (optimization-methodology research — joins the research-knowledge campaign
  behind WI-152) · **WI-165** (Process-tab circular loops, SR-055 — behind the
  v3 closer) · **WI-166** (`dev-setup.template.cmd` Windows double-click rung —
  the meta shim + codex dev-setup rows already shipped at the intake follow-up,
  log.md). Owner pre-req for Sol builds: install `@openai/codex` + `codex login`
  (`scripts/dev-setup.ps1 -Install` or the new double-click
  `scripts\dev-setup.cmd` offers it)._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-159** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** **the owner's WI-144 rendered critique** (in-chat) — open
  `PROJECT_STATE.html`, judge it against the three `docs/rubrics/dashboard-*.md`
  rubrics, and give APPROVE or the changes seen. run-state is **RUNNING** with the
  loop `docs/pause`-held so the verdict records without racing a session. On
  APPROVE: WI-144 closes, the full gate bar runs, the spine rejoins G3; then
  `docs/pause` is deleted and the loop resumes under `docs/gate-policy`=
  **autonomous** (the DAG-actionable WI-161/163/166/162 backlog, then the
  owner-sequenced research-knowledge campaign). Round-by-round evidence →
  [log.md](log.md), not here.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
