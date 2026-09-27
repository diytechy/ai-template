# Handoff 2026-09-27 (coordinator) — the third build wave, and consolidating the queue

For the next session's **coordinator**: an Opus session that coordinates
builders, arbitrates, and lands work on trunk. It replaces
[handoff-2026-09-26-coordinator.md](handoff-2026-09-26-coordinator.md) as the
resume map, and keeps that one's role and loop (restated below, since they
still hold). This session's record:

- the build log fragment [log.d/2026-09-26-wave3-build.md](log.d/2026-09-26-wave3-build.md);
- the arbitration file [reviews/2026-09-26-wave3/ARBITRATION.md](reviews/2026-09-26-wave3/ARBITRATION.md),
  rulings 1–22, with Sol's review files beside it;
- the owner's rulings [log.d/2026-09-26-owner-rulings-oi82-oi94.md](log.d/2026-09-26-owner-rulings-oi82-oi94.md);
- the C1 sitting's Decisions entry [log.d/2026-09-27-c1-sitting.md](log.d/2026-09-27-c1-sitting.md).

## The owner's direction for this session: consolidate, so the queue shrinks

The owner, closing this session: *"I'm noticing many new work items getting
drafted, but at this rate the queue will only grow. The next session should
also emulate consolidation and collection of work items to execute larger
chunks and to help the queue reduce in size instead of increase."*

This session closed 18 items and filed 30: the owner's rulings, the wave-2
drafts, review findings and successors. The queue went from 38 open to 49.
So the next session's first job is not the frontier's next item. It is to
cut the queue:

1. **Consolidate before building.** Group the queue (proposal below). Where
   several items touch one surface or one seam, merge them into one item. Use
   the kit's own machinery (`project-trajectory/scripts/consolidate.py`) and
   the 0→A→B rule (PROCESS.md §3, "Consolidate, don't duplicate"). Mark the
   absorbed items merged, as the 2026-09-26 backlog cleanup did, so their
   scope text stays traceable. Each merged item states the union of its
   parents' Done-when, deduplicated.
2. **One builder per consolidated group.** A group lands as one integration
   with one bar. It may be several commits on the branch, but it is one lane
   and one review chain.
3. **File new work only when nothing open can hold it.** A review finding
   first goes into the Context of an open item on the same surface, as a
   bullet and ideally a Done-when line. A new item is filed only when no open
   item covers that surface. A successor minted from an adjudication's
   Dispositions still gets filed, because that is the kit's contract, but it
   should then be consolidated with its surface's group.
4. **Batch the spine acts.** Every in-place amendment of an approved row owes
   an adjudication, and every snapshot act appends to one ledger
   (`docs/archive/last_approved/acts.toml`), so acts serialize. Gather each
   lane's amendments and first approvals into ONE adjudication per batch,
   judged by one independent adjudicator, as WI-669 judged 25 rows at once,
   rather than one adjudication per item.
5. **Measure it.** Report the open count at the start and at the end in the
   log fragment. The session should end with fewer open items than it
   started with.

### A consolidation proposal (the next session's to confirm or redraw)

