# Handoff 2026-10-14b (attended): batch 1's scope critiques are settled; B4 is next

Overnight: stop

It replaces [handoff-2026-10-14-attended-coordinator.md](handoff-2026-10-14-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (no code changed; no full suite owed):
  every batch-1 critique finding dispositioned in its row's "Critique
  dispositions" section (`b48e82227`, `fad552898`, `93f882b6b`), with
  coordinator-2026-10-14 D-006 to D-008, and the recipes' lessons in the
  close-out commit.
- **Owner rulings, 2026-10-14, in session:**
  - a confirming scope-critique round runs in convergence stance: it
    confirms each adoption (a failed confirmation keeps its original
    severity), and a new finding blocks the claim only if it is fail-open,
    data loss or a Done-when gap; any other new finding's disposition goes
    into the spec with no further round;
  - only the dispute sitting moves a BLOCKER or MAJOR to a successor row:
    the reviewer only tags each finding's class, and WI-911 adds a
    SUCCESSOR ruling to the dispute grammar (its deliverable 8, with a
    Trust section). D-006, which had given that say to the brief's
    convergence marking, is recorded overruled;
  - asked whether to raise the three-round review cap, the owner heard the
    coordinator's recommendation to keep it (the cap drops nothing: open
    findings go to the sitting, and a convergence-class finding is never
    deferred) and to revisit it with the trial's per-reviewer counts after
    about five lanes. Nothing was ruled.
- **Scope critiques: batch 1 is settled for the claim.** WI-911 (round 5,
  at `93f882b6b`), WI-912 (round 3), WI-913 (round 3), WI-914 (round 1),
  WI-915 (round 2) and WI-916 (round 3) APPROVE; the verdicts are in the
  scratch root's `crit-<wi>-<round>/`. All the critiques
  were Sol's; every finding was checked and none refuted, and three of the
  later-round MAJORs were defects the previous dispositions had introduced.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **No lease is held after the handback; no judgement is active.**
  `docs/work/pause` is tracked and unchanged.
- **Lanes:** WI-798 and WI-902 are unchanged (the 2026-10-11 handoff's
  "State" bullets still hold), and nothing is claimed.
- **Watermark** on trunk: WI 916; SR 239, LLR 326, IF 293, TC 351, OI 114;
  acts to seq 112.
- **Scratch root, kept:** `C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/`
  (critique briefs and verdicts in `crit-<wi>-<round>/`, the by-hand
  `critique-addendum.md`, the planner drafts in `drafts/`, M's
  intermediates). Delete it only after B4 is filed. The scratch checkout
  `C:/Projects/ai-template.wt/trunk-tmp` is detached at `93f882b6b`.

## How to run reviews now

Follow the 2026-10-11 handoff's "How to run reviews now", with
`critique-addendum.md` appended to every critique brief, until WI-911 lands
and the skill says the same; the two owner rulings above apply now. The
recipes (§1, scope critique) say where a confirming round's block comes
from. Until WI-911's deliverable 8 lands, the dispute grammar has no
SUCCESSOR: a finding a sitting would defer is ruled ESCALATE, for the owner
to rule it a successor (the coordinator's interim reading, recorded here
for the owner to overrule).

## The queue

The batch's edges are soft, so it is claimed under one scoped unpause; the
order below is the landing order, and each row's Done-when carries its holds.
Every row except M changes the cycle's machinery, so each lands alone, after
the cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | B4 | File WI-902's record-at-close amendment from `drafts/WI-902-amendment.md` with its lane record (`drafts/WI-902-lane-record.md`), then its scope critique. The same commit records the owner's 2026-10-14 verdict on coordinator-2026-10-11 D-005 (`owner = "overruled"`, the 2026-10-11 handoff's B4 verdict text as `review`), and the amended spec cites it as `docs/decisions/coordinator-2026-10-11.toml#D-005` (ruling-sync). The drafts' five open calls, with this session's proposed answers for the filer to rule and record: (1) no act of 113 to 117 lands: 113's and 114's rows re-sit at the rebuilt checkpoint, and 115 to 117 retire; (2) re-cut the lane from trunk's tip and port the survivors, archiving the old tip whole, instead of a 48-commit rebase that drops five act commits (no interactive rebase here, and each replayed registry commit risks recipes §4's conflicts); (3) keep LLR-335, TC-360 and IF-294 (keep-or-mint: the spirit is retained, fewer changes, and trunk never saw the old text); (4) the record's carrier is a declared `Adopted` column, as `Adjudicates` and `Digests` are; (5) the unpaired-fence fix stays with the record (S1, as filed). Add to its Trust section the lane record's last note: a successor cancelled on trunk between the close and an unrebased landing is not re-checked (the owner's validate-once trade). The rebuild owes a Done-when sitting before its first build (WI-841's hold) |
| 2 | Claim | One scoped unpause for WI-911 to WI-916 (recipes §2) |
| 3 | WI-913 (G) | Build first: `planmode = "none"`, built without the gate it builds (D-005) |
| 4 | WI-911 | B1's text, `single`: its plan through the landed gate |
| 5 | WI-914 | B2, `none`: may build beside the above; lands after WI-911. Its LLR-292 act is trunk's next act (113) |
| 6 | WI-912 | B1's verdict/act split, `single` |
| 7 | WI-916 | The RESYNC-presence check, `single`, after WI-914 |
| 8 | WI-915 | B3, `single` |
| 9 | WI-902 (B4) | The reshape, `single`, before P4 and P5 |
| 10 | WI-798 | Its remaining steps, as the 2026-10-11 handoff states |
| 11 | P1 to P9, then leg 03's rows | As the 2026-10-11 handoff's queue table states; re-order leg 03's rows against the plan with the owner. At that step, amend WI-801 (it deletes `coordinator_adjudicate.py`, so it must carry WI-912's act turn) |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule** `docs/decisions/coordinator-2026-10-14.toml` D-001
  to D-005, D-007 and D-008 (D-005, the plan gate's design, is high-risk;
  D-006 you overruled in session). The Trust rulings of WI-911 (the
  SUCCESSOR ruling's), WI-912, WI-913 and WI-916 are in their specs for you
  to confirm or overrule; none holds the claim.
- **Still open:** the `wi-880` worktree's uncommitted hook edit (keep or
  discard, then remove the worktree), and the old `coordinator-tools`
  folder (delete once the repo copy has run on a second machine). OI-98 and
  OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:** about 150 `RESYNC_PACK.md` entries
  sit under its §4 while its §1.3 tells an adopter to apply only §3's (a
  row before the FileBackup re-sync); and the baseline manifest counts
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
