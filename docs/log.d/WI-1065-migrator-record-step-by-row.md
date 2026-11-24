## 2026-11-23 — WI-1065: the vocabulary migrator writes no record copy in a row-by-row record, and refuses one still in the earlier vocabulary

Built on `maint/wi-1065` (cut from `refactor_again` at `c7d6bd6f4`) under the
plan `docs/plans/WI-1065/plan.md`, which the coordinator approved on
2026-11-23 before any build, D3 confirmed and D7 adopted. The operator's
ruling, refined (c), is the spec's. The spec's Deliverable holds the
per-item record, the approval and the acts owed.

- **What changed.** `migrate_vocabulary.py` reads the acceptance record's act
  ledger before its first step, as the kit's scripts read it. A record with
  no entry carrying `kept` is migrated as before. Once one does, a record in
  the current vocabulary has no copy written, so a run for other files and
  check mode pass the hook and the committed-history check with kept rows and
  pending drift present; a record still storing an earlier spelling (the
  earlier directory, an earlier ledger key, or a copy the registry step would
  rewrite or cannot prove) refuses the whole run before the registry step's
  walk of the record, nothing written, exit 1 in both modes, and the
  vocabulary check reports the refusal through IF-312. No core module
  changed.
- **A defect fixed (D7).** The Markdown link walk read the operator's
  scratchpad, and could rewrite a link in it, on every run and every
  vocabulary check; it now skips the scratchpad under either name. One
  measuring run before the fix, over this worktree, had the migrator read
  this repository's scratchpad in process (nothing printed, nothing written);
  the migrator was not run over this repository's tree again.
- **Rows.** SR-247 (`acceptance_criteria`, `rationale`), LLR-369 (`title`,
  `detail` rewritten whole without code names, `rationale`) and TC-427
  (`method`) amended, text only, all owed to a sitting; SR-179 and LLR-178
  unchanged. No id minted, no new row.
- **Deviations from the plan:** the hook's integrity step is compared before
  and after the run (a two-row tree carries findings of its own); the
  repository-level `--check` figure was taken over a copy of this
  repository's registries and record, per the coordinator's ruling (the
  migrator at `c7d6bd6f4`: exit 1, 79 lines; built: exit 0).
- **Byte deltas on budgeted files:** none (no budgeted or watched file
  changed).
- **Tests:** red first `79 passed, 14 xfailed in 52.72s`; after the build the
  two migrator modules `93 passed in 46.92s`; the 12 importer, runner, record
  and ratchet modules `294 passed, 1 skipped in 282.50s`; `trace.py --strict`
  and `check_trajectory.py --strict` exit 0; `run_menu.py smoke` `3887 passed, 3 skipped, 18
  warnings in 146.21s`, exit 0 (CPU 687.9 s over the 540 s budget, reported
  only); the tier now sits at its `max-tests` ceiling of 3,890.

<!-- fig: cmd="python -m pytest -q [-n auto] -p no:cacheprovider --basetemp <scratch> <modules>; python project-trajectory/scripts/run_menu.py smoke" rev="maint/wi-1065 at b92a67bfc and 47e762418, 2026-11-23" -->
- Deferred open items: none — the operator's design call was ruled before
  filing (refined (c)), and the three amended rows go to the next sitting as
  owed acts.
