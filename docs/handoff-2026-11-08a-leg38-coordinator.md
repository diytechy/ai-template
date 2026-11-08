# Handoff 2026-11-08a (headless leg 38): WI-1002 and WI-996 landed; the queue waits on the owner

It replaces [handoff-2026-11-07c-attended-coordinator.md](handoff-2026-11-07c-attended-coordinator.md)
as the resume map, and carries its owner items unchanged except where this
file says. The procedure is in the `coordinator-cycle` skill and its recipes;
this handoff holds state only. This leg is session
`6ff8217f-0977-47d2-976f-36ec59e2e4b1`, run `20261107T203037Z-c932d2`. It
closed out at about 32% of its window because no row can move without the
owner.

Overnight: stop

## What happened

- **WI-1002 landed** (`f24a68ca2`, act 179). The leg attested the crashed
  build, then ran one counted round (both APPROVE), the checkpoint (sitting
  003, MEANING, LLR-143 and TC-137 blessed), the gate (both APPROVE) and the act.
- **WI-996 landed** (`633715041`, acts 180 and 181). The leg rebased the lane
  onto WI-1002's landing with the partial build stashed around the rebase. A
  builder kept that build whole and finished C3 and C4, committed as two
  attests. Then:
  - two counted rounds; round 1's MAJOR (a tests root of `.` counted the
    declaration) was fixed with a regression test;
  - the checkpoint, sitting 005: SR-156 and LLR-207 MEANING+BLESS, LLR-368 and
    TC-421 to TC-426 approved;
  - the gate's convergence-class MAJOR went to dispute sitting 008, which
    ruled FIX, so the coordinator's hand landing now runs the red-mark check
    on its staged squash (recipes §3);
  - one fix round, then a final review, both APPROVE.
- Both sweeps minted nothing. Both lanes' tips are archived to `archive/lanes`.
  Their worktrees and branches are removed, and leg 36's and leg 37's scratch
  roots are deleted (coordinator-2026-11-08 D-002).

## State (trunk `refactor_again`)

- **Open claims:** none (`git ls-tree --name-only refactor_again docs/work/active/` is empty).
- **Primary checkout:** on `refactor_again`. `trunk-tmp` is detached at `633715041`.
- **Bars:** full suite at `633715041`, run as two foreground halves:
  4021 passed and 21 skipped, then 3886 passed and 8 skipped. The commit
  carrying this handoff states its smoke result. The landing's smoke tier read
  CPU 543.3 s against `cpu-seconds = 540`, which is reported only. Judge it at
  the next `run.cmd audit`.
- **Pause:** `docs/work/pause` is tracked and unchanged. The leg claimed
  nothing.
- **Usage:** `usage_ingest.py` exited 1 on both runs. It recorded every
  sub-agent of this leg (reviewers and builders), then refused the session
  transcripts. The first run printed
  `refused C:\Users\Peter\.claude\projects\c--Projects-ai-template\6ff8217f-0977-47d2-976f-36ec59e2e4b1.jsonl: line 1: type 'session-owner' is unknown`.
  The second (`--session 0fca19d1-aa5c-4130-a090-0bee2abcf379`) printed the
  same refusal for that transcript's line 2. Nothing was hand-patched. The
  defect is listed under status.md's unfiled follow-ups.
- **Disk:** 30G free on C:.
- **Scratch:** this leg's root `C:/Projects/ai-template.wt/review-tmp/2026-11-07-leg38/`
  holds the briefs, verdict drafts and logs. Its basetemps are deleted. Delete
  the root once this handoff is read.

## The queue

