# Handoff 2026-10-04 (wave 13, coordinator): build the lane-lifecycle program

For the next session's **coordinator**. It replaces
[handoff-2026-10-04-wave12-coordinator.md](handoff-2026-10-04-wave12-coordinator.md)
as the resume map. The wave-11 handoff
([handoff-2026-10-04-wave11-coordinator.md](handoff-2026-10-04-wave11-coordinator.md))
still holds for the in-lane cycle, the coordinator tools and the "never" list,
with the corrections below and in the wave-12 handoff.

This session (owner present) is recorded in
[log.d/2026-10-04-wave12-coordinator.md](log.d/2026-10-04-wave12-coordinator.md) and
[log.d/2026-10-04-owner-signs-needs-and-clears-slate.md](log.d/2026-10-04-owner-signs-needs-and-clears-slate.md).

## State (trunk `refactor_again`)

- **OI-104 is ruled** and WI-788 has landed. Its design note
  ([plans/2026-10-04-wi788-design/README.md](plans/2026-10-04-wi788-design/README.md))
  is approved with amendments A1 to A4, and the README's section "The owner's
  checkpoint ruling" overrides the chapters. Codex 6.1 Sol reviewed that fold in
  four rounds and found it SOUND.
- **The program is filed:** WI-797 to WI-817, the twenty-one S788-* rows, in the
  note's graph order; each row's specref names its anchor in the note's table.
  Also filed:
  - WI-796: re-judge TC-055, minted by the landing's sweep;
  - WI-818: the owner's verdict on a decision, `confirmed` or `overruled`;
  - WI-819 and WI-820, deferred, from the evaluation of `thebpandey/lanes`
    ([plans/2026-10-04-lanes-evaluation.md](plans/2026-10-04-lanes-evaluation.md)).
    WI-820 now carries the owner's rulings on provider trust and secrets.
