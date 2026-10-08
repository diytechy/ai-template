+++
id = "WI-808"
title = "One landing per lane on both paths, with the tip archived and the record checked"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-landing"
sr_refs = ["SR-225"]
needs = ["WI-807", "WI-801", "WI-818", "WI-849", "WI-851"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-landing (ch.4 §6, §11; OI-103 Q4). The loop
and the coordinator land through one operation: one ref advance by compare-and-swap
whose tree is the final attested tree, carrying `Lane-Tip:`, every item's `WI:` and
outcome. A single-item lane is one squash commit, act or no act (README Q-8, D-027);
a spine batch is one landing naming every item (README Q-11 (a), change 26).
`ARCHIVE` then appends to `archive/lanes` first, then deletes the branch, then
removes the worktree. RULING-6's audit becomes "a landing commit whose tree equals
its `Lane-Tip`'s attested tree" (change 11). One record check
(`_close_record_refusal`) runs on every landing, and the decisions-record gap is
accepted as history, recorded in a log fragment (D-018). F1 (a killed refresh) and
F2 (an incomplete unload) are this row's (ch.1 §8, D-025). The landing's hold time
is A4's named iteration point.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

Ordering (coordinator, 2026-10-04, from the pre-execution consolidation check): it
needs WI-818 too. Both amend SR-225 and touch the decisions machinery
(`kitlib/decisions.py`, `gen_open_items.py`, `pending.py`, `integrate.py`); WI-818
is small and ready, so it lands first and this row's record check reads its
`owner = confirmed | overruled` key, never the retired one.

## Done-when

- Both paths yield one landing per lane whose final tree equals the attested tree;
  a single-item lane yields one squash commit per item, act or no act; a spine
  batch yields one landing naming every item.
- A trunk moved under the lane fails the swap, naming the foreign commit.
- The tip is reachable from `archive/lanes`.
- F1: a refresh killed after `merge --no-commit` is recovered by the next one (it
  aborts its own unfinished merge); any other dirt still refuses.
- F2: an unload killed after `archive/lanes` and before `worktree remove` is
  finished by the next tick.
- A close that owes a record and has none is refused on either path.
- The gap's log fragment records the range and the count.
- The landing runs the shared lane-commit walk (WI-828) on both paths, so
  text-then-act and WI-851's held-rung state check judge every lane commit; a
  coordinator lane carrying acts lands through WI-849's verdict-backed
  approval-act rung.
- Each spine row the README matrix gives this row (SR-225; LLR-140 `--no-ff`;
  LLR-284, TC-294, IF-080, IF-154, IF-186; IF-173 shared with WI-799) is amended and
  passes adjudication of that row, on whichever adjudication path is the one path
  when this row lands.
- The row's test bar: its affected modules' tests (integrate, handback) plus the
  smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; landings become squash commits
  and `archive/lanes` gains its first kit writer.
