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

- **Active gate:** runnable **G1** (derived — `scripts/derive_gate.py`;
  per-phase `(default)=G3;v2=G2;v3=G1`, cached to [`docs/gate`](gate)) —
  **phase v3 (dashboard-ux) is open** (the `[v3]-[g1]` GATE entry, log.md
  2026-07-14) and the SR-051 rev holds v2 at G2 until re-verified. Spine self-adopted:
  **SN=24 SR=56 LLR=52 TC=52** (the 10 SR-no-LLR/no-TC orphans are the
  designed post-g1 window — closed by WI-135's decomposition), 52 seams,
  5 components.
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/campaign close: the full suite `pytest -q -n auto` (~66 s) and
  `check.py --gate G3 --phase v1` (v2 rejoins when its rev re-verifies; v3 at
  its own close).
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
- **Queued (owner intake 2026-07-13** — triage + dedupe + briefs:
  [specs/owner-intake-2026-07-13.md](specs/owner-intake-2026-07-13.md)):_
  **WI-135** `[v3]-[g2]` (dashboard-ux decomposition: LLR+TC per new SR
  **including the three Critique rows** — non-LLR-exempt per SR-047 — the
  `docs/rubrics/dashboard-*.md` rubrics, the LLR-052/TC-052 rev for the
  SR-051 amendment, and the dev-slice definitions; the g1 GATE entry lists
  the soft criteria to concretize) · **WI-136** + **WI-137** (independent
  off-spine `unattended` dev-slices — a natural `;`-batch: live console
  lines · telemetry commit hygiene) · **WI-138** (research track + durable
  knowledge layer, design)._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-064 · WI-065 · WI-080 · WI-081 · WI-082 · WI-108 · WI-110** in
  [work-items.csv](requirements/work-items.csv). The highest-value next step is
  the `main-decomposition` campaign (**WI-080** → **WI-081**), sequenced *behind*
  the owner sitting (highest-risk, test-seams-first, behavior-preserving).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus`, pulled downstream
  via the vendoring layer — nothing to build here.
- **Next action:** **WI-135** (`docs/next-wi`) — the `[v3]-[g2]`
  decomposition batch closing the post-g1 window (LLRs+TCs for
  SR-051rev/052–056, the three rubrics, dev-slice definitions); spine-touching,
  one batch review, and the **owner's single v3 ratification sitting lands at
  its close** (`single-ratify`). Lower-risk alternative if a smaller next step
  is wanted: the off-spine `;`-batch **WI-136;WI-137**. The deferred
  `main-decomposition` campaign (**WI-080→WI-081**) stays the highest-value
  refactor but is parked (`deferred`, not queued). Owner items
  (OI-3/OI-4/OI-7, [open-items.md](open-items.md)) don't block any of these.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
