+++
id = "WI-550"
title = "dispose: the close recorded at docs/handbacks/WI-540-wi-540-adjudicator-retention-layer.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "disposition"
+++

## Deliverable

OUTCOME: PARTIAL successors=1

Verdict: `docs/reviews/wi-550-dispose-the-close-recorded-at/001-ADJUDICATE-e3f0d04.md`

The WI-540 partial close is upheld as PARTIAL. The §A3 red-close handback had
already executed a complete, honest discard-all (all product commits reverted to
`9abdb5d982`, the failing diff preserved as
`docs/work/handback/wi-540-adjudicator-retention-layer.patch`); verified trunk
byte-identical to base, no dangling refs, smoke 1427 passed/6 skipped/31.49s. One
successor drafted under `## Dispositions` (`supersedes = "WI-540"`, strong) to
re-land the preserved patch inert at dial 0 after resolving the DESIGN-CHECK gate
failure that crashed the worker.

## Context

The closed spec is `docs/work/partial/WI-540-adjudicator-retention-layer.md`.

Its per-close report is `docs/handbacks/WI-540-wi-540-adjudicator-retention-layer.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

## Dispositions

```toml
title = "Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0, DESIGN-CHECK green"
workstream = "process"
buildtier = "strong"
safety_class = "ordinary"
priority = 2
supersedes = "WI-540"
```

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
