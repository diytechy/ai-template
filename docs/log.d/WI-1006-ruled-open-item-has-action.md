## 2026-11-19 — WI-1006: run.cmd audit reports each ruled open item whose action no work item, later open item or follow_up cell carries

Deferred open items: none.

Built on the maintenance branch `maint/wi-1006`, cut from `b696b6c36`,
outside the lane workflow: no claim, no lane review rounds, every commit
through the hooks.

- **The critique** (Gemini Argon, round 1, three findings): all three were
  adopted. The row takes `planmode = "single"`. The spec of record names
  the anchor: SR-148, with a new design row LLR-370 and no new SR. IF-073's
  contract carries the new cell. The check adds no module or seam, and it
  ships. The spec also closes the input space: the token boundary, which
  text is scanned, the `-000` rows, an item naming itself, the statuses, and
  a blank `follow_up` cell.
- **The check.** The rule lives in `kitlib/spine.py` (`ruled_uncovered`), the
  read and its lines in `pending.py`, and the flag in `gen_open_items.py`
  (`--ruled-cover`, exit 0 whatever it finds). Only a later open item, one
  with a higher number, covers. Coverage spreads from each covered ruled
  item to the earlier ruled items it names. The report text sits in
  `pending.py`, which keeps `gen_open_items.py` under the module-size
  threshold.
- **The schema.** `follow_up` is optional. The open-items template documents
  it beside the light-spine paragraph. One sentence of that paragraph was
  amended, because the report judges only `ruled` items and so tells
  `implemented` apart. Both `-000` rows show the cell, and IF-073's row and
  contract header state it.
- **The audit.** `docs/stack.ini` `[run] audit` runs the report, then the smoke
  budget. A finding exits 0.
- **The four items.** With this row's own file set aside, the report named
  OI-35, OI-79, OI-89 and OI-90. Three gained a `follow_up` cell citing its
  evidence:
  - OI-35: its ruling commit `4b8f9ab49`;
  - OI-89: `none — ...`, citing the ruling record of 2026-09-26;
  - OI-90: WI-638's `f7885a49e`, which gave the five observation cases their
    inputs and lifetime.

  OI-79 did not. Its ruled act, deleting the `-HELD-` remote ref, is the
  operator's push, and the fetch of 2026-11-19 still lists that ref. So
  nothing carries it, and only this row's own Done-when text covers it.
- **Review** (Sol on the code, Argon on the prose), four findings, all fixed:
  - only a later open item covers (the earlier draft let any other item
    cover);
  - the token rejects a letter, digit or underscore after the number too;
  - LLR-370 names `main`;
  - its detail says "done for `complete/`".

  The later-only rule then reported OI-80, which only the earlier OI-72
  names. Its ruling commit `525b2503c` carried it out, and a cell now cites
  that commit.
- **Measured at close:** the report finds 0 of 116 ruled items, and 1
  (OI-79) with this row set aside.
