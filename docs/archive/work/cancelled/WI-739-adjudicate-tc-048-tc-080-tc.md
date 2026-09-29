+++
id = "WI-739"
title = "adjudicate: TC-048, TC-080, TC-150, TC-199 - approved/routed cell(s) amended on merged trunk 205d02c..5dfd78c (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["TC-048", "TC-080", "TC-150", "TC-199"]
+++

## Deliverable

Cancelled: there is nothing in scope to rule. The kit's own amendment
composer refuses the brief: "none of the 4 row(s) this adjudication was
minted over (TC-048, TC-080, TC-150, TC-199) still carries approved text
that differs from its docs/archive/last_approved copy ... or moved only
TRACED cells".

WI-545 moved only traced pointer cells on these rows: `verifies` gained
IF-260 to IF-263, and `evidence` gained their structural tests. Batch J's act
(seq 12), re-taken on the merged trunk, re-copied `test-cases.toml` with
them in place. A traced cell re-opens no attestation, so no verdict is owed.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-048 `Verifies`: 'SR-154;LLR-048' -> 'SR-154;LLR-048;IF-260'
- TC-080 `Verifies`: 'SR-159;LLR-042' -> 'SR-159;LLR-042;IF-263'
- TC-150 `Verifies`: 'SR-137;LLR-155' -> 'SR-137;LLR-155;IF-261'
- TC-199 `Verifies`: 'LLR-203' -> 'LLR-203;IF-262'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
