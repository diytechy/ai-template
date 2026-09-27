+++
id = "WI-668"
title = "Make the shipped worker brief adopter-true: cite no meta-repo record in the sent body, point the close bar at its one home, and settle the skill's residual full-suite order"
workstream = "process"
specref = "project-trajectory/prompts/worker.template.md"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Restructured into WI-615.

## Context

Minted by hand at WI-602's integration from its `## Dispositions` draft (the
clean-close spot check of WI-580; the draft's `buildtier = "small"` is outside
the vocabulary and is filed as `quick`).

WI-580's final review round (REVIEW-A 012, APPROVE with four MINORs) named
three defects in kit-shipped prose and the row closed with them standing; WI-602
re-verified all three at the tip. (1) The SENT body of `worker.template.md`
(what survives `prompts.load`'s comment strip) cites `WI-540`'s sessions
005/006/007, `WI-538` and `LLR-206` - records of THIS repo that an adopter
copying the kit can never read, against `CLAUDE.md`'s "Templates must stay
copy-ready" rule. (2) The same bullet RESTATES the commit bar ("the fast test
tier plus its declared wall-time budget (docs/stack.ini), plus the docs
staleness check") instead of pointing at its home, and the restatement is false
downstream: `project-trajectory/stack.ini.template` declares `[tiers]` and no
`[smoke-budget]` section, so a scaffold's worker is told to run a budget its
repo does not declare. (3) `project-trajectory/skills/session-protocol/SKILL.md`
line 109 (and the byte-identical `.claude/` and `.agents/` copies) still orders
"Run the **full** unfiltered suite ... after a broad script change"
unconditionally - the one clause WI-580's deletion left, and it contradicts the
brief's "Run the full suite as well only if it demonstrably fits inside one
turn; NEVER end a turn waiting on one".

IN SCOPE - move the measured evidence (the WI-540 stall, the WI-538 stale
brief) into the template's `<!-- -->` header, where the kit already keeps its
own history, leaving the sent body with the rule and its reason in adopter-
neutral words; replace the bar restatement with a pointer to the step table
and `docs/stack.ini`'s `[tiers]` (the two homes that exist in every scaffold);
qualify or delete the skill's "after a broad script change" order so it agrees
with the brief, in all three copies (`tests/test_dogfood_sync.py` polices the
fan-out). Regenerate `prompts/CATALOG.md`; the rendered-prompt assertions in
`tests/test_agent_loop_worker.py` must keep passing or be re-aimed at the new
wording in the same diff.

NOT IN SCOPE - the close-bar doctrine itself (settled by the owner 2026-09-05,
`docs/handoff-2026-09-04.md`), the rung gating of `tests+coverage` in
`check.py`, and the fourth MINOR (the byte-budget-guard "parked at their caps"
sentence), which is this repo's own skill and a one-line fix for whoever next
edits it.

## Done-when

- `prompts.load("WORKER")`'s sent body cites no id of this repository's own
  records; the evidence moved to the template's comment header.
- The close-bar bullet points at the step table and `docs/stack.ini` `[tiers]`
  instead of restating the bar, and every scaffold declares what it names.
- The session-protocol skill's full-suite order agrees with the brief, in all
  three copies; `prompts/CATALOG.md` is regenerated; the commit bar passes.
