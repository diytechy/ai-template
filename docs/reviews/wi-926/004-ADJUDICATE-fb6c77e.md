# WI-926 adjudication 004: amendment of six rows and first approval of SR-240, LLR-340 and TC-370

I judged the lane at `fb6c77e9c` against the anchor in `docs/archive/last_approved`. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The diff:** I loaded the registries with `tomllib`. Since the anchor, the SR registry moved only in SR-019 and SR-020 and gained SR-240. The LLR registry moved only in LLR-019, LLR-020, LLR-140 and LLR-300 and gained LLR-340. The TC registry only gained TC-370.
  - Every amended cell keeps its anchored text verbatim and adds one sentence. LLR-300's sentence sits just before its existing lease-take sentence; every other addition is appended.
- **The code:**
  - The shared check reads only the checkout's hook configuration and names one repair per cause.
  - Every route calls it as its first act: the loop, the session launch, the bookkeeping commit, the claim (before its guard and its dispatch lock), the refresh, the merge slot, the lease take and the headless-leg launcher.
  - The pre-commit, commit-msg and pre-push hooks refuse with the scripts-lookup message when the kit scripts cannot be found.
- **Tests:** every test TC-370 cites exists. I ran them, together with the two route tests no TC cites and the three hook tests the arms map names for TC-019 and TC-020: 46 passed, and 1 was skipped (the non-executable-hook case, which is POSIX only, on this Windows box).

## amendment

- [MEANING+BLESS] SR-019 AcceptanceCriteria -> the hook blocks a failing floor and refuses below the interpreter floor -> the same, plus: with no kit scripts directory, the commit hooks refuse, name the repair, and neither run nor skip the floor -> a new refusal case. A hook that skipped the floor when it could not find the scripts satisfied the old text and fails the new one. **Blessed.**
  - It fails closed, it names no file (only the artifact class), and its parent's enforcement-floor purpose calls for it.
  - TC-019's Expected is "Satisfies SR-019 AcceptanceCriteria" over the whole `tests/test_pre_commit_hook.py`, which holds `test_each_hook_refuses_when_the_kit_scripts_cannot_be_found` and `test_privacy_and_loop_commits_get_the_same_scripts_refusal`.
- [MEANING+BLESS] LLR-019 Detail -> run the integrity floor and secrets scan, and classify every built-in step once -> it adds: when no kit scripts directory is findable, the commit-facing hooks refuse with exit 1, name the available repair steps, and neither run nor skip the floor -> a new refusal. **Blessed.**
  - It decomposes SR-019's new clause with its exit code and repair.
  - TC-019 verifies it with the tests above.
