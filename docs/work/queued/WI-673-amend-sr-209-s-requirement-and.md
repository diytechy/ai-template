+++
id = "WI-673"
title = "Amend SR-209's requirement and TC-242 to the loop-lane ownership rule its acceptance now states"
workstream = "requirements"
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-209"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

Found by codex Sol's cross-review of the WI-669 adjudication (arbitration
ruling 11 of `docs/reviews/2026-09-26-wave3/ARBITRATION.md`). SR-209's
acceptance was amended by WI-636 under wave-2 arbitration ruling 4 to the
lane-ownership rule: the merge slot sees commits, not processes, so a lane is
the loop's when its claim or any loop-writer commit in its range carries the
trailer, and every commit of a loop lane is judged, a person's commit there
carrying the trailer or moving to their own lane. WI-669 blessed that
acceptance, which is true of the code. But SR-209's `requirement` sentence
still scopes the rule to "a commit the unattended loop creates", its
rationale draws the actor distinction the proxy replaces, and TC-242's
`method`/`expected` still expect a non-loop process's commit to pass and
state neither the lane-ownership case nor the exemption window, although its
evidence module (`tests/test_loop_provenance.py`) already tests them.

IN SCOPE: amend SR-209's `requirement` and `rationale` to declare the
loop-lane proxy (minimally, consistent with the blessed acceptance and
ruling 4), and TC-242's `method` and `expected` to state the lane-ownership
and exemption-window cases its evidence drives, each in place with status
left Approved; file the amendment adjudication naming exactly SR-209 and
TC-242. No behaviour change.

## Done-when

- SR-209's requirement, rationale and acceptance agree with each other and
  with the built rule; TC-242 states every case its evidence drives.
- An amendment adjudication names SR-209 and TC-242, and the commit bar
  passes.
