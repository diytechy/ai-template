+++
id = "WI-567"
title = "Construction-first remedies: the reviewer's finding contract must justify a guard before proposing one"
workstream = "process"
specref = ""
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

## Deliverable

Wired the antidote doctrine into the reviewer's finding contract, warn-first.
`project-trajectory/prompts/reviewer.template.md` now requires, for any remedy
whose concrete change ADDS a check, guard, warn, or invariant, one clause
naming why the defect cannot be made *unrepresentable* instead — a stricter
type, a deleted path, or a single owning boundary — citing the vendored
`antidote` skill rather than restating it (plan §3.1; CLAUDE.md "Dogfood the
philosophy"). It binds the remedy's WORDING, not the verdict: no finding is
refused, downgraded, or blocked for want of the clause (plan §2, "Not a gate").
The MINOR/`for clarity` arm and validation at a genuine trust boundary are
explicitly exempt; the target is only a guard compensating for a *reachable*
bad state the design could have made unreachable.

- `prompts/CATALOG.md` regenerated (`gen_prompt_catalog.py`); the `REVIEWER`
  digest — the join key a session log's `prompt-sha` names — moved
  `5a363cd311c3` → `227c969affa9` (plan §3.2).
- `tests/test_prompts.py` gains `test_the_reviewer_brief_carries_the_construction_first_clause`,
  pinning the clause and its two exemptions in the module's existing
  load-bearing-clause style (plan §3.3).
- **Adjudicator briefs deliberately NOT widened** (plan §3.4). All four
  `adjudicate_brief.py` templates rule typed questions (meaning/clarity, close
  disposition, queue conflict, red-TC cause); none reviews a code diff and
  proposes a guard against a reachable bad state, so the clause does not apply.
  Widening there would be this plan's own named failure mode.
- Baseline recorded for a later re-measure (plan §3.5): 1 of 13 REVIEW-A
  remedies in the 2026-09-01 run was structural; the accretion trace is in the
  log fragment.

Verification: the check.py commit bar passed green (prompt-catalog fresh,
registry-integrity, trajectory clean). pytest is not installed on this box, so
the affected test modules' assertions (`test_prompts.py` new + existing
reviewer bones, the review-session detector regex, the single-machine-line
invariant) were exercised directly by loading the `prompts` module — all pass.
The `format` step SKIPPED (ruff not importable by this interpreter), a
pre-existing env condition, not a regression; the change is prose plus one
test module.

## Context

Filed by the 2026-09-01 supervised-unpause session from its own measured review/rework interplay: 1 structural remedy in 13 REVIEW-A rounds, and a three-guard accretion trace on the successor invariant whose construction alternative nobody proposed. The doctrine already ships (the vendored `antidote` skill, PROCESS.md 3's 0-A-B rule) - this row WIRES it into prompts/reviewer.template.md's finding contract, warn-first, and does not restate it. Read the plan's 2 (what this is NOT) before widening scope.
