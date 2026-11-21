+++
id = "WI-1013"
title = "A delegated run records only the calls no spine row states and that are not about conducting the run itself"
workstream = "process"
sr_refs = ["SR-225"]
specref = "docs/reviews/2026-11-20-decisions-overlap/README.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand on 2026-11-20 at the operator's direction. The decisions
records under `docs/decisions/` hold 1,193 entries from 132 runs between
2026-09-28 and 2026-11-20. The operator reads them only when they suspect a
run's choices carry risk (DA-020 as restated on 2026-11-20), and nobody can
read that volume, so a record is worth what an audit can find in it.

A judged sample of 106 entries, weighted back to the whole
(`docs/reviews/2026-11-20-decisions-overlap/`), puts them at:

- about 58% the conduct of the run: triage of review rounds, ceiling and
  budget re-stamps, commit grouping and order, working around a tool or
  environment failure;
- about 10% restating a spine row, usually an LLR the same run wrote or
  amended (LLR-306 holds wi-835's D-011, D-012 and D-015 almost word for
  word), and about 9% partly so;
- about 12% readings of scope, and about 11% design choices no spine row
  states.

The routing table in `PROCESS_OPTIONS.md` "Delegated decisions record"
sends every call that "touches a registry, the spine or a kit-owned file"
to the record, which is why the first two groups land there. Entries also
go stale once later work changes the spine: wi-841 D-002 places a hold in
`worker_endstate`, which LLR-309 now says asks no hold.

The operator's rule: "if the spine surfaces behavior that was selected,
there is no need to mention it as a decision."

## Done-when

- [ ] The routing table and `decisions.template.toml`'s header say that a
      call whose selection a spine row states, whether the run wrote it,
      amended it or found it standing, is not recorded: the row is its
      record.
- [ ] They say that a call about conducting the run is not recorded
      either: who reviewed and in which round, commit grouping or order, a
      re-stamp whose own ledger carries its reason, working around a tool or
      environment failure. The commit and the log fragment carry it. A
      review finding's outcome is judged by what it changes, so an outcome
      that selects a design no spine row states is still recorded.
- [ ] What is left to record is stated plainly: a reading of scope, and a
      design choice no spine row states.
- [ ] The instruction each build and adjudication session is handed under a
      recording dial says the same, read from the one home rather than
      copied.
- [ ] The confidence ratchet is unchanged: low confidence or a reviewer's
      dissent can still promote a call to the record or to an exit.
- [ ] The existing records stay as written; nothing rewrites or prunes them.
- [ ] A RESYNC entry tells adopters what the routing now leaves out, and
      that their records need no migration.
- [ ] The scope critique settles whether SR-225 or an LLR states the
      routing and so needs an amendment; any amendment is drafted for the
      operator's acceptance.
