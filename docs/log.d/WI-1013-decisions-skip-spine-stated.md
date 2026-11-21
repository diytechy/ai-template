## 2026-11-21 — WI-1013: a delegated run records only scope readings and design choices no spine row states

Review: pending (the coordinator).

Deferred open items: none — D-002 in the branch's record goes to the
coordinator, not the operator.

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
  `docs/decisions/maint-wi-1013.toml`, holds two scope readings under the new
  routing.
- **Left:** `PROCESS.md` §6 and the `coordinator-cycle` skill still send
  conduct-of-the-run calls (a dismissed finding, triage, dispute rulings,
  failed commit-check rounds) to a decisions record. They are outside this
  row's named surface (D-002).
- **RESYNC:** one entry; nothing is forced and no record migrates.
- **Byte deltas:** `PROCESS_OPTIONS.md` 201,438 -> 202,180 (+742, watched).
  It had drifted +1,897 unflagged since its 199,541 stamp, and is now
  re-stamped. `byte-budget-guard/SKILL.md` 4,613 -> 4,632 (cap 5,000).
