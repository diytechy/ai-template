+++
id = "WI-1013"
title = "A delegated run records only the calls no spine row states and that are not about conducting the run itself"
workstream = "process"
sr_refs = ["SR-225"]
specref = "docs/reviews/2026-11-20-decisions-overlap/README.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
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

### The delta

The routing table in `PROCESS_OPTIONS.md` "Delegated decisions record" is
the one home for what a run records. Two places copy it today and follow it:
`decisions.template.toml`'s header, and the instruction
`kitlib.decisions.session_note` returns, which `agent_loop.session_body`
appends to a build or adjudication session's body under `record` or
`escalate-first` (LLR-283, LLR-284). The instruction's text says "one
[decision.D-<n>] table per call that touched a registry, the spine or a kit
file, or that you are unsure of". It comes to name the table's home and the
two kinds of call left to record, and stops restating the routing.
`session_note` keeps its signature, so IF-256 is unchanged; the seam
`agent_loop` → `kitlib.decisions` already exists. No state, domain value or
boundary is added.

SR-225 states the record's mechanics (its required fields, the close
refusal, the overrule coupling) and not which calls go in it, so it is not
amended. LLR-283 states what `session_note` returns, so its detail is
amended to the new instruction. LLR-283 is `Accepted`: the amendment
changes its text only, stays `Accepted` and shows as drift for the
operator's re-accept, and lands in a commit before any act.

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
      design choice no spine row states. Anything else is not recorded by
      default: a call none of the lines above names goes in the record only
      when it is one of those two kinds, or when the confidence ratchet
      promotes it. The routing covers the calls a build or adjudication
      session makes under a recording dial through the kit's routes.
- [ ] The instruction each build and adjudication session is handed under a
      recording dial says the same, read from the one home rather than
      copied: `session_note` names the routing table's home and the two
      kinds left to record, and a test pins that it no longer carries the
      "touched a registry, the spine or a kit file" routing.
- [ ] The confidence ratchet is unchanged: low confidence or a reviewer's
      dissent can still promote a call to the record or to an exit.
- [ ] The existing records stay as written; nothing rewrites or prunes them.
- [ ] A RESYNC entry tells adopters what the routing now leaves out, and
      that their records need no migration.
- [ ] LLR-283's detail is amended to the instruction's new content, text
      only, for the operator's re-accept ("The delta"). SR-225 is unchanged.

## Critique dispositions

Round 1 (OpenAI Sol, low, 2026-11-21; Gemini Argon timed out, so Sol
reviewed alone; `docs/reviews/2026-11-21-scope-critiques/WI-1013.md`):
CHANGES-REQUESTED, two findings. Sol could not settle the last Done-when
item from the sources it read, so the coordinator settled it from SR-225 and
LLR-283's text.

- **S4 (MAJOR), `planmode` missing: adopted as `planmode = "single"`.** The
  row promises a routing over the space of a run's calls and changes both a
  shipped doc and the instruction code hands a session, so a short plan
  fixes the wording of the one home and what `session_note` says before the
  code (`docs/plans/WI-1013/plan.md`).
- **S3 (MINOR), no bound and no default for an unclassified call:
  adopted.** The third Done-when item now states the default (not recorded
  unless it is a scope reading or a design choice no spine row states, or
  the ratchet promotes it) and the bound (the calls a build or adjudication
  session makes under a recording dial through the kit's routes).
- **The amendment question (the last Done-when item as filed): settled.**
  "The delta" records that SR-225 does not state the routing and that
  LLR-283 states `session_note`'s content, so LLR-283 is amended and SR-225
  is not. The fourth Done-when item names the test that pins the change.
