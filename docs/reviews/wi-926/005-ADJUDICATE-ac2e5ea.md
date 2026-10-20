# WI-926 adjudication 005: re-sit of TC-370

This re-sits TC-370, which sitting 004 returned, on the text at `ac2e5ea3d`. Since sitting 004's verdict (`98f5e9cd5`), the only registry change is TC-370 itself. Its `Verifies`, `Evidence`, `Expected` and `Method` moved, and no other row changed. The TC rung is released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:** every test the reworked row cites exists. I ran all 24 citations (44 cases with parameters): 43 passed and 1 was skipped (the non-executable-hook case, POSIX only, on this Windows box). `Tier = Full` is correct, because `test_hooks_on_routes` is in `tests/conftest.py` `SLOW_MODULES`.

## first-approval

- [APPROVE] TC-370 -> verify:
  - each inactive-floor cause with its repair (activation, restoration, executable mode), and each active configuration (relative, absolute, linked worktree);
  - every route refusing before work, and a session launch's refusal kept distinct from a blackout refusal and not waited out;
  - the cited active-floor starts (session call, overnight legs, a freshly activated checkout) proceeding normally;
  - no override read;
  - the claim's floor refusal before its guard refusal and dispatch lock, and the lease take recording no holder;
  - the route census and its deleted and moved mutations.

  -> its chain: each of sitting 004's three disposition items is answered.
  1. **The blackout arm of LLR-340** is now stated in Expected and Method and cited (`test_through_blackout_does_not_wait_out_a_hooks_refusal`).
  2. **LLR-140 and LLR-300 are now in `Verifies`, with their parents SR-156, SR-229 and SR-237.** The ordering test (`test_the_hooks_refusal_comes_before_the_coordinator_guards`) is cited, and the ordering and the no-holder outcome are stated.
  3. **The active arm now matches its evidence.** The three route-level active cases are cited, and the Method now runs every route only with the floor inactive. The active arm is the cited starts, and Expected says "the cited active-floor starts proceed normally".

  SR-240, LLR-340, LLR-140 and LLR-300 were approved or blessed at sitting 004, and the clauses here observe exactly what they state.

  -> ready. It claims nothing its cited evidence does not carry, and nothing its verified rows state goes unverified.

OUTCOME: APPROVE rows=1

**For the later act turn:** flip TC-370 from `Drafted` to `Approved` and anchor its copy. The rung is not held.

SITTING: JUDGED kinds=first-approval
