# Handoff 2026-10-14c (attended): batch 1 is claimed; WI-913 and WI-914 have first build rounds; P9 is filed and split

Overnight: stop

It replaces [handoff-2026-10-14b-attended-coordinator.md](handoff-2026-10-14b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (no code changed on trunk; no full suite
  owed):
  - `f200e285b`: B4 filed. WI-902's record-at-close amendment, with its lane
    record (`docs/plans/2026-10-11-review-churn/wi-902-lane-record.md`). The
    owner's verdict on coordinator-2026-10-11 D-005 is recorded overruled,
    and the drafts' five calls are coordinator-2026-10-14 D-009 to D-013.
  - `aac06695e`: WI-902's round-1 disposition (D-014). Round 2 approved with
    no findings.
  - `e40114e50` to `e92cec843`: batch 1 claimed under one scoped unpause, in
    landing order (WI-913, WI-911, WI-914, WI-912, WI-916, WI-915). The pause
    was restored byte-identical.
  - `82485c62d`: P9 filed as WI-917 and WI-918, with WI-808 gaining WI-918 as
    a need; D-015 to D-017.
  - `a15beecc0`: WI-917's and WI-918's round-1 dispositions. Both approved at
    round 2 with no findings.
  - The close-out commit: this handoff, status, the log fragment and two
    recipe lessons (§7).
- **Owner rulings, 2026-10-14, in session:**
  - P9 is pulled forward: it lands right after WI-912, as the queue's fifth
    landing, so the overnight runner is usable sooner.
  - P9 is split. WI-917 is the marking (this repo's tooling only: no shipped
    file, no sitting). WI-918 is the merge slot's reading of the re-claim,
    and it lands before WI-808.
- **The overnight runner** is usable once WI-917 lands and the owner drops
  `Overnight: stop` from the handoff. The first headless run is the owner's
  call. Whether the next mechanism lane (WI-916) waits for that run is
  decided and recorded at WI-917's landing.
- **Lanes:**
  - `wi-913` (WI-913, G): build round 1 committed at `4a35bd719` (the
    coordinator re-ran its bar and its three new test modules). Its spine
    change list is `<scratch root>/wi-913/spine-changes.md`. The builder
    left four points for the review round: the gate's interim trace home
    (LLR-313, until Terra authors the gate's own LLR); the dispute-finding
    match, checked only at filing (the gate checks an accepted DISMISS per
    blocking finding id); the paths it holds fail-closed before a pass
    record (`integrate.py refresh`'s regenerated views, `close_partial`'s
    residue); and two hook gaps the landing walk still catches (a commit
    on a detached HEAD, a squash of a commit no local branch holds).
  - `wi-914` (WI-914, B2): build round 1 committed at `2cfe834db` (the
    coordinator re-ran its bar). Its spine change list is
    `<scratch root>/wi-914/spine-changes.md` (LLR-292's proposed Detail).
    Its new bar command, `run.cmd smoke`, exits 1 at `trace.py --strict`
    until LLR-292's act lands, by design.
  - `wi-911`, `wi-912`, `wi-915` and `wi-916`: claimed, with branches at
    `e92cec843` and no worktree or commit yet.
  - WI-798 and WI-902 are unchanged (the 2026-10-11 handoff's "State"
    bullets). WI-902's rebuild re-cuts its lane (D-010).
- **Watermark** on trunk: WI 918; SR 239, LLR 326, IF 293, TC 351, OI 114;
  acts to seq 112.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch root, kept:** `C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/`.
  It holds the critique briefs and verdicts (`crit-<wi>-<round>/`), the
  by-hand `critique-addendum.md`, the drafts, and the lanes' spine change
  lists and basetemps (`wi-913/`, `wi-914/`). Keep each lane's folder until
  that lane lands. The scratch checkout `C:/Projects/ai-template.wt/trunk-tmp`
  is detached at `a15beecc0`.

## How to run reviews now

Unchanged: follow the 2026-10-11 handoff's "How to run reviews now", with
`critique-addendum.md` appended to every critique brief, until WI-911 lands
and the skill says the same. A confirming round's block is in any
`crit-<wi>-r2/brief.md` here. Until WI-911's deliverable 8 lands, a finding
a sitting would defer is ruled ESCALATE, for the owner to rule it a
successor.

## The queue

Every row changes the cycle's machinery, so each lands alone, after the
cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | WI-913 (G) | Built without the gate (D-005); build round 1 is committed. Next: Terra's intent pass authors the change set from the lane's spine change list (SR-154's planning half, LLR-313, the gate's new LLR and TC, TC-333, IF-288 and IF-289, and whether the gate's command line needs its own IF), then the first full-lane review round with three reviewers (Sol, Fable, Opus) from separate renders, then the checkpoint |
| 2 | WI-911 | B1's text, `single`: its plan goes through the landed gate, so it builds after WI-913 lands |
| 3 | WI-914 | B2, `none`: Terra authors LLR-292's amendment from the spine change list, then the first full-lane review round (three reviewers), the amendment sitting and its act, which is trunk's next act (113). Lands after WI-911 |
| 4 | WI-912 | B1's verdict/act split, `single` |
| 5 | WI-917 | P9's marking, `single`: claim it under its own scoped unpause once WI-912 has landed (a hard edge). It lands alone, after the cycle has run once through WI-912's act turn; the overnight runner is usable from then |
| 6 | WI-916 | The RESYNC-presence check, `single`. Whether it waits for the first headless run is decided at WI-917's landing |
| 7 | WI-915 | B3, `single` |
| 8 | WI-902 (B4) | The reshape, `single`: re-cut the lane from trunk's tip and port the survivors the lane record lists (D-010), with a Done-when sitting before its first build (WI-841's hold). Before P4 and P5 |
| 9 | WI-798 | Its remaining steps, as the 2026-10-11 handoff states |
| 10 | P1 to P8, WI-918, then leg 03's rows | As the 2026-10-11 handoff's queue table states. WI-918 lands before WI-808, which needs it. Re-order leg 03's rows against the plan with the owner, and at that step amend WI-801 (it deletes `coordinator_adjudicate.py`, so it must carry WI-912's act turn and trailer line) |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule** `docs/decisions/coordinator-2026-10-14.toml`:
  D-001 to D-005, D-007 and D-008 from the earlier sessions (D-005, the plan
  gate's design, is high-risk), and this session's D-009 to D-014 (WI-902's
  lane calls) and D-015 to D-017 (P9's design: the lane-mode reading, the
  marking's design calls and the re-claim's form). The Trust rulings of
  WI-911 (the SUCCESSOR ruling's), WI-912, WI-913, WI-916, WI-917 (the
  launcher's audit gate) and WI-918 (the re-claim) are in their specs; none
  holds a claim.
- **Still open:** the `wi-880` worktree's uncommitted hook edit (keep or
  discard, then remove the worktree), and the old `coordinator-tools` folder
  (delete once the repo copy has run on a second machine). OI-98 and OI-105
  wait on their conditions.
- **Noted for the queue, not yet filed:** about 150 `RESYNC_PACK.md` entries
  sit under its §4 while its §1.3 tells an adopter to apply only §3's (a row
  before the FileBackup re-sync); and the baseline manifest counts
  regressions two ways (15 strict, 26 by the site test), so the phase-4
  re-measure must name one.

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
   (medium), Claude Fable (medium) and Claude Opus (high) review in parallel,
   a trial (the handoff's "How to run reviews now"); the independent adjudicator
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
