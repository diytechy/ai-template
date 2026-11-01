+++
id = "WI-987"
title = "The open-items page lists every stakeholder need and stakeholder owing an approval or a re-attest, from the same detector the approval brief reads"
workstream = "process"
sr_refs = ["SR-178"]
specref = "docs/specs/WI-987.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

Filed by hand on 2026-11-01 (attended), from the owner's report that
SN-036 does not show on `docs/open-items.html` as a spine row to
re-attest. The problem, the evidence and the questions its scope critique
answers are in its spec of record, `docs/specs/WI-987.md`. Its scope
critique runs before its claim (the `coordinator-cycle` skill, section 1).

## Done-when

- [ ] The page's approval and re-attestation section lists every row
      `baseline_snapshot.needs_owing` reports, read from that one detector
      (no second opinion of what owes): a drifted one with its moved cells
      before and after, and a first-approval one (`Drafted`, or with no
      Status cell) with its cells in full; any other row the detector
      returns is shown as it returns it. Coverage bound: the stakeholder
      need and stakeholder rows supported workflows and the kit's own
      routes produce (PROCESS.md §6); a hand-corrupted needs file or
      snapshot is outside it.
- [ ] The section's empty message is printed only when neither an SR chain
      nor a need owes, and says what it checked; the page's counts include
      the needs that owe.
- [ ] IF-126's consumed data names `needs_owing` beside `registry_stamps`
      and `SNAPSHOT_DIR`, and IF-074's data names the stakeholder needs and
      stakeholders owing an act in the approval and re-attestation section;
      IF-075 (the SR-chain model) is unchanged.
- [ ] A test renders the page over a tree with one drifted need and finds
      its card, and fails on today's renderer.
- [ ] `docs/open-items.html` is regenerated, and SN-028 and SN-036 show
      while their acts are owed.
- [ ] The commit bar is green, and both strict lints (`trace.py --strict`,
      `check_trajectory.py --strict`) are clean on the landing tip.
