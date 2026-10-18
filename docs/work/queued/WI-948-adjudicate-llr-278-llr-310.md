+++
id = "WI-948"
title = "adjudicate: LLR-278, LLR-310, LLR-338, TC-278 - approved/routed cell(s) amended on merged trunk 7c59c67..96c6ce1 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-278", "LLR-310", "LLR-338", "TC-278"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-278 `Detail`: 'acceptance_record.merge_approval_refusal applies the additional adjudication bounds whenever any claimed row records a …' -> 'acceptance_record.merge_approval_refusal applies the additional adjudication bounds whenever any claimed row records a …'
- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- LLR-338 `Detail`: 'From an accepted verdict and its binding as committed at a revision, the act assembler derives every authorized act tha…' -> 'From an accepted verdict and its binding as committed at a revision, the act assembler derives every authorized act tha…'
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
