+++
id = "WI-959"
title = "adjudicate: LLR-207, TC-132, TC-205 - approved/routed cell(s) amended on merged trunk be80354..ed84e25 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-207", "TC-132", "TC-205"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-956's in-lane sitting
`docs/reviews/wi-956/010-ADJUDICATE-1e022d9.md` blessed all three rows as
MEANING+BLESS, and the lane's act turn took act seq 143. At the landing
ed84e2510 the low-level and test registries are byte-equal to their
approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-207 `Detail`: 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…' -> 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…'
- TC-132 `Expected`: 'Satisfies SR-156 AcceptanceCriteria via the LLR-140 detail contract' -> 'Satisfies SR-156 AcceptanceCriteria via the LLR-140 claim/integration contract and the LLR-207 attest, producer and ref…'
- TC-132 `Method`: 'Run the integrator suite: each claim refusal fires by name (a dirty path the claim must write among them, refused befor…' -> 'Run the integrator suite: each claim refusal fires by name (a dirty path the claim must write among them, refused befor…'
- TC-132 `Verifies`: 'SR-156;LLR-140' -> 'SR-156;LLR-140;LLR-207'
- TC-205 `Method`: "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…" -> "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…"

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
