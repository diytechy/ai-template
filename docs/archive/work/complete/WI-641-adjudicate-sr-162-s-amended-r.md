+++
id = "WI-641"
title = "adjudicate: SR-162 - its approved Rationale was amended with no adjudication recorded; judge whether scope moved"
workstream = "requirements"
specref = ""
sr_refs = ["SR-162"]
needs = []
buildtier = "strong"
safety_class = "adjudication"
priority = 2
+++

## Deliverable

Ruled in an attended sitting on `refactor_again` (the loop is paused), from the
before/after cells, against the requirements record last written at 27a30842:

    VERDICT: CLARITY rows=1

SR-162's only moved cell is `rationale`. Its last sentence lost "and no SR
states it yet", a claim about other rows that Drafted SR-185 has since made
false. The `requirement` and `acceptance_criteria` cells that carry the
obligation are untouched. The verdict is
`docs/reviews/wi-641-adjudicate-sr-162-s-amended-r/001-ADJUDICATE-f263118.md`.
It counts SR-162 alone and lists the other nineteen rendered rows, excluded
from the count, with where each is ruled (the WI-566 rule, upheld by
arbitration; below).

Consequence: the attestation stands, no registry cell was edited, and nothing
further is owed. SR-162 stays drifted from its record until WI-642's approval
act copies `system-requirements.toml`, which the snapshot tool will do only
with `--approves` naming this verdict and WI-547's.

Review: codex Sol (medium) confirmed the call and found the anchor stamp and
the verdict's scoping wrong; a Fable arbiter ruled the scoping (keep one row,
record the rest as excluded, per WI-566's corrected verdict), and the anchor
now names the per-registry copy. The brief's whole-tree rendering and its
directory-wide stamp are filed as WI-646.

## Context

SR-162's approved `Rationale` differs from its copy in `docs/archive/last_approved/`, and no adjudication has read the change, unlike the seventeen sibling rationale edits WI-547 ruled CLARITY. It blocks the phase-6 approval act (WI-642), whose refresh of the requirements record would otherwise carry the edit unread. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- The amendment is ruled — CLARITY (obligation unchanged) or scope moved — with the verdict recorded where the adjudication brief puts it.
- A scope-moved ruling drafts its follow-ups; a CLARITY ruling asks for nothing more.
