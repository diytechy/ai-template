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

## Trust

A review file's findings decide two gates: the filing check and the
coverage gate (`project-trajectory/PROCESS.md` §3, "When a guard is owed").
This row changes only how a finding line is recognised. Every carrier and
failure contract below is unchanged.

- **Producers:** a fresh review session writes its verdict file. The
  coordinator files it with `project-trajectory/scripts/review_brief.py
  file` (exclusive create; a refused review writes nothing; a write failing
  part-way can leave a partial file). The loop's REVIEW phase writes its
  session log, which `agent_loop.py` reads back.
- **Consumers** (search: `score_reviews.parse_verdict`, `FINDING_RE`,
  `import score_reviews`, recorded 2026-10-10), each reading findings
  through `score_reviews.parse_verdict`:
  `project-trajectory/scripts/review_brief.py` (the filing check's count),
  `project-trajectory/scripts/plan_coverage.py` (F1..Fn),
  `project-trajectory/scripts/agent_loop.py` (direct, and injected into
  `kitlib/verdict.py`), `project-trajectory/scripts/dispatch.py` and
  `project-trajectory/scripts/integrate.py` (both injected into
  `project-trajectory/scripts/kitlib/verdict.py`'s round readers),
  `project-trajectory/scripts/gen_verdict_rollup.py` and
  `project-trajectory/scripts/score_reviews.py` itself.
  `project-trajectory/scripts/adjudicate_brief.py` has its own grammar and
  does not use this parser.
- **Ruling:** a line counts as a finding only when its bracket names a
  declared severity. Each consumer keeps its current handling of an absent,
  unreadable or partial file, which this row does not change; the lane
  records each reader's handling at its tip, and a reader that would read
  such a file as a verdict is filed as its own row. A bracketed word that is not a severity is prose. It
  never adds a finding, never shifts F1..Fn, and never refuses a filing.
  Findings bind to the verdict file's text at the reviewed sha.

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
