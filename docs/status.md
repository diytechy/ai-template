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
  per-phase `(default)=G3;v2=G2;v3=G2`, cached to [`docs/gate`](gate)) —
  **phase v3 (dashboard-ux) is decomposed to G2** (the `[v3]-[g2]` batch,
  log.md 2026-07-14): each v3 SR owns its LLR+TC, the three Critique rows own
  their `docs/rubrics/dashboard-*.md` rubrics, and the SR-051 rev holds v2 at
  G2 until the WI-141 dev slice re-verifies. Spine self-adopted:
  **SN=24 SR=56 LLR=57 TC=57** (orphans=0 — the post-g1 window is closed),
  52 seams, 5 components.
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~72 s) and
  `check.py` at the derived gate (now **G2**; its `trajectory` step gains
  `--strict`, so status.md must stay current — closed WI ids leave, open ones are
  named). The whole spine rejoins `--gate G3` when the v2/v3 dev slices
  (WI-141→144) re-verify.
- **Run-state:** [run-state](run-state) holds the declared value (don't
  paraphrase it here); when it reads NEEDS-HUMAN its `ask:` line is the
  canonical one-line summary the stop banner headlines.

- **Open items** _(one bullet per item; `OI-N` ids are stable and never
  renumbered):_
  - **Needs \<human>** _(the 2026-07-13 sitting ratified OI-1/OI-2 and ruled
    OI-5/OI-6 — records in [log.md](log.md) Decisions; under `single-ratify`
    the loop does **not** pause on these). Depth per item in
    [open-items.md](open-items.md):_
    - **OI-3** — **push decision** (git-checked: `origin` exists, this branch
      tracked, ~10 unpushed commits — not "48 local-only"); rec: push.
    - **OI-4** — rule **WI-097** (LICENSE + public/private intent); no rec —
      needs the owner's intent.
    - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 campaigns
      of medium-BUILD evidence.
    - **OI-8** — **ratify the `[v3]-[g2]` batch** (single-ratify's one human
      sitting at the phase g2 close): bless the decomposed v3 requirement work —
      SR-052…056's LLR+TC, the three `docs/rubrics/dashboard-*.md` rubrics, and
      the SR-051 rev — then the v3 dev slices run autonomously. Rec: ratify (the
      LLM-gate consistency sweep + green floor are recorded in the g2 GATE entry,
      [log.md](log.md)). Brief: [open-items.md](open-items.md) OI-8.
    - **OI-9** — **ratify the research-track + knowledge-layer design spec**
      ([specs/research-knowledge.md](specs/research-knowledge.md)); its §8
      implementation WIs file on ratification. Rec: ratify — same sitting as
      OI-8. Brief: [open-items.md](open-items.md) OI-9.
- **Queued (owner intake 2026-07-13** — triage + dedupe + briefs:
  [specs/owner-intake-2026-07-13.md](specs/owner-intake-2026-07-13.md)):_ the
  **v3 dev slices** run G2→G3 in series *after* the OI-8 sitting —
  **WI-141** (SR-051-rev interface-wired render + descend-a-layer) →
  **WI-142** (Process tab intake + human-decision loops) →
  **WI-143** (decomposition render polish) →
  **WI-144** (dashboard UI-quality pass + the SR-047 critique). The research
  track's implementation WIs are **not yet filed** — they come from
  [specs/research-knowledge.md](specs/research-knowledge.md) §8 at the OI-9
  ratification._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-110** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus`, pulled downstream
  via the vendoring layer — nothing to build here.
- **Next action:** **the owner sitting — WI-145 (`active`)**: everything left
  to execute is human-gated, so run-state is **NEEDS-HUMAN**. One sitting
  covers **OI-8** (ratify the `[v3]-[g2]` batch; closes WI-145 and unblocks
  the v3 dev slices **WI-141→144**, series G2→G3) and **OI-9** (ratify
  [specs/research-knowledge.md](specs/research-knowledge.md); files its §8
  implementation WIs) — plus the standing OI-3/OI-4/OI-7 rulings if wanted
  (they block nothing). The v3 slices' registry rows carry WI-145 as a hard
  predecessor, so the DAG itself records why the queue is parked. After the
  sitting: mark WI-145 done, flip [run-state](run-state) to RUNNING —
  `docs/next-wi` is pre-pointed at **WI-141**. The deferred
  `main-decomposition` campaign (**WI-080→WI-081**) stays parked (`deferred`,
  not queued).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
