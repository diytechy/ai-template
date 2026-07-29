+++
id = "WI-281"
title = "Smoke tier true to its name: re-tier the WI-122 opt-out partition until the commit bar runs <= 60 s wall at -n auto (currently 1088/1378 tests = 79% of the suite, measured 6-8 min on the dev box vs the declared ~3.3), and make the runtime its OWN budget item - declared seconds value + a deterministic membership ratchet that bites (growth-sensor idiom) + a CI wall-clock check; no test deleted, smoke+slow stay a total partition, full suite untouched"
workstream = "quality"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
order = 278
+++

## Deliverable

Integrated from train p0-g3-WI-281-9ae9 @ d8d50e6: WI-281: rework review A — green Windows commit bar + enforce the CI wall-clock budget
