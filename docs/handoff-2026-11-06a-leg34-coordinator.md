# Handoff 2026-11-06a (headless leg 34): WI-997 and WI-991 landed; WI-993 at its first round

It replaces [handoff-2026-11-05b-attended-coordinator.md](handoff-2026-11-05b-attended-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This leg's session is
`9821f7e8-3a3d-4374-b5aa-ea62e7bf28f2`, run `20261106T053406Z-1dfd0f`.

## State (trunk `refactor_again`)

- **Landed:** WI-991 as `fb2bb4e5a` (TC-055 re-judged: six judges APPROVE, RECORDED
  pass). WI-997 as `0c5fc7696` (2151 tags seeded; a strict finding holds tags and
  evidence cells equal, at 0 findings). Both sweeps minted nothing, and both lanes
  are archived and removed. WI-997's acts are seq 174 and 175.
- **WI-993's lane** `wi-993` is claimed and rebased onto `0c5fc7696`, with P1 to P5
  built and attested at `9da666cbf`. Round 1 is filed
  (`docs/reviews/wi-993/001-REVIEW-A-9da666c.md`, `002-REVIEW-B-9da666c.md`) and
  **its triage is owed**: nothing is dispositioned yet, and one counted round is
  spent. REVIEW-A has one MINOR; REVIEW-B has one MAJOR and three MINORs. The MAJOR:
  the command a minted item publishes is refused whenever another row of the same
  registry is unanchored. Findings are claims: confirm it first. The lane's decisions
  record is `docs/decisions/wi-993.toml`. Its spine change list is at
  `C:/Projects/ai-template.wt/review-tmp/2026-11-06-leg34/wi-993-spine-changes.md`.
- **WI-1001:** its round-1 scope critique came back CHANGES-REQUESTED (three MAJORs,
  two MINORs). The findings are recorded in `docs/specs/WI-1001.md`, and their
  dispositions are owed before its confirming round.
- **Watermark** (trunk): WI 1001, SR 246, LLR 366, IF 308, TC 412, OI 129. Acts run
  to seq 175.
- **Bars:** the full suite ran at `0c5fc7696`, in two halves from `trunk-tmp`: 7709
  passed, 33 skipped, no failure. The commit carrying this handoff states its smoke
  result. The tier's CPU read 497.1 s, 655.4 s and 525.2 s across the leg's three
  quiet readings against 540, so the one over the limit is noise, not the tags.
- **Usage:** see "Usage" below. The next close-out passes
  `--session 9821f7e8-3a3d-4374-b5aa-ea62e7bf28f2`.
- **Pause:** `docs/work/pause` is tracked and unchanged (sha256 `b0a709c8…`),
  restored byte-identical after the claims of WI-993 and WI-991.
- **Disk:** 34G free on C:.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-11-06-leg34/` holds
  WI-993's change list; it may go once WI-993 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first, and tell it never to hand a
  test run to a background sub-agent.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.

## The queue

The owner's order stands (coordinator-2026-11-03 D-003 and D-004). Each row that
changes machinery lands alone, after the cycle has run through the last
landing's changed steps. WI-983's changed step runs at the next decomposition
round's sitting, which no scheduled row is known to draw. WI-997's changed step,
an intent row's evidence note, runs at the next intent turn that adds a TC.

**Only the rows in this table are claimed**, in order and under their `needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route. Skip it while held |
| 2 | WI-995 | Critique confirmed, and WI-997 has landed. Claim it |
| 3 | WI-996 | Critique confirmed. Claim once WI-995 lands |
| 4 | WI-993 | Claimed. Triage round 1, then its fix round, checkpoint, gate and landing |
| 5 | WI-1001 | Dispositions of its round-1 critique, its confirming round, then claim |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-827 (attended only, though the frontier lists it as ready; it never lands
  from a lane);
- WI-908 (OI-122: the owner present);
- WI-964 (OI-123: the owner's Mac);
- WI-998 (off the table until a sample exists, though the frontier lists it);
- WI-999 and WI-1000 (OI-129);
- every row under `docs/work/deferred/` (D-011, D-016).

## For the owner

1. **A read you should know about.** A WI-997 builder's repo-wide search returned two
   lines of `OWNER_SCRATCHPAD.md`, one cut off. It reported this, says it used neither,
   and excluded the file afterwards. Nothing from them reached a commit. Every brief
   since has told builders to exclude the file, and the recipes now say so.
2. **WI-1001's debt cases.** Its critique's first MAJOR asks for WI-1000 and WI-999 in
   its `needs`, which would hold it on OI-129. Its Done-when allows "each exception
   named in the row". The disposition could go either way; a leg will take the `needs`
   route unless you say otherwise, since it adds no exception mechanism.
3. **TC-333.** Its false sentence is cut to what its rows state, blessed at the
   sitting. The tested clause that the planner template names no repository row left
   the cell with it, because no row states that clause (a gate MINOR).
4. **TC-055's focus ring.** One judge noted that no shot holds a focused control, so
   the rubric's T5 focus-ring clause went unseen by all six. It is not a finding. It
   is listed under status.md's unfiled follow-ups.
5. **Your local branch.** `git branch -f rolling_review origin/rolling_review` drops
   only a copy of WI-983 that trunk already holds. Until then, do not push local
   `rolling_review`.
6. **OI-129** (holds WI-999 and WI-1000): build or retire SR-165's derivation record
   and SR-035's token scan.
7. **OI-124** (WI-910) and **OI-121**'s attended session for WI-827.
8. **WI-998:** moving it to `docs/work/deferred/` would stop it reading ready.
9. **The FileBackup re-sync (OI-98):** first fix the act ledger entry's overwrite list
   and the tag entry's PROCESS classing, and amend TC-036's inputs to add
   `RESYNC_PACK.md`. WI-997's entry is a forced migration: seed your tags before
   re-syncing past it. FileBackup is on `Rust-Rewrite`, so the scratch trial needs a
   copy.
10. **Confirm or overrule:** coordinator-2026-11-06 D-001 and D-002, and everything
    the [replaced handoff](handoff-2026-11-05b-attended-coordinator.md) lists in its
    item 6.
11. **Push** `refactor_again`, `archive/lanes` and `id-carrier`, after item 5.

## Usage

`usage_ingest.py` for this session exited 0. The run for the replaced handoff's
session, `--session 3c08c037-5aaf-4966-971a-0109570bd30e`, exited 1 and printed:

```text
refused C:\Users\Peter\.claude\projects\c--Projects-ai-template\3c08c037-5aaf-4966-971a-0109570bd30e.jsonl: line 32: type 'tools-used' is unknown
```

It is not hand-patched.

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
