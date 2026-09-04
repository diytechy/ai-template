# The typed open-item brief: an adjudicator-minted OI must carry the owner's whole card

**Status:** plan of record for the row minted against it. Authored 2026-09-01
(evening supervised session) from WI-568's mechanized round
(`docs/reviews/wi-568-dispose-the-close-recorded-at/002-REVIEW-A-9d4fc41.md`,
MAJOR) and the owner's read of the two rows the new mint produced. The owner
asked for this fix to be prioritized.

## 1. The problem, measured

WI-552 arm 2 (`2381981b`, OI-70/OI-73 exit B) gave the adjudicator's
`## Dispositions` grammar a scalar `open_item = "<question>"` cell: at the
successor's merge, `intake._mint_open_item` appends a `pending` row to
`docs/requirements/open-items.toml` and injects its id into the successor's
`needs`, so the owner's ruling gates the work. The mint writes exactly five
cells — `title`, `status`, `raised`, `one_line`, `wi_refs` — and nothing
else. Every hand-filed row carries the owner brief as well: `decision` (what
is being decided), `blast_radius`, `options` (the `- (a) … FOR: … AGAINST: …`
idiom) and `recommendation`, and `gen_open_items.py` renders exactly those
onto the owner's card. The two rows the new path has minted so far (`OI-77`
at the WI-563 merge, `OI-78` at the WI-568 merge) therefore reached the owner
as a bare question with no alternatives and no recommendation; the WI-568
round caught it and the lane could only carry the brief in the successor's
captured scope, one link away from the card. The owner hand-filled both rows
on 2026-09-01 evening.

The construction fault is that the grammar accepts a question where the
registry contract wants a brief: a thin card is a state the mint can write.

## 2. What this is NOT

- Not a change to the open-items registry schema or to `gen_open_items.py`'s
  rendering — both already carry and render the brief cells.
- Not a ruling on any pending row; `OI-77` and `OI-78` are the owner's and are
  already filled by hand.
- Not a widening of the other adjudicator arms (amendment, spot-check); only
  the disposition arm mints an OI.

## 3. Done-when

1. The `## Dispositions` grammar carries the open item as a typed table —
   `[open_item]` with `one_line`, `blast_radius`, `options`, `recommendation`
   (all four required, non-empty) — and `intake.parse_dispositions` /
   `intake._mint_shape_refusal` REFUSE, by name, a draft whose open item is
   the bare scalar or a table missing any of the four cells. The scalar form
   is retired, not tolerated: a thin card must be unrepresentable at the mint,
   not caught by a reviewer.
2. `intake._mint_open_item` writes the four cells verbatim into the minted
   row (one key per line, triple-quoted strings, the `decision` cell derived
   as "what is being decided" from `one_line` if the grammar keeps it
   separate), so a minted row is field-identical in shape to a hand-filed
   pending row and `gen_open_items.py` renders it without special-casing.
3. `project-trajectory/prompts/adjudicate-disposition.template.md` (and any
   sibling that mentions `open_item`) documents the table and states plainly
   that the ADJUDICATOR authors the brief — blast radius under each answer,
   options with FOR/AGAINST, a recommendation with its reason — because the
   adjudicator is the party that has just measured the alternatives;
   `prompts/CATALOG.md` regenerated.
4. Tests in `tests/test_intake.py` (the module's existing style): a table
   draft is accepted and its four cells land verbatim in the registry; the
   scalar form and a table missing a cell are refused with the naming
   message; the OI edge still gates the successor; existing OI-mint tests
   updated rather than deleted.
5. Recorded so the effect is measurable: the fragment names the two rows
   minted thin before this fix (`OI-77`, `OI-78`) and the commit that
   hand-filled them, states `Deferred open items:` at file level, and carries
   `fig:` provenance on any driven figure.  <!-- fig-ok: prose about the convention -->

## 4. Evidence trail

The WI-568 round file above; the 2026-09-01 "Supervised evening run" log
entry (kit finding 3); `intake._mint_open_item` and `_inject_open_item`;
the WI-552 entry's arm-2 account; the hand-fill commit on
`docs/requirements/open-items.toml` dated 2026-09-01.
