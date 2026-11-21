+++
id = "WI-1031"
title = "docs/process.toml is validated against a kit-owned schema, and a re-sync adds settings but never overwrites values"
workstream = "process"
sr_refs = ["SR-137", "SR-036", "SR-031"]
needs = []
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
buildtier = "strong"
safety_class = "high-risk"
priority = 4
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(the queue drill's hand-off, §3.3 N2: the operator chose to build variant F
first and asked that the rest of phase 3 keep its rows). This is item 10's
step 3 ("adopter-owned values, kit-owned schema"), ruled 2026-10-11 with
the clarifications of revision 5.

Steps 1 and 2 have shipped. WI-915 parses `docs/stack.ini` in one place
(`kitlib/config.py`). The hooks read the privacy policy through
`check_privacy.py --hook-policy` after the 3.11 interpreter check
(`hooks/kit-python.sh`), so the shell grep, and with it the one-key-per-line
shape rule, can go (revision 5, not objected).

Today `docs/process.toml` (341 lines) and its template (497 lines) are
checked two ways. Each reader refuses a value it does not recognize
(`agent_policy.py`), and SR-137 refuses a duplicate or wrong-typed dial. But
an unknown table or key is silently ignored, and
`test_dogfood_sync.test_process_toml_declares_the_templates_keys_section_by_section`
requires the live file to hold every key the template holds. `RESYNC_PACK.md`
tells an adopter to "overwrite, then re-apply your dials" and warns that
`--force` resets every dial. The ruling replaces that: the kit owns the
schema, the adopter owns the values, and a re-sync adds new settings without
overwriting any value. Re-sync is applied by an LLM from the RESYNC entry;
no new migrator is built (item 10 ruling). The operator ruled on 2026-11-21
that re-sync need not be one entry, so this row carries its own.

**Named failure class.** On 2026-08-08 a value inside a trailing comment
made the privacy gate fail open (`docs/log.md`, the decoy-comment finding).
The validator reads `privacy_check` and `privacy_review`, so text in a
comment or in another key's string must never count as either key.

## Trust

The validator gains authority over a gate: the commit checks fail on a
`process.toml` it refuses. It is written by hand (the adopter, the operator,
an agent) and by one script route, `bootstrap.set_process_key`, which
rewrites one line in place. Its consumers are every reader through
`agent_policy.process_config`, the self-contained readers, and
`check_privacy.py --hook-policy`. One ruling applies to all of them: a file
that `tomllib` cannot parse, an unknown table or key, a key in the wrong
table, and a value outside its declared type or set are all refused, naming
the key and its table. An absent key reads as its declared default, as the
readers do today. PROCESS.md §3, "When a guard is owed", governs.

## Done-when

- [ ] One schema declares every `process.toml` setting: its table, key,
      type, allowed set or range, and default. It lives in one kitlib module,
      and the template's values equal its defaults (a test).
- [ ] One validator applies that schema and refuses per the Trust ruling.
      The commit checks run it, and the readers load through it.
- [ ] The structure test changes from "live declares the template's keys" to
      "live satisfies the schema".
- [ ] A test plants decoy privacy values in a trailing comment and inside
      another key's string. The validator and `--hook-policy` both read the
      real value.
- [ ] Where a row or the template header still states the one-key-per-line
      shape, it is amended. An accepted row changes text only, and its act
      goes to adjudication (§3.3 N4).
- [ ] `RESYNC_PACK.md` replaces "overwrite, then re-apply" with "add the new
      settings, keep your values" in its own entry; no new migrator.
