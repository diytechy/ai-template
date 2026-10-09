+++
id = "WI-876"
title = "adjudicate: LLR-046, LLR-207, LLR-310, LLR-313, TC-083, TC-327 - approved/routed cell(s) amended on merged trunk f9c7a91..03db0ea (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-046", "LLR-207", "LLR-310", "LLR-313", "TC-083", "TC-327"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-046 `Detail`: 'Computes advisory substance components and decay history; treats tripwires as gates and never rewards length. Severity …' -> 'Computes advisory substance components and decay history; treats tripwires as gates and never rewards length. Severity …'
- LLR-207 `Detail`: 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…' -> 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…'
- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- LLR-313 `Detail`: 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…' -> 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…'
- TC-083 `Expected`: 'Scores and decay match fixtures; all tripwires fire as gates; length is never positive; persistence is stable.' -> 'Scores and decay match fixtures; all tripwires fire as gates; length is never positive; persistence is stable; each mal…'
- TC-083 `Method`: 'Run substance components, corroboration, tripwires, decay, verdict parsing, and CLI cases.' -> 'Run substance components, corroboration, tripwires, decay, verdict parsing, and CLI cases, including malformed or ambig…'
- TC-327 `Expected`: 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…' -> 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…'
- TC-327 `Method`: 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…' -> 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
