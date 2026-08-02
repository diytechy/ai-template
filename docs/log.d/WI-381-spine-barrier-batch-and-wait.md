## 2026-08-02 — WI-381: the dispatcher split, the spine barrier, the ladder

**Summary.** The largest build of the concurrency-v2 program, as ruled (§A4,
§A8, and the 2026-08-01 amendment): `drive.py` became `dispatch.py` with
`lane.py` extracted; admission became the dispatcher's one scheduling
decision — the §A8 kind × gate-policy table plus the batch-and-wait spine
barrier; the claim's `safety_class != ordinary` refusal arm was DELETED and
replaced by the dispatch-lock constraint; the lanes dial landed on the
established ladder with the template seeding 2 and an absent key meaning 1;
the bare queue-drained exit became the three-rung empty-frontier ladder; and
the exit banners now derive from the same `pending_block(root)` read the
owner surfaces render. Five commits, each at the smoke bar: the mechanical
split (81cac0e1), the barrier + authority flip (82f516b2), the ladder +
shared banner + template seed (a119065e), the LLR/TC/IF registration
(d520d43f), and the two seam declarations the station view demanded
(82c64d46).

**Deliverables.**

- **The split** (§A4.2): `dispatch.py` owns the tick loop, the lane table
  and its count, pause, the frontier read, admission + the spine barrier,
  the per-lane merge slot and the stall guard; `lane.py` owns one lane's
  mechanics — ensure worktree (`integrate.lane_worktree`, unchanged home),
  the worker argv/subprocess, and the §A2 refresh as the lane's OWN
  subprocess so N bars overlap instead of queueing (§A4.3). At `lanes = 1`
  the loop degenerates to the serial cycle it grew from; the whole renamed
  suite passed at the split commit before any concurrency switched on.
- **The barrier** (§A4/§A8): an exclusive-kind frontier row stops new
  admission (wait — never a parallel claim slipped past), the station
  drains, then ALL spine rows admit together as ONE batch — one branch, one
  claim commit (subject `claim: A;B -> active/<branch>`), one
  `agent_loop --wi 'A;B'` worker, one re-attest window. The §A8 table is
  implemented verbatim in `_kind_action`; the attended attestation/gate stop
  is now exit 0 with `queue drained - N ratification(s) waiting in
  open-items.html` (the ruled honest correction of the old nonzero refusal);
  single-ratify admits the queued ratification batch only at the close;
  autonomous dispatches it exclusive.
