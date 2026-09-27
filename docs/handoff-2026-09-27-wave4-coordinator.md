# Handoff 2026-09-27 (wave 4, coordinator) — the queue consolidated, seven groups landed, batch B owed

For the next session's **coordinator**: an Opus session that coordinates
builders, arbitrates, and lands work on trunk. It replaces
[handoff-2026-09-27-coordinator.md](handoff-2026-09-27-coordinator.md) as the
resume map. The role, the loop and the bar below are that handoff's, with
this session's corrections folded in. This session's record:

- the log fragment [log.d/2026-09-27-wave4-consolidation.md](log.d/2026-09-27-wave4-consolidation.md):
  every landing, its bar, and the open count at each step;
- the arbitration file [reviews/2026-09-27-wave4/ARBITRATION.md](reviews/2026-09-27-wave4/ARBITRATION.md),
  rulings 1 to 17, with Codex Sol's review files beside it;
- the owner's ruling [log.d/2026-09-27-owner-ruling-oi88.md](log.d/2026-09-27-owner-ruling-oi88.md)
  (OI-88 (c)).

## What happened

**The queue went from 50 open to 13.** The consolidation (97815a8c) absorbed
29 rows into eleven host rows, one per shared surface. The table is in the
log fragment. Then the spine-acts batch A closed three adjudications in one
act, and seven groups landed, each through Codex Sol review rounds and
arbitration:

