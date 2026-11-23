## 2026-11-23 — WI-1061: the fifth adjudication sitting; SR-251's chain returned whole (SR-251, LLR-406, TC-483)

Deferred open items: none. The row needed no operator ruling: the verdict
authorizes no act.

Run on trunk by the queue drill's coordinator, by hand, as WI-1057 was
(queue-drill HANDOFF §3.7): Gemini Neon (`gemini-4-neon-high`) through the
Antigravity CLI in plan mode, 321 seconds, one session. The record is in
the row's Deliverable
(`../archive/work/complete/WI-1061-adjudicate-fifth-sitting.md`).

- The verdict returned all three rows. SR-251 and LLR-406 disagree on
  which test cases the rewrite reaches. LLR-406 gives a keyless case a key
  unconditionally. Neither row states an all-or-nothing write. TC-483
  verifies none of the three.
- Verdict `bba8aeac3`, recorded `4e3e9bf4b`. The coordinator removed two
  wrapper lines its own preface had asked for (the `## <kind>` heading and
  the `SITTING:` line, which a single-kind verdict does not carry);
  nothing else in the reply changed.
- LLR-406's flip held under WI-1057's verdict is void: this sitting
  returned the same text.
- Follow-up filed: WI-1062.
