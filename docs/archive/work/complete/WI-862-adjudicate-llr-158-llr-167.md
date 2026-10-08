+++
id = "WI-862"
title = "adjudicate: LLR-158, LLR-167, LLR-181, LLR-278, LLR-310, TC-218, TC-278 - approved/routed cell(s) amended on merged trunk 1412d96..ceab00c (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-158", "LLR-167", "LLR-181", "LLR-278", "LLR-310", "TC-218", "TC-278"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-849's in-lane adjudicator, through the retained session, ruled every amended row it names MEANING and re-attested it in the lane's own act (verdict `docs/reviews/wi-849-approval-act-in-lane/002-ADJUDICATE-e648cd9.md`). The low-level and test-case registries are byte-identical to their anchors under `docs/archive/last_approved/` at the landing.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'
- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint that has a brief to…" -> 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…'
- LLR-181 `Detail`: "kitlib is the kit's one home for behaviours that were previously copied per script: config.first_declared_line with its…" -> "kitlib is the kit's one home for behaviours that were previously copied per script: config.first_declared_line with its…"
- LLR-278 `Detail`: 'acceptance_record.merge_approval_refusal calls reattest_scope_refusal and held_reattest_refusal for an adjudication lan…' -> 'acceptance_record.merge_approval_refusal applies the additional adjudication bounds whenever any claimed row records a …'
- LLR-278 `Rationale`: 'At merge the first-approval scope check read flips alone, and a re-attestation moves no cell, so an amendment act could…' -> 'At merge the first-approval scope check read flips alone, and a re-attestation moves no cell, so an amendment act could…'
- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- TC-218 `Expected`: "Satisfies SR-191's acceptance clause that an assumption's approval is recorded as every other approval of approved cont…" -> "Satisfies SR-191's acceptance clause that an assumption's approval is recorded as every other approval of approved cont…"
- TC-218 `Method`: 'Driven on real git repositories, once for an assumption row and once for a surrogate row. A lane whose merge delta flip…' -> 'Driven on real git repositories, once for an assumption row and once for a surrogate row. A lane whose merge delta make…'
- TC-278 `Expected`: "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…" -> "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…"
- TC-278 `Method`: 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…' -> 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
