+++
id = "WI-551"
title = "Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0, DESIGN-CHECK green"
workstream = "process"
specref = "docs/archive/work/complete/WI-550-dispose-the-close-recorded-at.md"
buildtier = "strong"
priority = 2
safety_class = "ordinary"
supersedes = "WI-540"
+++

## Context

Drafted by WI-550 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

The adjudicator session-retention layer is still wanted — WI-541
(`docs/work/queued/WI-541-verify-retention-layer.md`, turn the dial on and
verify on-box) blocks on it, and the whole OI-69 adjudicator program depends on
it. The WI-540 lane's work is ~90% built and REVIEW-A-addressed, preserved
intact as `docs/work/handback/wi-540-adjudicator-retention-layer.patch`. The
successor RE-LANDS that patch (it does not rebuild): applying it re-adds
`adjudicator_session.py`, the `[adjudicator]` dial shipped inert at 0, and the
IF-174/LLR-163/TC-157/IF-064 spine amendments against their already-burned marks
(id-watermark IF=174). The proximate blocker was the DESIGN-CHECK gate erroring
then timing out and the §A2 refresh bar refusing (exit 1), so the successor must
reproduce and resolve that gate failure and get the bar green before landing.
Strong tier, not the report's suggested medium: the diff is 3876 lines across
the live `agent_loop`/`dispatch` runtime seams plus an unresolved gate failure
that crashed a worker. The design is settled (plan §2–§5 + OI-69 a–e) — a
build/repair, not a design fork.
