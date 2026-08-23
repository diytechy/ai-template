> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# DP-001 goal brief — wire the dual-plan decomposition round into the unattended coordinator

**Round:** DP-001 (the WI-190 dogfood run, 2026-07-16). **Owner prompt (verbatim):**
"Please grind through WI-190 here" — whose spec declares the `agent_loop`
wiring an explicit follow-up WI; this round decomposes that follow-up.

**Applies-when trigger (declared at filing):** design-shaping `strong`-tier
scope spanning the S8 coordinator seams (`agent_loop` ↔ `agent_route` ↔ the
prompt-map mechanism) — two or more modules and existing IF seams.

## The goal

The dual-plan decomposition layer (process-options master, "Dual-plan
decomposition") ships as a **manual** protocol: a human dispatches the three
hats (planner / plan-critic / arbiter), runs `plan_coverage.py`, and files the
verdict. The goal is for the **unattended coordinator** (`agent_loop.py`, S8
chassis) to run that round without a human dispatcher, honoring every safeguard
the layer states.

## Clauses (the commensurability targets)

- C1: A queued goal/WI that declares the dual-plan trigger is dispatched by the
  coordinator as a dual-plan round (two planner sessions) instead of a direct
  BUILD session.
- C2: Planner briefs are assembled redacted **by construction** — the goal
  brief + the SR surface + the IF registry, never `status.md`/`log.md`/any
  self-assessment — riding the existing `--prompt-map`/`AGENT_PROMPT_MAP`
  override mechanism with keys for the three hats.
- C3: The two planner sessions route to two different model families via
  `agent_route` where available, applying the reviewers'
  degraded-availability rule (two fresh same-family sessions, recorded) when
  only one family responds.
- C4: `plan_coverage.py` runs after generation and after revision; its report
  is injected into the critique and arbiter prompts; a findings exit (1)
  bounces the plan to its author **once** for mechanical repair before paging.
- C5: The coordinator enforces the hard caps: one cross-critique round, one
  revision each, then the arbiter runs **twice position-swapped**; verdict
  disagreement or cap exhaustion pages the human per `docs/gate-policy`.
- C6: Round artifacts are tracked repo files under `docs/plans/DP-NNN-<slug>/`
  (briefs, plans, revisions, critiques, coverage, verdict), the verdict is
  summarized in `docs/log.md`, and the selected plan's rows are filed as
  queued WIs in `work-items.csv`.
- C7: Sessions inherit the S8 per-session limits and telemetry; the round
  carries a declared total budget whose exhaustion follows the
  `docs/gate-policy` failure semantics.
