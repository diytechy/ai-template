+++
id = "WI-667"
title = "Decide how a red assumption-evidence test case reaches the dispatch census, once the red-TC rung is re-armed"
workstream = "unattended"
specref = "project-trajectory/scripts/census.py"
sr_refs = ["SR-197"]
needs = ["WI-631"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

WI-631 built `census.red_tc_census(..., assumptions=True)`, which counts
assumption-evidence test cases apart from requirement evidence (LLR-231), and
deliberately left it off the dispatch seam: `gap_census` and the intake mint
read only the requirement half, and the docstrings say so. The codex review
wanted it wired; the arbiter ruled wiring now would invent policy no row
states (whether a red premise mints an ordinary gap row or an adjudication
row, and with which brief), and noted the decisive fact: the red-TC rung is
structurally dead in any conformant repository today, because
`_TC_NOT_RED` spans the whole closed Status vocabulary, and re-arming it is
an owner judgement item.

IN SCOPE, once the rung's re-arming is ruled: decide the routing (the row
kind, its brief, and when a red assumption case counts as red: every
requirement citing its assumptions claimed built), draft the requirement or
design row that states it, and wire the assumption half into `gap_census`
and `intake._census_drafts` under that row.

## Done-when

- A row states how a red assumption-evidence case is routed, and it is
  approved through the normal route.
- `gap_census` carries the assumption half under its own prefix, and a test
  shows a red assumption case minting the ruled row kind while the
  requirement half's output is unchanged.
- The commit bar passes.
