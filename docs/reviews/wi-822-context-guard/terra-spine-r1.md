Spine rows drafted; no statuses changed and no interface row added.

- SR-229, all cells: new → “Coordinator context-drain admission” / SN-027 / cross-cutting. Separates lease-held threshold admission from implementation details.
- SR-230, all cells: new → “Coordinator successor at session exit” / SN-027 / cross-cutting. Separates exactly-once successor continuity.
- LLR-300, all cells: new → coordinator occupancy, lease, latch, hook, and claim-admission design. Covers the guard and integrator boundary.
- LLR-301, all cells: new → atomic relaunch request, exit acquisition, and platform launch design.
- LLR-140 `detail`: amended to add the enabled context-guard refusal before its existing claim ladder. The integrator now executes that rung.
- LLR-270 `code_symbol`: amended `…/store_lock/…` → `…/primary_out_dir/store_lock/dir_lock/…`; `detail`: amended to define the shared primary-runtime-store and lock extraction.
- TC-315–TC-318, all cells: new → concrete occupancy, lease/latch, claim-boundary, and relaunch evidence using the actual guard tests.
- `docs/id-watermark`: bumped SR `228→230`, LLR `299→301`, TC `314→318`.

Builder-list disposition:

- New SR: confirmed, but split into SR-229 and SR-230 to keep one decision per row; anchored to existing SN-027.
- LLR A/B: confirmed as LLR-300 and LLR-301.
- LLR-270 and LLR-140 amendments: confirmed and made.
- Interface row: refuted. `coordinator_guard.py` declares no `Contracts:` seam, so minting an interface row would invent a contract. Its existing connectivity warning remains advisory.
- TC coverage: confirmed and extended into four evidence-specific cases.
- Added `form = "cross-cutting"` to both new SRs.

Checks:

- `check_trajectory.py --strict`: PASS — `clean (819 work item(s), 721 done (88%), 26 cancelled, graph acyclic).`
- `trace.py --strict`: expected exit 1 solely for pre-existing `LLR-292 Detail uses 'minimal'`; new integrity result is `integrity=0`, `orphans=0`.
- Required pytest command with `-n 0` and the mandated basetemp: could not complete because stale child Python processes held the basetemp on Windows. It produced lock errors after `23 passed, 1 skipped`; I terminated only those test-owned orphan processes afterward. No functional assertion failure was reported.

The only unresolved item is rerunning that full pytest command in an environment where its child processes can complete and release the mandated basetemp.