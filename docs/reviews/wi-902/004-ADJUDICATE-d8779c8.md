# WI-902 adjudication 004: dispute on review 003

Range: `1ff05bc06..69c123798`. The code is unchanged at HEAD `d8779c8bb`, which adds only review files. Scope bound: project-trajectory/PROCESS.md §6 "Review threat model".

## Finding DA: `_standing_successors` imports a same-title row's lineage

**What I observed.** At `project-trajectory/scripts/intake.py:2557-2567` the range turns the exact-title dedup into a partition. Any registry row whose `Title` equals a draft's title becomes "standing", and the partition hands back that row's own recorded `Supersedes` as lineage (`(r["WI-ID"], supersedes_ids(r.get("Supersedes")))`). `_mint` (line 2523) then passes the standing set into `_repoint_owed`, `_supersede_source_refusal`, `_write_mint` and therefore `_apply_supersedes`. Nothing checks that the matched row's lineage is the lineage the draft intended. So a row that only shares a title gets its absorbed rows' inbound edges rewritten by a disposition that has nothing to do with them.

**Reproduction.** I ran it myself from the builder's fixture, copied into my scratchpad, against the real `intake_after_merge`:
- At lane HEAD the output was `re-pointed queued/WI-041-waiter9.md's edge(s) WI-009 -> WI-040` and `RESULT ([], None) WI-041: WI-040 WI-021: WI-020`. WI-041 had needed WI-009, which is unrelated to the WI-005 disposition. It now needs WI-040 alone, and WI-042, the other successor of WI-009, is dropped. The run reports success.
- I loaded the same fixture against `intake.py` from `1ff05bc06`, in memory, with no worktree change. The result was `RESULT ([], None) WI-041: WI-009 WI-021: WI-020`: the unrelated waiter stays untouched.

This is therefore a regression this range introduced. A dependency is silently corrupted, and the scheduler can then admit the waiter once WI-040 alone is done (review 003 also showed this with `hard_preds_satisfied`). That is the fail-open admission the review hunts for first.

**Scope.** The reproduction needs nothing beyond content an agent writes into the repository: a registry row's title and `Supersedes`, and a disposition's drafted title. That falls squarely inside what PROCESS.md §6 says a review hunts. It needs no compromised host, shim or tampered tool. So `out-of-scope` does not apply.

**Worth.** The fix belongs at the single boundary that owns the mint. Before any successor set is built, the title match must agree with the draft's intended `supersedes`. A mismatched or ambiguous match must refuse before any write. The builder estimates this as a small change inside `_standing_successors`/`_mint`, with no caller-side guard and the importer's return shape unchanged. That is far cheaper than the defect it removes. The builder confirmed the reproduction and holds FIX too. I reached FIX on my own runs, not on that agreement.

**Also seen, not ruled.** Before this range, the dedup already silently dropped a draft whose title collides with an existing row: WI-005's drafted successor is never minted, and nothing refuses. That predates this range and is not this finding. A refusal at the mint boundary as described would close it as a side effect. If the lane does not close it, it should be filed separately and not left implied.

RULING: DA FIX _standing_successors (intake.py:2557) takes an exact title match as mint identity and imports that row's recorded Supersedes, so an unrelated disposition silently rewrites another row's waiter to a partial successor set (reproduced: WI-041 WI-009 -> WI-040 at 69c123798, unchanged at 1ff05bc06); resolve title identity and intended lineage together at the mint and refuse a mismatch before any write
