# Rubric — Adversarial code review (WI-241)

**Adjudicates:** the heavyweight, break-it-first review of a single change under
review — the brief structure the 2026-07-18/19 review loop proved (7 of 11
builds shipped defects review caught, nearly every catch tracing to the
behaviors below). The continuous per-commit sweep — the embedded
`REVIEWER_PROMPT`
([agent_loop.py](../../project-trajectory/scripts/agent_loop.py)) — now carries
these clauses inline; this rubric is the fuller brief for a hand-dispatched
strong-tier review, and the standing reference the prompt compresses.
**Used by:** an independent reviewer of one diff (a REVIEW-A/REVIEW-B session,
or an owner-launched deep review) — a fresh context that did **not** write the
code, reading the diff + its requirement surface and **never** the implementer's
self-assessment (a leaked self-assessment collapses review finding-rates
several-fold).

## Anchors

**R1 — Subject framing.** Open by naming what the diff *is*: the behavior it
changes, its blast radius (callers, persisted state, downstream artifacts), and
the requirement it must satisfy (the spec-of-record + the registry rows it
touches). *Bad:* reviewing hunks in isolation with no model of what the change
is for. The frame decides which failure classes matter.

**R2 — Drive the real shipped code paths.** Reproduce, do not assess. Construct
the scenario and run the **actual** function or flow the diff changes, then
observe the result. Primitive probes (poking a git primitive, a library call,
an isolated helper) and plausibility reading are supporting evidence only —
never the basis for a verdict. *Bad:* the WI-230 miss — a live data-loss bug
survived because the reviewer probed git primitives instead of running the
shipped salvage function.

**R3 — Severity-ordered failure classes.** Before hunting, name the worst ways
**THIS** change could fail — silent wrong content, fail-open, data loss,
starvation, off-by-one on a boundary — and hunt those first, worst-first. *Bad:*
sweeping for style while the change's silent-content path goes untested. This is
what caught the WI-231 marker-straddle and CSV-newline silent-content defects.

**R4 — Done-when coverage map.** Map **each** spec Done-when item to the test or
observation that covers it, or mark it **UNCOVERED**. A change that passes its
own tests but leaves a Done-when clause unproven is not done — the
"passes-its-tests, fails-its-requirement" class (the WI-234 live-WI-229 miss and
the WI-236 stride starvation both slipped this way). *Good:* a table, one row per
Done-when item, each pointing at a covering TC or a driven observation.

**R5 — REWORK → consume → re-verdict.** When a review returns
CHANGES-REQUESTED and the next build claims the fix, do not re-read the diff for
plausibility: (1) **re-drive** the original break scenarios against the fixed
code and confirm they now hold; (2) **probe the new seams** the fix introduced —
a fix is itself a change with its own worst failure classes (R3); and (3) where
the fix adds a regression test for the defect, **confirm that test fails on the
pre-fix behavior** (a green that would stay green without the fix proves
nothing). Only then re-issue a verdict.

## Verdict

The reviewer writes its verdict to the review file in the `log.md` block format,
one finding line per issue, then **exactly one** machine line:

```
- [BLOCKER|MAJOR|MINOR] <file:line> -> issue -> the concrete change -> @owner
VERDICT: APPROVE|CHANGES-REQUESTED findings=N
```

**Verdict discipline.** An `APPROVE` must mean you *tried to break it and
failed* — every worst-class hunt (R3) run and survived, every Done-when item
covered (R4). Any UNCOVERED item or un-driven worst class is
`CHANGES-REQUESTED`, not an APPROVE with a caveat. The reviewer records the
verdict and stops; it never edits the code under review.
