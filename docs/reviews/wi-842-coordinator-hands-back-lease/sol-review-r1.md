2082e89a NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/coordinator_guard.py:786 — **A previous holder’s relaunch request blocks the current holder’s hand-back.** Confirmed sequence: A takes the lease, requests relaunch, then crashes before SessionEnd; the owner releases A; B takes the lease and closes with a valid handoff, requesting no relaunch. A’s request remains, so B’s hand-back refuses and tells B to exit for a successor. B’s SessionEnd instead rejects A’s foreign request, launches nothing, and leaves B’s lease held. The next coordinator again needs an owner release. Distinguish the current holder’s pending relaunch from superseded requests, and cover this recovery sequence.

## MINOR

- project-trajectory/scripts/coordinator_guard.py:776 — **Handoff validation can suppress the required non-holder recovery guidance.** A foreign or unnamed caller naming a missing or promptless handoff receives only “no session prompt,” because validation returns before the holder check. This contradicts the Done-when’s “Any other caller … told the owner releases” and docs/requirements/low-level-requirements.toml:3163. Confirmed with a foreign caller and absent handoff; the lease remains unchanged.

## Verified

Read the full WI, referenced WI-822 spec, builder notes, applicable PROCESS rules, and every changed file. Ordinary and drained hand-backs free the lease and permit another take. The six new tests fail against the baseline and pass against the reviewed implementation. SR-229’s requirement cell complies with R2; the hand-back backlink resolves to LLR-300’s module and symbol; no Status cells changed. Skill mirrors are byte-identical, and the RESYNC entry anchors at a trunk ancestor. The worktree remained clean.

The permitted test run produced **83 passed, 1 failed**: the unchanged POSIX launcher test failed before executing its launcher because Git Bash reported `CreateFileMapping … Win32 error 5`. Strict trajectory validation exited 0 with warnings.

## Commands

All Python runs used `PYTHONDONTWRITEBYTECODE=1`; pytest runs used the required literal scratch basetemp.

- `git status --short` — clean before and after review.
- `git diff --stat 8803d2ef..2082e89a`, `git diff --name-status 8803d2ef..2082e89a`, and path-filtered `git diff 8803d2ef..2082e89a -- …` — inspected all 11 changed files.
- `git diff --check 8803d2ef..2082e89a` — clean.
- `git log -4 --format='%h %s'`, `git branch --all --contains 8803d2ef`, `git rev-parse refactor_again`, `git merge-base --is-ancestor 8803d2ef refactor_again`, and `git show --no-patch --format='%h %s' 8803d2ef` — checked reviewed history and RESYNC anchoring.
- `git show 8803d2ef:project-trajectory/scripts/coordinator_guard.py` — confirmed baseline release preserves the request file.
- `Get-Content`, `Select-Object`, and `rg` inspections — read the specified documents, skills, guard implementation, test modules, conftest, lease-store helpers, registry cells, and runtime flows.
- `Get-FileHash project-trajectory/skills/session-protocol/SKILL.md,.claude/skills/session-protocol/SKILL.md,.agents/skills/session-protocol/SKILL.md` — identical SHA256 hashes.
- `Set-Content` — created only the baseline pytest plugin and reproduction script under the authorized review scratch directory.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-842-sol tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py
```

83 passed, 1 environment failure in 19.26s.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict
```

Exit 0; clean, with warnings.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -p wi842_baseline_plugin -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-842-sol tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py -k "hand_back or hands_back"
```

Scratch plugin substituted the `8803d2ef` guard implementation: 6 expected failures in 3.51s.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-842-sol tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py -k "hand_back or hands_back"
```

Reviewed implementation: 6 passed in 2.00s.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi842_stale_request_probe.py
```

Confirmed the stale-request failure, zero successor launches, and B’s retained lease.

```powershell
$validationProbe | C:/Projects/ai-template/.venv/Scripts/python.exe -
```

Confirmed missing owner-release guidance for a foreign caller naming an absent handoff.