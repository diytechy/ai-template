53547b55 NOT YET SOUND

## BLOCKER

none

## MAJOR

1. **Unknown probe output can authorize a retained launch.** project-trajectory/scripts/session_service.py:548 and project-trajectory/scripts/session_service.py:562. Confirmed with injected status runners: exit 0 with `Logged in? No credentials found` reads **signed-in**; Claude exit 2 with `{"loggedIn": true}` followed by a fatal diagnostic also reads **signed-in**. Both pass `require_signin`, allowing either route to launch where the owner requires unknown and refusal. Restrict recognition to the documented output/exit combinations and test these rejection cases.

2. **A primary-checkout invocation commits directly onto trunk and fails the integrator audit.** project-trajectory/scripts/coordinator_adjudicate.py:148. The entry point accepts a primary root without a lane or branch check; `session_service.call` commits its log there. A scratch primary checkout reproduced a non-merge `telemetry:` commit touching `docs/iteration/*.log`, which `integrate.audit` rejected. D-008 confirms telemetry recording, but does not make that path permitted trunk bookkeeping. Require a lane before launching, or provide an explicitly permitted, serialized trunk recording path.

3. **A failed call can return success using an old verdict.** project-trajectory/scripts/coordinator_adjudicate.py:97. Run once successfully, then reuse the verdict path for a call that exits 1 without writing anything. Confirmed: the entry point prints `adjudicate: exit 1`, reads the previous verdict, declares it valid, and returns 0. Establish a fresh verdict destination before launch and reject a failed or timed-out call.

## MINOR

1. **An undecodable brief escapes the promised input refusal.** project-trajectory/scripts/coordinator_adjudicate.py:122. A brief containing byte `0xff` raises `UnicodeDecodeError` instead of returning the documented exit 2 for an unusable brief. The handler catches only `OSError`.

2. **IF-283 combines three directional surfaces into one CLI row.** docs/requirements/interfaces.toml:2539. Its `cli` requestor row declares exit codes and sign-in stdout readings, while providing no argument schema. A planner consuming this row receives results as the invocation surface, and the architecture has no separate outgoing result seams. project-trajectory/PROCESS.md:1266 explicitly requires separate CLI-argument and exit-code rows; the stdout reading also needs its own channel.

**Verified:** The loop extraction preserves its previous request fields. Recognized missing/unknown readings refuse both ordinary routes before lease or home creation. First approvals participate correctly in `judged` and clear-point retirement. New LLR-305 tags match their modules and symbols; existing row Status values are unchanged; SR-227 satisfies R2. The RESYNC entry exists and `aa749a72` belongs to primary trunk history. Focused tests passed with stubbed launches and probes.

**Commands**

- `Get-Content` and `rg` over the required spec, rulings, reports, process rules, changed source and tests — completed source/text review.
- `git diff aa749a72..53547b55 -- <reviewed paths>`, `--stat`, and `--name-only` — inspected the change range.
- `git show`, `git log`, `git branch`, `git for-each-ref`, `git rev-parse`, and `git merge-base --is-ancestor aa749a72 refactor_again` — confirmed review identity, history, and shipping anchor.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-835 tests/test_coordinator_adjudicate.py tests/test_session_keep.py tests/test_frame_context.py` — **94 passed in 14.15s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi835_review_repro.py` — confirmed probe, trunk-commit/audit, and stale-verdict failures without real model or login calls.
- Inline Python via `python.exe -` — confirmed the Unicode failure, baseline missing-sign-in behavior, changed registry cells, Status preservation, and back-links.
- `git diff --check aa749a72..53547b55` — clean.
- `git status --short` — clean.

Full suite, smoke tier, and shallow-clone test were not run; the shallow-clone test was omitted as instructed because of the sandbox’s Git `sh.exe` Win32 error 5. All writes were confined to `review-tmp`.