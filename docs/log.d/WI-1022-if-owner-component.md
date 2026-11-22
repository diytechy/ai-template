## 2026-11-22 — WI-1022: interface rows name components, not files; one body per interface; only a call row covers an import

Deferred open items: none — every call the spec left open is settled in the
plan (`../plans/WI-1022/plan.md`), and the acts owed go to automated
adjudication.

Built on the maintenance branch `maint/wi-1022` from `1b15d07fb`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1022-if-owner-component.md`).

- **Plan** (`0b9921e98`): the mapping rule and the producing components, the
  declared scan surface, the uniqueness gate, the stricter cover, derived
  placement, the other readers, and the classification of all 134 `call`
  rows (80 crossing; 54 internal, 25 kept with the quoted rationale that
  earns them, 29 retiring).
- **Build** (`d8ac920b8`): every endpoint is a live `CMP-###` id or a
  declared `external:` party (`trace.py`, LLR-041), the party list on the
  registry header's `# External party:` lines; the `component` cell left the
  schema. `docs/stack.ini` `[arch-map] headers` declares the files outside
  `[paths] src` the contract scan and the census read; at most one file
  states each body, in a file of the owner's component (LLR-398, new). Only
  a `call` row owned by the imported file's component naming the importer's
  covers an import (LLR-067); no crossing was left uncovered. Placement in
  the component view, the interface-form gate's reach (with a `files`-mode
  fallback through the owner component), the How-SW views, the intake seam
  lines and the cadence trigger follow. 30 rows retired: the 29 internal
  ones the plan names, and IF-143, whose one requestor stopped calling it.
  LLR-398 and TC-462 to TC-467 are new and `Drafted`.
- **Two bodies found**: `dev-setup.template.ps1` repeated IF-292's and
  IF-293's bodies beside the `.sh`; the `.sh` keeps them.
- **Deviations**: the coordinator tooling under the root `scripts/` maps to
  CMP-008, not `external:coordinator` (the frame view holds each untied
  external row to a "No tie-back" note); CMP-006's notes and TC-435, TC-459
  and TC-460 amended beside the plan's list.
- **Ratchets** re-stamped down: `trace.py` 3844 -> 3789, `intake.py` 1947 ->
  1939, `gen_arch_map.py` 1657 -> 1654, `check_trajectory.py` 1657 -> 1656;
  two C901 entries deleted and six cognitive rows moved down.
  `docs/if-tc-coverage-allow` seed 116 -> 99 with the retired rows.
- **Byte deltas**: `PROCESS.md` +9 (101,959), `PROCESS_OPTIONS.md` +142
  (202,446), the byte-budget skill -8 (4,623).
- **Tests**: red first `15 failed in 2.78s`; the full suite `77 failed, 8206
  passed, 31 skipped, 18 warnings in 7631.51s (2:07:11)` (mid-run fixture
  rework, load, trunk's red, six old-shape fixtures rewritten; the reruns
  `1 failed, 815 passed, 1 skipped` and `466 passed, 1 skipped`, the one
  failure trunk's `check_vocab` G2 red in WI-1024's spec).
  <!-- fig: cmd="python -m pytest -q -n auto (and the module reruns the Deliverable lists)" rev="the worktree ahead of d8ac920b8" -->
- **Review round 1**: the two new cases `2 failed in 7.51s` on `b2c4c2725`, `2 passed in 0.25s` after; the importing modules `675 passed, 1 skipped in 165.89s (0:02:45)`; smoke `1 failed, 3716 passed, 3 skipped, 18 warnings in 80.39s (0:01:20)`, the one failure trunk's; `gen_arch_map.py` SLOC 1654 -> 1671, a reviewed bump (a listed Python file read as a module, bodies read with no marker).
  <!-- fig: cmd="python -m pytest -q -n 8 <each module listed>; python project-trajectory/scripts/run_menu.py smoke" rev="the worktree ahead of the review-round-1 commit, on b2c4c2725" -->
- **Review round 2**: the new case `1 failed, 171 deselected in 0.57s` on `edcd89c3f`, `1 passed, 171 deselected in 0.18s` after; the importing modules `676 passed, 1 skipped in 167.39s (0:02:47)`; smoke `1 failed, 3716 passed, 3 skipped, 18 warnings in 84.83s (0:01:24)`, the one failure trunk's.
  <!-- fig: cmd="python -m pytest -q -n 8 <each module listed>; python project-trajectory/scripts/run_menu.py smoke" rev="the worktree ahead of the review-round-2 commit, on edcd89c3f" -->
- **Smoke** over `d8ac920b8`: `trace.py --strict` `orphans=0 integrity=0`, `interface-findings=0`; `check_trajectory.py --strict` clean; `check_resync: OK`; the tier `1 failed, 3716 passed, 3 skipped, 18 warnings in 106.58s (0:01:46)`, the one failure trunk's.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="d8ac920b8" -->
