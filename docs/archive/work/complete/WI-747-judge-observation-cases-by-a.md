+++
id = "WI-747"
title = "Judge an observation case against a rubric, and re-judge it by a declared trigger no faster than every N work items"
workstream = "process"
specref = ""
sr_refs = ["SR-215"]
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Deliverable

An observation case is judged against a numbered rubric written before its first
judgement, and re-judged by a declared trigger no faster than every N closed work
items:

- **Cadence** (`observation_cadence.py`, LLR-293): counts distinct terminal archived
  WI ids added since the latest observation record, at the checkpoint revision;
  the floor is the greater of `[checks] observation_min_work_items` (default 10)
  and a case's `min_work_items`. `files:`, `component:`, `release` and
  `stage-gate` triggers fire only past the floor; an undeclared trigger keeps the
  input-digest rule; first judgement and expiry bypass the floor.
- **Checkpoints:** `intake.py rejudge --checkpoint` accepts `release` and
  `stage-gate` (fix round 1: the stage-gate trigger had no production caller);
  `rejudge.checkpoint_for` maps a case's trigger to its checkpoint.
- **Rubrics:** five numbered rubrics under `docs/rubrics/`; every observation row
  references one; `check_trajectory` warns on an omission (LLR-294).
- **Bound:** SR-215 and LLR-254 amended (adjudication at merge); LLR-293/294,
  TC-306/307 added Drafted for first approval; TC-279 trimmed to its rubric and
  DA-011 with `trigger = "release"`. PROCESS.md +1,450 bytes (94,466).
- **Reviews:** Sonnet 5.5, NOT YET SOUND at dfe92989 (the stage-gate caller);
  SOUND at d4f991a0 with four minors, three folded in at the landing, LLR-255 left
  as is on the reviewer's recommendation. The coordinator kept SR-215's
  requirement cell free of the command (ruling R2) and tagged `checkpoint_for`
  LLR-254.

## Context

Filed 2026-10-02 at the owner's direction (from WI-667's ruling): "it's critical
that judgement is not occurring from an LLM too frequently, both due to speed,
cost, and the non-determinate nature."

Today `rejudge.py` (SR-215, LLR-254) makes an observation case due at every
work-item merge whose commit changes any declared input, when its result expires
(`max_age`), or when it has none. The case's `tier` is not consulted. Measured over
September 2026 (about 236 work-item commits):

- TC-279 declares all of `project-trajectory/scripts` and both requirement
  registries, so it would be due after nearly every merge;
- TC-055 declares `gen_trajectory.py` and `rendering/` (10 commits; re-judged
  three times so far);
- TC-209, TC-210, TC-211 and TC-279 share `docs/test/inspection-procedures.md`,
  so one edit to it makes all four due, and recording one case's result in that
  file stales its siblings (WI-688's fold).

Only one open re-judge row per case keeps them from piling up; each close is
followed by a new row at the next qualifying merge.

## The owner's direction

1. **A rubric first.** When an observation case is created, a rubric (numbered
   anchors, as `docs/rubrics/` holds) is written before its first judgement, so the
   case can be spot-checked against something fixed rather than an LLM's reading
   alone. TC-055 has one (`dashboard-usability.md`); TC-036, TC-209, TC-210,
   TC-211 and TC-279 follow procedures in `docs/test/inspection-procedures.md`
   and need one each (the procedure stays as the how; the rubric is what counts as
   a pass).
2. **First judgement** as today: a case with no result is judged once.
3. **After that, a declared trigger with a floor.** A case is re-judged no faster
   than once every N work items (a default N in `docs/process.toml`; a case may
   raise it), and only when its declared trigger fires: matching files, a
   component, the release tier, or a stage gate. `max_age` stays as the backstop.
4. A case declaring no trigger keeps today's input-change rule, under the floor,
   so adopters need not migrate.

## Done-when

- The registry carries the trigger and floor cells (and a rubric reference) for an
  observation case; `rejudge.due_cases` honours them, with tests for each trigger
  kind, for the floor (a case is not due again within N work items of its last
  result), and for the undeclared default.
- `check_trajectory` reports an observation case with no rubric reference (a
  warning for existing cases; a creation-time requirement stated in PROCESS.md).
- Rubrics exist for TC-036, TC-209, TC-210, TC-211 and TC-279, and those cases and
  TC-055 declare triggers; TC-279's inputs are trimmed so it no longer covers the
  whole scripts tree.
- SR-215 and LLR-254 (and their TCs) are amended through the artifact adjudication
  route; the rule is stated once in PROCESS.md and linked; a RESYNC entry covers
  the shipped script and template changes.
- The commit bar passes.

Not in scope: per-merge spine-acts adjudication and its minting cadence (the S11
plan's batching question), which are LLM judgements too but of approval acts, not
observation cases.
