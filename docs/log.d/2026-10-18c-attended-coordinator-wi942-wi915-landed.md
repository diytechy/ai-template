## 2026-10-18 — Attended coordinator (c): WI-942 and WI-915 landed, WI-927 through its fix round, three builds in

An attended session from the 2026-10-18b handoff's queue. Lease taken at
its start and handed back at its close-out. No owner ruling was asked for;
the session's calls are in each lane's decisions record.

- **WI-942** (the merge slot reads an acted row's registry from its id):
  rebased, the judged rows checked unchanged since the verdict, its RESYNC
  entry re-anchored, the convergence map recorded (wi-942 D-004); the gate
  named one condition in both reviews, the act still owed after the accepted
  sitting, re-graded as the act turn's to answer (D-005); the act took seq
  129. Landed as `5790639d4`; the sweep's re-mint WI-945 closed as already
  settled.
- **WI-915** (one `docs/stack.ini` reader): round 1's two wording MINORs
  fixed by the coordinator (wi-915 D-004); the gate approved with no
  findings; the rebase conflicted only in RESYNC_PACK, the lane's diff
  otherwise byte-identical, so no post-rebase round (D-006). Landed as
  `b120c4722`, its bar within budget beside its parent's; the sweep minted
  nothing.
- **WI-927:** Terra's intent and P5's RESYNC entry in one commit, since the
  bar now refuses a shipped change without its entry (wi-927 D-005); round
  1 found a consent question hidden at a POSIX terminal and five POSIX-only
  test reds (the coordinator's WSL run found the same five); one two-stage
  fix round closed both and a JSON-null gap (D-006, D-007), POSIX-verified.
- **WI-943:** rebased onto WI-942's landing; build round 1 and Terra's
  intent committed (wi-943 D-001, D-002).
- **WI-925, WI-926:** build round 1 of each built, uncommitted at the
  close-out and backed up beside the worktrees: WI-925 waits on the
  coordinator's rulings on its builder's stop items, WI-926 on Terra's
  component rows and a re-tier of its routes test.
- **Full suite** at `b120c4722`: 6297 passed, 22 skipped, 0 failed.
- **Procedure folded into the recipes:** a gate finding that an accepted
  sitting's act is still owed is re-graded; create a reviewer's scratch
  folder before its launch; a lane rebased past the re-sync entry check
  carries its entry in its first commit; name WSL's Ubuntu distro and run
  the lane's base beside it.
