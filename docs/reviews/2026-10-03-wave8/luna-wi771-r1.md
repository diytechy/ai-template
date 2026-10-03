# Luna review — WI-771 (r1)

Reviewer: Codex Luna (gpt-6-luna, high), through `luna_review.sh` (lane unchanged). Builder: Claude Opus (kit-builder rules).

94ccce56 NOT YET SOUND

## BLOCKER

None.

## MAJOR

- `docs/requirements/system-requirements.toml:1316, 1318` still say an observation case “evidences an assumption.” A sampled observation passes, and an adopter could read this requirement and its acceptance criteria as allowing that pass to support the assumption. That contradicts the ruling that a pass proves nothing beyond its sample and conflicts with SR-206, which lets an active assumption pass regardless of results.

## MINOR

None.

**Verified:** The release gate reads standing and accepted-risk state; the retirement records name successors SR-201, LLR-238 and TC-233; TC-238 now verifies IF-216’s falsification and accepted-risk behavior. The RESYNC_PACK entry is anchored at `ae702b75`. No evidence level remains in the live renderer or computation paths. The worktree is clean.

**Commands**

- Focused pytest command from the spec: **302 passed, 1 failed**. The shallow-clone test failed because Git for Windows reported `CreateFileMapping ... Win32 error 5`.
- Isolated retry of that test: **1 failed** with the same Git for Windows process-mapping error.
- `check_trajectory.py --strict`: **clean, exit 0**, with repository advisories.