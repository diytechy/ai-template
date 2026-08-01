## 2026-08-01 — WI-387: three terminal outcomes, so a branch cannot hang

**Summary.** "WIs always land back in trunk; branches never hang" was a rule
someone had to follow. It is now a property of the tree.
[`concurrency-v2.md`](../concurrency-v2.md) §A3's three outcomes — **merged**,
**cancelled**, **handback** — are all merges, and a lane declares which one it
reached by the *directory it moved its claimed specs into*, which is the same
move that already made the branch finished. One fact, read twice; no fourth
option and no state file that could hold one. Two run-stops die with it (the
`EXIT_NEEDS_HUMAN` stop and the parked-branch stop), and so does
`drive._stranded_claims`, whose entire reason for existing was an ordering in
`integrate.claim` that this row inverts.

**Deliverables.**

- **The outcome is the folder.** `integrate.OUTCOME_DIRS` +
  `branch_outcomes(root, branch)` read the branch's own tree: `complete/` →
  `merged`, `cancelled/` → `cancelled`, any open folder (`queued/`, `draft/`,
  `deferred/`) → `handback`. A claimed spec that landed in no declared
  directory resolves to *nothing* and `integrate_one` refuses on it — a branch
  that deleted its spec has stated no outcome, and guessing one would let
  unreviewed work merge as if approved. The merge commit and the console line
  now name the outcome per id (`integrate: wi-401 merged (WI-401=handback)`),
  so a walk-away run cannot report a return as a completion.
- **The verdict gate is keyed off the OUTCOME, not the claim.** `_verdict_gate`
  took `wi_ids` from trunk's `active/<branch>/` and demanded an `APPROVE` for
  every one — but a handback leaves those ids claimed at merge time, so as
  written it demanded an approval for work being *returned*. Only `merged`
  asserts done and owes a verdict. This is not cosmetic: a review escalation is
  the commonest handback cause, so the unfixed gate would have deadlocked the
  common path on itself.
- **The claim is inverted: `write-tree`/`commit-tree` → `git branch` → advance
  trunk.** Trunk-first had one crash window that left a claim no lane could
  reach — invisible to the frontier (the WI is no longer queued) and to the
  parked-resume read (no ref) — which cost an exit-2 refusal and hand repair.
  Branch-first moves the same window to the benign side: a crash leaves at
  worst an orphan branch whose claim commit is not an ancestor of trunk while
  its WI is still `queued/`, which `_abandoned_claim` recognises by three facts
  (this branch's claim subject at the tip; the tip not an ancestor of trunk;
  its parent an ancestor of trunk) and the next claim deletes and re-cuts.
  **`drive._stranded_claims`, its exit-2 refusal and its test are deleted.**
- **`handback.py`, a new sibling kit script** (`hand_back` + `quarantine`):
  - `hand_back` commits the work so far **as-is** (`--no-verify` — "as-is" has
    to mean it, and the branch's own §A2 refresh regenerates and bars this tree
    before anything merges), moves each claimed spec back to `queued/` with a
    `## Handback` section naming what remains and **the commit range it lives
    in**, and sets `blockref` to the spec's own path.
  - The blockref is load-bearing, not decoration: `schedule._disposition` reads
    queued+blockref as `blocked`, so a returned WI leaves the ready frontier
    until a human clears it. Without it the driver would claim, hand back and
    re-claim the same WI forever — and because each handback *merges*, trunk
    would move every cycle and the stall guard would never fire.
  - `quarantine` is the ruled red arm (owner decision 1): revert the product
    paths to the merge base, keep the failing diff as a bar-inert `.patch` in a
    `handback/` directory under `docs/work/`. Nothing is lost — the reverted
    commits stay reachable in trunk history once the branch merges — and
    nothing is live.
    Bookkeeping paths (`docs/work/`, `docs/log.d/`) are exempt by construction:
    reverting them would revert the handback itself.
- **`drive.py`: the decision, not the write.** `_worker_stop_code` is replaced
  by `_lane_close`. A *decided* worker exit (`_WORKER_OUTCOMES`) hands back and
  the run continues; a **crash** (any other code) is deliberately not a hang
  and keeps the parked-resume path exactly as it was, bounded by the stall
  guard. `_drain` gained `_refresh_or_quarantine`: a red refresh still stops
  the run for a branch whose outcome asserts *done*, but a branch that merges
  nothing is quarantined once and refreshed again.
- **The `## Handback` section joined the spec body grammar** — `SPEC_HANDBACK`
  plus a four-line partition in `parse_spec_deliverable`, identical in all
  three F5 copies (`agent_common`, `check_trajectory`, `schedule`) and in
  `wi_convert`, which reads past it and does not reproduce it (it maps to no
  CSV column; `--verify` round-trips from a CSV and never sees one).

