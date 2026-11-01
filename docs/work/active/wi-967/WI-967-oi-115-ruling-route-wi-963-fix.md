+++
id = "WI-967"
title = "The act ledger records the registries each act copied, so WI-963's settlement holds on a squashed landing"
workstream = "process"
sr_refs = ["SR-178"]
specref = "docs/specs/WI-967.md"
needs = ["OI-115"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

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
- [ ] The scope critique's recommendations are dispositioned in this row
      before its claim, and a confirming round passes.
- [ ] Every act-ledger entry the snapshot writer appends names the
      registries its act copied, driven through the real producer for each
      act shape the spec lists: an approval or re-attestation act, a traced
      re-anchor naming no row, an act mixing `--approves` on one registry
      with ids in another, and a re-seed.
- [ ] The ledger's validators refuse an entry a commit adds (read against
      its parent by `seq`, as the ledger's readers already identify added
      entries) that omits the record or names a registry outside the
      snapshot's own registry files, and refuse a whole ledger in which an
      entry omits it after one that carries it. An entry written before
      this row parses unchanged and reads as copy set unknown, never as an
      empty one, and no reader infers it. Tests drive both sides. Coverage
      bound: the ledgers the snapshot writer and the kit's own routes
      produce (PROCESS.md §6); a hand-edited ledger is outside it.
- [ ] IF-220's row states the new entry shape, and its consumers list is
      the grep's.
- [ ] One RESYNC entry tells an adopter what their ledger gains and that no
      existing entry is edited.
- [ ] The commit bar is green, and both strict lints (`trace.py --strict`,
      `check_trajectory.py --strict`) are clean on the landing tip.
