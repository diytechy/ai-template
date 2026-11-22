## 2026-11-21 — WI-1040: the re-acceptance brief names the last acceptance act from the act ledger

Deferred open items: none. No act is owed, and this session took no
operator decision. One finding goes to the coordinator: the shared ledger
walk does not see across the record's move (below).

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1040` from `dd8f79e6c`, with the
commit hooks on. The plan is `../plans/WI-1040/plan.md` and the record is in
the row's Deliverable
(`../archive/work/complete/WI-1040-last-act-date-from-ledger.md`).

- **The heading** (`ea59f2a83`). The brief's `_Acceptance provenance:` line
  reads `baseline_snapshot.last_act`: the act ledger's newest entry and the
  commit that added it. It no longer reads the newest diff touching a
  `status =` line, which on trunk named WI-1021's build, a commit that
  accepted nothing. With no ledger, or an empty one, it says no act is
  recorded. When the entry's commit is not in the readable history (a
  shallow clone, an act not yet committed, no git), it gives the entry's
  date and names no other commit. `acceptance_stamp` is removed. The
  history-reader audit's class (c) site 1 is marked resolved.
- **One walk.** The accepted-risk anchor's walk over the ledger's commits
  is now `_ledger_commits`, and both readers call it; `risk_acceptance_act`
  is unchanged in behaviour.
- **Finding:** the walk follows the ledger's current path only, so
  `2bee2b551`, the record's 2026-11-16 move, reads as adding all 182
  entries it held. The heading is right here, since seq 185 postdates the
  move. A repository whose newest act predates its own move would see the
  move commit named, and `risk_acceptance_act` shares the limit.
- **Design call:** `../decisions/maint-wi-1040.toml` D-001, the outcomes for
  the states the spec does not name.
- **Tests:** seven new, red first on the old code (the draft test failed on
  the heading naming the draft's commit) and then green. The 95 modules
  that import or run the two scripts: `80 failed, 3067 passed, 2 skipped`.
  All 80 came from the run's long `--basetemp` path, and their nine modules
  pass whole on a short one: `414 passed in 2354.43s (0:39:14)`.
  `run_menu.py smoke`: `3714 passed, 3 skipped, 18 warnings in 237.51s
  (0:03:57)`, with a CPU budget WARN only. `trace.py --strict`:
  `orphans=0 integrity=0`. The unfiltered suite was not run.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Sizes and bytes:** `trace.py` re-stamped down 3844 -> 3835 SLOC;
  `baseline_snapshot.py` 987 SLOC, under the threshold. `RESYNC_PACK.md`
  737,613 -> 738,955 (unbudgeted). No budgeted file was touched.
- **Acts owed:** none.
