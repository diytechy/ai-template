+++
id = "WI-381"
title = "RULED 2026-07-31 (docs/concurrency-v2.md §A4) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. RESCOPED 2026-07-31: this row now carries the dispatcher SPLIT as well as the barrier, because the owner ruled question A (two modules) and question B (the dispatcher admits) together. THE SPLIT: drive.py becomes dispatch.py (the tick loop, the lane table and its count, pause, the frontier read, admission plus the spine barrier, the merge slot, stall) and lane.py is extracted from it (ensure worktree, launch the worker subprocess, run the WI-386 refresh, report the outcome - about 60 lines today, _ensure_worktree plus _default_worker). THE HANDSHAKE THAT MADE A SPLIT LOOK EXPENSIVE DOES NOT EXIST: a lane declares itself finished by moving its specs out of active/<branch>/, the tree-derived signal integrate.finished_branches already reads - no state file, no back-channel - and the merge slot is just the dispatcher's own serial loop over that list, which is what integrate() already is. At lanes=1 dispatch.py degenerates to today's serial loop, so the split is safe to land before concurrency is switched on. THE BARRIER: a spine-class WI must WAIT for all lanes to return to the station, then run as the ONLY thing touching trunk, and ALL spine WIs admit together as one batch (via agent_loop --wi 'A;B', its one surviving caller) so N spine changes cost one re-attest window and one owner sitting rather than N; spine work takes priority so it drains rather than starving. This is largely making an existing declaration TRUE: schedule.py already classifies spine|gate|attestation as serial-whole-project, but _disposition() still returns ready for those rows. QUESTION B IS RULED - the dispatcher admits - so integrate.py's blunt safety_class != ordinary refusal in _claim_refusal is DELETED: a hard stop replaced by a wait. That leaves one authority hole, closed by a constraint rather than by re-adding the refusal: integrate claim is also a hand-runnable CLI, so MAKE THE CLAIM REQUIRE THE DISPATCH LOCK - a hand claim on an idle station still works (useful, and attended-serial per RULING-8) while a hand claim during live lanes becomes unrepresentable instead of refused. LANE COUNT (question E, and owner decision 5 ruled 2026-07-31): a declared dial `lanes` in docs/stack.ini [agent-loop], resolving on the established ladder (CLI flag > AGENT_* env > stack.ini > code default). TEMPLATE SEEDS lanes = 2 - the smallest count that proves the barrier, the merge slot and the refresh race are real rather than vacuous, since a 1-lane default everywhere would let all three rot untested - BUT AN ABSENT KEY MEANS 1. That split is required, not stylistic: docs/stack.ini is ADOPTER-OWNED (ADOPTING.md §6 lists it under Preserve always - yours, kit only seeds them), so a re-sync will never overwrite a downstream lane count, which also means a kit-seeded key NEVER APPEARS in an existing adopter's file and their behaviour would fall to the code default alone. A code default of 2 would therefore switch a long-adopted repo from serial to two-lane concurrency SILENTLY ON UPGRADE. Seeding 2 in the template while defaulting an absent key to 1 gives fresh scaffolds the concurrency (visibly, on a line they can read and change) and upgrades nobody into concurrency they did not ask for. THE RENAME IS ACCEPTED (owner decision 6): drive.py -> dispatch.py forces a downstream resync - bootstrap.py's MAPPING, test_bootstrap.py's file lists, the README kit contents and adopting repos - and that cost is accepted because the module's job genuinely changed and a name that lies costs more than one migration. Treat it as a SCAFFOLD-SURFACE CHANGE and verify it by BOOTSTRAPPING A SCAFFOLD, per the WI-280 lesson: the MAPPING omission that broke every fresh scaffold while this repo stayed green is exactly this shape. Contention was measured honestly: the merge bar was NEVER concurrent (integrate holds out/integrate.lock) and after WI-386 there is no merge bar at all, but the REFRESH bars are concurrent and that is where the 11 minutes moved - on a plain Windows desktop the root conftest.py job object makes a second run JOIN the shared 50% ceiling so N bars split one half-machine (per-bar wall-clock, not a wedged desktop), while on POSIX there is no cap at all and N lanes genuinely oversubscribe. GATE POLICY IS THIS ROW'S AUTHORITY DIAL (docs/concurrency-v2.md §A8) and the barrier must honor it per kind. ordinary and critique dispatch parallel at every level; high-risk and protected dispatch exclusive at every level; a `spine` row DISPATCHES at every level because building a scope change is WORK, not a ratification (it opens a window, and closing it is the next row's job); an `attestation`/`gate` row does NOT dispatch under attended - the dispatcher drains the lanes, leaves the cards on open-items.html and exits - dispatches only the queued batch at the phase [g2] close under single-ratify, and dispatches under autonomous where a recorded fresh-context reviewer verdict ratifies. This preserves today's behaviour, which the owner confirmed must keep working: a gate change is detected, no work can be taken, and the ratification items surface in open-items. ONE HONEST CORRECTION TO CARRY: today that exit is a REFUSAL (a queued spine row sorts first, drive claims ready[0], _claim_refusal rejects it, the run stops NONZERO) which reads as a failure in a walk-away log when what actually happened is that the machine finished everything it was allowed to do - the barrier must exit 0 with 'queue drained - N ratification(s) waiting in open-items.html'. agent_route.failure_action('attended') already words the behaviour this way (start nothing new, let in-flight sessions close out, then alert the user), so the barrier is that existing contract implemented rather than new policy. The fixed points hold at every level and the dispatcher must not paper over them: G-Final is the human's, no un-run greens, the harness is still the bar, and ratified owner decisions are never re-decided by an agent. THE MID-FLIGHT CASE, unchanged: a WI that discovers it needs spine work cleans up what it can, records that its scope changed, and HANDS BACK (WI-387) with a draft spine WI for the remainder - never doing the spine work inline, which is what WI-280 did under an honest-at-filing ordinary class. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written. AMENDED 2026-08-01 (owner session; log.md Decisions this date): THE EMPTY-FRONTIER LADDER replaces the bare queue-drained exit. When the frontier is empty the dispatcher runs three rungs in order: (1) derive the gap census mechanically (unverified in-scope SRs, orphan rows, draft SNs - what trace.py already names) and hand it to the intake mint helper (WI-388) to mint concrete gap-closure rows - no model; (2) census empty but gate below G-Release: that is a PENDING ATTESTATION, not missing work - surface the cards and exit 0 with the honest banner; (3) census empty AND registries complete: exit 0 queue drained (an owner-ambition planning rung was considered and DEFERRED - no silent planner mints). ALSO CARRIED from the same session: the exit-0 banner correction in this spec is confirmed ruled, and the dispatcher's exit banner must derive from the SAME pending_block(root) read the dashboard and open-items.html already share (gen_open_items reuses gen_trajectory.pending_block verbatim), so agent-resume and the owner surfaces can never disagree about what is blocking - the coordinator's git-trailer read stays for in-flight lanes only."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-383", "WI-386", "WI-387"]
+++

