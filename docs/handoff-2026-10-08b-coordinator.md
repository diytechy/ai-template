# Handoff 2026-10-08 (second coordinator session): three rows landed; WI-860 and WI-866 open mid-cycle

It replaces [handoff-2026-10-08-coordinator.md](handoff-2026-10-08-coordinator.md)
as the resume map. The wave-18, wave-17 and wave-11 handoffs still carry the
in-lane cycle, the roles and the "never" list until WI-848 (the
`coordinator-cycle` skill) lands. This session's record is
[log.d/2026-10-08b-coordinator.md](log.d/2026-10-08b-coordinator.md).

## State (trunk `refactor_again`, nothing pushed)

- **Landed:**
  - WI-849 (`ceab00c1`), the approval act in the authoring lane;
  - WI-846 (`8ab50ddb`), the adjudicator home's long-lived token;
  - WI-864 (`f3f4b495`), the review-response consolidation sitting (queue
    with edges).

  The re-mints WI-862 and WI-863 are closed as settled. `archive/lanes` is at
  `b3c69994`.
- **Owner rulings and directions (2026-10-08):**
  - the review threat model, recorded in
    [log.d/2026-10-08-owner-ruling-review-threat-model.md](log.d/2026-10-08-owner-ruling-review-threat-model.md);
  - Sol reviews at medium;
  - WI-861 is folded into WI-811, and the coordinator's dispute class is split
    out as WI-865 (needs WI-860 only);
  - WI-811's `needs` on WI-805 is dropped.
