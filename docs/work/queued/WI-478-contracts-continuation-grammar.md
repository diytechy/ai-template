+++
id = "WI-478"
title = "gen_arch_map harvests Contracts: declarations from the marker line only, so continuation-line IF ids report as undeclared (repo review 2026-08-19 M-09)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

`gen_arch_map.py` (~:233-246) harvests IF identifiers only from the exact line
containing `Contracts`, while `dispatch.py:72-77` writes `Contracts:` on one
line and IF-088/IF-089 on continuation lines — so the strict trajectory report
calls two visibly-declared interfaces undeclared. False architecture warnings
dilute the one real error (WI-474's seam) and train readers to discount the
report.

Fix per the review: define and parse an indented continuation grammar, or
enforce all identifiers on the marker line with a lint that REFUSES the
ambiguous form — either way, one declared rule, a multiline regression test,
and a hard failure on ambiguity rather than a silent miss. Adjacent, not the
same defect: OI-42's pending ruling tightens the same module's `implements()`
prose harvester — if both land near each other, share the landing so
`gen_arch_map`'s two parsing rules move once.