| commit | item | what it carried |
|---|---|---|
| daa7bab3 | OI-88 | the owner's ruling (c): SR-212 gains a Boundary arm over crossings |
| 97815a8c | consolidation | 29 rows absorbed into 11 hosts |
| bc6a245f | WI-675, WI-676, WI-604 | batch A: one Fable adjudicator, one act (`--reattests SR-209,TC-242,SR-217,LLR-257,TC-250`); WI-604 RETURNED, folded into WI-582 |
| 07d552a0 | WI-656 (+670, 626, 658) | checker findings that lie |
| 6383a012 | WI-582 (+677, 644, WI-604's RETURN) | the spine authoring sweep; new derived SR-220 |
| 39c95c77 | WI-679 filed | the owner's consolidation question (below) |
| b58b7ccd | WI-672 (+663, 598, 619) | tier ↔ smoke membership; `trace.py --tests-for`; new derived SR-221 |
| 6957fb38 | WI-581 (+659, 570) | quarantine, claim relink, typed open-item brief |
| f7885a49 | WI-638 (+634) | re-judging of observation tests; the assumption gate's four steps |
| 9ecb934f | WI-657 parts 1–3 (+623, 539) | the complexity ratchet green; flag-axis; the sensor layer and skill |
| f61e22ff | handoff | this document's first version |
| 5da9dbf1 | WI-621 (+608, 622) | review and Done-when integrity; session logs append-only |

Nothing is in flight: every lane launched this session has landed, and no
worktree remains. Every `build/wi-NNN` branch is kept.

## Your first jobs, in order

1. **Confirm the smoke tier quietly** before anything lands:
   `python scripts/check_smoke_budget.py --mode enforce`, with no agent
   running. The last quiet reading was 27.7 s over 1647 tests at 5da9dbf1.
   Readings reached 411 s under four lanes. The membership ceiling was
   re-stamped 1620 -> 1690 for in-process growth, with its reason in
   `docs/stack.ini`. The 60 s budget stands.
2. **Spine-acts batch B: one independent Fable adjudicator, one snapshot
   act.** Two verdict grammars mean two adjudication rows (an `amendment`
   brief and a `first-approval` brief). Hand-file both from the lists below,
   in one commit, then one adjudicator session judges both and takes ONE
   act: `intake.py snapshot --reattests <blessed amendments> --approves
   "<registry>=<ref>;…"`. Precedent: batch A (bc6a245f) and WI-669. The
   approval dial is `human_approval_through` in `docs/process.toml`; read
   it.
   - **Amendments** (approved rows amended in place, left Approved,
     unanchored):
     - WI-582: LLR-051, LLR-056, LLR-057, LLR-124, LLR-139, SR-151, SR-152,
       SR-175, SR-157;
     - WI-656: LLR-160, LLR-180, TC-175;
     - WI-672: the `tier` cells of TC-067, TC-068, TC-077, TC-086, TC-100,
       TC-189 and TC-198, and TC-068's `expected`;
     - WI-638: SR-198, SR-212, LLR-233, LLR-244, LLR-254, TC-228, TC-239,
       TC-247, TC-036, TC-055.
   - **First approvals** (Drafted rows):
     - WI-582: SR-220, LLR-210, TC-208, TC-254, LLR-259, TC-252, TC-253;
     - WI-672: SR-221, LLR-260, LLR-263, TC-255, TC-258;
     - WI-657: LLR-261, TC-256;
     - WI-638: TC-209, TC-210, TC-211;
     - WI-621: LLR-262, TC-257, TC-259.

     `trace.py --approve modified` lists every Drafted row owing a first
     approval, including older ones (LLR-205/TC-201 and others). Take the
     whole population the released rungs allow.
   - SR-220 and SR-221 are **labelled derived requirements** (SN-025 and
     SN-012). The adjudicator judges the derivation (the spine-authoring
     skill's rule (c)). The owner may prefer widening the need instead; both
     rationales feed that back.
   - Recorded, and not this act's: CMP-006 `Notes` drift, recorded three
     times now, which owes its own judgement. The Drafted IF rows
     (IF-176–178, IF-228–233, IF-239, IF-240, IF-242) follow their own
     route. IF-177 and IF-178 carry citation-frame advisories (a WI id,
     dates) to clean before any approval.
3. **WI-679: consolidation through the kit's own machinery** (see "For the
   owner").
4. Then the remaining groups, one builder each, at most four at once:
   - **WI-615**: the doctrine sitting, eight parts, the terminology pass last.
     Do not run it alongside anything that edits PROCESS.md or
     PROCESS_OPTIONS.md.
   - **WI-620**: the session service, with WI-605, WI-606 and WI-551; large,
     several commits in one lane.
   - **WI-616**: absolutes, the check then the sweep; the sweep's SR rewrites
     join a spine-acts batch.
   - **WI-651**: snapshot and carrier, with WI-666 and WI-671; it no longer
     waits on anything, since WI-638 landed.
   - **WI-655**: C2 content, strong. It also takes the `boundary_refs`
     re-point of SR-151, SR-152, SR-175 and SR-220, which WI-582 left for C2.
   - **WI-657**: part 4 only, WI-624's research write-up.
   - Singles, triage before building: WI-541 (after WI-620), WI-545, WI-557,
     WI-618, WI-667 (gated on re-arming the red-TC rung), and WI-625
     (deferred, last).

## Landed last: WI-621

WI-621 (with WI-608 and WI-622) reproduced WI-608 (a later session rewriting
a round cleared the gate) and closed it by reading each round at its own
session's commit. Session logs are now append-only evidence. The
coordinator accepted one deviation: the claim WARNS on a missing Done-when
rather than refusing, because every minted row (adjudications, gap closures)
is filed with none, 28 of the 74 completed rows since WI-550. Refusing waits
on the mint writing a Done-when, or on an owner ruling that minted
adjudications are exempt.

## For the owner

- **Your consolidation question is now WI-679, and there is a sharper
  finding under it.** The hand consolidation bypassed the census, the
  adjudication and the close, for two adopter-facing reasons. First, the
  census refuses while ANY adjudication is queued, so a loop that always has
  one open never consolidates. Second, its signals do not see groups that
  share a surface rather than a spec. The bypass also blinded the machinery:
  every hand host's `supersedes` names a restructured row, which
  `consolidate.consolidation_successors` reads as a consolidation's own
  successor, so guard 3 now treats the eleven hosts as already judged,
  although no adjudicator judged them. WI-679 decides both gaps, decides the
  hosts' standing (a retroactive judgement from the kit's consolidate brief
  is one option), and runs the machinery end to end.
- **Coordinator rulings you may overturn** (none moves a rung):
  - ruling 1: a design row's `module` cell lists the modules holding its
    `code_symbol` entries;
  - ruling 7: SR-212's Boundary arm judges interface-form requirements only,
    because approved SR-212 already puts the other forms out of scope and
    OI-88 moved the rung, not the population;
  - ruling 11: a committed symbolic link is not content for an observation
    test's digest.
- **SR-220 and SR-221 are derived requirements.** You may prefer to widen
  SN-025's acceptance (the loop keeps its own queue free of duplicated work)
  and SN-012's (a builder reaches the tests for a change) instead.
- Unchanged from before: merge-to-main and push, the held branches, and the
  C1 stand-in's two stakeholder assignments to check (SN-043 -> STK-03;
  SN-044 -> STK-01 + STK-03).

## Your role and the loop

- **You coordinate and arbitrate.** When a builder and a Sol review
  disagree, or you disagree with Sol, rule yourself. State the governing
  text, then the ruling, and record it in the wave's ARBITRATION.md. Put a
  real doubt to a Fable arbiter. An approved row outranks a Drafted one.
  Sol reviews from the builder's base commit, so it cannot see a grant you
  recorded later (ruling 14). Put every grant in the builder's note AND in
  Sol's item-specific notes.
