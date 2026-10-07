# Handoff 2026-10-06 (wave 18, coordinator): four of five rows landed; the Done-when blessing lane is open

It replaces [handoff-2026-10-06-wave17-coordinator.md](handoff-2026-10-06-wave17-coordinator.md)
as the resume map. The wave-11 handoff's roles and "never" list still hold. This
session's record is
[log.d/2026-10-06-wave18-coordinator.md](log.d/2026-10-06-wave18-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Claimed under one scoped unpause** (`465cceab`, restored byte-identical in
  `d69e04f3`): WI-841, WI-838, WI-839, WI-840 and WI-842. WI-842 was filed at
  the session start from the owner's question about the stranded lease
  (coordinator D-001).
- **Landed:**

  | Row | Squash | Acts | Sol rounds |
  |---|---|---|---|
  | WI-839, the docs state the lane-carried module-size stamp | `2648d1dd` | none | 2 |
  | WI-842, a closing coordinator hands its lease back | `f9265d99` | 41 | 2 |
  | WI-838, a route's first retained mint takes the lease | `0ccebafb` | 42, 43 | 3 |
  | WI-840, passing tests' temp dirs are removed; one dated scratch root | `76b1d212` | none | 2 |

  The re-mints WI-843 and WI-844 were closed citing acts 41 and 42. Every
  lane tip, and each pre-rebase tip, is in `archive/lanes` (`3ebafeb2`).
- **Open: WI-841, the in-lane Done-when blessing**, lane
  `C:/Projects/ai-template.wt/wi-841` at `538bc9a3`, rebased onto `76b1d212`.
  Done so far:
  - Five builder rounds, seven Terra rounds and four Sol rounds.
  - Adjudication 001 re-attested SR-156, LLR-167, LLR-262, LLR-278, LLR-305,
    TC-257 and TC-278 (MEANING, blessed; on the lane).
  - Adjudication 002 approved LLR-309 and TC-326 and returned the rest; both
    follow-ups are answered in the lane, including the LLR-308 split into
    LLR-310 under derived SR-232.
  - Adjudication 003 blessed LLR-278 but could not re-anchor it, and returned
    LLR-262's wording, which Terra restated in round 7.
- **Watermark:** SR 232, LLR 310, IF 287, TC 329, WI 844 (the lane's values;
  trunk's are lower until it lands). `docs/work/pause` is tracked and unchanged.
- **The full unfiltered suite** at trunk `76b1d212` (detached worktree, fixed
  basetemp): 5291 passed, 17 skipped, 0 failed, in 711.0 s (11:50); the basetemp held 206 MB afterwards (WI-840's retention policy) and was deleted once recorded.
- **The coordinator lease** is handed back with this handoff (WI-842's
  `handback`), so the next session takes it without the owner.

## Owed on WI-841, in order

1. **Builder round 6** (Sol round 4's MAJOR,
   `docs/reviews/wi-841-done-when-blessed-in-lane/sol-review-r4.md`). The
   carrier resolver `acceptance_record._carrier_rows_at` reads TOML and CSV but
   not the markdown needs carrier (`stakeholder-needs.md`), so a combined act
   re-attesting SN-001 is refused as WIDENED. This is the third carrier miss in
   a row:
   - Resolve every registry through the kit's one existing carrier-aware
     reader, not a third special case.
   - Add the mixed-act regression on the markdown carrier.
   - Resume the builder agent rather than starting fresh: it holds five rounds
     of context. Its spine list is in
     `C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/`.
2. **Terra round 8** (resume session `01a1139e-fff3-7371-8e26-48b6d3feea07` from
   the lane). Cells:
   - the cells the fix touches;
   - Sol round 4's two MINORs: IF-175's `requestors` gains
     `scripts/acceptance_record`, and IF-175's `data` returns under 160
     characters.
   - Brief it "UTF-8 only": it wrote two cp1252 dashes this session.
3. **Sol round 5**, narrow, over `538bc9a3..HEAD`.
4. **Replace the `## Dispositions` block** of adjudication 003 (the LLR-262
   wording, answered in `538bc9a3`) under the "answered in this lane" heading.
5. **Adjudication.** The old way, per the spec, through
   `coordinator_adjudicate.py adjudicate` from the lane:
   - an amendment sitting over LLR-262 and LLR-278, plus anything round 8
     moves (both re-attested in one act);
   - a first-approval sitting over SR-232, LLR-307, LLR-308, LLR-310, TC-325,
     TC-327 and TC-328.
6. **Land:**
   - rebase;
   - squash, with the close in the same commit (no owner overrule is recorded
     in the lane);
   - re-anchor the RESYNC entry at the landing's parent;
   - run the full regeneration list;
   - archive both tips;
   - sweep, and close the re-mint citing the acts.

   Then **WI-834**, the blackout row, under one scoped unpause. Its
   adjudications use the combined sitting.

## Corrections learned this session

- **A hook-refused lane commit leaves HEAD where it was,** and Sol then reviews
  an empty range and answers SOUND. Check that `git log -1` moved before
  launching a review.
- **Terra can write cp1252 bytes** through its Python replace. Check
  `bytes.decode('utf-8')` on every registry before committing.
- **A TC citing an LLR must also cite that LLR's SR,** or `registry-integrity`
  refuses the commit.
- **Rebasing parallel lanes:**
  - RESYNC_PACK: keep both sides' entries, trunk's first.
  - The watermark: take `--ours`, then run `trace.py --bump-ids`.
  - Byte-budget skill rows: take each side's own row.
- **A handoff must link the one it replaces.** The wave-17 handoff did not, and
  seven handoffs became orphans (fixed in `dc1d2851`).
- **A retained adjudicator session judges one work item's chain:** a new work
  item mints a session, and a re-sit resumes it.
- **Codex plan limit:** about 20 Sol and Terra sessions in roughly 2.5 hours;
  it reset at 23:02.

## For the owner

- **The adjudicator's dedicated Claude home.** Its OAuth refresh failed from
  21:17 (`Failed to refresh OAuth token`, each call leaving
  `.oauth_refresh.lock` behind, with no other process on that home). The
  owner's re-sign-in at 21:24 fixed it. The root cause is not established:
  - The home was last written at 13:12, the first refresh after that failed,
    and nothing records how the home was first provisioned.
  - It is the first time the kit runs Claude under its own config directory
    across a token expiry.
  - Three gaps belong to WI-834's sign-in step (part C):
    - the probe reads "signed-in" for a home whose token cannot refresh;
    - an auth failure retired the retained session;
    - the home's provisioning is not recorded.
  - **Question for the owner:** if a clean `/login` fails to refresh again, do
    you want the dedicated home on a long-lived token (`claude setup-token`)
    instead? Otherwise, nothing changes.
- **Decisions to confirm or overrule** (high risk first):
  - `coordinator-2026-10-06.toml` D-001 (WI-842 joined the batch) and D-009
    (WI-841 left on its lane at the stop), then D-002 to D-008.
  - The lane records:
    - `wi-842.toml` D-002 (only the holder's own pending relaunch blocks a
      hand-back);
    - `wi-838.toml` D-002 (a mint lands only on its own lease);
    - `wi-840.toml` and `wi-839.toml`.
  - `wi-841.toml` (D-001 to D-016, on the lane) lands with it.
- **Push** `refactor_again` and `archive/lanes`. Remove the archived lane
  worktrees (`wi-806`, `wi-818`, `wi-821`, `wi-822`, `wi-835`, `wi-838`,
  `wi-839`, `wi-840` and `wi-842`) when convenient.
- **Rule** OI-107, OI-106, OI-98 and OI-105.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-06-wave18-coordinator.md (the open lane,
its owed steps in order, the corrections, the owner's questions); the wave-17
and wave-11 handoffs for the in-lane cycle, the roles and the "never" list;
your memory index.

Scope: finish WI-841 on its lane (builder round 6 for the markdown needs
carrier through the kit's one carrier reader; Terra round 8; Sol's narrow
round; the Dispositions answer; the two adjudication sittings; the landing),
then WI-834 if context allows, claimed under ONE scoped unpause (a reviewed
deletion commit, the claim, a byte-identical restore). Take the coordinator
lease first. Roles: Claude Opus builds (kit-builder, medium; resume WI-841's
builder if it is still listed); GPT Terra (medium) authors rows, UTF-8 only;
Codex 6.1 Sol (high) reviews; adjudicate from the lane through
coordinator_adjudicate.py adjudicate, never a subagent. Check every lane
commit landed before a review. Rebase onto trunk before landing; land by
squash, archive the tips, sweep with --before/--after/--branch/--merged, and
close the re-mint citing the act.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff linking this one and a log fragment, run the full unfiltered suite
once from a detached worktree with a fixed --basetemp under one dated
review-tmp root and delete it once recorded, then hand the lease back with
`coordinator_guard.py handback --handoff <the new handoff>` as the last act.
```
