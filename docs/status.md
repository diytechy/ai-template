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
- **v3 dashboard-ux campaign — COMPLETE** (owner intake 2026-07-13). All slices
  shipped; the closing UI-quality slice (SR-052/053/054 Critique) passed the
  owner's manual critique 2026-07-15 and the spine rejoined G3. **WI-159**
  (Knowledge-tab density) stays deferred as the remaining graphic-breakdown
  iteration the owner flagged._
- **Queued (research-knowledge campaign, OI-9 §8** —
  [specs/research-knowledge.md](specs/research-knowledge.md)):_ filed at the
  2026-07-14 ratification; the ref-integrity slice (trace.py Knowledge resolution
  + knowledge⇒component coupling) landed 2026-07-15 ([log.md](log.md)). The
  dogfood packs + first live research pass, pack library, and domain-filtered
  skill library also landed ([knowledge index](knowledge/README.md)). Remaining:
  **WI-158** remains deferred (OKF pack export). The iterative-optimization pack
  and grounded review closed the campaign.
  The owner **greenlit**
  this campaign (2026-07-15) to **follow the off-spine backlog automatically** —
  no stop in between; the DAG now sequences its remaining slices._
- **Queued (owner intake 2026-07-14** — triage + answers:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)):_
  All owner-intake WIs are complete — the loop worked them in id order after the
  2026-07-14 sitting._
- **Queued (owner intake 2026-07-14b** — 4 items, triage + answers:
  [specs/owner-intake-2026-07-14b.md](specs/owner-intake-2026-07-14b.md); item 1
  — the codex-CLI swap + Sol builder preference — was executed at intake as a
  dial turn, Decisions log; its per-phase preference follow-up is complete):_
  The optimization-methodology research is complete. Codex **Sol builds are now live** (`codex` on PATH + logged in
  2026-07-15)._
- **Queued (parallel-dispatch campaign, phase `v4`** —
  [specs/parallel-wi-dispatch.md](specs/parallel-wi-dispatch.md)):_ requirements
  **ratified + decomposed** 2026-07-15 (SN-025 in Core needs; SR-057…065 +
  LLR-058…066 + TC-058…066 Planned), so `v4` sits at **G2** (see Active gate). The
  eight build slices remain, in DAG order: **WI-179** (A: scheduler + safety
  classifier) · **WI-180** (B: de-author status / remove next-wi) · **WI-181**
  (C: worker assignment) · **WI-182** (D: dispatcher + reservations) · **WI-183**
  (E: change-train continuation) · **WI-184** (F: atomic integrator) · **WI-185**
  (G: recovery + fault injection) · **WI-186** (H: telemetry + migration +
  dogfood). Edges wire the §15 DAG (A→{B,C}; D after A,C; E after D; F after B,D;
  G after D,F; H the join). Each slice implements + verifies its SR (→G3) at its
  commit; grinding under `gate-policy: autonomous`._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-159** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** the **parallel-dispatch campaign (phase `v4`)** is the live
  frontier (above), now at **G2** with the spine ratified + decomposed. Next WI is
  **WI-179** (Slice A: `schedule.py` frontier + deterministic ordering + the safety
  classifier + the `Priority`/`Exclusive`/`BlockRef`/`EstTokens`/`SafetyClass`
  schema fields + unit fixtures), building under `gate-policy: autonomous`
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
