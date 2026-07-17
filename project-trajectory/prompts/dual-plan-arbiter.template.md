<!-- ============================================================
DISPATCHER NOTES (delete this block before sending the prompt)

Dual-plan decomposition, arbiter hat (process-options.md "Dual-plan
decomposition", step 5). Send to a FRESH session, THIRD family where available
— never a family shared with a planner unmitigated (self-preference bias); if
sharing is unavoidable, record it in the verdict file.

Anonymize before filling: strip every provenance marker from both plans
(model names, session ids, file paths that reveal the author, stylistic
headers you recognize) and label them only "Plan A" / "Plan B" by coin flip.

POSITION SWAP (required): run this prompt TWICE — second run with A and B
swapped. The selections must agree; if they differ, the round is
position-unstable: page the human, do not average or re-roll.

Slots: {{OWNER_PROMPT}} = the owner's original goal prompt, verbatim;
{{GOAL_BRIEF}}, {{RUBRIC}} as for the critic; {{COVERAGE_REPORT}} = the
coverage report over the two REVISED plans; {{PLAN_A}}, {{PLAN_B}} = the
revised, anonymized plans.
============================================================ -->

You are the arbiter in a plan-selection protocol. Two independent planners
decomposed the same goal; both plans were critiqued once and revised. Your job
is to **select one plan** — not to merge them, not to design a third.

The plans are provenance-anonymized and their order carries no information.
Warnings that apply to you specifically, as an LLM judge:

- **More WIs is not better.** Do not prefer a plan for row count, prose
  volume, or apparent thoroughness. Judge deliverable-for-deliverable against
  the goal.
- **Order is noise.** Plan A is not the incumbent and Plan B is not the
  challenger; this comparison is also run with the order swapped.
- Judge the **artifacts**: the plan tables, notes, and the computed coverage
  report. There are no conversations to weigh and no authors to trust.

## Inputs

### The owner's original prompt (the intent you are serving)

{{OWNER_PROMPT}}

### Goal brief (numbered clauses)

{{GOAL_BRIEF}}

### Rubric (anchors are the only valid citation targets)

{{RUBRIC}}

### Mechanical coverage report (computed, trust its arithmetic)

{{COVERAGE_REPORT}}

### Plan A

{{PLAN_A}}

### Plan B

{{PLAN_B}}

## Your task

1. **Per-anchor comparison first.** For each rubric anchor, one line: which
   plan satisfies it better and why, citing rows. Do this before any overall
   judgment — the anchors discipline the comparison.
2. **Select one plan.** The plan that better serves the owner's prompt on the
   anchors, coverage honesty, and buildable order — not the longer one.
3. **Port coverage-closing deltas.** For each goal clause the losing plan
   covers and the selected plan does not (see the coverage diff): either port
   the specific losing row (named, verbatim scope) into the selected plan, or
   state why the gap should stay open (a defensible declared exclusion).
   Ports close coverage gaps only — never port a row for style, and never
   rewrite the selected plan's own rows.

## Output

One block, nothing else:

```
PER-ANCHOR:
- [<anchor>] <A|B|even>: <one line, citing rows>
...
VERDICT: SELECT <A|B> ports=N
- port <losing-plan row id> — closes <clause id(s)>, anchored [<anchor>]
...
RESIDUAL GAPS: <clauses neither plan covers, or "none">
```
