# WI-848 dispute sitting at 4a7c619

## dispute

### LANDING

**Scope bound.** PROCESS.md §6's review threat model keeps this sitting to a
normal working environment. The finding says a shipped procedure doesn't match
its spec. That is content written into the repository, and no compromised or
contrived host is needed, so it is in scope.

**The claim.** The reviewer says the canonical coordinator procedure still
lands a lane with a hand squash: `coordinator-cycle/SKILL.md` §4 step 3 and
`references/recipes.md` "Squash … `git merge --squash <lane>`". They say this
contradicts the Done-when's "reconciled with every row landed since
2026-10-07", because PROPOSAL.md §7.1b's "The landing" bullet routes
coordinator lanes through `integrate.py integrate` once the approval-act rung
admits in-lane acts, and WI-849 (`ceab00c1`) is in the base.

**What I observed at 993deeee.**

- `ceab00c1` (WI-849) is an ancestor of the lane. That part holds.
- PROPOSAL.md §7.1b does carry the "The landing" bullet. But the proposal's own
  reconciliation, §8.1, which the Done-when points into via "proposal §8.4",
  narrows that row. P2 is "File narrowed: docs plus the approval-act rung only",
  and the reason it gives is "The landing switch is WI-808's ('Both paths yield
  one landing per lane')". P2 was filed as WI-849 in that shape.
- WI-849's own spec (`docs/archive/work/complete/WI-849-approval-act-in-lane.md`,
  line 33) says: "Not this row: switching the coordinator's landings to the
  slot is WI-808's." So WI-849's landing changed the rung and the docs, not the
  coordinator's landing route.
- WI-808 ("One landing per lane on both paths…") is still in
  `docs/work/queued/`, and its `needs` include WI-849, WI-851 and others. Its
  Done-when is where both paths are made to yield one landing, with
  single-item lanes as one squash commit each.
- `docs/status.md` (line 96) records the standing owner direction of
  2026-09-28: hand integration, one squash commit per item, lane tips kept in
  `archive/lanes`. The skill's landing step describes exactly that.

So the Done-when's reconciliation is "with every row landed since 2026-10-07",
and the row that switches the landing route has not landed. The skill agrees
with every row that has, and with the owner's standing direction. The switch
the finding asks for is WI-808's change. Making it here would put a landing
route nobody has yet run end to end on a lane carrying in-lane acts into the
procedure the coordinator follows tonight, ahead of the row built to prove it.
The procedure/spec mismatch the finding claims does not exist at this range.

**Note for the coordinator (it does not change the ruling).** Builder decision
D-008 left "a hand landing runs none of the merge slot's rungs" out of the skill
as state. When WI-808 lands it should rewrite the skill's §4 step 3 and the
recipes' Squash step. Its spec could name those two sites so the switch isn't
missed.

RULING: LANDING DISMISS refuted The landing switch belongs to the still-queued WI-808, not to WI-849: PROPOSAL.md §8.1 narrows P2/WI-849 to "docs plus the approval-act rung only — the landing switch is WI-808's", and WI-849's spec says the same, so the hand-squash landing matches every row landed since 2026-10-07 and the owner's standing direction in docs/status.md.
