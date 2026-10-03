## 2026-10-03 — wave 8 (coordinator): WI-747 lands

Resumed from [the wave-7 handoff](../handoff-2026-10-03-wave7-coordinator.md). Reviews
for this wave: [reviews/2026-10-03-wave8/](../reviews/2026-10-03-wave8/).

### WI-747 lands: rubric-first observation judgement on a closed-work cadence

Sol built it at `dfe92989`. Sonnet 5.5 found it NOT YET SOUND: the `stage-gate`
re-judge trigger had no production caller
([r1](../reviews/2026-10-03-wave8/sonnet-wi747-r1.md)). The Sol
fix round made `intake.py rejudge --checkpoint` accept `stage-gate` (red 6 failed,
then green) and extracted `rejudge.checkpoint_for`. The coordinator committed it at
`d4f991a0` with two corrections:

- SR-215's requirement cell stays free of the command. The fix prompt had asked
  for it, and ruling R2 forbids a requirement cell naming a concrete artifact.
  The command lives in LLR-293.
- `checkpoint_for` is tagged LLR-254, which owns `rejudge.py`, not LLR-255, and it
  joins LLR-254's `code_symbol` inside that row's pending amendment.

Sonnet 5.5 found `d4f991a0` SOUND ([r2](../reviews/2026-10-03-wave8/sonnet-wi747-r2.md)),
with four minors:

- Three were folded in at the landing: the `_cmd_rejudge` docstring, the
  `REJUDGE_CELLS` comment, and an assertion that `merge` stays first in
  `CHECKPOINTS`.
- LLR-255 is left as is: it is incomplete about stage-gate, not false.

Landing:

- Registries were merged table by table; trunk and the lane added disjoint ids.
- The watermark was raised by `--bump-ids`.
- The lane's RESYNC entry was re-anchored at `122816da`, and its fix-round entry was
  folded in, because that entry was anchored at a lane-only sha.
- PROCESS.md: 93,016 -> 94,466 (+1,450, the WI-747 rule), re-stamped in the
  byte-budget skill (4,444 bytes, cap 5,000) and its two mirrors.