- **The owner's slate is clear.** SN-003, SN-008, SN-025 (exclusions restored) and
  SN-043 are signed with SN-009, as act seq 31. The parked items (OI-49 (b), OI-61
  (c), the wording round's findings) are settled. The eleven high-risk decisions
  are confirmed. Decisions to review: 60, all low risk.
- **The router lineup** (`docs/agents.toml`): strong is Opus 5.5 at high, medium
  is Sonnet 5.5 at medium, quick is Sonnet 5.5 at low. Sol, Terra and Luna run at
  medium.
- **Pending open items:**
  - OI-98, the owner's FileBackup re-sync, holds WI-684;
  - OI-105, the FreeLLMAPI router, holds WI-795.
- **Approval acts run to seq 31.** `docs/work/pause` is tracked and unchanged.
- **The full unfiltered suite** at `6613ddd0`: 5050 passed, 13 skipped, 0 failed, in
  595.7 s from a detached worktree with a fixed basetemp.
- **Not pushed.** `refactor_again` is ahead of `origin`, and `archive/lanes` has
  never been on `origin`. Pushing is the owner's act (`push = "human"`).

## How the program runs (owner, 2026-10-04)

- **By coordinator session, not the unattended loop.** Claim each batch of
  ready rows under ONE scoped unpause:
  1. a commit deleting `docs/work/pause`; confirm HEAD moved before claiming
     (`integrate.py claim` reads the working tree's pause file);
  2. the claims;
  3. a byte-identical restore commit.
- **Roles** (memory and wave-11 handoff):
  - Claude Opus builds through the `kit-builder` agent at medium effort, and the
    coordinator verifies and commits;
  - GPT Terra at medium authors spine rows;
  - Codex 6.1 Sol reviews through the CLI. Hand reviews run Sol at high, by the
    owner's choice; the router keeps Sol at medium.
  - An independent Opus agent adjudicates.

  A1's routing table is not built yet (WI-801), so these hand roles stand until
  it is.
- **Order.** Follow `needs`. Ready now:
  - WI-797, the glossary;
  - WI-803, the plan gate;
  - WI-806, text before act;
  - WI-818, the decisions verdict key;
  - WI-796, a CRITIQUE re-judge of TC-055.

  The backbone runs WI-798, WI-799, WI-800, WI-801, then the station authority
  and the landing.
- **Owner signatures during the program.** The dial holds Needs and the frame:
  - WI-814 (pacing) drafts a new need and stops for the owner's signature;
  - a row that adds an external crossing to the frame does too.
- **Each landing.** Squash, archive the tip, then run
  `intake.py sweep --merged <WI> --branch <lane> --before <trunk> --after <landing>`.
  The sweep can mint rows, so read the watermark after it, never before.

## Corrections learned this session

- **A landing's sweep mints first.** It took WI-796, so ids planned before the
  sweep shifted by one. Mint only after the sweep.
- **The hook's `approval-fresh` step** refuses a commit that changes spine text
  while `docs/ratify/CURRENT.md` is stale. Regenerate with
  `trace.py --approve modified --out docs/ratify/CURRENT.md` and read what it lists
  before an act.
- **The `interface-reference` step** refuses an edit to a declared file's header or
  contract (for example `docs/agents.toml`). Regenerate with
  `gen_arch_map.py --src project-trajectory/scripts --contracts-doc docs/interface-reference.md`.
- **`intake.py snapshot --approves`** splits on `;`, so never put one in the
  reference text.
- **Specref anchors.** `check_trajectory`'s heading slug differs from GitHub's for
  backticks and apostrophes. Give anchored sections plain headings, and give
  every row its own anchor (rows sharing an unanchored spec raise a warning per
  pair).
- **Closing a row.** Scrub its id from `status.md`'s hand text in the same commit
  (the forward-only rule). Move the spec with `spec_move.py`, which relinks
  inbound links.
- **Verify a ref a record says was kept.** `wi416-parked-handback-contract`'s tag
  and commit, which a 2026-09-05 record called "tagged", exist nowhere.
- **Decisions are confirmed or overruled, never approved.** Until WI-818 lands,
  write `reviewed = true` with "Confirmed by the owner, <date>". An overrule is
  carried by a work item that cites the entry, new or amended.

## Open for the owner (not blocking the program)

- **Push** `refactor_again` and `archive/lanes`.
- **The duplicate-code census.** Five exact-body groups (three are duplicate
  readers), plus seven named near-duplicates such as the two open-items readers
  and the two bar-vocabulary tables, are recorded in
  [plans/2026-09-28-duplicated-stage-detection.md](plans/2026-09-28-duplicated-stage-detection.md)
  §7 and await the owner's burn-down decision: no row is filed. WI-788's dual-path
  census (D1 to D18) is separate and is filed (WI-799, WI-816, WI-817).
- **OI-98, OI-105,** and the 60 low-risk decisions.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-04-wave13-coordinator.md (the resume map);
the wave-11 handoff for the in-lane cycle, the coordinator tools and the "never"
list; the design note docs/plans/2026-10-04-wi788-design/README.md, its section
"The owner's checkpoint ruling" first; your memory index.

Build the lane-lifecycle program, WI-797 to WI-817, plus WI-818 and WI-796, in
`needs` order, by coordinator session (owner, 2026-10-04):
- claim each batch of ready rows under ONE scoped unpause (deletion commit,
  check HEAD moved, claims, byte-identical restore);
- per row, the wave-11 cycle: Opus builds (kit-builder, medium), Terra authors
  spine rows (medium), Codex 6.1 Sol reviews (high), an independent Opus
  adjudicates in the lane; land by squash, archive the tip, run the sweep with
  --before/--after, then read the watermark;
- every row's Done-when, review bar and RESYNC flag are in its spec; the note's
  ruling section overrides its chapters;
- record every call made on the owner's behalf in docs/decisions/<branch>.toml,
  high risk listed first; ask the owner to confirm or overrule, never to approve.

Stop for the owner only where a row needs a signature (WI-814's new need, a
frame change) or a decision only the owner can make: file it as a pending open
item with its placeholder row, and continue with the next ready row. Push and
merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end: update docs/status.md (forward-only), write the next handoff and a
log fragment, and run the full unfiltered suite once from a detached worktree
with a fixed --basetemp.
```
