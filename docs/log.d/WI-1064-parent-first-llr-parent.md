## 2026-11-23 — WI-1064: the parent-first rule reads a child design row's parent link

Deferred open items: none. The one design call, which tier a design row's
`parent` cell is judged against (design rows alone), is stated by the
amended SR-245 and LLR-357, so no decisions record is written.

Built on the maintenance branch `maint/wi-1064` from `c7d6bd6f4`, with the
commit hooks on, under the plan `docs/plans/WI-1064/plan.md` (`76f388527`)
and the coordinator's go-ahead, which confirmed D1 to D8 with rulings on D3
and D7. The record is in the row's Deliverable
(`../archive/work/complete/WI-1064-parent-first-llr-parent.md`).

- **The edge:** the rule's one table (`kitlib.spine.PARENT_EDGES`) maps each
  child tier to its parent cells, and a design row gains its `Parent`, read
  against design rows alone. An accepted child under a parent design row
  that is not accepted is one parent-first finding, worded as the others,
  with the same exclusions and the same status-movement condition at the
  commit.
- **Every route, unchanged:** the standing integrity check, the hook's
  staged `parent-first` step, a lane commit's admission at the slot
  (IF-308) and the derived act's waiting flips all read that table, so each
  reaches the edge with no change of its own.
- **The re-parent (D7):** re-parenting an accepted child under a `Drafted`
  design row moves no status, so the `parent-first` step passes it and the
  hook's `registry-integrity` step refuses it with the standing finding, as
  for a re-pointed `SR-Refs`; one new test shows both edges.
- **Rows:** SR-245 (`Requirement`, `AcceptanceCriteria`), LLR-357 (`Detail`)
  and TC-396 (`Method`, `Expected`) amended in text, each owed an amendment
  act. SR-246, LLR-358 and TC-397 read and left unamended (D3): none states
  an edge list. No id minted.
- **Docs:** the `spine-authoring` skill (three copies), the registry
  machinery reference and the enforcement audit name the edge; a RESYNC
  entry anchored at `c7d6bd6f4`.
- **Byte deltas on budgeted files:** none touched.
- **Deviations from the plan:** one build commit instead of two (the RESYNC
  entry rides with the shipped change it describes); the D7 re-parent test
  added at the coordinator's ruling; the test builders leave a row's refs
  key out when it names no parent, as the full loader asks.
- **Tests:** the four touched modules `159 passed in 56.90s`; the 50
  importing and spine-linked modules `1 failed, 1957 passed, 2 skipped, 18
  warnings in 491.54s (0:08:11)`, the failure
  (`test_snapshot_readers.py::test_a_lone_retirement_on_a_held_rung_is_refused_by_row`)
  failing the same way with this branch's changes stashed and passing
  alone, so not this row's; `trace.py --strict` and
  `check_trajectory.py --strict` exit 0; smoke exit 0, `3878 passed, 3
  skipped, 18 warnings in 184.71s (0:03:04)`, its CPU line over budget
  (warn-only, WI-1039).
  <!-- fig: cmd="python -m pytest -q -n auto <the 50 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="9ed8a5268's tree; the close-out tree for smoke" -->
- Review round 1: Sol and Hydrogen APPROVE, no findings.
