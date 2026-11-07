## 2026-11-07 — WI-1002: the parked-lane resume leaves out a lane whose claimed row reads blocked

Deferred open items: none.

`dispatch._parked_branches` now drops a parked lane whose claimed row reads
`blocked` in the shared schedule, the open-item hold the scheduler already
derives: the lane draws no worker and keeps its claim, and the run claims the
next ready row with no stall. Any other disposition resumes as before.

- Headless leg 38 finished the build the machine crash cut off in leg 37, then
  ran one counted round (both APPROVE; REVIEW-B raised three MINORs), the
  checkpoint (TC-137's added sentence reworded; a stray `import pytest` left
  the stub check string), sitting 003 (MEANING, both rows blessed), the gate
  (both APPROVE) and the act (seq 179, LLR-143 and TC-137 re-attested).
- Follow-ups, not built here (wi-1002 D-002, D-004): one public schedule reader
  for the four sites that compose `schedule.evaluate` through the private
  loader; and a held lane the filter leaves out prints no line, so the final
  review banner still reads "nothing is blocked" while the claim remains.
