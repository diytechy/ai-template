## 2026-11-24 — WI-1070: the amendment brief shows a linked row's whole text and lists the rows its moved links name

Built on `maint/wi-1070` (cut from `refactor_again` at `ec188f984`) under the
plan `docs/plans/WI-1070/plan.md`, which the coordinator approved on
2026-11-24 before any build, D1 to D12 confirmed. The spec's Deliverable
holds the per-item record, the approval, the measure and the acts owed.

- **What changed.** A shown row with a moved adjudicated link now lists its
  other nonempty accepted cells, as they read, under an "unmoved" label after
  its moved cells, so a link-only row is judged against its own text. A new
  required template slot, `{linked}`, lists once each id a moved link names,
  before or after, by its tier's identifying cells (a need's statement; a
  crossing's direction, entity and what it carries; a requirement's or design
  row's title and text; an interface's channel, owner and stated contract,
  else its data cell), each cell on one line and clipped at 2,400 characters,
  labelled as context outside every judged-text identity. The identity and
  every reader of a binding are unchanged.
- **On this repository.** Over WI-1068's 28 owed tokens the composed sitting
  grows from 188,615 to 218,919 characters: 26 interfaces listed (none
  clipped), 21 unmoved lists, and LLR-167's and TC-161's own amendments; 22
  of its 24 identity lines are byte-identical, the other two the amended rows.
- **Rows.** Amended, text only, owed to a sitting: LLR-167, TC-161, LLR-359.
  No id minted. TC-398's wording routed to WI-1071.
- **Deviations from the plan:** one test beyond the table (a linked row with
  every accepted cell moved lists `(none)`); the identity-equality pin reads
  the row's unmoved links too; forced by checks, the deferred-import window
  in `tests/test_import_layers.py` 44 -> 46 (the contract harvest's two
  function-body imports, the approved D9) and a positional `False` passed by
  name for the readability report. The Deliverable holds each, with its
  reason.
- **Byte deltas on budgeted files:** none (no budgeted file touched).
- **Tests:** red first `19 failed, 9 passed in 4.33s`; the 42 importer and
  named modules `1 failed, 2394 passed, 17 skipped in 2377.34s` (the window,
  re-stamped; rerun `36 passed in 9.57s`); `check_trajectory.py --strict`
  clean; `trace.py --strict` and so `run_menu.py smoke` exit 1 at the first
  step on LLR-484's `such as` form finding, present at the base and outside
  this row; the chain's remaining steps by hand pass, the smoke tier `3947
  passed, 3 skipped, 18 warnings in 192.10s`. The unfiltered suite is the
  coordinator's, before the merge.

<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 42 modules>; scripts/check_smoke_budget.py --mode warn; scripts/coordinator/compose_lane.py WI-1068 combined <the 28 owed tokens> ..." rev="maint/wi-1070 at dda7a821f (modules, measure) and 674492855 (smoke steps), 2026-11-24" -->
- **Review round 1:** Sol and Hydrogen APPROVE findings=0; the import window's re-stamp confirmed.
- Deferred open items: none — the operator owes no decision from this row;
  the amended rows go to the next sitting as owed acts, and the coordinator
  filed the verbatim-cell identity finding (the plan's D12) as its own row.
