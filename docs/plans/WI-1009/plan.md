# WI-1009 plan: the delegated decisions leave docs/open-items.html

Planned on branch `maint/wi-1009` at `26c3bf808`, a maintenance branch cut
from trunk `refactor_again` at `6a78f63a7`. Read in full: the row, its
scope critique, SR-225, LLR-118, LLR-283, IF-074, IF-164, IF-255, IF-256,
TC-123, TC-293, DA-020, `pending.decisions_to_review` and `citing_rows`, the
render path and section 4 of `gen_open_items.py`, `traj_status._open_item_lines`,
`kitlib/decisions.py`, `integrate._decision_record_refusal`, the shipped
`decisions.template.toml` and the "Delegated decisions record" layer of
`PROCESS_OPTIONS.md`.

## Construction

1. **The read** (`pending.py`). `decisions_to_review` and `citing_rows` give
   way to `decision_records(root)`, which returns `(unseen, findings)`:
   how many entries across `docs/decisions/*.toml` have no verdict (the count
   of `kitlib.decisions.review_queue`'s first list, so an unrecognized value
   and the retired key read as not yet seen, and `-000` is never counted),
   and each record's `record_findings`, prefixed by its file. `unseen` is
   None when the directory is absent. The ordering, the overruled list, the
   confirmed count and the citing work items were section 4's alone, so they
   go.
2. **The page** (`gen_open_items.py`). Section 4's band leaves `render`,
   with `_DECISION_FIELDS`, `_decision_card`, `_citing_field`,
   `OVERRULED_HEADING` and `decisions_block`. `record_findings_block(findings)`
   renders the findings notice that closes section 3, or `""` when no record
   carries a finding. No CSS rule was section 4's alone: `.pill.accept`,
   `.empty` and `.notice` are all used by other sections. The module
   docstring's section list and the `Contract IF-074:` block follow.
3. **The status line** (`traj_status.py`). `- **Delegated decisions not yet
   seen:** N — [docs/decisions/](decisions/)`, still only when the directory
   exists. Kept rather than dropped: across 132 files nothing else says how
   many entries are still unseen. That is the backlog DA-020's obstacle
   names, and TC-293 already checks the count.
4. **The text.** `kitlib/decisions.py`'s docstring paragraph that names the
   section (docstring only; WI-1004 works in that file, and `review_queue`
   stays as IF-256 states it). The shipped template header. The
   `PROCESS_OPTIONS.md` sentence. A RESYNC entry.
5. **The rows.** SR-225's requirement and acceptance criteria, plus one
   rationale sentence for the ruling. IF-074's data and contract. LLR-118's
   detail. LLR-283's detail and its traced `module`/`code_symbol` cells.
   TC-123's method. TC-293's method, expected and evidence. IF-164's data
   (Drafted). No id is minted.

## Files

`project-trajectory/scripts/pending.py`, `gen_open_items.py`,
`traj_status.py`, `kitlib/decisions.py` (docstring);
`project-trajectory/decisions.template.toml`, `PROCESS_OPTIONS.md`,
`RESYNC_PACK.md`; `docs/requirements/system-requirements.toml`,
`low-level-requirements.toml`, `interfaces.toml`;
`docs/test/test-cases.toml`; `tests/test_decisions_to_review.py`,
`tests/test_open_item_queue.py`, `tests/test_generated_newlines.py`; the
regenerated views.

## The arms the tests pin

- The page has sections 1 to 3 only, with no `decisions-to-review` anchor and
  no entry's text, even with unseen, hoisted and overruled entries on disk.
- The findings notice closes section 3 when a record carries a finding: an
  unknown verdict, the retired key, a blank review on an overrule, a
  malformed hoist, an unparseable record. It is absent when the records are
  sound and when the directory is absent.
- The count: an absent key, an unknown value and the retired key each count
  as not yet seen. A note alone does not change that. Confirmed, overruled
  and `-000` entries are not counted.
- The status line: the count and the `docs/decisions/` link; 0 when all are
  confirmed; no line without the directory; never the removed anchor.
- The shipped template: sound, `-000` not counted, and its header names the
  record files rather than the section.
