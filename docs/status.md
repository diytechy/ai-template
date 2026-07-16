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

- **Active gate:** runnable **G2** (derived — `scripts/derive_gate.py`; per-phase
  `(default)=G3;v2=G3;v3=G3;v4=G2`, cached to [`docs/gate`](gate)) — the ratified
  spine stays at **G3**; the **`v4` parallel-dispatch phase is at G2** (requirements
  ratified + decomposed 2026-07-15: SN-025 in Core needs, SR-057…065 + LLR-058…066
  + TC-058…066 Planned), so the min-aggregated runnable gate is **G2** until the
  build slices implement and verify their SRs (→G3). Spine: **SN=25 SR=65 LLR=66
  TC=66** (orphans=0, 0 drafts), 52 seams, 5 components. The v3 dashboard-ux
  campaign closed at G3 (SR-052/053/054 Verified via the owner's manual critique,
  [reviews/074-CRITIQUE.md](reviews/074-CRITIQUE.md)).
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~72 s) and
  `check.py` at the derived gate (now **G2** — the `--strict` trajectory step is
  live (R-B…R-E gate: open WIs named, no done id, SpecRefs resolve), while the
  G3-only `lint`, `dupes`, and `--require-verified` steps arrive when v4 reaches
  G3; R-A (Deliverable non-empty iff done) stays the
  always-on floor). Keep status.md current regardless: closed WI ids leave, open
  ones are named.
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
- **Recently closed** _(detail in [log.md](log.md); the status-repetition rules
  R-B/C/D are retired per WI-180, so history lives in the log, not here):_ the
  **v3 dashboard-ux** campaign (SR-052/053/054 Critique, spine rejoined G3); the
  **research-knowledge** campaign (ref-integrity + dogfood packs + pack/skill
  libraries — [knowledge index](knowledge/README.md); **WI-158** OKF pack export
  stays deferred); and both **owner-intake** sittings (2026-07-14 / -14b — Codex
  **Sol builds live**, `codex` on PATH 2026-07-15). **WI-159** (Knowledge-tab
  density) stays deferred._
- **Queued (parallel-dispatch campaign, phase `v4`** —
  [specs/parallel-wi-dispatch.md](specs/parallel-wi-dispatch.md)):_ requirements
  **ratified + decomposed** 2026-07-15 (SN-025 in Core needs; SR-057…065 +
  LLR-058…066 + TC-058…066 Planned), so `v4` sits at **G2** (see Active gate).
  **Slices A + B shipped:** A = `scripts/schedule.py` (SR-057/058 **Verified**);
  B (WI-180) = retired `docs/next-wi` + `docs/run-phase` and every live dependency
  + the generated-root-status **contract** (owner ruled "full literal B",
  [log.md](log.md) 2026-07-16). **SR-059/LLR-060/TC-060 stay Planned** — the
  *generation* half (integrator-generated `status.md`, dispatcher-derived
  `run-state`, "only on the integration branch") lands with Slices D/F and
  verifies then. Interim: the coordinator's phase is now in-process, so the
  managed loop routes within a run but its cross-crash persistence + per-WI
  BuildTier pin return with C/D. Remaining build slices, in DAG order: **WI-181**
  (C: worker assignment) · **WI-182** (D: dispatcher + reservations) · **WI-183**
  (E: change-train continuation) · **WI-184** (F: atomic integrator) · **WI-185**
  (G: recovery + fault injection) · **WI-186** (H: telemetry + migration +
  dogfood). Edges wire the §15 DAG (C after A; D after A,C; E after D; F after
  B,D; G after D,F; H the join). Grinding under `gate-policy: autonomous`._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-159** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** the **parallel-dispatch campaign (phase `v4`)** is the live
  frontier (above), at **G2** with **Slices A + B shipped**. Next WI is **WI-181**
  (Slice C: worker assignment — explicit `--wi/--train/worktree`, collision-safe
  logs/reviews, legacy `--track` deprecation window), unblocked after A; then
  **WI-182** (D: the dispatcher) after C. Grinding under `gate-policy: autonomous`
  (single-agent adversarial self-review at gates, recorded as a limitation vs a
  provider-heterogeneous reviewer). Deferred main-decomposition
  (**WI-080**→**WI-081**) stays parked pending deliberate owner ordering; Codex
  Sol builds are live.
  Round-by-round evidence → [log.md](log.md), not here.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
