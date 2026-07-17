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
  `1=G3;2=G3;3=G3;4=G3`, derived current **phase=4**, cached to
  [`docs/gate`](gate)). Spine: **SN=25 SR=65 LLR=69 TC=69** (orphans=0,
  0 drafts), 57 seams (IF-057 `Proposed`), 5 components. The full
  `check.py --gate G3 --jobs 0` bar passes as a unit (15/15 steps, coverage
  91.13%).
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/phase close: the full suite `pytest -q -n auto` and `check.py` at the
  derived gate (now **G3** — all 15 steps including the G3-only `lint`, `dupes`,
  and `--require-verified`, plus the `--strict` trajectory step). Keep status.md
  forward-only: closed WI ids leave this file (history is the log's).
- **Run-state:** [run-state](run-state) holds the declared value (don't
  paraphrase it here); when it reads NEEDS-HUMAN its `ask:` line is the
  canonical one-line summary the stop banner headlines.

- **Open items** _(one bullet per item; `OI-N` ids are stable and never
  renumbered; ratification history lives in [log.md](log.md) Decisions;
  `docs/gate-policy` is **`autonomous`** (owner directive 2026-07-15) so the
  loop does **not** pause on these. Depth per item in
  [open-items.md](open-items.md):_
  - **OI-3** — **push decision** (git-checked: `origin` exists, this branch
    tracked, unpushed commits accumulating); rec: push.
  - **OI-4** — rule **WI-097** (LICENSE + public/private intent); no rec —
    needs the owner's intent.
  - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 phases
    of medium-BUILD evidence.
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-065 · WI-082 · WI-097 · WI-108 · WI-123 · WI-158 · WI-159 ·
  WI-187** in [work-items.csv](requirements/work-items.csv) (WI-097/WI-123
  are the OI-4/OI-7 subjects above).
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** the build frontier is **WI-194…WI-199** — the coordinator
  dual-plan wiring decomposition selected by the
  [DP-001 verdict](plans/DP-001-dual-plan-loop-wiring/verdict.md) (WI-199 is
  the integration fan-in; WI-197 ≺ WI-194) — plus **WI-200** (restore the
  status.md forward-only enforcement, parallel-dispatch robust;
  [specs/WI-200.md](specs/WI-200.md)). Owner items OI-3/OI-4/OI-7
  stay open under `gate-policy: autonomous`. Grinding under single-agent
  adversarial self-review at gates (a recorded limitation vs a
  provider-heterogeneous reviewer); session evidence → [log.md](log.md).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
