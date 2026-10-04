# ADJUDICATE (amendment, round 2): WI-790, twelve amended rows and two retirements at b74b80a3

An independent spine adjudicator (Claude Opus) re-judged this amendment after fix round 2, in the
lane as the owner directed on 2026-10-03 (S11). It made none of the changes it judges. In round 1
it wrote the fixes this round applies (`001-ADJUDICATE-AMENDMENT-92ece28.md`), and here it judges
whether they landed as required and whether the rows now stand. The judgement used the kit brief
recomposed at b74b80a3. The anchor is unchanged: `docs/archive/last_approved/`, with
system-requirements, low-level-requirements and test-cases all last written at 9c9e83b7.

## What fix round 2 changed, checked

A cell-by-cell comparison of the three spine registries between b6f268a0 (the round-1 verdicts)
and b74b80a3 finds exactly 26 moved cells. They are the 26 the round-1 fixes named (A1 to A11
here, F1 to F4 in the first-approval verdict). No other cell moved, and no `Status` moved.

- Every moved cell equals, byte for byte, the replacement round 1 fenced. SR-225's `rationale` is
  the anchor text with the one sentence inserted after "...a reporting defect.", and nothing else
  in the cell moved.
- The tests: the nine tests round 1 prescribed are in `tests/test_ruling_sync.py` (three),
  `tests/test_open_item_readiness.py` (two for TC-301, three with their helper for TC-314) and
  `tests/test_open_item_queue.py` (one, with `import re`). They are byte-identical to the blocks
  in the round-1 verdicts.
- The code: one line, `_specref_staleness`'s `Implements: SR-148, LLR-299` (Fix F2). No other
  script changed.

## Baseline and mutation probes

Baseline at b74b80a3, on a scratch export made with `git archive` outside the lane: 210 passed
over `test_open_item_readiness`, `test_open_item_queue`, `test_ruling_sync`,
`test_decisions_to_review`, `test_decision_record`, `test_schedule` and the profile's placeholder
case. That is round 1's 200, plus the nine new tests and the profile case. The slow modules
the blessed rows cite (`test_intake`, `test_gen_open_items`, `test_gen_open_items_render`,
`test_bootstrap` and `test_decision_record_merge`): 227 passed.

Every round-1 probe was re-run against b74b80a3, each a single-point mutation reverted before the
next. The lane was never touched.

| # | Mutation | Row | Round 1 | Round 2 |
|---|---|---|---|---|
| R7a | no registry: every open-item edge satisfied | TC-301 | survived | **caught** |
| R8 | a `-000` example item counts as a real one | TC-301 | survived | **caught** |
| G3 | Decisions to review placed before section 3 | LLR-118 / TC-123 | survived | **caught** |
| I3 | the context join reads `wi_refs` (kin only, never the row) | LLR-153 / TC-147 | survived | survived (observation 6) |
| R1-R6, R7b | readiness, unknown items, mixed edges, hold reasons, titles, mutex; TC-253's absent registry | LLR-058, LLR-288 / TC-301 | caught | caught |
| G1, G2 | an uncited item as a card; the empty-queue claim beside the notice | LLR-118 / TC-123 | caught | caught |
| D1-D6 | the reviewed vocabulary, unrecognized values, the note, high-risk order, a malformed hoist, the reviewed finding | SR-225, LLR-283 / TC-293 | caught | caught |
| I1, I2, I3b | the id into `needs`, the SpecRef only when absent, the `wi_refs` join | LLR-153 / TC-147 | caught | caught |
| B1, B2 | the placeholder row filed; the WI mark raised | LLR-010 / TC-010 | caught | caught |

The first-approval verdict (`004-ADJUDICATE-FIRSTAPPROVAL-b74b80a.md`) lists the M and P probes.

## Rulings

