## 2026-10-15 (h) — attended coordinator: the process-text row through its checkpoint; the owner's plausibility rulings

The eleventh attended coordinator session under the review-churn program
(handoff-2026-10-15g-attended-coordinator). It took the batch's process-text
row through its rebase and checkpoint, dispositioned both critique rounds of
the trunk-hold row, recorded the store-lock row's stress re-run, and, at the
owner's request, traced and closed a gap in how reviews dismiss contrived
scenarios.

- **WI-911 (B1 text):** rebased onto trunk's tip (D-015: two conflicts, the
  recipes' retired by-hand bullet and RESYNC_PACK.md; no lane code or row
  changed, so no rebase round). Terra reconciled the set in three turns; the
  closure check found two TC clauses no requirement stated, fixed before the
  sitting. The owner's text fix landed in the lane (D-016, D-017): PROCESS.md
  section 6 now dismisses contrived scenarios, reachability gates every
  severity class, a spec's promise reaches only supported routes, and the
  dispute brief weighs plausibility. Sitting 010 blessed every LLR and TC
  (act seq 117) and returned SR-234 for a bound its Requirement did not
  state; the rework went through TC-334 (D-018), and re-sit 011 blessed
  SR-233, SR-234, SR-236 and TC-334 (act seq 118). The gate is next.
- **WI-925 (the trunk reference-update hold), still queued:** round 1
  (Sol): two MAJORs adopted, the pre-filter's base and the Q8 exemption's
  carrier contract (coordinator-2026-10-15 D-006). The confirming round
  raised a fail-open MAJOR, a strict rewind of trunk judged over an empty
  delta; the owner asked when it could occur, the answer was only by a hand
  rewind no kit route makes, and the owner dismissed it, keeping a word fix
  (Q8's exemption covers fast-forwards only) (D-009).
- **Why a contrived fail-open got through:** the owner's 2026-10-13
  plausibility ruling had reached only a plan-review brief, never PROCESS.md
  section 6, and the shipped severity rule ("reachable in normal use, or a
  fail-open, data-loss or security path") exempted any fail-open from
  reachability. A read-only audit of accepted MAJORs since 2026-10-08 found
  15 of 52 contrived, every one from Sol, with three patterns: the critic's
  stock trust-boundary framing, over-broad promises in specs, and dispute
  sittings that weighed cost but not plausibility. The owner held WI-922 and
  WI-925 for a re-scope against the ruling before any lane is cut (D-010).
- **WI-923:** the coordinator's P2 re-run matches the builder's: trunk's code
  lets 161 access refusals escape in 15833 holds, the change none in 16184.
- **Bars:** smoke 34.5 to 42.0 s across the session, all quiet, at
  below-normal priority; trunk's strict lints clean apart from LLR-292. No
  trunk code changed, so the full suite was not run.
