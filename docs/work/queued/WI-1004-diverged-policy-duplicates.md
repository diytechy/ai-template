+++
id = "WI-1004"
title = "The policy duplicates the OI-130 re-score found disagreeing each get one home, with the disputed inputs pinned"
workstream = "process"
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#one-home-per-behaviour-still-a-code-obligation"
buildtier = "strong"
safety_class = "ordinary"
priority = 4
planmode = "single"
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from the OI-130
re-score record's "One home per behaviour" section, the second of the three
rows the 2026-11-11a handoff left unfiled (its owner item 3). Its scope
critique is owed before a claim.

WI-448's consolidation stopped short: 19 policy behaviours still have more
than one independent home, and 11 of them disagree on some input. This row
takes those 11. The 8 that agree, and the 18 plumbing duplicates, stay out
unless the critique folds them in. `PROCESS.md` §3's 0→A→B rule applies:
extract the shared stage and delete the copies.

The 11, as the record lists them:

- **B3 `value_to_cell`:** `None` becomes `''` in `migrate_carrier` and
  `'None'` in `spine_carrier`. The pin has no `None` case.
- **B5 SN-id universe:** on a TOML needs file, `check_docs` and `check_flows`
  scrape ids from comments and descriptions, and `check_flows` also counts
  SN-000. The `need_ids` pin returns early on TOML, so it checks nothing.
- **B8b spec parse:** `wi_convert.parse_spec` and
  `kitlib.registry.parse_spec_row` disagree on `title = 5`, on an id that does
  not match its filename, and on `["a;b"]`.
- **B10 ref split:** `adjudicate_brief`, `consolidate` and `intake` split on
  `;` only, so `consolidate.py:451` misses OI edges `split_pred_edges` finds.
- **B12 module key:** `migrate_carrier._short_module` differs from
  `kitlib.spine.norm_module` on `__init__.py` and on non-`.py` paths.
- **Queued-spec lookup:** given two matching specs, `handback` takes the
  first, `integrate` refuses, and `consolidate` takes the first.
- **Id number from an id:** `kitlib.spine` and `kitlib.decisions` take the
  digits after the last dash; `wi_convert` and `kitlib.registry` take the
  first run of digits.
- **Rolling review §13.13, §13.14, §13.16 and §13.22** (unmerged
  `origin/rolling_review`, `04488d5cd`): spec precedence, the generator
  freshness arm, the declared-file grammar and the command tokenizer.

No SR is named here: each behaviour sits under its own requirement. The
critique attaches them, and splits this row per behaviour if one row is too
large to review.

## Done-when

- [ ] Each of the 11 has one implementation that every former copy calls, and
      the copies are deleted.
- [ ] Where copies disagreed, the kept answer is chosen per input and pinned
      by a test naming that input. A choice that changes what an adopter sees
      is named in the Deliverable, with a RESYNC entry where a shipped script's
      output changes.
- [ ] The two pins that check nothing are repaired: `value_to_cell` gains the
      `None` case, and the `need_ids` pin runs on a TOML needs file.
- [ ] `consolidate` finds every OI edge `split_pred_edges` finds (B10).
- [ ] The `[dupes-census]` baseline is re-stamped downward if the count drops.
