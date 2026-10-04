# ADJUDICATE (first approval, round 2): WI-790, LLR-298, LLR-299, TC-313 and TC-314 at b74b80a3

An independent spine adjudicator (Claude Opus) re-judged these four first drafts after fix round
2, in the lane as the owner directed on 2026-10-03 (S11). It authored none of them; in round 1 it
returned all four with the fixes this round applies (`002-ADJUDICATE-FIRSTAPPROVAL-92ece28.md`).
The SR, LLR and TC tiers are released in this repository, so the approval is this session's. The
judgement read SR-148's whole chain as the kit brief recomposed it at b74b80a3. Every cell the
round-1 fixes named landed byte for byte, and so did the six tests and the back-link (see
`003-ADJUDICATE-AMENDMENT-b74b80a.md`).

## Mutation probes on these rows, re-run at b74b80a3

| # | Mutation | Row | Round 1 | Round 2 |
|---|---|---|---|---|
| M1 | removing a pending item's row is no trigger | LLR-298 / TC-313 | survived | **caught** |
| M8 | merge admission no longer calls the ruling-sync rung | LLR-298 / TC-313 | survived | **caught** |
| M9 | the pre-commit hook drops the ruling-sync step | LLR-298 / TC-313 | survived | **caught** |
| M2-M7, M10-M12 | unreadable parent, `rev^1`, emptied Done-when, citing set from the new tree, TOML only, tip only, path-stripped compare, root refused, exit 0 | LLR-298 / TC-313 | caught | caught |
| P6 | a cited item absent from the registry read as ruled | LLR-299 / TC-314 | survived | **caught** |
| P8 | SpecRef integrity judged on queued rows only | LLR-299 / TC-314 | survived | **caught** |
| P9 | a registry SpecRef citing no item passes | LLR-299 / TC-314 | survived | **caught** |
| P1-P5, P7 | the uncited finding, its place before the vacuity return, deferred citers, the anchor check, the CSV spelling, the per-item clock | LLR-299 / TC-314 | caught | caught |

## Rulings

- [APPROVE] LLR-298 -> the obligation: when a commit takes an open item out of pending, by ruling it or by removing its row, every row open in the parent tree that cites it must in that commit close, be removed, or keep a non-empty, changed raw Done-when section, or the commit is refused naming the row and the item; the citing set is the parent's; either carrier is read, and an unparseable side is refused; the hook's staged step and merge admission apply the one comparison, a root commit closes nothing, and an unreadable parent is refused by name -> the chain: UPWARD, SR-148 holds work behind a human-held stop and derives it from tracked registries, and this row keeps the released row's criteria in step with the ruling that releases it (the owner's OI-102 Q3 mechanism; parentage is an observation, not a defect). SIDEWAYS, it overlaps none of LLR-288, LLR-299 or the backlog-staleness warning. DOWNWARD, TC-313 states every clause, and M1 to M12 are all caught -> ready.
- [APPROVE] LLR-299 -> the obligation: a pending open item no queued work item cites is an error at any gate, before the no-work-items return, read from the one queue projection; an open row whose SpecRef names the registry, under either spelling, is reported when its anchor names an item it does not cite, and when none of its cited items is pending or absent; the registry SpecRef is clocked per cited item -> the chain: UPWARD, as LLR-298. SIDEWAYS, LLR-118 renders the notice from the same projection, LLR-288 owns the block, and the per-item clock now has this row as its one home. DOWNWARD, TC-314 states every clause, the text now matches the code in each of round 1's three disagreements, and P1 to P9 are all caught -> ready.
- [APPROVE] TC-313 -> the obligation: drive the staged, hook-step, committed and merge-ladder paths through every arm LLR-298 states -> the chain: it verifies SR-148 and LLR-298, and its evidence names a test for each clause, among them the merge-ladder, hook-step and row-removal tests that kill M8, M9 and M1 -> ready.
- [APPROVE] TC-314 -> the obligation: drive the open-item and work-item registries through every clause LLR-299 states -> the chain: it verifies SR-148, LLR-299, IF-073 and IF-054, and its method now states the anchor rule, the CSV spelling, every open status, the absent item, the uncited row and the per-item clock, each pinned by a named test (P6, P8 and P9 now caught) -> ready.

OUTCOME: APPROVE rows=4

## Aftermath: the act

The four rows are approved. In the lane's single act, in its own commit after the two verdicts,
their `Status` moves from `Drafted` to `Approved`, and nothing else in either registry changes.
The same commit takes the scoped snapshot:

`python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-790;docs/test/test-cases.toml=WI-790" --reattests LLR-010,TC-010,LLR-118,TC-123,LLR-058,LLR-288,TC-301,LLR-153,TC-147,SR-225,LLR-283,TC-293,LLR-289,TC-302`

The `--reattests` list is the twelve amended rows and the two retirements that the amendment
verdict blesses.
