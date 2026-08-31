+++
id = "WI-556"
title = "Spine-authoring doctrine: the children-coverage rule stated as trust-based prose (OI-72 ride-along)"
specref = "docs/requirements/open-items.toml#OI-72"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Context

`OI-72`'s ruling closes with a doctrine act the owner sized honestly: the
rule exists nowhere in the repo (searched the rulings, the log and the
process masters, 2026-08-31), and there may be no efficient validation beyond
trust. State it where breakdown authors read; no validator.

## Done-when

The spine-authoring skill (the kit master and this repo's copy, kept in sync
where `tests/test_dogfood_sync.py` covers it) states the rule: an LLR may be
satisfied by its parent's coverage; an SR may be satisfied by its children
only when the children span the SR's full dimensional space and are not
interdependent; otherwise the honest states are a recorded orphan or a direct
TC. Cites `OI-72` as the ruling of record. One commit; byte budgets respected
if the touched doc is capped.
