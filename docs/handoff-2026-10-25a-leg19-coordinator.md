# Handoff 2026-10-25a (headless leg 19): WI-878 and WI-920 landed, WI-976 filed

It replaces [handoff-2026-10-24a-leg17-coordinator.md](handoff-2026-10-24a-leg17-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 19 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`f1fd0de7-f543-46ff-9daa-fad5a685b193`) continued WI-878, which leg 18
(coordinator session `86d1a7e5-e94b-4188-a637-03c4d5b6b0e2`) had claimed
and built but left unreviewed with no close-out, and landed it; claimed,
re-judged and landed WI-920; and filed WI-976 (P3). It carries no
`Overnight: stop` line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** leg 18's scope-critique commit (`d0457611e`), unpause
  (`a8490c4ab`), WI-878's claim (`b528ba59a`) and restore (`a7c89a5da`);
  then WI-878's landing (`e592e5eee`, act seq 159), the re-mint WI-975
  (`70336fc0a`) closed as settled (`d10265cc2`); the unpause for WI-920
  (`9e5906759`), its claim (`f8d02acb7`) and restore (`825dd47de`), its
  landing (`2695213c6`); WI-976's filing (`eada7b9cd`) and its answered
  critique (`5755a78b6`); then this close-out.
- **WI-878 and WI-920 are closed.** Both specs are archived or complete,
  both lane tips are in `archive/lanes`, and the four spine registries equal
  their anchors (the interfaces anchor was already stale before WI-878 and
  is not one of the four). Their worktrees
  `C:/Projects/ai-template.wt/wi-878` and `wi-920` and their branches
  remain; nothing reads them. WI-920's `scripts/dashboard-shots/node_modules`
  is a junction to the primary checkout's install: remove the worktree with
  `git worktree remove --force`, which leaves the target alone.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373; recount `acceptance_record.py`'s size at its rebase.
- **WI-976** (P3) is queued and claimable: `planmode = "single"`, its scope
  critique answered and confirmed (coordinator-2026-10-25 D-003 to D-005).
  It changes the sitting briefs, so it lands alone, and it ends at an
  owner-held act (SN-036's re-attestation): a leg brings the lane there
  and stops.
- **Watermark** on trunk: WI 976, SR 246, LLR 359, IF 308, TC 398, OI 115;
  acts to seq 159.
  - Lane-held: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-360, TC-399 and IF-309.
- **Smoke ceiling:** `max-tests` is 3410 (the tier counts 3289).
- **Full suite** at `5755a78b6`: 7334 passed, 33 skipped in 23:22.
- **Usage:** this close-out's ingest recorded this session and its
  sub-agents, leg 17's tail and leg 18 (which never closed out). The next
  close-out passes `--session f1fd0de7-f543-46ff-9daa-fad5a685b193`.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:**
  - `C:/Projects/ai-template.wt/review-tmp/2026-10-25a-leg19/` may go once
    read (WI-878's round and gate verdicts, WI-920's raw re-judge material
    the adjudicator read, WI-976's critiques and draft).
  - `2026-10-24b-leg18/` and `2026-10-24a-leg17/` may go; keep the leg-07
    root until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019), coordinator-2026-10-21 D-004 to D-006, and the owner's 2026-10-23
direction that a scope critique settles a row's scope and never grows it
(the rubric's S7). Each row that changes machinery lands alone, after the
cycle has run through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 3 | WI-976 | Claim (critique answered and confirmed), plan in lane, build, review, checkpoint sitting; stop at SN-036's owner-held act, recorded for the owner; it lands alone, after the act |
| 4 | Filings P4 to P6, P8 | P4 and P5 may file (`docs/handoff-2026-10-11-attended-coordinator.md` names them); P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip.
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Hold the FileBackup re-sync (OI-98) until WI-976 lands**, so the one
  known adopter never receives the perspective record (D-003).
- **Confirm or overrule:**
  - coordinator-2026-10-25 D-001 to D-005, notably D-003 (WI-976's
    filing: the six lane-authored sidecars stay as inert records, and
    WI-684 is not edited);
  - wi-878 D-001 to D-008, notably D-004 (round 1 re-rendered after leg 18
    ended unfiled), D-005 (round 1's MINORs, one fixed before the
    checkpoint) and D-008 (the gate's TC-069 tier MINOR to the
    follow-ups);
  - WI-920's re-judge record names its departures (no judge could run a
    shell command in its sandbox); the adjudicator accepted it.
- **Still open from the last handoff**, every item it listed:
  - coordinator-2026-10-24 D-001 to D-005 and wi-856 D-001 to D-006;
  - coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk) and
    wi-851 D-001 to D-014;
  - coordinator-2026-10-22 D-002 to D-004, wi-850 D-001 to D-012 (D-002
    high risk), wi-961 D-010 to D-017 and the earlier items those handoffs
    carried;
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
  - your owner-held rows.
- **Push** `refactor_again` and `archive/lanes`.

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