- **Filed:** WI-860, WI-864, WI-865 and WI-866 (and WI-861, cancelled).
- **Order of the review-response rows (WI-864's verdict plus the split):**
  WI-860, then WI-852 and WI-865, then WI-853, then WI-848; WI-811 stays
  behind WI-809.
- **Two lanes are open**, claimed under one scoped unpause (`c06fb310`,
  restored byte-identical in `9559f785`). Both are committed and clean. Their
  notes are in `C:/Projects/ai-template.wt/wi-860-notes/` and
  `wi-866-notes/` (outside the repository).

  | Lane | Where it stands |
  |---|---|
  | `wi-860` (review threat model) | Built (§6 paragraph, reviewer-brief link, test), at `ba1dc190`. SR-233, LLR-311 and TC-332 were returned twice (verdicts 001 and 002), and both follow-ups are answered in the lane. **Owed:** re-sit 003 (first approval of all three), the fresh full-lane Sol review, land. |
  | `wi-866` (the close keeps every edge) | Built, at `afd61d49`. LLR-312 approved (verdict 002). **Owed:** re-sit 003 for TC-254's re-attestation alone, the fresh full-lane Sol review, land. |

  Terra's retained sessions:
  - `wi-860`: `01a11de7-f55a-74f0-b411-6aa5584fd775`;
  - `wi-866`: `01a11dea-297b-72c2-a972-b6c51196ad4d`.
- **ID collision handled:** both lanes' Terras allocated LLR-311. `wi-866`'s
  was renumbered LLR-312 before its commit. Land `wi-860` first; `wi-866`'s
  rebase then takes the watermark with `--ours` and `trace.py --bump-ids`.
- **Full suite** at `9559f785` (detached worktree, fixed basetemp under `review-tmp/2026-10-08-coordinator-b/`): **5425 passed, 17 skipped, 0 failed** in 724 s. The conftest isolation test WI-859 tracks passed this run. The basetemp was deleted once recorded.
- **Acts** run to seq 63 on trunk. `docs/work/pause` is tracked and unchanged.
- **The smoke tier is over budget** (91.7 s against 60 s; it was already 88.7 s
  at this session's start, `cb92f2cb`). It is environment-caused (the
  workstation's job object, WI-859), not re-stamped, and the owner's call.

## Next

1. **`wi-860`:**
   - compose the re-sit (`compose_lane.py WI-860 combined
     "first-approval:SR-233;first-approval:LLR-311;first-approval:TC-332"
     "SR-233" docs/reviews/wi-860-review-threat-model/003-ADJUDICATE-ba1dc19.md
     <brief>`);
   - adjudicate, then the fresh full-lane Sol review (medium), rebase, squash,
     archive, sweep.
2. **`wi-866`:** re-sit 003 (`amendment:TC-254`, SR-220), then the same gate
   and landing, after `wi-860` lands.
3. **Then claim WI-865 and WI-852 under one scoped unpause**, then WI-853,
   WI-848 and WI-834.

## Corrections learned this session

- **Every sitting now needs the token.** Since WI-846 landed, the entry point
  refuses (exit 7) unless `AGENT_CLAUDE_TOKEN_FILE` names the token file. Set
  it in the launching shell; never read the file.
- **Review prompts carry the threat model.** The coordinator-tools Sol and
  review templates now carry the out-of-scope clause. Triage each finding
  before dispatch: dismiss compromised-host findings with a recorded line,
  sweep and fix real ones, and send contested or third-round ones to the
  adjudicator (WI-865 builds the route; until then, record and ask the owner).
- **A done row clears its SpecRef.** Only `--strict` catches R-F, so run it
  after every close. An open row's Deliverable is empty. A claim needs a
  SpecRef.
- **Cross-lane ID collisions:** parallel Terras allocate the same next ID.
  Renumber in the later lane before committing.
- **Do not launch a review until the rebase has finished.** A rebase that
  stops on generated-file conflicts leaves the lane mid-rebase. Take
  `--ours`, regenerate, continue, then render the prompt at the real tip.
- **The mechanical close:** `handback.close_adjudication` needs
  `Path(root).resolve()`, not a string. It kept only the last of several
  edges on one waiter (WI-866 fixes it). A row with no `needs` line cannot be
  edged by the close (WI-856).
- **A hand-chosen consolidation cluster works.** Mint the `consolidate` row
  with `adjudicates` and `digests` (`consolidate.digests`); the composer needs
  every row queued and some mechanical overlap among them.
- **Brief rows precisely about record homes.** The delegated-decisions record
  is dial-gated (off by default), so it is not a home that always exists.
  WI-860's second return came from the coordinator's own guidance.
- **Observed, not chased:** the retained adjudicator session
  `b8cf33a7…` resumed for both WI-866 and WI-860, so one retained session
  judged two work items' chains. It authored neither, so independence holds;
  whether that is intended is a question for the owner.

## For the owner

- **Push** `refactor_again` and `archive/lanes`. Remove the archived worktrees
  `wi-846`, `wi-849`, `wi-855` and `wi-864` (and the earlier list) when
  convenient.
- **Set `AGENT_CLAUDE_TOKEN_FILE`** to your token file in your environment, so
  sittings no longer depend on the coordinator setting it.
- **Decisions to confirm or overrule, high risk first:**
  - `coordinator-2026-10-08.toml` D-003 (WI-849 landed before WI-846), D-004
    (the threat-model rows' wording), D-005 (the token path set for WI-846's
    own sittings), D-006;
  - `wi-846.toml` D-007 to D-010 (D-009: two round-6 findings dismissed under
    your ruling; D-010: the tombstone text restored, not moved), then D-001
    to D-006;
  - `wi-849.toml` D-003 (the scope cell's accepted shape), then D-001 and
    D-002;
  - `wi-864.toml` D-003 (the lost edges added by hand);
  - the earlier handoffs' lists.
- **The smoke budget:** say whether to file a row to re-measure it on this
  workstation.
- **Rule** OI-98 and OI-105, still pending.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Take the coordinator lease FIRST
(`coordinator_guard.py take`), before reading anything long. Read, in order:
CLAUDE.md; docs/status.md; docs/handoff-2026-10-08b-coordinator.md (state, the
two open lanes, next steps, corrections, decisions for the owner); the
wave-18, wave-17 and wave-11 handoffs for the in-lane cycle, the roles and the
"never" list; your memory index. Then each open lane's notes folder
(C:/Projects/ai-template.wt/wi-860-notes/ and wi-866-notes/).

Two lanes are open mid-cycle, both committed: wi-860 (the review threat model;
its third first-approval re-sit is owed) and wi-866 (the consolidation close
keeps every edge; TC-254's re-attestation is owed). Finish each: the re-sit
through coordinator_adjudicate.py adjudicate --brief combined (set
AGENT_CLAUDE_TOKEN_FILE to the token file's path first; never read the file),
a fresh full-lane Codex Sol review at MEDIUM, and the landing; wi-860 lands
first. Then claim WI-865 and WI-852 under one scoped unpause. Roles: Terra
(medium) authors spine text, UTF-8 only, re-reading every cell it splices; an
independent adjudicator judges it through the entry point, never a subagent;
Claude Opus builds (kit-builder, medium); Codex 6.1 Sol (medium) reviews.
Apply the owner's review threat model to every finding: dismiss one that
needs a compromised or contrived host in one recorded line, never with code;
send contested or third-round findings to the adjudicator.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md or the
adjudicator's token file.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff linking this one and a log fragment, run the full unfiltered suite
once from a detached worktree with a fixed --basetemp under one dated
review-tmp root and delete it once recorded, then hand the lease back with
`coordinator_guard.py handback --handoff <the new handoff>` as the last act.
```
