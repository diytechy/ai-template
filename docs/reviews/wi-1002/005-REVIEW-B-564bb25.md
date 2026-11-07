Reviewed: 564bb25b3fda778e6e8854bc037b6a4da1a4b991

REVIEW-B (independent, convergence stance, full lane 36476624e..564bb25b) - WI-1002, rubric docs/rubrics/kit-change-review.md

Verified. I named the worst failure classes this change admits and hunted them in severity order. (1) Fail-open: a held lane resumes anyway, or a lane that should resume is silently left out. (2) A wrong stall, or a run that never ends. (3) A lost claim, meaning the held lane's spec or branch is dropped. The filter at project-trajectory/scripts/dispatch.py:204-213 reads the shared schedule's own `blocked` disposition (`schedule.evaluate` over `schedule._load` with `load_oi_status`, the LLR-288 derivation) against the trunk's claimed ids (`integrate._claimed_wi_ids`, the evidence the merge slot also reads). It excludes only `blocked`; every other disposition still resumes, so it adds no second predicate over `needs`. That reading of trunk is the right one: PROCESS.md (Open items) keeps a claim at an owner-held step "only while the item is filed and cited on trunk".

I drove the real `dispatch.run` path:
- The new blocked-lane test fails on the pre-fix dispatch.py. I took a git-archive copy of 564bb25 with dispatch.py swapped for its 36476624e version and ran it: the worker launched for the held lane, `AssertionError: [('wi-402', 'WI-402'), ('wi-401-widget', 'WI-401')]`. The ruled-item companion passes there, which matches its stated purpose as an already-correct pin. On the post-fix code both pass.
- The ruled-item test would fail on either plausible wrong implementation: excluding every parked lane, or excluding every lane whose `needs` cites an open item.
- Extra probes on the post-fix code:
  - lanes=2: no worker for WI-402, WI-401 merged, rc 0.
  - Under a committed pause, with the held lane present: no worker, rc 8. The held lane is not a stall, and its claim and branch are kept, as the test also asserts.

Done-when map:
- (1) Resume leaves the blocked lane out, launches no worker, keeps the claim, claims the next ready row, no stall; any other disposition resumes as before. Covered by tests/test_dispatch.py `test_a_parked_blocked_lane_draws_no_worker_and_the_ready_row_is_claimed` and `test_a_parked_lane_citing_a_ruled_item_still_resumes_first`.
- (2) Resume LLR amended: LLR-143 `detail`. The text is true to the code and the right way round (K1). It names no new carrier at the SN/SR tier (K2). Its status is unchanged.
- (3) The tests/test_dispatch.py case asserts no launch, the claim kept and the next row claimed: covered by the first test above.
- (4) RESYNC entry: project-trajectory/RESYNC_PACK.md:10658. It is accurate and anchored by the pack's usual preceding-commit convention.
- (5) Review bar A+B: this round is the B half.

Counterpart decisions:
- LLR-143 changed (child) and TC-137 changed (its verifier). The change is carried: the TC-137 method adds the blocked and ruled-item cases, and both are tested.
- SR-026 (LLR-143's parent): retain. Its headless-resume promise is unaffected; a held lane simply resumes nothing.
- SR-148 (cited by the WI): retain. The change brings resume admission into line with readiness SR-148 already owns through LLR-288 and adds no new SR obligation.
- LLR-288: retain. It is consumed, not altered.

No requirement row is added. The amended cells conflict with no existing row I swept (SR-026, SR-148, LLR-288, TC-137). This is not a decomposition. The convergence stance barred me from reading the lane's ADJUDICATE record, so I took the LLR-143 amendment sitting as present in the range by file name only.

Coverage-extension note (fails closed, no severity): a FINISHED branch that still owes a review round and whose trunk row reads `blocked` is now also left out of `_parked_branches`. It used to be resumed to draw the round. It now reaches `_drain`, where the merge slot refuses it loudly ("no logged review round names its current tree") and the run stops. That stops the run, it does not fail open. Reaching it also needs a lane closed while its trunk row still cites a pending item, which PROCESS.md's same-commit ruling rule makes unlikely.

Commands:
- `git rev-parse HEAD` -> 564bb25b3fda778e6e8854bc037b6a4da1a4b991
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi1002-gate-B/wi-1002 <the 30 declared test files>` -> `1147 passed, 5 skipped in 1277.50s (0:21:17)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (999 work item(s), 888 done (89%), 34 cancelled, graph acyclic).`
- Pre-fix red check (git-archive copy at 564bb25 with the 36476624e dispatch.py, outside the worktree): `pytest tests/test_dispatch.py -k "parked_blocked_lane or citing_a_ruled_item"` -> `1 failed, 1 passed, 39 deselected`. The blocked test fails on the worker launching for WI-402.
- Post-fix probes in the same scratch copy (lanes=2; under pause): rc 0 with only WI-401 launched; rc 8 with no launch.

- [MINOR] project-trajectory/scripts/dispatch.py:213 -> (K1/B1, confirmed by running it) A held lane is dropped from resume with no output line, so a run that skips it never names it. The lanes=2 probe ended with "queue drained - no ready work items; 1 WI(s) integrated this run." followed by "FINAL REVIEW - the run is COMPLETE and nothing is blocked" (dispatch.py:1459), while WI-402 stayed claimed and blocked on OI-005. `final_review = "always"` is the default in both docs/process.toml and process.toml.template, so every default run that skips a held lane prints this false "nothing is blocked" line. -> Print one line per lane the filter leaves out (branch, WI id and the holding items from the record's `open_items`), and make the final-review banner stop claiming "nothing is blocked" while a held claim remains. This reports a state; it adds no guard, so no unrepresentable clause is owed. -> @owner
- [MINOR] project-trajectory/scripts/dispatch.py:207-210 -> (§3 "Consolidate, don't duplicate") The new filter repeats the composition `schedule.evaluate(schedule._load(root), oi_status=schedule.load_oi_status(root))`. It already appears at project-trajectory/scripts/agent_brief.py:208-209, project-trajectory/scripts/integrate.py:718 and project-trajectory/scripts/traj_status.py:383-384. Every copy reaches into the private `schedule._load`, so one change to how a repo's schedule is read must be made in four places. -> Add one public `schedule` entry point that evaluates the repo's schedule from a root, and call it from all four sites. This is a consolidation, not a guard, so no unrepresentable clause is owed. -> @owner

VERDICT: APPROVE findings=2
