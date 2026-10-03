+++
id = "WI-785"
title = "adjudicate: LLR-243, TC-238 - approved/routed cell(s) amended on merged trunk be6500f..1fda46e (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-243", "TC-238"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held.

- WI-782's adjudicator returned LLR-243 `detail` and TC-238 `method`. It then re-judged and blessed them after the in-lane fix round: see the re-judgement section of `docs/reviews/wi-782-adjudicate-llr-238-llr-240/001-ADJUDICATE-d040ad7.md`, lane commit c042a79c.
- Act seq 25 (lane commit 1b2bbfa4, landed as 1fda46ed) re-attested both rows. Codex Luna's cross-review found it SOUND.
- At this row's mint (cbda7d44), both rows are byte-identical to their `docs/archive/last_approved/` anchors, so no drift is left to judge.

Intake minted this row because its amendment trigger diffs the merged commit without reading the snapshot. That is the re-mint trap in the S11 plan, §4.2 (`docs/plans/2026-10-03-s11-in-lane-adjudication.md`), and its slice 1 removes it. The wave-9 coordinator closed it.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-243 `Detail`: 'release_gate_findings(das, srs, risks) fails each assumption cited by at least one requirement whose standing reads fal…' -> 'release_gate_findings(das, srs, risks) fails each assumption that at least one requirement cites and whose standing rea…'
- TC-238 `Method`: 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule cal…' -> 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule cal…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
