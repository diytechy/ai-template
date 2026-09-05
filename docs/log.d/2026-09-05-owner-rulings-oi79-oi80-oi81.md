## 2026-09-05 — OI-79, OI-80 and OI-81 ruled under the owner's delegation of the peripheral queue

**The delegation, quoted, because it bounds everything below.** At the
2026-09-05 review sitting the owner wrote: *"I see so many open items and a few
issues there. … most of the open items don't seem to have a functional impact.
I don't think I have an opinion on most of them, and likely the recommendations
can be followed directly. Please use your best judgement, and only retain open
items that affect the core functionality / vision of this project."*

The supervising session classified the six pending rows, ruled the three with no
bearing on the spine, the gates or the loop — each taking that row's OWN
recommendation, none invented here — and RETAINED the three that do, filling out
the briefs the machine mint had left as bare questions. The census and the
reasoning are in
[../decisions-for-review-2026-09-05.md](../decisions-for-review-2026-09-05.md)
§6.

**OI-79 — RULED (a), delete the `-HELD-` remote ref, after one tag.** The guard
the row itself asked for was driven before ruling: `git merge-base
--is-ancestor fa3c99c4 contract_split` returns 0, so every commit that ref
points at is already an ancestor of the trunk and nothing on it is single-copy.
The delete is a push and therefore stays the owner's act under `push =
"human"` — this ruling decides WHICH act, not who performs it.

**OI-80 — RULED (b), append a dated correction, and APPLIED in the same
commit.** OI-72's `decision` cell now carries a CORRECTION clause naming the
true split (LLR-203 and LLR-204 were Approved on the wi508 branch since
2026-08-30 at `580df781`; only TC-199/TC-200 were Drafted), placed after the
original sentence, which is left byte-identical. A ruled row's bytes are the
owner's: the correction adds and never replaces. The ruling's substance was
never in question — OI-72 ruled the SR-163 verification SHAPE, not those rows'
Status.

**OI-81 — RULED (c) for the branches; the publication half NOT ruled and left
pending the owner.** The single-copy exposure is the only irreversible thing in
the queue and it is disposed: `wi416-parked-handback-contract` is ONE commit
ahead of the trunk (`7372e239`, "park: WI-416's proposed disposition,
mid-flight and NOT ruled"; 3 files, +344), which is the whole of what exists
nowhere else, so it is tagged and then deleted rather than left one disk
failure from loss. Deliberately NOT delegated: merging `contract_split` to
`main` and pushing it. OI-44 gates that on the identity and publication
question, which is about putting this repo's history beyond the owner's
machines — not a supervisor's call. The three older branches are triaged with
it.

**Retained as core, and their briefs filled rather than ruled.** OI-82 (does
the owner's approval brief narrow to the held rungs — it governs what a signing
sitting SEES, and WI-577 is parked on it), OI-83 (a long-lived coordinator
executes the modules it imported at launch — it has already produced a false
BLOCKER on WI-579 round 033), OI-84 (`agent_loop.default_base` goes blind on a
resumed single-checkout worker — three readers still carry it, one of them
re-claiming work already built). All three were minted by
`intake._mint_open_item`, which writes only five keys, so the owner had a bare
question and no options to choose between; each now carries a `decision`,
`blast_radius`, `options` and `recommendation` written from the evidence in the
tree. **The recommendations are the supervising session's and are NOT
rulings** — these three are the owner's to answer. WI-570 is the row that makes
the thin machine-minted brief unrepresentable going forward.

**One defect found and not fixed here.** `intake._mint_open_item` writes `title
= _clip(question, 100)` — a mid-sentence clip of the one-line — so every
machine-minted row's heading was a fragment ending in an ellipsis, which is the
truncation the owner saw on the surface. The six live titles are repaired to
real names in this commit; the WRITER still needs fixing (derive the title from
the question's first sentence, clip only if that is still over 100), which is a
kit change owing a test and a RESYNC entry.
