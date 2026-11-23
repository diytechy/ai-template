## 2026-11-22 — WI-1052: an unproven risk no act ever accepted is reported as never accepted, not as reopened

Deferred open items: none. The row changes two kit scripts, their tests and
spine text, and takes no operator decision; it needed no decisions record.

Built on the maintenance branch `maint/wi-1052` from `3c33b3783`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1052-risk-never-accepted-wording.md`).

- **The wording.** The accepted-risk advisory and the release gate now word
  an unproven risk by why it reads unproven: "has reopened" and "accepted
  again" only where an acceptance act accepted the risk and a later change or
  failing record undid it; "was never accepted in an acceptance act", until
  an act accepts it, where the history and every act ledger on it were read
  whole and no act accepted it; and the reading's own reason alone, claiming
  neither, where they could not be read whole (a shallow clone's window, a
  malformed ledger, no git). No reading changes.
- **The mechanism.** With no anchor, the act reader's view gains
  `unaccepted`, saying which of the last two cases it is; the reading leads
  its one reason accordingly, and both reports read the case from that lead.
  `risk_acceptance_act` keeps its `(commit, reason)` contract. RESYNC entry
  added.
- **Rows.** LLR-239 (Accepted) gains a sentence stating the advisory's three
  wordings; LLR-243 (Accepted) says the gate names why the risk does not
  cover, in the same three cases, where it said "the triggers that reopened
  its risk". New TC-500 (the advisory, real git) and TC-501 (the gate,
  in-memory), Drafted. SR-202, SR-206, TC-234 and TC-238 checked, unchanged.
  IF-217's `data` (Drafted) lists the new key.
- **Tests:** the 46 modules importing the two changed scripts or holding the
  touched cases' tests, with the whole-tree and RESYNC readers:
  `1702 passed, 2 skipped in 2462.25s (0:41:02)`. `trace.py --strict`:
  `orphans=0 integrity=0`; `check_trajectory.py --strict`: clean.
  `run_menu.py smoke`: `3725 passed, 3 skipped, 18 warnings in 253.68s
  (0:04:13)`, with a CPU budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Test runs list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `RESYNC_PACK.md` +1,580, `low-level-requirements.toml` +929,
  `test-cases.toml` +2,683.
- **Acts owed:** LLR-239's and LLR-243's amendments (re-acceptance), and the
  first acceptance of TC-500 and TC-501.