## Deliverable

Shipped 2026-08-02, five commits (81cac0e1 the mechanical split, 82f516b2
the barrier + authority flip, a119065e the ladder + shared banner + template
seed, d520d43f the registration, 82c64d46 the seam declarations), each at
the smoke bar.

**The split (§A4.2).** `drive.py` became `dispatch.py` (tick loop, lane
table + count, pause, frontier read, admission + the spine barrier, the
per-lane merge slot, stall guard) with `lane.py` extracted (ensure worktree
via `integrate.lane_worktree`, the worker argv/subprocess, and the §A2
refresh as the lane's OWN subprocess so N bars overlap — §A4.3). At
`lanes = 1` the loop degenerates to the serial cycle; the whole renamed
suite passed at the split commit before any concurrency switched on. The
rename is treated as the scaffold-surface change it is: bootstrap MAPPING +
docstring, test_bootstrap file lists, kit README rows, ADOPTING.md §6
resync note, downstream-resync skill (+ per-agent copies), PROCESS_OPTIONS
layer table (+13 bytes), and every cross-reference in
agent_loop/integrate/handback.

**The barrier (§A4/§A8).** Admission is the dispatcher's one scheduling
decision: `_kind_action` is the ruled §A8 table verbatim (ordinary/critique
parallel at every level; high-risk/protected exclusive at every level;
spine batch at every level — building a scope change is WORK; attestation/
gate surfaces under attended, admits only as the queued batch at
single-ratify's close, dispatches exclusive under autonomous), and
`_admission` is the batch-and-wait barrier: an exclusive-kind frontier row
stops new admission outright, the station drains, then ALL spine rows admit
together as ONE batch — one branch, one claim commit, one
`agent_loop --wi 'A;B'` worker (its one surviving caller), one re-attest
window. The attended stop is now exit 0 with `queue drained - N
ratification(s) waiting in open-items.html` (the ruled correction of the
old nonzero refusal).

**The authority flip (§A4.1).** `_claim_refusal`'s
`safety_class != ordinary` arm is DELETED; the claim REQUIRES the dispatch
lock (`agent_common.dispatch_lock_path` = `out/agent-loop.lock`; one
acquisition site `_dispatch_lock` beside `_slot`'s, ladder before lock so
the clean-trunk rung never refuses over the lock's own file). A hand claim
on an idle station works; a hand claim during live lanes is unrepresentable;
the dispatcher's in-process claim passes `dispatch_lock_held=True`. The
claim machinery is batch-aware end to end (single-WI subject byte-identical)
and `integrate()` gained `branches=` so each lane's branch merges as its own
refresh completes.

**The lanes dial (§A4.3).** `--lanes` > `AGENT_LANES` > `docs/stack.ini
[agent-loop] lanes` > 1; malformed/sub-1 falls to serial loudly. The
TEMPLATE seeds `lanes = 2` on a live line; an ABSENT key means 1, so no
adopter is upgraded into concurrency on re-sync (this repo's own stack.ini
deliberately carries no key).

**The empty-frontier ladder + shared banner (the 2026-08-01 amendment).**
`gap_census(root)` — the named WI-388 intake-mint handoff seam — derives
unverified in-scope SRs, orphan rows and draft SNs from `trace.analyze`;
rung 1 reports the census and mints NOTHING; rung 2 counts pending cards
off `gen_trajectory._blocked_pending + _spine_pending` (the same
`pending_block(root)` derivation the dashboard and open-items.html render,
via the facade import gen_open_items uses — judgment recorded in
`_pending_cards`); rung 3 is the honest drained banner. Each rung driven
red-then-green; the coordinator's git-trailer reads stay for in-flight
lanes only.

**Registration.** LLR-149 (SR-093: admission table + barrier + dial +
census seam, dispatch.py) / LLR-150 (SR-132: lane mechanics, lane.py) /
LLR-151 (SR-132: dispatch-lock rung + batch claim, integrate.py) with
TC-143/144/145 over tests/test_dispatch_admission.py, tests/test_dispatch.py
and tests/test_integrate.py; IF-088/IF-089 declare the dispatcher's two new
cross-component reads (driven: the scratch-clone arch-map regen promoted
them to --strict ERRORs); IF-015's Contract cell names dispatch.py +
lane.py; `schedule.kind_of` is the extracted kind-resolution home;
`agent_common._open_lock_fd` the shared open+flock primitive. LLR-143/
TC-137 keep their drive.py-era traced pointers for the §A9.1 connectivity
batch (WI-390) — unhooking them now reds the knowledge⇒component web
against the still-committed arch-map (driven); `docs/declared-absences`
carries the old paths with that pointer.

**Evidence (dated 2026-08-02, tree 82c64d46).** Watched red-then-green: the
deleted safety arm (old refusal test red, flipped to the ruled contract),
the neutered barrier arms (2 failed / 12 passed, restored), the four ladder
tests (red on pre-ladder code). Scaffold bootstrap run (the WI-280 lesson):
a fresh scaffold's OWN `agent_loop.py --root .` printed
`dispatch: queue drained - no ready work items; 0 WI(s) integrated this
run.` and exited 0 through the shipped dispatch.py + lane.py at the seeded
`lanes = 2`
<!-- fig: cmd="bootstrap.py --dest <tmp> --agents none; git init/commit; AGENT_CMD='stub-agent {prompt}' python scripts/agent_loop.py --root ." rev=82c64d46 -->.
Branch checks: `trace.py --strict` 0 findings; `check_trajectory.py
--strict` rc=0; `check_doc_refs.py --strict` rc=0; `check_figures.py
--strict` rc=0; `derive_gate.py --check` rc=0 — the new rows move the
basis to LLR=134 TC=131 (value G3 unchanged), so docs/gate is regenerated
with the close, the WI-401/WI-402 precedent for registry-adding branches
(the derive-gate dogfood test demands the committed cache stay fresh); in a
scratch clone the post-regen `check_trajectory --strict` is also rc=0 and
the connectivity WARNs shift drive → dispatch + lane as specced. Smoke: 641 passed, 6 skipped
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=82c64d46 -->.
Full unfiltered suite: 1924 passed, 5 skipped in 310.78s (0:05:10), rc=0 — watched
<!-- fig: cmd="python -m pytest -q -n auto" rev="82c64d46 plus the close records (docs/gate regenerated, spec moved, log fragment) - shipped code identical to 82c64d46" -->.
