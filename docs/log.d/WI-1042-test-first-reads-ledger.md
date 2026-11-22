## 2026-11-22 — WI-1042: the test-first order reads when each row was accepted from the acceptance record

Deferred open items: none. The one operator-level question this row raised
(whether the check reads the record's earlier spelling, which D3 rules out)
went to the coordinator and was ruled the same day: D3 stands.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1042` from `6915cde7d`, with the
commit hooks on. The plan is `../plans/WI-1042/plan.md` and the record is in
the row's Deliverable
(`../archive/work/complete/WI-1042-test-first-reads-ledger.md`).

- **The stop and the ruling.** The spec read the record across its
  2026-11-16 move. Before the move, the record is in an earlier spelling:
  the directory `last_approved`, the ledger keys `approved`/`reattested`,
  and the copies' status `Approved`. D3 rules out readers of an earlier
  spelling. The builder stopped with both readings measured. The
  coordinator's ruling: the move `2bee2b551` is the record's cut, what it
  carries is at or before the commit that brought it onto trunk, and
  `_ledger_commits` keeps reading the current path only. The spec's Context,
  Trust ruling and Done-when were amended in the plan commit (`c2d6bc52a`).
- **The reader** (`4f62438e5`). `check_test_first.record_acceptances` reads
  the commits that wrote the act ledger or the record's registry copies,
  through the one walk, and no longer replays the registries. An act's
  commit dates what its copies first hold accepted, so a re-pointing is
  accepted at its re-accepting act. A side-branch act is ordered where it
  reached trunk. The cut dates what it carries at or before itself while
  its ledger records an act; with no ledger there, an empty one or a
  malformed one, what it carries is unread (review round 1). A gap,
  a malformed ledger on the walk, and a row accepted with no act on record
  read unread, never a pass. The history-reader audit's class (c) site 3
  is marked resolved.
- **Completeness:** in the current spelling, one change since seq 1 carries
  flips or new pairs with no ledger entry, the move (the cut); since the
  cut, none. No row to file.
- **Verdict here:** unchanged, the same OK line before and after (57 s,
  then 15 s). The cut reaches trunk's first-parent line at `f6dd5b87a`,
  the declared start. SR-247's act has its own commit `9b377be1e` (seq
  183), after the cut on the side branch, and it too reaches trunk's
  first-parent line at `f6dd5b87a`.
- **Tests:** the text-then-act test failed on the old code with the text
  commit's date, then passed. The importers and whole-tree tests:
  `1438 passed, 1 skipped in 2998.50s (0:49:58)`. The final-tree rerun:
  `122 passed, 1 skipped in 204.83s (0:03:24)`. `run_menu.py smoke`:
  `3717 passed, 3 skipped, 18 warnings in 270.61s (0:04:30)`, CPU budget
  WARN only. `trace.py --strict` and `check_trajectory --strict`: exit 0.
  The unfiltered suite was not run. Review round 1 (the cut's ledger
  validated; three new tests red on `18afb666e`, `3 failed in 29.92s`):
  `285 passed, 1 skipped in 575.67s (0:09:35)`, then smoke `3717 passed,
  3 skipped, 18 warnings in 123.05s (0:02:03)`, CPU budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Sizes and bytes:** `baseline_snapshot.py` 966 SLOC and
  `check_test_first.py` 410, both under the threshold. `RESYNC_PACK.md`
  +2,339 (unbudgeted), the kit README +352, `docs/enforcement-audit.md`
  +34. No budgeted file was touched.
- **Acts owed:** LLR-257's and TC-250's re-acceptance (text amended), and
  the first acceptance of TC-468 to TC-471 (Drafted). Amending TC-250 is
  the builder's call: two of its clauses described the replay.
- **Review:** round 1, OpenAI Sol (low) over the whole diff and Gemini
  Hydrogen (low, the Antigravity CLI) over the prose: Hydrogen APPROVE; Sol
  two MINORs, adopted, fixed in `bc0e4e056`. Round 2 narrow: both
  `VERDICT: APPROVE findings=0`.