- **Consolidate before filing** (the owner's standing direction). A finding
  goes into the Context and Done-when of the open item on its surface. A new
  row is filed only when nothing open holds it, as WI-604's RETURN was folded
  into WI-582.
- **Builders** are general-purpose subagents, each in its own worktree cut
  from a named trunk commit (`git worktree add -b build/wi-NNN <path>
  <sha>`). Never use the Agent tool's `isolation: "worktree"`. Hand each
  builder [the builder brief](plans/2026-09-26-assumption-tier-builder-brief.md),
  its item (a consolidated host: tell it to read the absorbed specs under
  `docs/archive/work/restructured/`), its worktree, its pre-assigned ids and
  `-n 2`. Run **at most four** at once, fix rounds included. An amendment
  item's note grants amendment authority over the named rows explicitly: in
  place, status left Approved, no adjudication filed by the builder.
- **Adjudications** go to an independent **Fable** agent (`model:
  "fable"`) that directed none of the amendments. It renders
  `adjudicate_brief.compose`, rules each row, and takes the act. One
  snapshot act at a time.
- **Sol reviews** run read-only from the tip's worktree, backgrounded:
  `codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" -c 'windows.sandbox="elevated"' -s read-only --skip-git-repo-check -o <out> - < <prompt>`.
  This session's scratchpad holds the template (`reviews/template.md`, with
  `@SHA@ @WI@ @BASE@ @SPEC@ @NOTES@` slots) and `mkprompt.py <template> <out>
  <sha> <wi> <base> <spec> <notes-file>`. Pass Windows-form paths
  (`cygpath -m`) to Python. Each fix round gets a Sol confirmation.
- **Integrate:**
  1. Squash-merge. Stash any uncommitted trunk edits first; the merge
     refuses otherwise. Resolve conflicts:
     - `docs/id-watermark`: take trunk's (`git show HEAD:docs/id-watermark`),
       then `trace.py --bump-ids`;
     - registries, `interfaces.toml`, RESYNC_PACK: parallel lanes add
       independent rows and entries, so keep both, trunk's first. Re-anchor
       only the landing lane's own entries to `[since <trunk HEAD>]`, never a
       blanket replace;
     - `tests/test_module_size_ratchet.py`: re-measure the merged count (set
       0, read the failure) and keep both lanes' reasons.
  2. Close the spec: `close_spec.py` (scratchpad) writes `## Deliverable`
     before `## Context`, then `spec_move.py … docs/archive/work/complete/`.
     A host absorbs by `supersedes`. A host never chains through a
     restructured row.
  3. Add a log section, then `trunk_step.py --regen`.
  4. Run the bar (`bar.sh` in the scratchpad), plus the touched slow modules
     and both ratchets, plus `check_complexity.py --mode enforce` (now
     green; keep it so). Commit `WI-NNN: …` with the `WI:` trailer, stating
     only what ran.
  5. Copy Sol's reviews into the wave folder with links re-rooted, and point
     links at the spec's new home.

## Traps (new this session)

- **The live-frame pin** in `tests/test_frame_context.py` lists every
  untied "No tie-back" interface by id. It broke at two merges this session
  (IF-229, IF-240) because each lane's new CLI row joins the list. An IF row
  with no `notes` cell fails its "reason starts No tie-back" clause as well.
  Consider having the pin read those rows rather than list them (a
  suite-honesty item).
- **Composition reds.** Lanes are green alone and red together: the frame
  pin, the smoke membership ceiling, and complexity rows for functions a lane
  landed while the ratchet was red. Run the full bar at every integration,
  and re-measure the ratchets after the merge, not the builder's numbers.
- **`[step:complexity]` starts at DevStg-Impl** while the derived stage is
  DevStg-Tests, so no bar ran the census and the ratchet drifted 50 rows.
  Consider selecting it at the actual stage or in the hook (WI-657's Context
  records it).
- **`spec_move.py` with a backslash path** skips the inbound relink. Pass
  forward slashes.
- **Every earlier trap still holds**: UTF-8 prompt files, the line-number
  pin in `test_generated_newlines.py`, the byte-budget ledger's three copies,
  and a session limit stopping every agent at once (resume each with
  SendMessage; their worktrees keep the work).

## The full unfiltered suite is still owed

`python -m pytest -q -n auto` has not run since the third build wave. Run it
quietly before any phase close, and paste the real output.
