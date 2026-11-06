# WI-993 dispute at 26b4d09: finding PARK

I ruled the one disputed finding against the code in the lane range `ee2b19b9e..f1c769303`. `project-trajectory/scripts/dispatch.py` is byte-identical at `f1c769303` and at HEAD `26b4d09`, and the lane does not change it. I read PROCESS.md §6, "Review threat model", and the §6 triage list before ruling, and applied them as written.

## PARK

**What I observed.**
- A plain `agent-resume` reaches `dispatch.run` (`agent_loop.py:3614-3619`), so this is the kit's own unattended route.
- Each tick, `_admit` resumes parked branches before anything else (`dispatch.py:1183`).
- `_parked_branches` (`dispatch.py:174`) lists every claimed `active/<branch>/` that has a branch ref. It consults no schedule and no disposition.
- For such a row, `agent_brief.worker_prompt` composes only the line `BLOCKED <wi>: <items>. See docs/open-items.html; no worker assignment.` The kit already treats the row as one that draws no worker, yet the dispatcher launches a session for it.
- A worker exit inside `_WORKER_OUTCOMES` sends `_lane_close` to `handback.close_partial`. Sessions that commit nothing trip the stall guard instead.

**The reproduction.** I ran it as a scratch test, deleted afterwards and never committed, built on `tests/test_dispatch.py`'s own fixtures. The setup:
- WI-401 is claimed in `active/wi-401/` with its branch ref, and its `needs` cites OI-5, which is pending in `open-items.toml`.
- WI-402 is queued.

The result:
- `schedule.evaluate` reads WI-401 as `blocked` and WI-402 as `ready`.
- `_parked_branches` still returns `['wi-401']`.
- `dispatch.run` printed `resuming parked branch wi-401 (WI-401)`, launched the worker on it first, and on its exit 4 printed `handback: closed WI-401 as partial from wi-401 (worker exit 4)`.

So the dispatcher drops the claim and spends a worker session doing it. WI-402, the ready row, was never reached. The run then stopped on an integrate refusal that came from my bare fixture (no `docs/stack.ini`), not from the finding.

**What follows.** WI-993's §5 text makes this state sanctioned: "A lane keeps its claim at a planned owner-held step ... only while the item is filed and cited on trunk". The kit's unattended driver does not honour that state:
- It closes the lane partial, so the pending item is left cited only by a closed row, which is the uncited-item error on trunk.
- When the worker exits 0 instead, the run stalls with a ready row unclaimed.

The claim copy's Trust sentence "a claimed one draws no worker assignment" is true of the brief and false of the driver. The finding holds.

**Grade.** I re-grade it from MAJOR to **MINOR**:
- **Reach.** The path is reachable only through supported acts, but rarely. A dispatch-route lane must be parked rather than closed at its planned step: an interrupted run, a crash, a restart exit, or a coordinator's kept lane followed by an `agent-resume` in the same repository. A person must also have filed the item on its claim copy. On the dispatch route itself, a worker that stops for the owner exits NEEDS-HUMAN and is closed partial on the same tick, which §5's "Otherwise ... the lane closes partial" already sanctions. So the route does not produce the parked-at-step state by itself.
- **Not convergence-class.** Nothing fails open: the uncited-item error is loud and holds the trunk. Nothing is lost: `close_partial` commits the residue and the handback mints a disposition row. The Done-when names the policy text and the mint, not the driver.
- **Not high-risk** in §6's triage sense. It touches no security, money, irreversible act or gate closure, so it is not ESCALATE.

**Worth the change, but in its own row.** The fix is small and right: the resume admission reads the `blocked` disposition that LLR-288 already derives, and the worker brief already acts on it. That adds no second predicate and no detector for a session that stopped and filed nothing, which is what call 7 forbids. It honours a filed item, the coordinator's rule that §5 assigns, on the route where the dispatcher is the coordinator. It does not belong in this lane, for three reasons:
- **It changes approved behaviour.** It changes an approved row's behaviour, the dispatcher's resume admission, which owes its own spine amendment and sitting.
- **It is outside the lane's spec.** This lane's spec lists `dispatch.py` as an unchanged consumer, and the lane is past three review rounds and two amendment sittings.
- **It predates the lane.** A claimed row citing a pending item was already representable (LLR-288), and the dispatcher already launched it against the brief's "no worker assignment". WI-993 makes the state sanctioned; it does not create the driver's gap.

RULING: PARK SUCCESSOR the dispatcher's parked-lane resume leaves out a lane whose claimed row reads blocked in the shared schedule (LLR-288's disposition), so it launches no worker, keeps the claim, goes on to claim the next ready row and ends without a stall; the resume LLR is amended to say so and a tests/test_dispatch.py case over a parked blocked lane plus a ready row asserts no launch, the claim kept and the next row claimed
