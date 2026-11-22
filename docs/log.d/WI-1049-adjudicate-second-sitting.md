## 2026-11-22 — WI-1049: the second adjudication sitting; 23 amendments re-accepted and 22 rows accepted, two reverted by the operator's ruling

Deferred open items: none. The operator's one ruling this row needed (revert
the two unblessed amendments and take the act) is recorded in the row's spec,
under "The verdict and the operator's ruling".

Run on trunk by the queue drill's coordinator, by hand, as WI-1047 was
(queue-drill HANDOFF §3.7): the brief composed by `adjudicate_brief.compose`,
the verdict path reserved and the request bound by the entry point's own
functions, Gemini Neon (`gemini-4-neon-high`) through the Antigravity CLI
in plan mode, 488 s, one session. The record is in the row's Deliverable
(`../archive/work/complete/WI-1049-adjudicate-second-sitting.md`).

- The verdict blessed 23 amendments and accepted 22 rows; it ruled LLR-244
  and LLR-257 MEANING without the bless mark (each amendment added code
  names) and returned TC-457, TC-468 and TC-475.
- The act's first snapshot was refused over the two unblessed rows. By the
  operator's ruling their `detail` went back to the accepted text
  (`0333b64f0`), and the act was taken: re-acceptance `4e3e28a2f`, first
  acceptance `55e40f407`.
- WI-1050 re-lands LLR-244 and LLR-257 without the names and answers the
  three returned test cases, for a third sitting with F-3's acts.
- `docs/ratify/CURRENT.md` waits on three chains, down from fourteen.
