ea3e6688 NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/coordinator_guard.py:781 — **Lock contention can still strand a failed relaunch.** After consuming the request, a failed launch must reacquire the store lock before restoration. Holding that lock in another handler beyond the ten-second wait produced `StoreBusy`, no `relaunch.json`, one consumed request, and an installed successor token. After releasing the lock, a subsequent exit handler returned `False` without launching. This contradicts SR-230’s recovery acceptance and LLR-301’s restoration guarantee.

## MINOR

- docs/requirements/interfaces.toml:2504 — **IF-280 combines opposite directions in one seam.** It declares incoming CLI arguments through `requestors` and `channel = "cli"`, then includes outgoing exit codes in its data. For a refused `clear` invocation, the returned code has no separate `exit-code` seam or consumer declaration. PROCESS.md §8 explicitly requires CLI arguments and exit codes to be separate rows; adjudication `001` also identified this obligation.

- docs/test/test-cases.toml:3218 — **TC-318 omits the token-save regression from its evidence.** `test_a_failed_token_save_restores_the_request` exists and catches the round-2 stranding defect, but the committed evidence cell omits it despite Fix 8’s explicit replacement. Reintroducing the unprotected token save leaves this failure outside TC-318’s cited evidence.

- project-trajectory/scripts/coordinator_guard.py:440 — **The new implementation still lacks code back-links.** The guard contains zero `Implements:` declarations, and `integrate.claim` at project-trajectory/scripts/integrate.py:790 omits LLR-300. A literal backlink scan therefore cannot connect the guard’s implementation to LLR-300 or LLR-301. Adjudication `001` identified this remaining gap.

## Verified

All four round-2 findings are addressed: token-save recovery, Windows roots containing spaces, IF-274’s verification link, and IF-276’s reservation. The relevant regression tests fail against `6bdf3f3a` and pass against `ea3e6688`. New assertions catch the reason-recording, shared-store, compaction-request and CLI-clear mutations. SR requirement cells comply with R2; dispatcher and latch-lifetime wording matches the code. Existing-row changes are confined to the authorized LLR-140 and LLR-270 cells, with no Status flips. The RESYNC anchor `176b6aef` is on trunk’s first-parent history. The worktree and index remained unchanged.

## Commands

Repeated reads and searches are grouped.

- `Get-Content`, numbered reads, and `rg -n` — inspected contributor rules, applied skills, complete WI/spec, owner R2, prior reviews, adjudications, decisions, code, tests, launchers, settings and spine rows.
- `git diff --stat 6bdf3f3a..ea3e6688`; scoped diffs over `6bdf3f3a..ea3e6688` and `eae1f486..ea3e6688`; `git diff --name-status eae1f486..ea3e6688`; `git log --oneline 6bdf3f3a..ea3e6688` — checked change inventory and authored changes.
- `git diff --check 6bdf3f3a..ea3e6688` — passed.
- `git show`, `git rev-parse HEAD`, `git merge-base --is-ancestor 176b6aef eae1f486`, and first-parent log search — confirmed reviewed tip and shipping anchor.
- `$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"`; `$env:PYTHONDONTWRITEBYTECODE = "1"` — constrained discovery and disabled bytecode writes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-822 tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_frame_context.py tests/test_integrate_admission.py` — **140 passed, 1 failed in 72.28s**. Git Bash failed with `CreateFileMapping` error 5 before POSIX launcher assertions.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; **clean, 821 work items, graph acyclic**, with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi822-r3-probes.py` — confirmed regression failures before the fixes, mutation detection, authorized registry deltas and evidence-symbol resolution. An initial scratch-harness error was corrected before the successful run.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi822-r3-lock-probe.py` — reproduced request stranding under lock contention in **10.12s**.
- `git status --porcelain`; `git diff --quiet`; `git diff --cached --quiet` — final checks clean; both diff checks exited 0.