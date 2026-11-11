# Handoff 2026-11-11a (attended analysis): OI-130 re-scored; the queue still waits on the owner

This handoff replaces
[handoff-2026-11-08c-leg39-coordinator.md](handoff-2026-11-08c-leg39-coordinator.md)
as the resume map. It carries that handoff's owner items unchanged except
where this file says otherwise. The procedure is in the `coordinator-cycle`
skill and its recipes; this handoff holds state only.

This was an attended analysis session with the owner, not a coordinator
session. It took no lease, claimed nothing, and changed no code, registry row
or open item. Its session id is `728a1840-6889-4e4c-a57d-c9a6302c34e9`.
`usage_ingest.py` was not run. The next close-out's `--session` run records
this session, and leg 39's open `session-owner` refusal still applies to it.

Overnight: stop

## What happened

- **The owner asked what is open,** then asked to dig into OI-130. OI-130
  implies the depth-0 component partition was never settled, so the work is
  built around a structure whose derivation no one recorded.
- **The re-score decision 10 required was run.** Decision 10 (2026-08-13)
  deferred approving P5 until after WI-448, on re-derived numbers. WI-448
  closed on 2026-08-23, but the numbers were never re-derived. The re-score
  is measurement only, on today's 130-module tree. The record, its scripts,
  and the census inputs are in
  [plans/2026-11-11-oi130-rescore/](plans/2026-11-11-oi130-rescore/README.md).
  The results:
  - P5 ranks first on every measure:
    - cut 140, against P3\* 152 and P4\* 235;
    - 6 boundaries, against 9 and 22;
    - policy-behaviour straddle 12 of 19, against 15 and 14.
  - Whichever objective the record declares, selecting P5 needs no human
    override.
  - One home per behaviour is still unsatisfiable by any partition.
    - 19 policy and 18 plumbing behaviours still have more than one
      independent home, and 11 of the policy duplicates disagree on some
      input.
    - The violation is in the code: WI-448's consolidation stopped short.
  - The live partition has three defects of its own:
    - 29 of 130 modules carry two or three component tags, so 194
      cross-component edges reach only the warn-only advisory.
    - The seam check resolves imports by bare stem and never sees an import
      into `kitlib/*` or `rendering/*`. 10 cross-component edges have no
      interface row and are reported by nothing.
    - The module → component join exists twice: in `gen_components` and in
      `trajectory_arch`.
- **`origin/rolling_review` was cross-checked** at the owner's request. It is
  the 2026-11-05 maintenance review, unmerged, at `04488d5cd`. What it found
  that bears on this work:
  - It independently confirms the duplication, the multi-tag drift and the
    component rows' missing "what it hides".
  - Its §13.32 finds SR-165, WI-999's subject, is one of four incompatible
    stopping-record specifications. It proposes `hides` and `stops` CMP keys
    in its place, and records that changing SR-165 is an amendment act.
  - It points at the review-churn rulings that already moved this ground:
    - variant F retires LLR → CMP and declares membership on the
      realization, in phase 3;
    - item 12 rules a depth-0 decomposition critique, an Architect role, and
      `run.cmd audit arch`;
    - the W3 dry run found W3 under-decomposed.
  - It does not have the seam check's import blindness, or most of the
    divergences listed in the record.

## State (trunk `refactor_again`)

- **Open claims:** none.
- **Primary checkout:** on `refactor_again`. Trunk is unchanged since the
  replaced handoff's close-out commit `0fe7277b2` except for the commit
  carrying this handoff, which adds this file, the plans folder and the
  status.md pointer.
- **Bars:** no code changed, and the smoke tier was not run for this
  docs-only commit; the commit hooks ran. The replaced handoff's full-suite
  result at `aace1d57d` stands.
- **Pause:** `docs/work/pause` is tracked and untouched.
- **Scratch:** this session kept nothing outside the repo that a successor
  needs. Leg 38's and leg 39's roots under
  `C:/Projects/ai-template.wt/review-tmp/` still wait to be deleted (the
  replaced handoff's note).
- **Nothing was filed.** The defects above are not yet rows, and OI-130's
  text still carries its 2026-11-08 options.

## The queue

The table is unchanged from the replaced handoff. Only row 1's next step
moves.

| # | Row | Next |
|---|---|---|
| 1 | WI-999 | Held on OI-130. OI-130's options predate the re-score. Re-walk it with the owner from the [record](plans/2026-11-11-oi130-rescore/README.md#what-this-changes), together with owner item 2 below. Do not build the backfill until both are answered. Once ruled: write the ruling into its spec, drop its `needs`, and claim (`planmode = "single"`) |
| 2 | WI-1001 | Critique confirmed. Claimed once WI-999 lands (its `needs`) |
| 3 | WI-910 | Held on OI-124: a push, or the owner rules the WSL POSIX route. Skip it while held |

**Never claimed by a leg:** as the replaced handoff lists.

## For the owner

1. **Re-walk OI-130 on the new evidence.** The record's recommendation:
   - **Q1 (b):** approve P5 now, as the depth-0 partition, on today's numbers.
   - **Q2:** declare OI-14's objective, with its constraint measured as
     straddle and cut as the tie-breaker. P5 ranks first with no override, so
     the choice between OI-130's (a) and (b) no longer changes the outcome.
2. **Decide what shape the derivation record takes before WI-999 builds.**
   - The two candidates: SR-165 as written, or rolling review §13.32's
     `hides`/`stops` CMP keys.
   - Choosing the keys means amending SR-165, an Approved row under SN-040.
     The rolling review's verifier also offers moving SR-165 under the
     dual-plan layer as a cheaper route.
   - Item 12's ruled `run.cmd audit arch` is where future re-scores belong.
   - The record recommends settling the shape first.
3. **Rows to file** (none filed yet; each wants a scope critique):
   - the seam check's stem-only import resolution (`_classifiable_edges`);
   - the diverged policy duplicates the record lists;
   - the duplicated module → component join.
   The multi-tag drift is not a new row: variant F's phase-3 migration
   removes its cause.
4. **`origin/rolling_review`** is unmerged. Its §14 names the items that need
   an owner ruling before any lane.
5. Unchanged from the replaced handoff: its items 2 to 7.

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
