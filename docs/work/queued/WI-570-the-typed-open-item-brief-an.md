+++
id = "WI-570"
title = "The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a recommendation, or is refused"
workstream = "process"
specref = "docs/plans/2026-09-01-typed-open-item-brief.md"
buildtier = "medium"
priority = 5
safety_class = "ordinary"
+++

## Context

Filed 2026-09-01 (evening supervised session) at the owner's direction and
prioritized P1. `intake._mint_open_item` (WI-552 arm 2) writes only
title/status/raised/one_line/wi_refs, so the two rows it has minted so far
(`OI-77`, `OI-78`) reached the owner as a bare question with no options and no
recommendation; both were hand-filled at `6032ce69`. Make the thin card
unrepresentable: a typed `[open_item]` table (one_line, blast_radius, options,
recommendation — all required) that `parse_dispositions` /
`_mint_shape_refusal` refuse when incomplete and the mint writes verbatim; the
ADJUDICATE template states that the adjudicator authors the brief. Read the
plan's §2 (what this is NOT) before widening scope.

**Standing constraint (owner ruling 2026-09-01, the approval act is the
adjudicator's):** if this row authors or amends spine rows (SR/LLR/TC), leave
them `Drafted`; do NOT flip any `Status`, and do NOT run `intake.py snapshot`
or write `docs/archive/last_approved/` on this lane. The flip and the
snapshot are performed on trunk by the adjudication arm once it ships.

## Done-when

- A disposition draft carries its open item as a typed `[open_item]` table
  whose `one_line`, `blast_radius`, `options` and `recommendation` are all
  required and non-empty, and `intake` refuses, by name, the bare scalar form
  and a table missing any cell.
- `intake._mint_open_item` writes those cells verbatim, so a minted row has the
  shape of a hand-filed pending row and `gen_open_items.py` renders it with no
  special case.
- `prompts/adjudicate-disposition.template.md`, and any sibling brief that
  mentions `open_item`, documents the table and says the adjudicator authors
  the brief; `prompts/CATALOG.md` is regenerated.
- `tests/test_intake.py` pins the accepted table, both refusals and the
  open-item edge still gating the successor, and the log fragment names the
  two rows minted thin before the fix (plan §3 item 5).
- The commit bar passes, and nothing in the change flips a spine row's
  `Status` or writes the approval snapshot.