The owner's order stands (coordinator-2026-11-03 D-003 and D-004). **Only the
rows in this table are claimed**, in order and under their `needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route. Skip it while held |
| 2 | WI-1001 | Critique confirmed. Waits on WI-999 and WI-1000 (OI-129). Skip it while held |

**Never claimed by a leg:** WI-684 (OI-98, the owner's re-sync); WI-795
(OI-105, then WI-820); WI-827 (attended only; it never lands from a lane);
WI-908 (OI-122: the owner present); WI-964 (OI-123: the owner's Mac); WI-998
(off the table until a sample exists); WI-999 and WI-1000 (OI-129); every row
under `docs/work/deferred/` (D-011, D-016).

WI-996's changed steps run at the next lane's first attest, its refresh and
its hand landing. WI-993's held-act arm and WI-983's decomposition arm are
still waiting for a row that exercises them.

## For the owner

1. **The queue is empty without you.** Ruling OI-124 or OI-129 (items 6 and 7
   below) frees a row. Otherwise file or re-order rows for the next run.
2. **WI-996 is a forced adopter migration.** Every adopter declares
   `[bars] red_mark`, and a lane cut before the landing refuses at `attest`
   until it rebases. Two lanes are affected today: the `wi-902` worktree
   (`bf96c4de7`; trunk no longer tracks its claim) and
   `codex/simplify-spine-resync` at `D:/ai-template-spine-resync`
   (wi-996 D-005).
3. **Confirm or overrule wi-996 D-005.** The fix round moved the review set's
   test-file rule byte for byte from `gen_arch_map.py`, which is outside the
   plan's file list, into `kitlib/spine.py`. The counter and the tag reader now
   call one predicate.
4. **WI-996's near-miss spelling (wi-996 D-007, D-010).** A strict mark written
   with an added argument, such as `reason=`, counts 0, so its still-red test
   can land green. The spec's coverage bound puts this outside the check, and
   the skill now says to write the declared text verbatim. The open choice is
   whether to widen the count to the declared text's call head, or to state
   the bound in SR-156.
5. **Usage ingest:** `usage_ingest.py` refuses Claude Code's new
   `session-owner` transcript record (see State). The defect is listed under
   status.md's unfiled follow-ups. Filing it as a row is your call.
6. **OI-129** (holds WI-999 and WI-1000, and so WI-1001): build or retire
   SR-165's derivation record and SR-035's token scan.
7. **OI-124** (WI-910) and **OI-121**'s attended session for WI-827.
8. Unchanged from the replaced handoff: its items 1 (wi-995 D-003), 2
   (WI-1001's read), 3 (WI-995's re-attest), 6 (WI-998), 7 (the FileBackup
   re-sync, OI-98), 8 (your local `rolling_review` branch), 9 (the confirm or
   overrule list), 10 (push `refactor_again`, `archive/lanes` and
   `id-carrier`, after item 8), 11 (the weekly usage limit) and 12 (the
   machine crash).
9. **Confirm or overrule this leg's calls:** coordinator-2026-11-08 D-001 to
   D-003, wi-1002 D-001 to D-004, and wi-996 D-003 to D-010.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running ATTENDED in an interactive
session with the owner. Ask the owner at real decision points; record every
other call in docs/decisions/. Background tasks and notifications are fine
here (this is not a headless leg).

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, report why and stop.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names), all of it; the Status and every "Owner
   rulings" section of docs/plans/2026-10-11-review-churn/README.md
   (2026-10-11 through revision 37) and its pointer-rules.md; the
   coordinator-cycle skill and its references/recipes.md;
   your memory index (review-churn-program-rulings first).
3. Run reviews the way the handoff's "How to run reviews now" says. It
   overrides the skill where they differ, until batch row B1 lands and the
   skill says the same.
4. Work the handoff's queue table in order: the "pre" trunk fix and the
   baseline manifest (M); file and
   land B1, then the plan gate G, then B2–B4 (B4 is WI-902's reshape), each
   filed on trunk with its scope critique and dispositions first; then
   continue WI-798; then P1–P9 under the dependencies their rows name; then
   re-order leg 03's rows against the plan with the owner. Claim under
   one scoped unpause per batch (a reviewed deletion commit, the claims, a
   byte-identical restore). Cut lanes from trunk's tip and land them one at a
   time. Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
   (medium) authors spine text in one retained session per lane; Codex Sol
   (medium) and Claude Opus (high) review in parallel (coordinator-2026-10-16
   D-008; the handoff's "How to run reviews now"); the independent adjudicator
   judges spine text and disputes through coordinator_adjudicate.py from the
   lane (set AGENT_CLAUDE_TOKEN_FILE to the token file's path from memory
   first; never read the file), never a sub-agent.
5. Before each landing commit: regenerate the views, run the smoke bar and its
   budget, run trace.py --strict and check_trajectory.py --strict, and read
   the summaries for failures.
6. Close out when `coordinator_guard.py status` reads 40% or more, at the
   latch, or when the owner says so (session-protocol section 4): land or
   safely commit every lane; update docs/status.md (forward-only); write a NEW
   handoff whose `## Session prompt (paste to start the next session)` block is
   this prompt, copied verbatim, keeping the `Overnight: stop` line unless the
   owner asks for headless legs; write a log fragment; fold procedural lessons
   into the coordinator-cycle skill; run the full suite once if code changed;
   commit; then `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review or adjudicate through a sub-agent; change ~/.claude
settings or install software; bypass a commit hook.
```