| group | items | why together |
|---|---|---|
| **Spine acts batch** | WI-675 (SR-217 chain), WI-676 (SR-209/TC-242's owed re-anchor, see below), WI-677 (LLR-259/TC-252 fix + re-filed first approval), WI-604 (LLR-210/TC-208 first approval), WI-582 (residual sweep: a TC to author), WI-644 (the reversal sweep's row amendments) | one adjudicator, one act per batch; WI-644 and WI-582 draft rows that should join the same verdict |
| **Test-tier and pins** | WI-672 (tier ↔ SLOW_MODULES check + 13 older mismatches), WI-663 (noqa), WI-598 (regen step table whole) | all are the suite's own honesty; WI-672's check would have caught the stale live-frame pin WI-678 fixed |
| **Snapshot and carrier** | WI-651 (need + stakeholder tiers in SNAPSHOT_TIERS, OI-91), WI-666 (each registry's own anchor copy on owner surfaces), WI-671 (needs_from_text carrier), WI-659 (scratchpad relink) | same modules: baseline_snapshot, spine_carrier, intake |
| **Checker advisories that lie** | WI-656 (IF-owner reachability), WI-670 (unbound module count), WI-626 (shared-spec anchors), WI-658 (generated list) | each is a false or missing advisory in trace or check_trajectory |
| **Doctrine prose (one byte-budget sitting)** | WI-609, WI-613, WI-614, then WI-615; WI-556, WI-668, WI-536, WI-610 | they share PROCESS.md's byte budget and the role prompts. The earlier handoff already ordered WI-609, WI-613 and WI-614 before WI-615 |
| **Session service** | WI-620 (keep/act/record), WI-551, WI-605, WI-606, WI-541 | one service; WI-551 is already its keep operation |
| **Review integrity** | WI-608, WI-621, WI-622 | the verdict file and Done-when guards |
| **Assumption tier, remaining** | WI-638 (carried over, below), WI-634 (gate steps; OI-88 still open on its Boundary arm), WI-655 (C2 content), WI-667 (census routing) | the plan's remaining build and content |
| **Absolutes** | WI-616 (check), WI-617 (sweep) | the check first, then the sweep that uses it |
| **Quality and research** | WI-545, WI-539, WI-623, WI-624, WI-557, WI-570, WI-581, WI-618, WI-619 | lower priority. Triage these for cancel or defer before building any |

## State at handoff

Trunk is `refactor_again` at 6ee918f5. Twenty-two commits landed this
session, one per item, each with its bar:

- the owner's rulings and the draft filings;
- WI-653, WI-654, WI-665, WI-602;
- WI-652, the smoke re-tier, whose seconds bar is now green at 26–54 s
  (under load);
- WI-662, WI-660, WI-664;
- WI-669, the joint adjudication, 25 rows re-anchored;
- WI-649, WI-577, WI-661;
- WI-643, the C1 sitting, with the dial at DevStg-Boundary;
- WI-674 (RETURN, successor WI-677), WI-673, WI-650, WI-678;
- WI-676's verdict;
- WI-633.

**Carried over, not landed. Start the spine-acts batch with these two:**

- **WI-676's re-anchor.** The verdict (MEANING, blessable, Sol SOUND) is on
  trunk. Its act, taken at 7f98adc9, was refused at integration because WI-650
  had since amended SR-217 and TC-250 in the live files, so the copy was no
  longer byte-identical to live. Take ONE act on current trunk that
  re-attests SR-209 and TC-242 together with WI-675's rows once WI-675 is
  adjudicated: `intake.py snapshot --reattests SR-209,TC-242,<WI-675's>`.
  Both specs record this.
- **WI-638, checkpoint re-judging.** The branch `build/wi-638` holds
  32aa17bc and f40373e3 on base b37dbbb1, and its worktree is kept.
  Arbitration rulings 19 and 22 hold what remains:
  - the approved SR-215, LLR-254 and TC-247 require filing cases that cannot
    be re-judged, so either amend them or declare `inputs` and `max_age` on
    TC-036, TC-055, TC-209, TC-210 and TC-211;
  - a committed symlink escapes `input_escape`;
  - the checkpoint revision can be extracted twice;
  - the new always-on declaration failure exceeds approved LLR-233 and
    TC-228, so it needs an amendment or must go.

  Rebase it onto trunk before its next round.

Worktrees were removed except `wt-638`. Every branch `build/wi-NNN` is kept.

## Your role and the loop (unchanged)

- **You coordinate and arbitrate.** When a builder and a Sol review disagree,
  or you disagree with Sol, rule yourself. State the governing text, then the
  ruling, and record it in the wave's ARBITRATION.md. Put a real doubt to a
  Fable arbiter. An approved row outranks a Drafted one.
- **Builders** are general-purpose subagents, each in its own worktree cut
  from a named trunk commit (`git worktree add -b build/wi-NNN <path>
  <sha>`). Never use the Agent tool's `isolation: "worktree"`, which cuts
  from `main`'s July commit. Hand each builder
  [the builder brief](plans/2026-09-26-assumption-tier-builder-brief.md), its
  item, its worktree, its pre-assigned ids and `-n 2`. Run **at most four**
  at once. An amendment item's note must grant amendment authority over the
  named rows explicitly: in place, status left Approved, no adjudication
  filed by the builder unless told.
- **Adjudications and sittings** go to an independent **Fable** agent
  (`model: "fable"`) that directed none of the amendments. It renders the
  kit's brief (`adjudicate_brief.compose`), rules each row, and re-anchors
  with `intake.py snapshot --reattests <ids>` or `--approves`. A
  held-rung sitting is done as the owner's stand-in under a recorded
  delegation (PROCESS.md §4, OI-86). Only one snapshot act at a time: acts
  append to one ledger.
- **Sol reviews** run read-only from the tip's worktree:
  `codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" -c 'windows.sandbox="elevated"' -s read-only --skip-git-repo-check -o <out> - < <prompt>`.
  The prompt template is `reviews/template.md` in this session's scratchpad,
  and the ARBITRATION file carries each prompt's gist. Sol cannot run pytest
  there, so the builders' red and green runs and your bar are the executed
  evidence. Fixes go back to the same builder as one follow-up commit, and
  each fix round gets a Sol confirmation. Resume an agent after a limit with
  SendMessage; it keeps its context.
- **Integrate:**
  1. A base item squash-merges; resolve conflicts:
     - `docs/id-watermark`: take trunk's, then `trace.py --bump-ids`;
     - `docs/stage`: regenerate;
     - RESYNC_PACK: keep both entries, oldest first, and re-anchor
       `[since <sha>]` to the commit before the landing.
  2. Close the spec with `## Deliverable` before `## Context`,
     `specref = ""`, LF, then `spec_move.py … docs/archive/work/complete/`.
     This session's helper is `close_spec.py` in its scratchpad.
  3. Add a log section and run `trunk_step.py --regen`.
  4. Run the bar, then commit `WI-NNN: …` with the `WI:` trailer.
  5. Copy Sol's review into the wave folder and rewrite its absolute worktree
     links (they break `check_docs` once the worktree goes).

## The bar (per commit), and what it misses

`check_trajectory --strict`, `trace.py --strict-integrity`,
`trace.py --approve modified --check`, `gen_open_items --check`,
`check_docs --stale`, `scripts/check_smoke_budget.py --mode enforce`, and
the **slow modules the change touches**. The smoke tier is representative
now (OI-92 (b)), but it drops the slow modules. This session found three
slow-tier reds only because it ran touched modules by hand:

- the deferred-import window;
- the byte-budget-guard self row;
- the live-frame pin, which became WI-678.

Run the bar before the commit, and put in the message only what you ran:
the lapse at 470f2648 is recorded in the build log. The full unfiltered
suite is still owed before any phase close.

## For the owner

- **OI-88** (a Boundary-rung arm for SR-212) stays open for discussion. Its
  brief carries the driver's option (c): the frame's crossings are the
  level-0 interfaces, so the Boundary arm would judge crossings and the Arch
  arm IF rows. WI-634 builds the Arch arm as approved in the meantime.
- **The C1 sitting's stand-in assignments to check:** SN-043 → STK-03 and
  SN-044 → STK-01 + STK-03, beyond the package's table. They are in the
  Decisions entry.
- The standing owner acts from the previous handoff are unchanged:
  merge-to-main and push, and the held branches.

## Traps (new this session)

- **Prompt files must be UTF-8.** Write them with a quoted heredoc
  (`<<'EOF'`, so backticks are not executed) and Python
  `open(..., encoding="utf-8")`. A cp1252 write makes `codex` refuse the
  prompt.
- **Line-number pins:** `tests/test_generated_newlines.py` pins
  `gen_open_items.py`'s one non-literal write site by line.
- **The byte-budget-guard ledger has three copies** (`project-trajectory/`,
  `.claude/`, `.agents/`), which must stay byte-identical. It also records
  its own size.
- **A session limit** stops every agent at once. Their worktrees keep the
  work, and SendMessage resumes each one with its context.
- **The observation re-judge path** will file rows for TC-036, TC-055,
  TC-209, TC-210 and TC-211 unless they declare `inputs` and `max_age`
  (arbitration ruling 19). That declaration work belongs with the assumption
  group.
