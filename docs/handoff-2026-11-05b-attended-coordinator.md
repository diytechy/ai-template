# Handoff 2026-11-05b (attended): OI-121, OI-126, OI-127 and OI-128 ruled; the queue can move

It replaces [handoff-2026-11-05a-leg33-coordinator.md](handoff-2026-11-05a-leg33-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This attended session was
`3c08c037-5aaf-4966-971a-0109570bd30e`. It wrote the rulings and this handoff, and built nothing.

## State (trunk `refactor_again`)

- **The primary checkout is back on `refactor_again`.** Local `rolling_review`
  still holds a copy of WI-983's landing (For the owner, item 1).
- **Rulings** (`docs/log.d/2026-11-05-owner-rules-oi121-oi126-oi127.md`,
  `docs/decisions/coordinator-2026-11-05.toml`):
  - OI-121 (a): WI-827 runs in an attended session only.
  - OI-126 Q1 (a), Q2 (a): a lane never parks for a held-rung approval. It
    lands its text and the act is ruled on trunk. WI-993's Done-when carries
    this; its confirming round is owed.
  - OI-127 (b), revised: TC-165's token-scan half and TC-166 leave WI-997.
    Its amended Done-when is blessed by D-001.
  - OI-128: `npm ci` ran in `scripts/dashboard-shots` in this session
    (playwright 1.61.1; Chromium launches). A leg installs nothing: a lane
    uses the recipes' junction to the primary checkout's install.
- **WI-997's lane** `wi-997` is rebased onto the commit carrying this handoff.
  Its pre-rebase tip is `519d6bc21`: add it at the landing's archive step. It
  holds plan revision 1, a decisions record, no critique, no pass record and no
  build, so the plan cap is unspent. Revision 1 was written against the old
  stop, so the plan is revised for the two moved cases before its critique.
- **Filed:** WI-999 is now TC-166's row; WI-1000 (TC-165's token scan); WI-1001
  (an approved automated test case with no tagged test is a strict finding);
  OI-129 (build or retire), which WI-999's and WI-1000's needs cite.
- **Watermark** (trunk): WI 1001, SR 246, LLR 365, IF 308, TC 409, OI 129. Acts
  run to seq 173.
- **Bars:** the commit carrying this handoff states its smoke result. The last
  full suite is leg 33's, at `ef2d68610` (7687 passed, 33 skipped). No code has
  changed since.
- **Usage:** this session's ingest is recorded below under "Usage". The next
  close-out passes `--session 3c08c037-5aaf-4966-971a-0109570bd30e`.
- **Pause:** `docs/work/pause` is tracked and unchanged (sha256 `b0a709c8…`),
  and no judgement is active.
- **Disk:** free space on C: swung between 15G and 38G on 2026-11-05 as other
  work ran. The full suite needs about 4 GB.
- **Scratch:** leg 33's root,
  `C:/Projects/ai-template.wt/review-tmp/2026-11-04-leg33/`, may go now.

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
round's sitting, which no scheduled row is known to draw.

**Only the rows in this table are claimed**, in order and under their `needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route. Skip it while held |
| 2 | WI-997 | Claimed, lane rebased. Revise the plan for the two moved cases, then its critique, then build |
| 3 | WI-995 | Critique confirmed. Claim once WI-997 lands |
| 4 | WI-996 | Critique confirmed. Claim once WI-995 lands |
| 5 | WI-993 | Its confirming round, then claim |
| 6 | WI-991 | TC-055's re-judge by its Method (the recipes' section 8); a fail is recorded as a fail |
| 7 | WI-1001 | Its scope critique, then claim once WI-997 lands |

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

1. **Your local branch.** `git branch -f rolling_review origin/rolling_review`
   drops only a copy of WI-983 that trunk already holds. Until then, do not
   push local `rolling_review`. Its upstream has moved on to 14 commits past
   the shared point.
2. **OI-129** (new; holds WI-999 and WI-1000): build or retire SR-165's
   derivation record and SR-035's token scan.
3. **OI-124** (WI-910) and **OI-121**'s attended session for WI-827.
4. **WI-998:** moving it to `docs/work/deferred/` would stop it reading ready.
   No scheduled row produces its sample.
5. **The FileBackup re-sync (OI-98):** first fix the act ledger entry's
   overwrite list and the tag entry's PROCESS classing, and amend TC-036's
   inputs to add `RESYNC_PACK.md`. FileBackup is on `Rust-Rewrite`, so the
   scratch trial needs a copy.
6. **Confirm or overrule:** coordinator-2026-11-05 D-002 and D-003, and
   everything the [replaced handoff](handoff-2026-11-05a-leg33-coordinator.md)
   lists in its items 6 and 8.
7. **Push** `refactor_again`, `archive/lanes` and `id-carrier`, after item 1.

## Usage

Both `usage_ingest.py` runs (this session, then leg 33's id) exited 0 and 0.

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
