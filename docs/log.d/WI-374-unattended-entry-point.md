## 2026-07-31 — WI-374: the unattended entry point (S1 — the claimer)

**One line:** a plain `agent-resume` launch now drives the serial
claim→build→integrate loop instead of exiting 2 with a map — the scheduling
front end Phase 5's dispatcher deletion took with it is back, as ~280 lines of
composition instead of 4,042 lines of machinery.

**Deliverables.** New `scripts/drive.py` (269 lines, stdlib only): the drive
loop — re-derive the ready frontier (`schedule.py`, IF-053) at the top of
EVERY cycle, claim the next queued WI in build order (`integrate.py claim`,
IF-080), run one worker session on the claimed branch's own worktree
(`agent_loop.py --worktree --wi`, IF-015), drain the serial merge queue at the
full gate bar (`integrate.py integrate`), repeat. `agent_loop.py`'s no-role
branch now delegates there (+20 lines net, itemized below) under the
coordinator lock;
[IF-015 is amended to v3](../requirements/interfaces.csv) — the contract
sentence "a plain launch refuses with the map" is exactly what changed.
Packaging: bootstrap MAPPING row + docstring, kit README row,
test_bootstrap file list. Ten tests in `tests/test_drive.py` (slow tier;
smoke membership unchanged), two of them end-to-end against the REAL
composed-tree bar on a bootstrapped scaffold — green (claim→merge→drained
banner, worker worktree GC'd) and red (bar RED stops the run with the claim
parked).

**Design calls, recorded.**
- *Mode on agent_loop, body in a sibling.* The spec's first shape (amend
  IF-015) won, but the loop's body lives in `drive.py` so the 3,006-line
  `agent_loop.py` — a named H-2 decomposition target — grows by only the
  delegation. No new seam row: the plain launch is agent_loop's existing
  Provides surface; drive.py has no CLI of its own.
- *Frontier re-derived per cycle* — this is what makes work filed mid-run
  (by a worker, a review, or a human dropping a spec into `queued/`)
  ingested in the SAME run, with no restart. Nothing is cached.
- *Parked claims resume rather than refuse.* An interrupted run leaves
  `active/<branch>/` + the branch; the next plain launch relaunches the
  worker on it before claiming anything new — the double-click that started
  the run is the one that restarts it.
- *Merged means the branch is GONE.* The integrated counter checks the ref,
  not the worker's word; a worker that reports DONE without finishing its
  branch leaves the trunk unmoved and trips the driver's own stall guard.
- *Refusals stop, never skip.* A refusing claim rung, a red bar, a held
  branch — the run ends with that exit code. The one new refusal is
  BEFORE any claim: an unwired AGENT_CMD (no template, no enable-list)
  refuses at preflight rather than parking a branch nothing can build.
- *Pause is checked every cycle,* so `docs/work/pause` dropped mid-run
  stops the next claim with the pause banner (exit 8), not a claim-rung
  refusal.

**Not built, per spec:** worktree pools, reservations, train grouping,
run-state files, a second lane. `schedule.py simulate --jobs N` remains the
way to ask the ordering question without building the concurrency.

**Deviations from spec:** none of scope. One addition the spec did not name:
the pre-claim AGENT_CMD preflight (argued above — fail before the claim, not
after it).

**Ratchet re-stamps (deliberate, this is the recorded reason):**
`agent_loop.py` 3006 → 3026 — the delegation (`_drive_entry`), the docstring
re-grounding, and `_coordinator_lock` (the acquire/report/register sequence
extracted to one home so the drive mode and the explicit-role path share it
instead of duplicating it — the dupes census pinned the copy).
`bootstrap.py` 2078 → 2085 — the drive.py MAPPING row + docstring inventory
lines, the same required-registration shape as the Phase 4 integrate.py row.
The complexity census moved for neither module (`agent_loop.py:main` stays
27; `drive.py`'s functions all sit under the C901 threshold — the loop body
was decomposed rather than stamped).

**Bars:** `tests/test_drive.py` 10 passed; smoke + `check_docs --stale` green
at each commit; full unfiltered suite green at close (totals in the review
record). Byte budgets untouched (no budgeted file edited).
