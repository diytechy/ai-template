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

## Deliverable

Defined and enforced a marker-line-only `Contracts:` grammar in
`gen_arch_map.module_contracts` — every declared IF-### id must appear on
the line carrying the word `Contracts`; a continuation line OPENING with an
undeclared bare id now raises `ContractsGrammarError` (a hard failure
propagating uncaught through the inventory scan) instead of being silently
dropped. The continuation-grammar alternative was REJECTED on measurement:
eight other modules legitimately re-mention other modules' IF ids in
flush-left prose, so treating continuation ids as declared would
over-declare, and no indentation convention exists to lean on; a later line
may safely RE-mention an already-declared id. dispatch.py's real instance
fixed (IF-015/088/089 all on the marker line), eliminating the two false
"undeclared" strict warnings — verified by a before/after strict diff whose
ONLY change is those two lines disappearing. Two regression tests pin the
defect shape and the safe re-mention shape. No RESYNC entry: gen_arch_map
is the "overwrite freely" kit-owned class.

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
