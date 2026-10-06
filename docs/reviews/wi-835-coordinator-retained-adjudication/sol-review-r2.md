0800a858 NOT YET SOUND

| Round-1 finding | Assessment | Evidence |
|---|---|---|
| MAJOR 1: undocumented probe output authorizes launch | **PARTLY** | Original reproductions now read unknown. Claude parsing is corrected, but Codex still accepts contradictory or fatal output accompanying a recognized line. See MAJOR 2 below. |
| MAJOR 2: telemetry committed directly onto trunk | **RESOLVED** | project-trajectory/scripts/coordinator_adjudicate.py:112 refuses primary roots. Adapted reproduction committed telemetry only on the claimed lane. Windows case/slash aliases passed; detached and subdirectory roots refused. |
| MAJOR 3: failed call succeeds using an old verdict | **PARTLY** | Existing paths now refuse, and failed/timed-out calls return 1 without reading the verdict. Overlapping calls can still accept another call’s verdict. See MAJOR 1 below. |
| MINOR 1: undecodable brief raises an exception | **RESOLVED** | project-trajectory/scripts/coordinator_adjudicate.py:155 catches `UnicodeDecodeError`; the `0xff` reproduction returns 2 before launch. |
| MINOR 2: IF-283 combines directional surfaces | **RESOLVED** | docs/requirements/interfaces.toml:2534 separates CLI arguments, exit codes and stdout into IF-283/284/285, with requestors versus consumers correctly assigned. Module contracts match. |

## BLOCKER

none

## MAJOR

1. **The fresh-verdict check does not establish exclusive ownership.** project-trajectory/scripts/coordinator_adjudicate.py:144 and project-trajectory/scripts/coordinator_adjudicate.py:177.

   Confirmed with two entry-point invocations sharing an initially absent verdict path: call A passes `_inputs`; call B then writes its verdict; A subsequently launches, exits 0 without writing a verdict, and returns 0 using B’s file. The reproduction also passes with retention enabled: A resumes B’s retained session, so the session lease does not prevent this gap.

   This contradicts docs/requirements/system-requirements.toml:1712’s success-from-this-call condition and docs/decisions/wi-835.toml:91’s claimed guarantee. Reserve ownership of the destination through launch and reporting; another existence check alone remains racy.

2. **Codex still treats undocumented combined output as signed in.** project-trajectory/scripts/session_service.py:574.

   Confirmed: exit 0 with either of these responses reads `signed-in`:

   ```
   Logged in using ChatGPT
   Not logged in
   ```

   ```
   Logged in using ChatGPT
   fatal: status unavailable
   ```

   Matching any positive line ignores contradictory or failed-status content. These are not the documented status forms, so the owner’s rule requires unknown and refusal. Validate the complete response, allowing the documented warning lines, and add rejection cases to TC-323.

## MINOR

1. **The new non-repository test does not exercise lane admission.** tests/test_coordinator_adjudicate.py:513.

   Confirmed by disabling `lane_refusal`: this test still passes because its fixture has no route registry. The command returns 2 for the missing route instead. Supply otherwise valid launch inputs and assert the non-worktree diagnostic so the test detects removal of the lane check.

## NOTE

- Focused tests: **111 passed in 18.71s**.
- `check_trajectory.py --strict`: exit 0, clean with warnings.
- Live status probes under newly created scratch homes: Claude **2.1.289** and Codex **0.160.1** both exited 1 and correctly read **missing**. Signed-in forms were checked with stubs; no sign-in was performed.
- Adapted `wi835_review_repro.py` confirmed the original fixes and the retained verdict race.
- Existing row Status values are unchanged; `lane_refusal` matches LLR-305’s module/symbol group. `git diff --check` passed and the lane remains clean.
- Full suite, smoke tier and shallow-clone test were not run. All writes stayed in `review-tmp`.