- [MEANING] LLR-010 detail -> before: writes the mapped kit files so the generated harness runs green -> after: the same, plus, for a non-Python profile, append_stack_checklist files the pending toolchain open item and file_stack_placeholder files the queued work item whose needs cite it, its placeholder, both raising their watermark marks -> not the same: a new filing obligation. It is Fix A1 byte for byte, it attributes each filing to the function that performs it, and it names the placeholder once; B1 and B2 are caught. I bless it.
- [MEANING] TC-010 method -> before: the bootstrap suite runs green on a fresh scaffold -> after: plus a node scaffold whose pending toolchain item is cited by its queued placeholder, blocked, both marks raised, --strict passing, no double filing on a re-run -> not the same: a new case. It is Fix A2 byte for byte, and each clause is pinned by test_the_scaffolded_oi3_is_filed_with_its_queued_placeholder (B1, B2 caught). I bless it.
- [MEANING] LLR-118 detail -> before: every pending open-items row as a brief; Draft or Modified chains; the stamp, mask and empty-state contracts; no second opinion; the audit list newest first or None recorded -> after: the queue-cited pending items as briefs beside their citers, the integrity notice before them, the empty-queue claim only with neither; drifted or owing chains with before/after and the empty section's wording; the audit list's order and empty state; the pending owner actions; Decisions to review last; the imported read models; legibility not claimed -> not the same: the card population narrowed, and a notice and a section were added. It is Fix A3 byte for byte, and the CodeSymbol no longer names the deleted mask_local. G1, G2 and G3 are caught. I bless it.
- [MEANING] TC-123 method -> before: the enumerated method -> after: the same enumeration, with the cited-only cards, the notice, the status snapshot agreeing with the page, the drifted state in place of Modified, and the section order -> not the same: new cases. It is Fix A4 byte for byte, and every clause names a test that exists; G1, G2 and G3 are caught. I bless it.
- [MEANING] LLR-058 detail -> before: the frontier from the WI registry and reservations, never prose; the ready set is the WIs whose hard predecessors are done -> after: the open-item states added as an input, never from prose kept, and the ready set further bound to OI-### edges naming present, non-pending items -> not the same: the ready set gained a condition. It is Fix A5 byte for byte, it no longer restates LLR-288's disposition, and R1, R2 and R7b are caught. I bless it.
- [MEANING] LLR-288 detail -> before: wi_refs gates refuse a queued row, mutex candidacy included, reported blocked with ids and titles -> after: needs-cited items attached with titles; the shared predicate, which mutex candidacy reads, unmet while a cited item is pending or absent; blocked with one code per holding item, then the waiting reasons; the record lists the holding items and titles; a ruling releases the row unedited -> not the same: the edge reversed direction. It is Fix A5 byte for byte, it is accurate to the code, and R1 to R6 are caught. I bless it.
- [MEANING] TC-301 method -> before: wi_refs-held rows; absent and example registries claimed -> after: needs-held rows through every projection, several items, an unknown item, mixed edges, a historical pointer, no registry and a `-000` example -> not the same: the edge it drives changed. It is Fix A6 byte for byte, the two tests it required are present, and R7a and R8, which survived round 1, are now caught with R1 to R6. I bless it.
- [MEANING] LLR-153 detail -> before: the anchor's design -> after: the anchor's design, with the open-item draft (its id written into needs, the placeholder blocked until the ruling, the registry record as SpecRef when the draft has none) and a context join over needs citations, in which wi_refs joins nothing -> not the same: two new behaviours. It is Fix A7 byte for byte, it restores every clause the lane's rewrite had dropped, and I1, I2 and I3b are caught. I bless it.
- [MEANING] TC-147 method -> before: the anchor's enumeration -> after: the same, plus the open-item draft and the context join's needs citations and wi_refs -> not the same: two new cases. It is Fix A8 byte for byte, and both are pinned by named tests (I1, I2, I3b caught). I bless it.
- [MEANING] SR-225 requirement, acceptance_criteria, rationale -> before: judge a closing lane against its record and report malformed entries; the format findings -> after: hold a delegated run to a record that reaches its owner, the listing for the owner now in the one shall; the reviewed-value finding; the reviewed key among the judged keys; "reads no record" scoped to the close; what the owner's listing shows; the rationale arguing the listing and the single key -> not the same: a new obligation and a new finding. It is Fix A9 byte for byte. The acceptance no longer contradicts itself, its obligations are all in the Requirement, and D1 to D6 are caught through TC-293. I bless it.
- [MEANING] LLR-283 detail -> before: the pure module's design -> after: that design restored, with reviewed_state's vocabulary, review_queue, and the read model and renderer the CodeSymbol claims -> not the same: new functions. It is Fix A10 byte for byte, and LLR-198 no longer claims decisions_to_review, so the method has one home. D1 to D6 are caught. I bless it.
- [MEANING] TC-293 method, expected -> before: clauses (a) to (i) -> after: (a) to (i) restored, (g) extended, (j) the reviewed key and (k) the queue added; the expected cell covers the reviewed-value finding and the listing -> not the same: new cases. It is Fix A11 byte for byte, and every clause is pinned (D1 to D6 caught). I bless it.

