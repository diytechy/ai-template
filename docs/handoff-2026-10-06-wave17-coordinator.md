# Handoff 2026-10-06 (wave 17, coordinator): WI-835 landed; the adjudication batch is next

## State (trunk `refactor_again`, nothing pushed)

- **Landed: WI-835, the coordinator's retained adjudicator** (acts 37 to 40).
  The squash is `181ec900` and the close is `dc0333a3`. The session's record is
  [log.d/2026-10-06-wave17-coordinator.md](log.d/2026-10-06-wave17-coordinator.md).
  - The coordinator adjudicates from a lane with
    `project-trajectory/scripts/coordinator_adjudicate.py adjudicate`, never a
    subagent. The call goes through the loop's keep operation, so one retained
    session judges a work item's whole chain.
  - The work item's own five adjudications were the entry point's first live
    run, all on one retained session. The run surfaced two defects, both fixed
    in the lane. A missing review directory refused the first call. Switching
    brief classes drained the session, because the governing hash was keyed on
    the call's own template.
  - Codex 6.1 Sol: five rounds, the last `3b5e0c65 SOUND` after Sol withdrew a
    finding under dispute. Full suite at that tip: 1 failed (the committed
    `docs/stage`, regenerated at the landing), 5282 passed, 13 skipped, in
    627.6 s.
- **Swept:** WI-836, the re-mint, was closed as already settled (`cfccb02a`).
  WI-837, the Done-when goalposts row, was cancelled by the owner's review
  (`c42ddb13`).
- **Filed for the next session:** WI-838, WI-839, WI-840 and WI-841, all `P9`.
  WI-834 (the blackout row) moved to `P8`, by the owner's direction.
- **Approval acts run to seq 40.** `docs/work/pause` is tracked and unchanged.
  The watermark's WI mark is 841.
- **`archive/lanes`** is at `48bad5ec`. It holds both the rebased lane tip and
  the pre-rebase tip whose shas the verdicts cite.
- **Worktrees** `wi-806`, `wi-818`, `wi-821`, `wi-822` and `wi-835` remain under
  `C:/Projects/ai-template.wt/`. All are archived and can be removed.
- **The retained adjudicator session** `ce1fccc0…` is `draining` at 18%, since
  it was minted under the old per-class hash. It retires at its first launch
  outside WI-835's chain, so the next session's first adjudication mints a fresh
  one under the fixed hash. That is expected.
- **The coordinator lease:** this session claimed nothing. Take it before any
  claim (`coordinator_guard.py take --transcript <path>`).

## The next batch (owner, 2026-10-06)

Claim all four under ONE scoped unpause, then build them:

1. **WI-841, the in-lane Done-when blessing.** Build it first. It adds:
   - a Done-when brief class whose verdict is bound to the exact Done-when text;
   - a hold on the lane's next build dispatch and on its close until that
     verdict, or an owner ruling citing the change, covers the current text;
   - intake's after-merge goalposts row, kept only as a safety net;
   - one combined adjudication sitting per lane checkpoint (drifted rows,
     Drafted rows and the Done-when change), with the code review kept
     separate.

   Its own adjudications still run the old way.
2. **WI-838, the first-mint lease.** A route's first retained call writes a
   lease-only record before it launches.
3. **WI-839, the stamp docs.** PROCESS_OPTIONS.md and §5.3 state the
   hand-stamped `linecounts` exception that `integrate.py` already implements.
4. **WI-840, test-scratch retention.** It sets
   `tmp_path_retention_policy = failed`, and each session's runs share one
   dated root in `review-tmp`. It also edits the session-protocol skill.

WI-838 to WI-840 are small and can build beside WI-841. Then comes WI-834, the
blackout row, whose adjudications use the combined sitting.

## Corrections learned this session

- **Adjudicate through the entry point** (recipe:
  `C:/Projects/ai-template.wt/coordinator-tools/README.md`, last section). Run
  it in the background. Exit 2 is a refusal before launch, 7 means the home is
  not signed in, and 1 means a failed call or a bad verdict.
- **A follow-up answered in the lane** replaces the spec's `## Dispositions`
  section under a different heading. Intake refuses that heading with no toml
  block.
- **Terra leaves registry working copies in CRLF.** Normalize them to LF before
  any snapshot.
- **A row split leaves code `Implements:` tags on the old id.** Retag them in a
  coordinator commit.
- **The hand landing:**
  - Rebase the lane onto trunk first, even when trunk moved only by the pause
    restore, because text-then-act exempts a squash only of a tip that contains
    HEAD. On a generated-file conflict, take trunk's side.
  - When the lane recorded an owner overrule in `docs/decisions`, land two
    commits: the squash up to the commit before the close, then the close.
    Ruling-sync needs an open work item citing the overrule.
  - Pass `--src project-trajectory/scripts` to both `gen_arch_map` forms.
  - Archive the pre-rebase tip as a third parent.
  - A goalposts row minted by the sweep is real work (here the owner ruled it).
- **Restore trunk-only generated artifacts on the lane** before the final
  review: PROJECT_STATE.html, the generated part of status.md, stage,
  open-items.html, components.derived.toml, cli-reference.md and
  interface-reference.md. The module-size stamp is the exception: a lane
  carries it, with its reason.

## Open for the owner (not blocking)

- **Push** `refactor_again` and `archive/lanes`.
- **Remove** the five archived lane worktrees if you like.
- **Rule** OI-107, OI-106, OI-98 and OI-105, and the decisions waiting in
  [open-items.html](open-items.html#decisions-to-review).

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-06-wave17-coordinator.md (the batch, its
order and the landing corrections); the wave-16, wave-15 and wave-11 handoffs
for the in-lane cycle, the roles and the "never" list; your memory index.

Scope: the four-row adjudication batch (WI-841 first; WI-838, WI-839 and WI-840
beside it), then WI-834 if context allows. Take the coordinator lease, then
claim the batch under ONE scoped unpause (a reviewed deletion commit, the
claims, a byte-identical restore). Per row: Claude Opus builds (kit-builder,
medium); GPT Terra (medium) authors the rows; Codex 6.1 Sol (high) reviews;
adjudicate from the lane through coordinator_adjudicate.py adjudicate, never a
subagent, and watch it; restore trunk-only generated artifacts before the final
review; rebase onto trunk before landing; land by squash (two commits when the
lane recorded an owner overrule), archive the tip, sweep with
--before/--after/--branch/--merged, and close the re-mint citing the act.
Lanes with acts land one at a time.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff and a log fragment, and run the full unfiltered suite once from a
detached worktree with a fixed --basetemp, deleting it once the result is
recorded.
```
