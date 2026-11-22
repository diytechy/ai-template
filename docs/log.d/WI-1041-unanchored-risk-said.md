## 2026-11-21 — WI-1041: an accepted risk no acceptance act names is reported unanchored, not bound to a commit found in history

Deferred open items: none. The act owed (LLR-239's drift) goes to automated
adjudication, which the operator-acceptance dial releases, and this session
took no operator decision.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1041` from `ca7039691`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1041-unanchored-risk-said.md`).

- **The reader** (`7440bc961`): with no act ledger entry naming the
  assumption, `baseline_snapshot.risk_acceptance_act` returns no anchor.
  Its reason names the assumption, says its accepted risk is unanchored and
  tells the operator to accept it in an acceptance act. It no longer walks
  the live registry's history for the first commit at which
  `accepted_risk` took its current value (the history-reader audit's class
  (c) site 2, now marked resolved). `_risk_first_written` had no other
  caller and is deleted.
- **Callers**, none changed: the risk view, `record_observation`'s evidence
  read (IF-217's requestor), the pure risk rule, `trace.py`'s advisory and
  the release gate's `assumption-evidence` step already read no anchor as
  unproven with the reason. Such a risk now reads unproven, not covered,
  and the RESYNC entry tells an adopter to accept it in an act.
- **LLR-239** (`Accepted`): text only, the fallback sentence replaced. No
  test case stated the fallback, so none drifts. No id was minted.
- **Tests:** the new case failed on the base and passes now.
  `test_accepted_risk`: `15 passed in 16.87s`. The 24 modules importing
  `baseline_snapshot` plus `test_spine_carrier`:
  `1075 passed in 1225.30s (0:20:25)`. The whole-tree ratchet, layer and
  dogfood modules: `55 passed, 1 skipped in 11.03s`. The RESYNC pack's 8
  readers: `102 passed in 61.50s (0:01:01)`. `run_menu.py smoke`:
  `3714 passed, 3 skipped, 18 warnings in 391.95s (0:06:31)`, with a CPU
  budget WARN only. `trace.py --strict`: `orphans=0 integrity=0`;
  `check_trajectory.py --strict`: clean. The unfiltered suite was not run.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** `RESYNC_PACK.md` 737,613 -> 738,909 (unbudgeted). No
  budgeted file was touched.
- **Acts owed:** LLR-239's re-acceptance (its Detail drift).
