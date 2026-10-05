c1fd7837 NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/coordinator_guard.py:706 — **Failed-launch recovery remains incomplete.** After the request is renamed to `.consumed`, saving the successor token happens outside the restoration handler. Injecting a disk-full error into that save leaves one consumed request, no `relaunch.json`, and no launched successor. This contradicts LLR-301’s promised recovery for every failure before launch confirmation.

- project-trajectory/scripts/coordinator_guard.py:759 — **Windows relaunch fails when the repository path contains spaces.** The generated `cmd /c` command lacks the outer quoting needed to preserve its quoted command path alongside quoted arguments. A hidden-console probe using `root with spaces` exited 1 without running the harmless launcher. The same launcher succeeded with an explicit outer quote pair. Existing launcher tests use paths without spaces.

## MINOR

- docs/test/test-cases.toml:3179 — **IF-274 has the wrong verification link.** TC-315 exercises transcript occupancy, not the hook’s stdin JSON contract. Breaking `_hook_main`’s stdin parsing leaves that evidence unaffected. The relevant test, `tests/test_coordinator_guard_e2e.py:98`, is absent from every TC’s evidence. Link the interface to the test that actually exercises it.

- docs/id-watermark:30 — **IF-276 is available for reuse despite D-013 retiring it.** The watermark is 275; the next allocation therefore receives IF-276. D-013 explicitly says that removed seam’s ID stays retired, and the committed round-2 report already cites it. Preserve that reservation.

## Verified

Round-1’s Windows console handles, fenced headings, recorded compaction evidence, dispatcher exception, seam declarations, unrounded comparison, claim-reason assertion, `exec_claude` description, and Full-tier corrections are addressed. Launch recovery is only partially fixed, as reported above. The Windows probe confirmed working console handles for all three streams; relevant regression probes failed against the earlier implementation.

The SR requirement cells comply with R2. Existing row amendments are limited to LLR-140’s detail and LLR-270’s symbols/detail; no Status flips occurred. Shipping inventory and the RESYNC entry anchored at trunk ancestor `176b6aef` are present. The worktree and index remained unchanged. Actual Claude exit-survival behavior remains unverified.

## Commands

Repeated reads and searches are grouped.

- `Get-Content` and numbered/ranged reads — read CLAUDE.md, the two applied skills, PROCESS.md, complete WI/spec, prior reviews and briefs, decisions, code, tests, settings, launchers, registries, status and coordinator log.
- `rg -n ...`; `rg --files ...` — located rules, symbols, backlinks and evidence. One PowerShell wildcard-path search failed; subsequent searches resolved the locations.
- `git status --short`; `git diff --stat 883b3edf..c1fd7837`; `git log --oneline 883b3edf..c1fd7837` — inspected the clean starting state and change inventory.
- Scoped `git diff` calls over the lane and fix ranges — inspected authored changes and generated-view deltas.
- `git diff --check 883b3edf..c1fd7837` — passed.
- `git merge-base --is-ancestor 176b6aef 883b3edf`; `git rev-parse HEAD` — confirmed the trunk anchor and reviewed tip.
- `$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"`; `$env:PYTHONDONTWRITEBYTECODE = "1"` — constrained test discovery and disabled bytecode writes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-822 tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_session_keep.py tests/test_seam_resolution.py` — **138 passed, 1 failed in 21.10s**. Git Bash failed with `CreateFileMapping` access error before POSIX launcher assertions.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0: **clean; 820 work items, 723 done, 26 cancelled, graph acyclic**. Advisory warnings remain.
- PowerShell Python-stdin probes, confined to `review-tmp` — confirmed both launch defects, Windows handles, regression failures, exact registry amendments, equal skill copies and IF-276 allocation exposure. Exploratory API-signature and encoding failures were followed by corrected probes.
- Official [hooks reference](https://code.claude.com/docs/en/hooks) `open`/`find` calls — checked event and output contracts.
- `git status --porcelain`; `git diff --quiet`; `git diff --cached --quiet` — final worktree and index unchanged.