- **The authority flip** (§A4.1): `integrate.claim` requires the dispatch
  lock (`agent_common.dispatch_lock_path` = `out/agent-loop.lock`, the lock
  a live dispatcher holds for its process lifetime; one acquisition site,
  `_dispatch_lock`, mirroring `_slot`'s discipline). A hand claim on an idle
  station works; a hand claim during live lanes is unrepresentable. The
  claim machinery went batch-aware end to end (`_claim_refusal`,
  `_abandoned_claim`, `_claim_delta`, `_relinked_exactly` on the whole move
  remap), and `integrate()` gained the `branches=` restriction so each
  lane's branch merges as its own refresh completes.
- **The lanes dial** (§A4.3): `--lanes` > `AGENT_LANES` >
  `docs/stack.ini [agent-loop] lanes` > 1; malformed and sub-1 values fall
  to serial, loudly. `stack.ini.template`'s `[agent-loop]` section now ships
  LIVE seeding `lanes = 2`; this repo's own `stack.ini` deliberately carries
  no key (stays serial until the owner opts in).
- **The empty-frontier ladder + shared banner** (the amendment):
  `gap_census(root)` derives the mechanical census (unverified in-scope SRs,
  orphan rows, draft SNs — `trace.analyze` reused, not re-derived) and is
  the named WI-388 intake-mint handoff seam; rung 1 reports it and mints
  NOTHING; rung 2 counts the pending cards off
  `gen_trajectory._blocked_pending + _spine_pending` — the same
  `pending_block` derivation the dashboard and open-items.html render — and
  rung 3 is the honest drained banner. Import judgment recorded in
  `_pending_cards`: the gen_trajectory FACADE (the gen_open_items shape),
  deferred; no forbidden seam crossed, no agent_common F5 pin needed.
- **Scaffold surface** (owner decision 6, the WI-280 lesson): bootstrap
  MAPPING ships `dispatch.py` + `lane.py`, test_bootstrap pins both plus the
  `lanes = 2` seed, kit README rows rewritten, ADOPTING.md §6 resync note
  (delete the old `drive.py`; absent lanes key means 1), downstream-resync
  skill + per-agent copies, PROCESS_OPTIONS.md layer table. Verified by
  bootstrapping a fresh scaffold and running ITS OWN loop entry:
  `dispatch: queue drained - no ready work items; 0 WI(s) integrated this
  run.` exit 0
  <!-- fig: cmd="bootstrap.py --dest <tmp> --agents none; git init/commit; AGENT_CMD='stub-agent {prompt}' python scripts/agent_loop.py --root ." rev=82c64d46 -->.
- **Registration**: LLR-149 (SR-093, the admission table + barrier + dial +
  census seam) / LLR-150 (SR-132, lane mechanics) / LLR-151 (SR-132, the
  dispatch-lock rung + batch claim), TC-143/144/145 over their suites;
  IF-088/IF-089 declare the dispatcher's two new cross-component reads
  (driven: the scratch-clone arch-map regen promoted them to --strict
  ERRORs, and the station must not be first to see a red this row caused);
  IF-015's Contract cell names `dispatch.py + lane.py`; `schedule.kind_of`
  extracted as the one kind-resolution home (census row `kind-resolution`,
  deliberate); `agent_common._open_lock_fd` extracted as the shared
  open+flock primitive.

**Red-then-green, watched.** (1) Deleting the safety arm turned
`test_claim_refuses_a_spec_that_is_not_safety_class_ordinary` red before it
was flipped to the ruled contract (idle-station spine claim succeeds; the
dispatch-lock test drives the live-lanes refusal and the
`dispatch_lock_held=True` path). (2) Neutering the barrier's wait arm and
the attended surface arm turned the two barrier admission tests red (2
failed, 12 passed) before restore. (3) All four ladder tests (census unit
×2, rung 1, rung 2) were run red on the pre-ladder code (2 failed + 2
failed) before the implementation turned them green.

**Deviations and judgments.**

1. **LLR-143 and TC-137 keep their drive.py-era traced pointers** (Module /
   CodeSymbol / Method prose): unhooking LLR-143's Module now reds the
   knowledge⇒component web against the still-committed arch-map inventory
   (driven at --strict), and the whole connectivity move is §A9.1's
   program-close batch (WI-390). TC-137's Evidence cell does follow the
   rename; `docs/declared-absences` carries the three old paths with the
   §A9.1 pointer, so `check_doc_refs --strict` is honest rather than
   silenced. The lane module's no-IF-row WARN stays deliberately — the
   handback.py posture, recorded in lane.py's docstring.
2. **`docs/gate` is regenerated with the close**: the new LLR/TC rows move
   the basis counts (LLR=134, TC=131) while the VALUE holds at G3, and the
   derive-gate dogfood test demands the committed cache stay fresh — the
   WI-401/WI-402 precedent for registry-adding branches (both committed a
   4-line docs/gate alongside their rows). Driven both ways: on the
   pre-regen tree the full suite ran 1 failed (that test), and after
   `derive_gate.py` the check answers `docs/gate up to date (G3)`, rc=0
   <!-- fig: cmd="python project-trajectory/scripts/derive_gate.py --check" rev="82c64d46 + the regenerated docs/gate" -->.
   A scratch clone additionally shows post-regen `check_trajectory --strict`
   rc=0 and the connectivity WARNs shifting from the drive entry to
   the dispatch + lane entries, as the spec predicted.
3. **The refresh subprocess replaces the in-dispatcher refresh for lane
   branches** (residue branches keep the in-process drain path, now
   skipping already-merge-ready tips). The refusal STRING for a lane's red
   refresh is the subprocess's own stderr plus the retained
   `out/run-logs/refresh-refused-*.log`; the dispatcher's quarantine
   decision reads the exit code and `branch_outcomes` — same §A3 ruling,
   stated in `_refresh_failed`.
4. **`single-ratify`'s "queued batch at the phase [g2] close"** is
   implemented as: attestation/gate rows admit (as one exclusive batch) only
   when nothing else on the frontier is dispatchable and the station is
   idle — the mechanical reading of "the close"; otherwise they surface and
   non-dependent work keeps running. Recorded in `_kind_action`'s table
   docstring.
5. **The stall counter is per-lane-close** (trunk head at admission vs at
   close) rather than per-cycle — the same guard, generalized to a table;
   at lanes=1 it reproduces the serial behavior the suite pins.
6. **Carried, not created**: `check_docs` names 4 broken links in old
   `docs/work/complete/` specs that pre-exist on trunk; untouched here.

**Byte deltas on budgeted files.** PROCESS_OPTIONS.md 169125 → 169138
(+13: the layer table names `dispatch.py`/`lane.py`); AGENTS.template.md
untouched (9991).

**Size/census stamps.** agent_common 1824, agent_loop 2985, integrate 2251
(reasons in the baseline); smoke `max-tests` 640 → 660 (+20 in-process
admission/ladder tests); dupes census +`kind-resolution` (1, deliberate).

**Verification.** Branch tree at 82c64d46: `trace.py --strict` 0 findings;
`check_trajectory.py --strict` rc=0; `check_doc_refs.py --strict` rc=0;
`check_figures.py --strict` rc=0. Smoke: 641 passed, 6 skipped
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=82c64d46 -->.
Full unfiltered suite: 1924 passed, 5 skipped in 310.78s (0:05:10), rc=0 — watched
<!-- fig: cmd="python -m pytest -q -n auto" rev="82c64d46 plus the close records (docs/gate regenerated, spec moved, log fragment) - shipped code identical to 82c64d46" -->.