- [MEANING+BLESS] SR-020 AcceptanceCriteria -> the pre-push hook blocks a secret or identity and refuses below the interpreter floor -> the same, plus the same scripts-lookup refusal at push, neither running nor skipping the scan -> a new refusal case. **Blessed,** on the same grounds as SR-019. TC-020 covers the whole `tests/test_pre_push_hook.py`, where `test_pre_push_honors_kit_scripts_dir` drives the refusal without the override.
- [MEANING+BLESS] LLR-020 Detail -> scan the outgoing range and block a secret or a private identity -> it adds the refusal with exit 1, the repair steps, and neither run nor skip the scan -> a new refusal. **Blessed.** It decomposes SR-020's clause, and TC-020 verifies it.
- [MEANING+BLESS] LLR-140 Detail -> the claim's first refusal is the coordinator guard's (when enabled and off the dispatcher's route), then the ladder, then the dispatch lock -> the shared commit-floor refusal precedes even the guard refusal and the dispatch lock -> a new first rung. A claim that consulted the guard or took the lock before the floor satisfied the old text and fails the new one. **Blessed.**
  - The text states this route's place in LLR-340's contract, and the code matches it: the check is the claim's first statement.
  - `test_claim_refuses_a_hookless_checkout_first`, cited by TC-370, shows no lock, no branch and no move.
  - `test_the_hooks_refusal_comes_before_the_coordinator_guards` drives the precedence over the guard and passes, but no TC cites it yet. The draft under `## Dispositions` binds it, so this row's verification lands with TC-370's rework.
- [MEANING+BLESS] LLR-300 Detail -> the lease take reads the guard hooks' state before recording a holder -> before recording a holder, the take refuses an inactive commit floor and records no holder -> a new precondition. **Blessed.**
  - It serves SR-229 and SR-237's holder model: a holder installed in a checkout without the floor would make unenforced commits.
  - It fails closed, and every other sentence is verbatim.
  - `test_take_refuses_a_hookless_checkout_and_records_no_holder`, cited by TC-370, drives it.

VERDICT: MEANING rows=6

**For the later act turn:** all six rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests SR-019, SR-020, LLR-019, LLR-020, LLR-140 and LLR-300. No row is held, and no amended row is returned.

## Dispositions answered in the lane (sitting 005 approved the reworked TC-370)

```toml
title = "WI-926 spine rework: TC-370 cites and states every arm its rows carry (answer checkpoint 004)"
workstream = "process"
sr_refs = ["SR-240", "SR-156"]
needs = ["WI-926"]
safety_class = "ordinary"
buildtier = "medium"
```

Spine and trace text only. The tests exist and pass at `fb6c77e9c`; no code change is called for.

1. **Bind LLR-340's session-launch arm.** TC-370's Expected and Method should state that a session launch's commit-floor refusal is distinct from a blackout refusal, so it is not waited out as one, and its Evidence should cite `tests/test_hooks_on_routes.py::test_through_blackout_does_not_wait_out_a_hooks_refusal`.
2. **Bind the two route rows TC-370 already exercises.**
   - Add LLR-140 and LLR-300 to TC-370's `Verifies`.
   - Cite `tests/test_hooks_on_routes.py::test_the_hooks_refusal_comes_before_the_coordinator_guards` in its Evidence.
   - State in its Expected that the claim's commit-floor refusal precedes its guard refusal and its dispatch lock.
3. **Make the "active floor admits the route" claim match its evidence.** The Method says every route is run "with the floor inactive and active", but every route case it cites drives the inactive arm only; the active arm is cited only at the check level. Either cite the route-level active cases that exist (`test_act_runs_as_today_with_hooks_on`, `test_overnight_legs_runs_as_today_with_hooks_on`, `test_a_fresh_repo_reads_hookless_and_hooks_on_admits_it`), or narrow the Method to what is cited.
4. **Re-sit TC-370 alone.** This sitting blesses LLR-140 and LLR-300 and approves SR-240 and LLR-340 as they stand.

## first-approval

- [APPROVE] SR-240 -> where a checkout's commit floor is inactive, every delivered agent route refuses to start, naming the repair that activates the floor. It refuses before creating a lock, branch, commit, holder, log or session; it starts normally with an active floor; and no external setting, flag or parameter disables the refusal -> its chain:
  - **Upward:** SN-005 makes git hooks the agent-neutral enforcement floor, and a route that can commit in a checkout without that floor defeats it. The row is honestly DERIVED through SECURITY, whose `listens_for` (an action with no requirement naming its authority) names the failure prevented. The cell records the hat and the Rationale argues it, including why a bypass was refused.
  - **Downward:** LLR-340 decomposes it.

  -> ready. No file is named, and the acceptance criteria are observable conditions over a closed domain (the routes' own inputs). **Advisory:** the opening keyword is `Where`, the optional-feature pattern; an inactive floor is a fault condition, which reads as `If ... then`. The obligation is the same either way.
- [APPROVE] LLR-340 -> one check over the checkout root returns no refusal only when the resolved hooks directory is the checkout's or the primary checkout's `.githooks` and both commit hooks can run. Otherwise it names the cause and its repair: activation for a hooks path or a Git answer, restoration for a missing hook, executable mode for an unrunnable hook. Each route applies it before route-specific work, and a session launch tells it apart from a blackout refusal -> its chain:
  - **Upward:** it decomposes SR-240.
  - **Sideways:** LLR-140 and LLR-300 state only their routes' places in it.
  - The code matches every arm, and each arm has a passing test.

  -> ready. The text is a closed contract (inputs, outcome, causes, repairs), it names only the shipped `.githooks` directory, and it carries no `shall`. Its verification is incomplete only in TC-370, which is returned below.
- [RETURN] TC-370 -> verify each inactive cause and its repair, each active configuration, every route refusing before work, the census and its mutations, and no override -> its chain:
  - All 19 cited tests exist and pass.
  - Three gaps:
    1. it claims to verify LLR-340, but LLR-340's blackout-distinction arm has neither a clause nor a cited test;
    2. the claim's ordering before the guard (LLR-140) and the take's refusal (LLR-300) are exercised but not in `Verifies`, and the ordering test is cited by no TC at all;
    3. its Method claims every route run with the floor active, while every route case it cites is inactive.

  -> not ready. A TC that leaves an arm of its own verified row uncited, and claims a route-level active run its evidence does not hold, is a claim the record would carry unchecked. The follow-up is the one `## Dispositions` draft under `## amendment` above, so that one row answers both sections and nothing is minted twice.

OUTCOME: RETURN rows=3

**For the later act turn:** flip SR-240 and LLR-340 from `Drafted` to `Approved` and anchor their copies. TC-370 stays `Drafted`. Neither rung is held.

SITTING: JUDGED kinds=amendment;first-approval
