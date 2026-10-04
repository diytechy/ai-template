+++
id = "WI-799"
title = "Lane-state provider that derives each lane's state from evidence, representation only"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-lane-state-provider"
needs = ["WI-797"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-lane-state-provider (ch.1 §1-§6, §9.2). A
lane's state is derived, never stored (B1): `kitlib/station.py` holds the pure
enums and `state_of`, and `scripts/lane_state.py` gathers evidence and is the one
door for lifecycle effects (`derive`, `census`, `decide`, `enact`), per D-005.
`MERGE` is read from trunk's tree, not ancestry (D-002, README change 19); liveness
comes from the dispatcher's handles or a lock probe, never a pid file (D-006). The
slice is representation only (B12): today's flow moves onto it unchanged and it
adds no locking, minting or archive ordering. It also retires `out/review-owed`
and folds the two review-owed readers into one (D-007, D14), removes the D13
re-exports, and probes F3 (`refs/stash` across worktrees) in its
`STASHED_LEFTOVERS` fixture (ch.1 §8).

## Done-when

- Every ch.1 §2.1 transition and decision goes through `enact` or `decide`, and no
  lifecycle module calls another's effect directly.
- There is a pure test per state and per condition.
- A repo fixture covers each ch.1 §5 crash shape; the `STASHED_LEFTOVERS` fixture
  also probes F3.
- The existing `test_dispatch`, `test_integrate_*`, `test_handback*` and
  `test_agent_loop_*` suites pass with only call sites edited.
- No new lock, mint or archive ordering is added.
- The import rank is enforced (`tests/test_import_layers.py` `LIFECYCLE_RANK`).
- `out/review-owed` is retired, one `REVIEW_OWED` reader remains, and the D13
  re-exports are gone.
- Each spine row the README matrix gives this row (LLR-140 `code_symbol`, LLR-150,
  LLR-182, IF-136, IF-173 shared with WI-808, TC-205, and TC-132/143/144 only if a
  cited test moves; a new LLR, IF and TCs for `lane_state`) is amended or added and
  passes adjudication of that row, on whichever adjudication path is the one path
  when this row lands. `docs/runtime-flows.md`, `docs/iteration/wi-lifecycle.html`
  and `docs/registry-machinery-reference.md` name the provider and its states.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus a fixture per crash shape (the F3 probe).
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; kit-owned files only, and a
  stray `out/review-owed` is ignored.
