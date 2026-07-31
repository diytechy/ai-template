## 2026-07-31 — WI-374: the unattended entry point (S1 — the claimer)

**One line:** a plain `agent-resume` launch now drives the serial
claim→build→integrate loop instead of exiting 2 with a map — the scheduling
front end Phase 5's dispatcher deletion took with it is back, as ~427 lines of
composition (ratchet splitlines method, all files) instead of 4,042 lines of
machinery.

**Deliverables.** New `scripts/drive.py` (400 lines by the size-ratchet's
splitlines method, stdlib only): the drive
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
test_bootstrap file list. Thirteen tests in `tests/test_drive.py` (slow tier;
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
- *Merged is counted from the tree, not the worker's word.* The integrated
  counter reads `finished_branches` ahead of each green drain (exact,
  residue included — a held branch exits nonzero first); a worker that
  reports DONE without finishing its branch merges nothing, leaves the
  trunk unmoved, and trips the driver's own stall guard.
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

**Round 1 → round 3 (the review pass).** REVIEW-A round 1: APPROVE
findings=3, all MINOR record-accuracy (the line-count figure, the bars
wording, the drained-banner undercounting residue merges). Round 2 (APPROVE
findings=2) caught the residue counter still under by one step on a mixed
residue+claim drain and a self-contradicting Deliverable cell; the counter
now reads what the drain will actually merge — `finished_branches` before
each green drain, which is exact because a held branch exits nonzero — and
the records were re-stamped.
A codex cross-review (owner-directed cross-provider leg, advisory) returned
6 findings; 4 taken as code: (1) a **stranded claim** — active specs whose
branch ref is gone, reachable when the claim's trunk commit lands but the
branch cut fails — is now a named fail-closed refusal instead of an
invisible state a run could report as "queue drained" (plus
`check-ref-format` validation before any claim); (2) the config preflight
is applied **lazily** — only when work actually needs a worker — so an
inert scaffold with an empty queue drains to exit 0 per the spec's
empty-frontier contract; (3) the clean-trunk refusal is hoisted to the top
of every cycle so the parked-resume path meets it before a worker session
is spent; (4) the plain launch's session dials (`--model`, the five maps,
`--stall-limit`, `--wait-on-limit`/fallback, `--live-status`) now ride to
the worker explicitly instead of being silently dropped. Not taken:
duplicating agent_loop's full launchability/identity preflight ahead of the
claim — the worker's own preflight is the authority, its refusal is loud,
and the parked claim resumes on relaunch; duplicating that ladder in the
driver is exactly the drift the census exists to catch (recorded here as
the disposition).

**The composed-tree bar caught the missing spine paperwork** — the first
integrate attempt redded on the `trajectory` step: the regenerated arch-map
now carries `scripts/drive` and the knowledge⇒component web check requires
every arch-map module in a CMP. Fixed the Phase-4-precedent way (the
integrate.py shape): **LLR-143** (Module=drive.py, Component=CMP-004,
SR-026's chain) + **TC-137** (Evidence=tests/test_drive.py), both Verified
with the review record as the autonomous-ratification verdict. A first
draft of LLR-143 cited its own WI id in the Detail cell; `trace.py --strict`
red it (spine stand-alone rule) and the token was removed — the harness
working as designed, twice in one merge.

**Bars:** `tests/test_drive.py` 13 passed; the smoke tier green at each
commit except the standing WI-357 work-branch conditional
(`test_this_repo_is_not_a_work_branch`, red by design on any claimed-branch
checkout), plus the commit bar's configured `check_docs` step green; full
unfiltered suite at close: totals in the review record. Byte budgets
untouched (no budgeted file edited).
