+++
id = "WI-951"
title = "adjudicate: LLR-208, LLR-307, LLR-337, TC-206, TC-325, TC-367 - approved/routed cell(s) amended on merged trunk 8d64910..9f911f9 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-208", "LLR-307", "LLR-337", "TC-206", "TC-325", "TC-367"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-208 `Detail`: 'One file per review scope under docs/reviews/rollup/<train>.md, compiled from the round files that scope carries: ordin…' -> 'One file per review scope under docs/reviews/rollup/<train>.md, compiled from the round files that scope carries: ordin…'
- LLR-307 `Detail`: 'bound_items reads each current Done-when item that only ticks or evidences a claim-time item as that claim-time item; d…' -> 'bound_items reads each current Done-when item that only ticks or evidences a claim-time item as that claim-time item; d…'
- LLR-337 `Detail`: "The gate reads only rows claimed by the lane's own active folder at the claim base. The closed planmode set is absent, …" -> "The gate reads only rows claimed by the lane's own active folder at the claim base. The closed planmode set is absent, …"
- TC-206 `Expected`: 'Satisfies SR-170: the per-review-scope rollup is written by a regenerator the serial merge step runs and never by a wor…' -> 'Satisfies SR-170: the per-review-scope rollup is written by a regenerator the serial merge step runs and never by a wor…'
- TC-206 `Method`: 'The rollup as DERIVED state, driven on a scaffold carrying one review scope. Regeneration writes docs/reviews/rollup/<t…' -> 'The rollup as DERIVED state, driven on a scaffold carrying one review scope. Regeneration writes docs/reviews/rollup/<t…'
- TC-325 `Expected`: 'An in-lane changed Done-when holds subsequent build or rework dispatch, staged close and serial landing until blessed; …' -> 'An in-lane changed Done-when holds subsequent build or rework dispatch, staged close and serial landing until blessed; …'
- TC-325 `Method`: 'Run test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close, test_an_unchanged_or_only_ticked_done_when_holds_not…' -> 'Run test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close, test_an_unchanged_or_only_ticked_done_when_holds_not…'
- TC-367 `Expected`: 'Build output is held at each gate until a supported pass record binds it, and a changed plan or Done-when unbinds it wh…' -> 'Build output is held at each gate until a supported pass record binds it, and a changed plan or Done-when unbinds it wh…'
- TC-367 `Method`: 'Drive a claimed single-plan lane through pre-commit, squash and landing checks before and after a pass record. Change t…' -> 'Drive a claimed single-plan lane through pre-commit, squash and landing checks before and after a pass record. Change t…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
