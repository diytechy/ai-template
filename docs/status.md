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
  `1=G3;2=G3;3=G3;4=G3`, derived current **phase=4**, cached to [`docs/gate`](gate))
  — **WI-188 (2026-07-16) made *phase* a DERIVED first-class spine property and
  retired the old per-WI grouping** (`Phase` now on SR/LLR/TC — integers or `vN`
  both digit-parse; the current phase is derived = highest ratified; a ratified
  blank/unparseable `Phase` is a `--strict-schema` finding, vacuous-until-armed;
  the dashboard tiers `phase ⊃ workstream ⊃ work-item`). Spine: **SN=25 SR=65
  LLR=67 TC=67** (orphans=0, 0 drafts), 56 seams, 5 components. The full
  `check.py --gate G3 --jobs 0` bar passes as a unit (all 15 steps, coverage 91%).
- **Bar (per commit):** `python -m pytest -q -n auto -m smoke` (~47 s) +
  `python project-trajectory/scripts/check_docs.py --root . --stale`, both green.
  At slice/phase close: the full suite `pytest -q -n auto` (~117 s) and
  `check.py` at the derived gate (now **G3** — all 15 steps including the
  G3-only `lint`, `dupes`, and `--require-verified`, plus the `--strict`
  trajectory step). Keep status.md current regardless: closed WI ids leave, open
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
    - **OI-7** — rule **WI-123** (review cadence); rec: wait for ≥2 phases
      of medium-BUILD evidence.
- **Recently closed** _(detail in [log.md](log.md); the status-repetition rules
  R-B/C/D are retired per WI-180, so history lives in the log, not here):_ the
  **v3 dashboard-ux** effort (SR-052/053/054 Critique, spine rejoined G3); the
  **research-knowledge** effort (ref-integrity + dogfood packs + pack/skill
  libraries — [knowledge index](knowledge/README.md); **WI-158** OKF pack export
  stays deferred); and both **owner-intake** sittings (2026-07-14 / -14b — Codex
  **Sol builds live**, `codex` on PATH 2026-07-15). **WI-159** (Knowledge-tab
  density) stays deferred._
- **parallel-dispatch effort (phase `v4`) — COMPLETE** (2026-07-16;
  [specs/parallel-wi-dispatch.md](specs/parallel-wi-dispatch.md)):_ all eight
  slices A–H shipped and **G3-closed** — SN-025 + SR-057…065 + LLR-058…066 +
  TC-058…066 all **Verified**. `agent-resume --jobs N` now runs the full
  dispatcher/integrator: `schedule.py` frontier + safety classification (A),
  retired `next-wi`/`run-phase` (B), explicit `--wi`/`--train` worker
  assignment with trailer-evidence (C), the `--jobs` dispatcher with atomic
  `refs/llm/reservations/*` + a worktree pool + dynamic refill (D), the
  one-review-cycle traincar model + fork/join (E), the CAS-only atomic
  serialized integrator + durable publish-intent publication (F), the
  fault-injected crash matrix + git-as-authority recovery (G), and telemetry +
  gated downstream migration + the parallel-by-default scaffold flip (H). The
  legacy single-session resume loop is untouched without `--jobs`/`AGENT_JOBS`;
  a downstream repo holds at `--jobs 1` until its soft-edge + SafetyClass
  audits pass (the `downstream-resync` skill). Round-by-round evidence →
  [log.md](log.md)._
- **Deferred backlog** _(first-class `deferred` rows; each carries its reason in
  the registry — read it there, not here):_ **WI-060 · WI-061 · WI-062 ·
  WI-063 · WI-065 · WI-082 · WI-108 · WI-159 · WI-187** in
  [work-items.csv](requirements/work-items.csv). (`main-decomposition` is
  **CLOSED** — WI-080 + WI-081 done, WI-082 deferred indefinitely as planned;
  **WI-064 is CLOSED** — its still-gated AXES residuals live on as WI-187,
  applies-when each in [specs/WI-064.md](specs/WI-064.md) §2.)
- **External follow-up** _(not this repo's work):_ guardrails content enrichment
  is owner-ruled to live in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Next action:** **WI-188 is CLOSED** (2026-07-16, external plan
  `splendid-hopping-pike.md`, evidence in [log.md](log.md)) — *phase* is now a
  **derived** first-class spine property and the old per-WI grouping tag is
  retired: `Phase` on SR/LLR/TC (integers or `vN` digit-parse), the current
  phase derived = highest ratified, a ratified blank/unparseable `Phase` a
  `--strict-schema` finding (vacuous-until-armed), the dashboard tiered `phase ⊃
  workstream ⊃ work-item`, PROCESS_OPTIONS **"Phase cadence"** (the renamed
  cadence section), ADOPTING §6 migration note. Full suite **941p/3s**; `check.py --gate
  G3 --jobs 0` **PASS** (15/15, 91% coverage); **grep-zero** for the retired word over
  the live repo (minus history + `docs/repo-review-2026-07-12b.md`, preserved as a
  review verdict). Follows the same-day **WI-064** (AXES enforceability) and
  **main-decomposition** closes. Open owner
  items (push ruling OI-3, LICENSE OI-4, review cadence OI-7) are unchanged under
  `gate-policy: autonomous`; Codex Sol builds are live. **The owner feedback
  sitting (2026-07-16) filed three queued WIs** — **WI-189** (dashboard
  render-critique screenshot loop, meta-only), **WI-191** (specs act on declared
  interface boundaries), and **WI-190** (dual-plan decomposition protocol,
  predecessor-gated on WI-191) — with the research evidence preserved as the
  [co-planning knowledge pack](knowledge/co-planning.md). The same sitting
  found and filed **WI-192** (defect: the WI-081 trace golden masters are
  Windows-generated — `os.sep` + mojibake — so the golden net fails on POSIX;
  pre-existing at clean HEAD, will surface in CI the moment OI-3 pushes). The
  build frontier is **WI-189 + WI-191 + WI-192** (WI-190 follows WI-191); the
  deferred backlog stays owner-ordered. Grinding
  under single-agent adversarial self-review at gates (a recorded limitation vs a
  provider-heterogeneous reviewer). Round-by-round evidence → [log.md](log.md).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/`); no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
