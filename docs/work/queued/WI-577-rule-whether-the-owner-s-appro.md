+++
id = "WI-577"
title = "Rule whether the owner's approval brief narrows to the held rungs, then apply the ruling to trace --approve"
workstream = "process"
needs = ["OI-82"]
specref = "docs/archive/work/complete/WI-574-spot-check-the-clean-close-of.md"
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

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
