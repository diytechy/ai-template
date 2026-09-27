+++
id = "WI-581"
title = "Lane-close and intake hygiene: quarantine spares monotone and record paths, integrate.lock declared, the claim never rewrites the owner's scratchpad, and a minted open item carries its full brief"
workstream = "process"
needs = ["~WI-579"]
specref = "docs/plans/2026-08-31-verdict-record-and-queue-blockers.md#2-the-other-things-that-stopped-the-queue"
buildtier = "medium"
priority = 6
safety_class = "ordinary"
supersedes = "WI-561;WI-562;WI-560;WI-659;WI-570"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-659 (Keep a claim's relink from rewriting the owner's scratchpad, so a dirty scratchpad stops refusing the claim), WI-570 (The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a recommendation, or is refused). All three are defects in the claim, close and mint path (`handback.quarantine`, `integrate`, `intake._mint_open_item`) that each surfaced as a stopped or thin close, and each is small. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

**Why one row.** Three quick, edgeless, priority-3 items in the lane-close
path (`dispatch._refresh_or_quarantine`, the unload residue set, the trunk
step's regeneration list). One quick lane instead of three.

**Re-scoped 2026-09-26 (owner-approved backlog audit).** WI-560's item 3,
regenerating the approval brief, landed in `dc395734` as the trunk step's
`approval-brief` regeneration step, so it and its quote leave scope. Re-read in
the code, the rest is still open: the revert WI-561 names now runs in
`handback.quarantine`, whose `BOOKKEEPING` exemption
(`project-trajectory/scripts/handback.py`) spares `docs/work/`, `docs/log.d/`
and `docs/handbacks/` but neither `docs/id-watermark` nor `docs/reviews/`; and
`integrate._RESIDUE_OUT_FILES` declares `out/review-owed` and
`out/agent-loop.lock` but not `out/integrate.lock`.

## Done-when

- `handback.quarantine`'s revert leaves `docs/id-watermark` (and any other path
  monotone by contract) as the lane left it, and the reverted tree passes
  registry-integrity (WI-561 item 1).
- The revert keeps `docs/reviews/` as a record path, beside `docs/log.d/` and
  the handback report it already keeps (WI-561 item 2).
- `out/integrate.lock` is in `integrate._RESIDUE_OUT_FILES`, with the same
  test-and-fixture treatment `out/agent-loop.lock` received (WI-562 item 1).
- Tests drive both revert exclusions on a scaffold quarantine and the lock on
  an unload, and the full suite stays green with no other residue class
  regressing (WI-561 item 3, WI-562 item 3).
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-561 (Done-when, verbatim)

1. `dispatch._refresh_or_quarantine`'s revert excludes `docs/id-watermark`
   (and anything else monotone by contract): a minted id is burned whether
   or not its row survives, and the reverted tree passes
   registry-integrity.
2. The revert preserves `docs/reviews/` and `docs/log.d/` as record paths,
   the way it already preserves the handback report — evidence of what
   happened survives the reverting of what was done.
3. Tests drive both exclusions on a scaffold quarantine.

### From WI-562 (Done-when 1 and 3, verbatim)

1. `out/integrate.lock` is declared in the unload residue set, with the
   same test-and-fixture treatment the agent-loop lock received.
3. The full suite stays green; no other residue class regresses.

### From WI-659 (Done-when, verbatim)

- A test with a dirty owner scratchpad naming the claimed id shows the claim
  succeeds and leaves the scratchpad byte-identical.
- The commit bar passes.

### From WI-570 (Done-when, verbatim)

- A disposition draft carries its open item as a typed `[open_item]` table
  whose `one_line`, `blast_radius`, `options` and `recommendation` are all
  required and non-empty, and `intake` refuses, by name, the bare scalar form
  and a table missing any cell.
- `intake._mint_open_item` writes those cells verbatim, so a minted row has the
  shape of a hand-filed pending row and `gen_open_items.py` renders it with no
  special case.
- `prompts/adjudicate-disposition.template.md`, and any sibling brief that
  mentions `open_item`, documents the table and says the adjudicator authors
  the brief; `prompts/CATALOG.md` is regenerated.
- `tests/test_intake.py` pins the accepted table, both refusals and the
  open-item edge still gating the successor, and the log fragment names the
  two rows minted thin before the fix (plan §3 item 5).
- The commit bar passes, and nothing in the change flips a spine row's
  `Status` or writes the approval snapshot.