VERDICT: MEANING rows=12

## The retirements carried in: LLR-289 and TC-302

The round-1 rulings stand. Nothing about either retirement moved in fix round 2, and both
successors are now settled (see the first-approval verdict).

- [BLESS] LLR-289 (successor LLR-299) -> its subject, check_trajectory.open_item_wi_ref_findings, is deleted as design 3 and A3 require, and test_a_historical_wi_refs_pointer_holds_nothing pins its absence. LLR-299, approved this round, carries the integrity the reversed edge needs. Blessed.
- [BLESS] TC-302 (successor TC-314) -> its subjects, LLR-289 and the wi_refs resolution, are gone. TC-314, approved this round, verifies what replaces them, and IF-073 too. Blessed.

## Aftermath: the act

Every amended row is blessed and both retirements are blessed. The SR, LLR and TC tiers are
released in this repository, so the re-attestation is this session's. It is taken as the lane's
single act, in its own commit after the two verdicts. That act also flips the four first-approval
rows, and it runs:

`python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-790;docs/test/test-cases.toml=WI-790" --reattests LLR-010,TC-010,LLR-118,TC-123,LLR-058,LLR-288,TC-301,LLR-153,TC-147,SR-225,LLR-283,TC-293,LLR-289,TC-302`

The system-requirements registry is copied because `--reattests` names SR-225. A dry run of this
exact act on a scratch export of b74b80a3 was accepted: it copied three registry files, each
byte-identical to its live file, and recorded one act-ledger entry.

## Observations carried from round 1 (no fix required by this verdict)

1. **IF-073** (Drafted, off-spine). Its consumers drop `scripts/schedule`, which still reads the
   registry, and its notes say a citing row's SpecRef becomes real "after the item is ruled",
   where a row citing several items keeps the registry reference until none is pending.
2. **Parentage.** No SR states the owner-decision coupling as such. A labelled derived SR would
   give the open-item machinery its own home.
3. **A refresh merge can be refused for good.** The slot judges a refresh merge against its first
   parent, so a trunk ruling of an item only a lane-side row cites refuses the merge, and no
   later commit repairs that. The refresh merge must carry the citer's update.
4. A **registry SpecRef with no `#OI` anchor** passes while a cited item is pending, though A6
   calls the reference row-specific.
5. `kitlib.spine._held_rows` compares the queued status case-sensitively. This has no effect
   with the folder carrier.
6. **I3**, a narrower `wi_refs` join (a predecessor's or sibling's pointer, never the row's own),
   survives; the faithful variant I3b is caught.
7. **LLR-198**'s approved detail does not describe the `open_item_queue` its CodeSymbol claims
   (owed outside the judged rows).
