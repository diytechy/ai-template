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

- **Active gate:** **G3** (derived — `scripts/derive_gate.py`; per-phase
  `(default)=G3;v2=G3`, cached to [`docs/gate`](gate)). Spine self-adopted:
  **SN=24 SR=51 LLR=52 TC=52, 0 orphans**, 52 seams, 5 components.
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~66 s) and
  `check.py --gate G3 --phase v1,v2`.
- **Run-state:** [run-state](run-state) holds the declared value (don't
  paraphrase it here); when it reads NEEDS-HUMAN its `ask:` line is the
  canonical one-line summary the stop banner headlines.

- **Open items** _(one bullet per item; `OI-N` ids are stable and never
  renumbered):_
  - **Needs \<human>** — the owner ratification sitting (items bundle into one
    sitting; under `single-ratify` the loop does **not** pause on these). Depth
    per item — blast radius, options, recommendation — in
    [open-items.md](open-items.md):
    - **OI-1** — attest the **SR-049** spine cut + the **v2 batch**
      (SR-050 / SR-051 → G3); rec: review the provisional verdicts, attest at
      one sitting.
    - **OI-2** — review the **single-ratify enablement** commit; until then
      [gate-policy.md](gate-policy.md) stands DRAFT.
    - **OI-3** — **push decision**; rec: private remote now.
    - **OI-4** — rule **WI-097** (LICENSE + public/private intent); no rec —
      needs the owner's intent.
    - **OI-5** — rule **WI-098** (masters provenance comments); rec: thin.
    - **OI-6** — rule **WI-103** (PROCESS_OPTIONS budget + index); rec: budget
      + index, defer the split.
    - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 campaigns
      of medium-BUILD evidence.
  - **In flight** _(driver; no approval needed):_ none — the open-items-surface
    campaign closed 2026-07-13 (this surface + its shipped template + the
    warn-tier `check_docs` lint; record in [log.md](log.md)).
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-110** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus`, pulled downstream
  via the vendoring layer — nothing to build here.
- **Next action:** the loop parks in **NEEDS-HUMAN** — when the owner rules
  OI-1…7 ([open-items.md](open-items.md)), that ruling creates the next
  actionable scope; until then there is no autonomous BUILD to route.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
