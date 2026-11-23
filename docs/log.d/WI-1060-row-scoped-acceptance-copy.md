## 2026-11-23 — WI-1060: an acceptance act writes only the rows it names; one unblessed row no longer blocks its registry

Built on `maint/wi-1060` (rebased onto `refactor_again` at `121ce2e00`) under
the plan `docs/plans/WI-1060/plan.md`, which the coordinator approved on
2026-11-23 before any build, with D4 corrected (an act that would write
nothing stays refused, naming the rows that stay owed). The spec's Deliverable
holds the per-item record, the approval and the acts owed.

- **What changed.** `intake.py snapshot` writes the acceptance record row by
  row (`scripts/record_rows.py`, new, CMP-006): the rows an act names (its
  flips, rows born accepted, `--reaccepts` ids and retirements) are copied
  byte for byte from live; an unnamed row keeps its recorded text while its
  accepted cells or its routed links (`SN-Refs`, `Boundary-Refs`, `SR-Refs`,
  `Verifies`) differ from live; every other row follows live. Rows keep live's
  order with live's bytes around them, so an act that keeps nothing writes the
  live file exactly as before. A kept row no longer refuses the act: it is
  printed as LEFT OWED and listed in a new act-ledger field, `kept`. An act
  that would write nothing over drift is still refused. The writer composes
  and re-reads every copy before writing anything. The mirror checks judge a
  copy at the row once the ledger holds an entry carrying `kept`, name each
  fault by its row, and refuse deleting the ledger while the record stands; a
  record written before that is judged as written, so no record migrates.
- **Rows.** Fifteen accepted rows amended, text only, all owed to a sitting
  (SR-207's shown to the operator): SR-140, SR-179, SR-207, LLR-173, LLR-178,
  LLR-245, LLR-271, LLR-361, LLR-364, TC-167, TC-173, TC-240, TC-269, TC-400,
  TC-403; IF-220 (Drafted, off-spine) rewritten. No id minted.
- **A hole closed.** A whole-file copy could re-anchor a held-rung MEANING
  row's routed link through another row's act, so the held-act mint read it
  settled and minted no operator row; the routed link now waits for its row's
  own act (TC-147's new test).
- **Deviations from the plan:** D4 as the coordinator corrected it; the first row of a copy
  carries no leading lines (so a comment-only preamble stays live's head); a
  re-seed reads its previous copy; the legacy-carrier refusal names rows and
  cells; `kept` is shape-checked as a list of ids; more of the judge than
  planned lives in `record_rows` (the size ratchet), injected with the judge's
  own readers; a merge's act-ledger entries brought in over the first parent
  name their rows; a template example row (`-000`) follows live (a defect the
  wide run found: the shipped needs template's `STK-000` reads `Accepted`); the
  held-act two-landings test rewritten; SR-179's acceptance bounded; the
  complexity entry for `committed_snapshot_findings` deleted and `intake.py`'s
  size baseline re-stamped down (1,946 -> 1,944). The spec's Deliverable
  holds each, with its reason.
- **Byte deltas on budgeted files:** `PROCESS.md` +58 (102,060 -> 102,118,
  watched); `PROCESS_OPTIONS.md` -13 (202,593 -> 202,580, watched).
- **Tests:** red first `1 passed, 32 xfailed in 42.65s`; the 79 importer
  and named modules `4 failed, 2940 passed, 1 skipped in 2484.84s` (the four
  fixed or explained in the Deliverable), then the 18 record-heavy modules
  `664 passed, 1 skipped in 1760.66s`; `run_menu.py smoke` `3768 passed, 3
  skipped, 18 warnings in 163.92s`, exit 0 (CPU 671.9 s over the 540 s budget,
  reported only, on a box shared with two other builders); `trace.py --strict`
  and `check_trajectory.py --strict` exit 0. The hook's integrity step: before
  8.58 s to 9.02 s, after 9.32 s to 10.94 s. The unfiltered suite is the
  coordinator's, before the merge.

<!-- fig: cmd="python -m pytest -q -n auto <modules>; python project-trajectory/scripts/run_menu.py smoke; pwsh Measure-Command trace.py --root . --strict-integrity x3 before and after" rev="maint/wi-1060 at 72f0a63ca (and its tree before it), 2026-11-23" -->
- Deferred open items: none — the row's one operator decision (SR-207's
  amendment) is shown to the operator by the coordinator, and every amended row
  goes to the next sitting as an owed act.
- **Review:** round 1 Hydrogen APPROVE; Sol (code and docs halves) two
  MINORs adopted (a row's acting reviewer read at the row; the README's
  deletion rule), four dismissed (the migrator's record step is WI-1065).
  Round 2, narrow: Sol and Hydrogen APPROVE.
