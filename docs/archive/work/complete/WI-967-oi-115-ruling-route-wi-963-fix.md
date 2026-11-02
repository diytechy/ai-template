+++
id = "WI-967"
title = "The act ledger records the registries each act copied, so WI-963's settlement holds on a squashed landing"
workstream = "process"
sr_refs = ["SR-178"]
specref = ""
needs = ["OI-115"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

The act-ledger preparatory row OI-115 ruled (a): every new act-ledger
entry records `copied`, the sorted registry files its act actually wrote,
so a traced re-anchor naming no row, a mixed act and a re-seed each name
every file they copied. A legacy entry parses unchanged and reads as copy
set unknown, never empty. The whole-file rule refuses a malformed
`copied` and an entry omitting it after one that carries it; the
commit-bound rule (`added_acts_findings`, on the integrity floor) refuses
an entry a commit adds without it or naming a file outside the snapshot's
registry files. One home for "which entries a commit adds"
(`acceptance_record.added_ledger_entries`). IF-220 states the shape (v2);
LLR-361 and TC-400 carry it (sitting 004, act seq 165, whose own entry is
the first to carry `copied`). One RESYNC entry. WI-963 now rebases onto
this landing and builds its settlement from the ledger.

## Context

Filed by hand in headless leg 08 (2026-10-21) with OI-115, as the queued
placeholder row a pending open item is filed with (OI-102). The owner ruled
OI-115 on 2026-11-01, option (a): this row becomes the preparatory row for
the act ledger's producer, landed as its own lane before WI-963, which then
rebases onto it and builds its settlement fix from the ledger. The problem
and the questions its scope critique answers are in its spec of record,
`docs/specs/WI-967.md`. It owes that scope critique before its claim, and it
lands alone: it changes the act ledger the cycle runs on.

## Done-when

- [x] OI-115 ruled 2026-11-01 (a): a preparatory row for the act ledger's
      producer, landed first; WI-963 rebases onto it.
- [x] The scope critique's recommendations are dispositioned in this row
      before its claim, and a confirming round passes. — DONE:
      coordinator-2026-11-01 D-006 (the four dispositions) and D-007 (the
      confirming round's APPROVE)
- [x] Every act-ledger entry the snapshot writer appends names the
      registries its act copied, driven through the real producer for each
      act shape the spec lists: an approval or re-attestation act, a traced
      re-anchor naming no row, an act mixing `--approves` on one registry
      with ids in another, and a re-seed.
- [x] The ledger's validators refuse an entry a commit adds (read against
      its parent by `seq`, as the ledger's readers already identify added
      entries) that omits the record or names a registry outside the
      snapshot's own registry files, and refuse a whole ledger in which an
      entry omits it after one that carries it. An entry written before
      this row parses unchanged and reads as copy set unknown, never as an
      empty one, and no reader infers it. Tests drive both sides. Coverage
      bound: the ledgers the snapshot writer and the kit's own routes
      produce (PROCESS.md §6); a hand-edited ledger is outside it.
- [x] IF-220's row states the new entry shape, and its consumers list is
      the grep's.
- [x] One RESYNC entry tells an adopter what their ledger gains and that no
      existing entry is edited.
- [x] The commit bar is green, and both strict lints (`trace.py --strict`,
      `check_trajectory.py --strict`) are clean on the landing tip.
