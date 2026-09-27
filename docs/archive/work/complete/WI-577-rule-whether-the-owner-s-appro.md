+++
id = "WI-577"
title = "Rule whether the owner's approval brief narrows to the held rungs, then apply the ruling to trace --approve"
workstream = "process"
needs = ["OI-82"]
specref = ""
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

## Deliverable

OI-82 is ruled (a), refined by the owner, and applied. `trace.py --approve
modified`, and the `docs/ratify/CURRENT.md` it renders, still render every
owing chain. A chain whose every owing row sits on a tier the dial releases
(Drafted, or drifted against its approved copy) renders in full inside one
`<details>` block. The block is collapsed by default and labelled "Waiting
for automated adjudication". A chain with any held-rung row stays in the
owner's section as before.

The page's title claims no human act, and its signing instruction covers
only the sections outside the block. The dial is read only through
`agent_common.human_approves_spine`, once per spine tier. No new rung table
exists, and `SPINE_APPROVAL_RUNGS` is unchanged. PROCESS_OPTIONS.md states
the ruled owner surface (+268 bytes).

- **Spine:** no spine row stated this rendering, so WI-577 authored LLR-259
  (under SR-139) and TC-252 Drafted. TC-252 cites the new seam IF-224
  (`agent_common` read from `trace`), so nothing is allowlisted. Their first
  approval is **WI-674**.
- **Evidence:** four tests in `tests/test_trace_briefs.py`, run red before
  the code:
  - a held and a released rung, Drafted chains;
  - a released-rung re-attestation, whose diff renders inside the block
    while a held amended chain stays in the owner's section;
  - the default dial rendering no block;
  - the neutral framing.
- **Review:** Sol took three rounds (arbitration rulings 10 and 13) and the
  last was SOUND.
- **Not in scope, noted:** `open-items.html` (gen_open_items) still renders
  the unsplit population. The plan-of-record row in
  `docs/plans/2026-09-01-approval-act-adjudicator-only.md` §2a is left as
  history.

## Context

**OI-82 RULED 2026-09-26: option (a), refined by the owner.** Every unapproved chain still appears in the brief; a chain on a rung the dial releases renders in full (not ids only) under the label "Waiting for automated adjudication", collapsed by default (a `<details>` block in `docs/ratify/CURRENT.md`, or an expansion toggle). Held-rung chains render as today. Record: `docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md`.

Drafted by WI-574 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks `waiting:open-item-pending`
until the ruling lands (OI-73 exit (B) — there is no standalone OI exit). IN
SCOPE once ruled: apply the ruling to `trace.py`'s `--approve modified`
population and to whatever `docs/ratify/CURRENT.md` renders, reading the dial
through the EXISTING `agent_common.human_approves_spine` — a third copy of the
rung table is the exact defect WI-572's round-1 MAJOR was about — plus the
PROCESS_OPTIONS.md §2a table row that describes the owner's surface, which is
unsatisfied prose until this lands either way. EXPLICITLY NOT IN SCOPE: the
adjudication-side filter (shipped and correct), and any change to
`SPINE_APPROVAL_RUNGS` itself.

Advisory registry joins (WI-388; never gating):

### Pending open items whose WI-Refs touch this row's kin (premise risk)
- OI-82 (pending): WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint a…

## Done-when

- OI-82 is ruled in `docs/requirements/open-items.toml`, naming the option
  chosen.
- `trace.py --approve modified`, and the `docs/ratify/CURRENT.md` it renders,
  show the population the ruling names, reading the dial through the existing
  `agent_common.human_approves_spine`; `SPINE_APPROVAL_RUNGS` is unchanged and
  no new copy of the rung table exists.
- A test drives the command on a scaffold with one held rung and one released
  rung and shows each rendered as the ruling says.
- PROCESS_OPTIONS.md's description of the owner's approval surface states the
  ruled behaviour, and the commit bar passes.
