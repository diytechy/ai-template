# WI-1002 checkpoint sitting 003 (8e5e5441)

This sitting judges the two approved rows whose text WI-1002 moved: LLR-143's
Detail and TC-137's Method.

What I checked beyond the cells shown:
- The WI-1002 spec and its Done-when, and the round-1 reviews at c873dcf8.
- SR-026, the parent of both rows, is unchanged.
- TC-137 verifies SR-026 and LLR-143. Its evidence is `tests/test_dispatch.py`,
  declared Full, and that module is in `tests/conftest.py` `SLOW_MODULES`.
- Both tests the added TC-137 sentence describes exist in that module:
  `test_a_parked_blocked_lane_draws_no_worker_and_the_ready_row_is_claimed` and
  `test_a_parked_lane_citing_a_ruled_item_still_resumes_first`.

I ran no suites; this sitting rules on text.

## amendment

Both rows change meaning, and I would bless both.

- [MEANING+BLESS] LLR-143 Detail -> every parked claimed branch resumes before a new row is claimed, and a lane that does nothing counts toward the stall guard -> a parked lane whose claimed row reads blocked in the shared schedule is left out of resume: it launches no worker, keeps its claim, and the next ready row is claimed, and the excluded lane does not count as a stall; a parked lane whose row reads anything else resumes as before -> a correct implementation of the old text relaunches the blocked lane and fails the new one, so the obligation moved; I would bless it. Its parent SR-026 is still met, because every lane that does resume still resumes from its claimed assignment. It reuses the blocked state the schedule already derives rather than a second predicate. It states both halves, the exclusion and the unchanged default. It adds no code name beyond those the approved cell already carried. TC-137 verifies both halves
- [MEANING+BLESS] TC-137 Method -> the drive suite's existing arms -> the same arms, plus a parked lane whose claimed row reads blocked, beside a ready row, which draws no worker and keeps its claim while the run claims and merges the ready row and ends without a stall, and the same lane citing a ruled item, which resumes first -> new assertions a test of the old method never made; I would bless it: it checks LLR-143's new exclusion, its no-stall clause and its unchanged-default half. It names the run, not the lane, as the claimant, and its Full tier matches its slow evidence module

The LLR and TC rungs are released, and neither registry holds another
unblessed drifted row among those judged here. The later act turn can
re-attest both rows and copy both registries.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
