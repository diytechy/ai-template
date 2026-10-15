+++
id = "WI-924"
title = "adjudicate: LLR-019, LLR-307, LLR-309, TC-019, TC-325 - approved/routed cell(s) amended on merged trunk 9ddc5ee..9d0f1c5 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-019", "LLR-307", "LLR-309", "TC-019", "TC-325"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-019 `Detail`: 'Runs trace --strict-integrity and the check_privacy secrets scan on staged content and blocks a failing commit.' -> 'Runs trace --strict-integrity and the check_privacy secrets scan on staged content and blocks a failing commit. Every b…'
- LLR-307 `Detail`: 'bound_items reads each current Done-when item that only ticks or evidences a claim-time item as that claim-time item; d…' -> 'bound_items reads each current Done-when item that only ticks or evidences a claim-time item as that claim-time item; d…'
- LLR-309 `Detail`: "After routed_session selects a build or rework session, build_hold asks LLR-307's lane_hold and returns the worker's HE…" -> "After routed_session selects a build or rework session, build_hold asks LLR-307's lane_hold and returns the worker's HE…"
- TC-019 `Method`: 'Run the pre-commit-hook suite; a failing integrity/secrets check blocks the commit.' -> 'Run the pre-commit-hook suite; a failing integrity/secrets check blocks the commit. Run the commit-floor census: every …'
- TC-325 `Expected`: 'An in-lane changed Done-when holds subsequent build or rework dispatch, staged close and serial landing until blessed; …' -> 'An in-lane changed Done-when holds subsequent build or rework dispatch, staged close and serial landing until blessed; …'
- TC-325 `Method`: 'Run test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close, test_an_unchanged_or_only_ticked_done_when_holds_not…' -> 'Run test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close, test_an_unchanged_or_only_ticked_done_when_holds_not…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