**How the invariant is tested.** [`tests/test_handback.py`](../../tests/test_handback.py)
(10 tests, new; filed in `conftest.SLOW_MODULES` beside its two siblings — real
claims mean the real `trunk_step --regen` subprocess) constructs every topology
it measures. The anti-livelock property is asserted against `schedule.frontier`
itself, driven both ways (ready before the claim, `blocked` after the return);
the quarantine is proven bar-inert in all three diff shapes (edit, add, delete)
*and* lossless (`git apply --check` then `git apply` restores the lane's work);
all four registry readers are driven over one real returned spec. In
`tests/test_drive.py` the two run-stop deletions are driven end to end against a
**conditional** stub bar — red exactly while the lane's broken file is present,
which is what lets the red-handback ruling be *shown* (refresh red → quarantine
→ refresh green → merge) rather than asserted. `tests/test_integrate.py` gains
the crashed-claim shape (re-claimed) beside its two negatives (a branch carrying
work, an unrelated same-named branch — both still refuse), the four-way outcome
read, the landed-nowhere refusal, and the outcome-keyed gate driven at both the
helper and the whole slot.

**Deviations from spec.**

- **`hand_back`/`quarantine` ship in a new sibling module, not in
  `integrate.py`.** The row's scope said "while the file is open"; the file is
  a monolith ratchet away from its ceiling. The extraction is the ratchet's own
  documented escape and the WI-374 precedent (the drive loop went to `drive.py`
  rather than into `agent_loop.py`). It costs the scaffold surface — MAPPING
  row, README kit-contents, `test_bootstrap` file list — all three registered.
- **`integrate.py` still crosses THRESHOLD (1418 → 1588) and takes a NEW
  reviewed baseline entry.** What remains is irreducibly its own: the claim,
  the outcome read the merge slot gates on, and the verdict gate. Re-stamp
  DOWN with WI-390's deletions.
- **No CLI subcommand for `handback`.** The driver is the only mechanical
  caller; a lane agent that wants to cancel or hand back by hand writes the
  move and the reason, which is a judgement, not a command.
- **The spine is untouched**, per the standing ruling that spine work waits and
  batches. `LLR-143` and `TC-137` still describe `_stranded_claims` and
  "NEEDS-HUMAN propagates as exit 7"; both are false as of this merge and are
  owed to WI-390 along with `PROCESS_OPTIONS.md`'s attended-mode
  "the loop stops `NEEDS-HUMAN`" sentence. Nothing mechanical enforces LLR
  `Code`/`Detail` cells, so this is prose debt, recorded rather than absorbed.
- **`handback.py` declares no `Contracts:` line.** IF-080 already sits in the
  interface registry with no script declaring it (§A9.1's inherited drift);
  declaring it from the sibling rather than from `integrate.py` would
  paper over that. The module will add a fifth `connectivity undeclared` WARN
  once the trunk lane regenerates the arch-map — same pre-existing WARN class
  as `drive`, `traj_graph`, `traj_panels`, `traj_render`.

**Stamps re-stamped, each with its reason in
[`tests/test_module_size_ratchet.py`](../../tests/test_module_size_ratchet.py).**
`integrate.py` NEW 1588; `agent_common.py` 1731 → 1741 and
`check_trajectory.py` 3251 → 3261 (the body-grammar lines, identical text in
both by construction); `bootstrap.py` 2243 → 2250 (the scaffold registration).
`docs/dupes-allow`: the two F5 fingerprints moved again
(`221f967454e5` → `a17abce26cb8`, `e781cf6ec0e8` → `7a1470c3f0c1`) for the same
structural reason as WI-384 — the new lines land *inside* the matched block in
all three copies at once, and `check_trajectory == schedule` keeping its fp
(`1dbf7e455ac3`) is the tell that nothing new was copied. **No byte-budgeted
file was touched** (`AGENTS.template.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`
unchanged).

**Findings for their own WI (not fixed here).**

1. **A worker that reports DONE without closing its specs still parks.** The
   invariant covers every *non-zero* exit; exit 0 with specs still in
   `active/<branch>/` leaves the branch parked and relies on the stall guard.
   Handing that back too would make the invariant airtight, but it changes the
   stall semantics this row was not asked to touch.
2. **A red refresh on a `merged` branch still stops the run.** Deliberate and
   unchanged (WI-386's rule: the lane that caused the red fixes it, and the
   branch is retried on every relaunch rather than stranded). It is the one
   remaining shape where a branch waits on a human, and whether it should also
   convert to a handback is a design question for §A3, not a builder's call.
