# WI-1006 plan: report each ruled open item whose action nothing carries

Planned on branch `maint/wi-1006` at `8e08e7bbd`, a maintenance branch cut
from trunk `refactor_again` at `b696b6c36`. Read in full: the row, its spec
of record `docs/specs/WI-1006.md` (archived at the close as
`docs/archive/specs/WI-1006.2026-11-19.md`) and the scope critique. Also
read: SR-148, LLR-298, LLR-299, IF-073, IF-102, IF-118, the open-items template and this
repository's registry, `kitlib/spine.py` (`open_item_queue`, `open_items_at`),
`kitlib/registry.py` (the status directories), `pending.py` (`open_item_queue`,
`citing_rows`), `gen_open_items.py` (`main`) and `docs/stack.ini` `[run]`.

## Construction

1. **The rule, a pure function** (`kitlib/spine.py`, beside
   `open_item_queue`). `OPEN_ITEM_TOKEN` is the boundary the spec of record
   states, and `open_item_numbers(text)` reads the item numbers a text names.
   `ruled_uncovered(oi_rows, named)` takes the registry rows and a map from
   item number to the statuses of the work items whose text names it. It
   returns `[(OI id, row)]` for each real `ruled` item that is not covered.
   Rules 1 and 3 give a set of base-covered items, and an item a `pending`
   citer names joins them. Coverage then spreads from each covered `ruled`
   item to every `ruled` item it names until nothing changes. That reading
   needs no recursion, and a cycle with no covered member never reaches a
   covered item.
2. **The read** (`pending.py`, beside its `open_item_queue`).
   `ruled_cover(root)` loads the registry through the carrier handle the
   module already uses, and returns None when there is none (vacuous).
   `work_item_naming(root)` walks each `WI-*.md` under a status directory of
   both work roots through `kitlib.registry`'s roots, file listing and status
   map. A `-000` example is skipped.
3. **The report** (`gen_open_items.py --ruled-cover`). One `WARN` line per
   finding, naming the item and its title, then a count line. It exits 0
   whatever it finds and says "vacuous" without a registry. A registry that
   does not parse stops it through the carrier's own refusal.
4. **The schema.** `follow_up` joins `OFFSPINE_KEYS["OI-ID"]`, the carrier's
   column map (`FollowUp`) and `migrate_carrier`'s inverse map. The template
   header documents the cell beside the light-spine paragraph and asks a
   follow-up item to name the item it continues. Its `-000` row sets it, and
   so does this repository's `-000` row. IF-073's row and its `Contract
   IF-073:` header gain the cell and the rule.
5. **The audit.** `docs/stack.ini` `[run] audit` runs
   `gen_open_items.py --ruled-cover` first and the smoke budget step after it,
   joined by `&&`. A finding exits 0, so only the budget step decides the
   audit's exit code. The smoke budget test that pinned the audit to one step
   finds the budget step among the audit's steps instead.
6. **The four items.** A `follow_up` cell goes on OI-35, OI-89 and OI-90 only
   where a commit, work item or log entry shows what carried the ruling out.
   OI-79's ruling deletes a remote ref, and today's fetch still lists that
   ref. With no evidence, OI-79 gets no cell, and the cell text it would need
   goes to the operator. The four are judged with this row's own file set
   aside, because its Done-when names them.

## Files

`project-trajectory/scripts/kitlib/spine.py`, `pending.py`,
`gen_open_items.py`, `spine_carrier.py`, `migrate_carrier.py`;
`project-trajectory/registries/open-items.template.toml`;
`project-trajectory/RESYNC_PACK.md`; `docs/requirements/open-items.toml`,
`low-level-requirements.toml` (LLR-370), `interfaces.toml` (IF-073);
`docs/test/test-cases.toml` (TC-430, TC-431); `docs/stack.ini`;
`tests/test_ruled_open_item_cover.py` (new, in-process) and
`tests/test_check_smoke_budget.py`. None of them is pinned by the module size
ratchet.

## The arms the tests pin

TC-430, the rule (`tests/test_ruled_open_item_cover.py`):

- each covering status, draft, queued, active, deferred and complete, under
  either work root;
- each non-covering one: cancelled, partial and restructured;
- handed to a pending item;
- handed through a ruled item that is itself covered;
- not handed through a ruled item that is not covered;
- a cycle of ruled items with no row;
- a `follow_up` cell, and a blank one;
- the token boundary (`OI-350` is not OI-35, `OI-035` is);
- the historical `wi_refs` cell and an item naming itself cover nothing;
- a `-000` row is neither judged nor read as a citer;
- a citer outside `pending` and `ruled` covers nothing.

TC-431, the report and the audit:

- no registry is vacuous and exits 0;
- a registry that does not parse stops the report;
- a finding exits 0 and names the item and its title;
- the audit runs the report ahead of the budget step;
- the template's `-000` row and this repository's `-000` row set
  `follow_up`.
