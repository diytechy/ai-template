## 2026-11-21 — WI-1013: a delegated run records only scope readings and design choices no spine row states

Review round 1 (Sol, low): two findings, both fixed in `81b24a125`. Sol
(low) reviewed alone; Argon timed out and was skipped. Review round 2
(Sol, low, narrow over `6969c7e16..17ee547c1`): APPROVE, no findings.

- MAJOR: `PROCESS.md` §6 and the `coordinator-cycle` skill still sent the
  run's conduct to a decisions record; both now follow the routing table.
- MINOR: TC-293 (g) overstated the change; it now says touching a registry,
  the spine or a kit file no longer routes a call to the record by itself.

Deferred open items: none — the row's one open question (D-002) was ruled
by the coordinator and fixed in this row.

Built on the maintenance branch `maint/wi-1013`, outside the lane workflow,
at the operator's direction, with the commit hooks on.

- **The routing** (`PROCESS_OPTIONS.md` "Delegated decisions record", still
  the one home): it now covers the calls a build or adjudication session
  makes under a recording dial. A reading of scope or a design choice no
  spine row states is recorded. A choice a spine row states goes to the row,
  "the row is its record". The conduct of the run goes to the commit and the
  log fragment. A review finding's outcome routes by what it changes, and any
  other call stays out unless the confidence ratchet promotes it. The ratchet
  and the `escalate-first` rule are untouched.
- **Its two copies:** `decisions.template.toml`'s header says what goes in a
  record and what does not. `kitlib.decisions.session_note` names the
  table's home and the two kinds of call left to record, in place of "touched
  a registry, the spine or a kit file". Its signature is unchanged (IF-256).
- **Tests:** two in `tests/test_decision_record.py` (TC-293), red first. Each
  kind the note names must be found in the routing's home and in the
  template's header, so the note cannot name a kind its home does not hold.
- **Rows:** LLR-283's `session_note` clause and TC-293's clauses (g) and (i),
  text only. Both stay `Accepted` and show as drift for re-acceptance.
  SR-225 and IF-256 are unchanged, and no id was minted.
- **Records:** nothing under `docs/decisions/` is edited, the stale
  `run-000-example.toml` included (D-001). The branch's own record,
  `docs/decisions/maint-wi-1013.toml`, holds two entries under the new
  routing.
- **Review round 1:** `PROCESS.md` §6 drops its dismissal-to-the-record
  clause, with SR-233, LLR-311 and TC-332 amended to match, text only. The
  `coordinator-cycle` skill (all three copies) records a call only when the
  routing table routes it there. Dismissals, re-grades, dispute rulings and
  the convergence map go to a commit message, because a convergence reviewer
  reads the log fragment but not commit messages. Reviewer stand-ins, failed
  commit-check rounds and the other run-conduct notes go to the commits and
  the log fragment (D-002).
- **RESYNC:** one entry; nothing is forced and no record migrates.
- **Byte deltas:** `PROCESS_OPTIONS.md` 201,438 -> 202,180 (+742, watched).
  It had drifted +1,897 unflagged since its 199,541 stamp, and is now
  re-stamped. `PROCESS.md` 100,990 -> 100,922 (-68, watched).
  `byte-budget-guard/SKILL.md` 4,613 -> 4,615 (cap 5,000).
