+++
id = "WI-888"
title = "A review's finding line is one whose bracket names a declared severity, not any bracketed word"
workstream = "process"
sr_refs = ["SR-154"]
specref = "project-trajectory/scripts/score_reviews.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-10 from WI-880's full-lane gate
(`docs/reviews/wi-880/004-REVIEW-A-fd55051.md`). `score_reviews.FINDING_RE`
matches `- [<any letters>] ...`, so the reviewer's coverage line
`- [run] lines: ...` parsed as a finding of severity `RUN`.
`review_brief.py file` then refused the review (its VERDICT line said
findings=3; the parser counted 4). The coordinator backticked the line to
file the round, recorded in the lane's commit.

The same parser feeds every reader of a review's findings, so the count is
wrong wherever a verdict carries a bracketed word at a bullet's start:
`review_brief.py` (the filing check), `plan_coverage.py` (F1..Fn numbering
for the coverage gate, which shifts every later finding's id),
`agent_loop.py`, `integrate.py`, `gen_verdict_rollup.py` and the scores.
The reviewer template's finding grammar names the severities
(BLOCKER, MAJOR, MINOR).

Landing order: one deliverable, one lane. The parser is the one owning
boundary; its readers change only if one depends on the open grammar.

## Done-when

- A finding line is one whose bracket names a declared severity, from one
  home that the reviewer template's grammar and the parser both read; any
  other bracketed word at a bullet's start is prose.
- Every reader listed above reads findings through that parser alone
  (grep at the tip, recorded).
- Tests, red first: a verdict with a `- [run] ...` coverage bullet and three
  findings files with findings=3, numbers F1..F3 in `plan_coverage`, and
  scores three findings.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script
  changes).
