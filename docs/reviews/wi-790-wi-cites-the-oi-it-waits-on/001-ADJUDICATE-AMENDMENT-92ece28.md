# ADJUDICATE (amendment): WI-790, twelve amended rows and two retirements at 92ece287

An independent spine adjudicator (Claude Opus) judged this amendment, in the lane as the owner
directed on 2026-10-03 (S11). It made none of the changes it judges: a Claude Opus builder wrote
the code, GPT Terra authored the rows, and Codex 6.1 Sol reviewed them (review 1, fixed in
04e27e35 and 144e722b). The judgement used the kit brief composed for this lane's merge. The
anchor is `docs/archive/last_approved/`, whose system-requirements, low-level-requirements and
test-cases copies were all last written at 9c9e83b7 (2026-10-04); the lane did not touch it.

The adjudicator read PROCESS.md §3 and §4, the work item in full (the three owner passes,
"Decisions to review", amendments A1 to A9 and the Done-when), OI-102 and its ruling, Sol's
review 1, and the code each row describes at 92ece287: `schedule.py` (`load_wis`,
`hard_preds_satisfied`, `_open_item_holds`, `_held_disposition`, `evaluate`, `_load`),
`kitlib/spine.py` (`split_pred_edges`, `open_item_queue`), `check_trajectory.py`
(`uncited_open_item_findings`, `open_item_specref_findings`, `_specref_staleness`, `main`),
`acceptance_record.py` (the ruling sync), `check.py` and `integrate.py` (its two wirings), the
pre-commit hook, `intake.py` (`_inject_open_item`, `_mint_open_item`, `_pending_oi_lines`),
`gen_open_items.py`, `pending.py`, `kitlib/decisions.py` and `bootstrap.py`
(`append_stack_checklist`, `file_stack_placeholder`).

## Baseline and mutation probes

Baseline, in the unmodified lane: 200 passed over `test_open_item_readiness`,
`test_open_item_queue`, `test_ruling_sync`, `test_decisions_to_review`, `test_decision_record`
and `test_schedule`.

The probes ran on a scratch export of 92ece287 made with `git archive` outside the lane. Each is
a single-point mutation of a clause a row states, run against the tests that row cites, and
reverted before the next. The lane was never touched. "Killed by the fix" means the mutant fails
the tests this verdict requires, run on a second scratch copy carrying them.

| # | Mutation | Row | Result |
|---|---|---|---|
| R1 | readiness ignores open-item edges | LLR-288, LLR-058 / TC-301 | caught |
| R2 | an item absent from the registry satisfies its edge | LLR-288, LLR-058 / TC-301 | caught |
| R3 | a mixed-edge row loses its waiting reason | LLR-288 / TC-301 | caught |
| R4 | an open-item hold reported as waiting | LLR-288 / TC-301 | caught |
| R5 | holding items lose their titles | LLR-288 / TC-301 | caught |
| R6 | mutex candidacy ignores open-item holds | LLR-288 / TC-301 | caught |
| R7a | no registry: every open-item edge satisfied | TC-301 "absent registries" | **survived** (killed by Fix A6) |
| R7b | the same, against TC-253's evidence | TC-253 | caught |
| R8 | a `-000` example item counts as a real one | TC-301 "example registries" | **survived** (killed by Fix A6) |
| G1 | an uncited item rendered as a card | LLR-118 / TC-123 | caught |
| G2 | the empty-queue claim made beside the notice | LLR-118 / TC-123 | caught |
| G3 | Decisions to review placed before section 3 | LLR-118 "last" / TC-123 | **survived** (killed by Fix A4's test) |
| D1 | `done` dropped from the reviewed words | LLR-283 / TC-293 | caught |
| D2 | an unrecognized value reads reviewed | LLR-283 / TC-293 | caught |
| D3 | a review note alone marks an entry reviewed | LLR-283 / TC-293 | caught |
| D4 | high-risk entries not first across records | LLR-283 / TC-293 | caught |
| D5 | a malformed hoist crashes the queue | LLR-283 / TC-293 | caught |
| D6 | the reviewed-value finding dropped | LLR-283, SR-225 / TC-293 | caught |
| I1 | the minted item's id not written into `needs` | LLR-153 / TC-147 | caught |
| I2 | the registry SpecRef overrides a real one | LLR-153 / TC-147 | caught |
| I3b | the context join reads `wi_refs` again (row and kin) | LLR-153 / TC-147 | caught |
| I3 | the same, kin only, never the row itself | LLR-153 / TC-147 | survived (observation 6) |
| B1 | the placeholder row not filed | LLR-010 / TC-010 | caught |
| B2 | the WI mark not raised | LLR-010 / TC-010 | caught |

The first-approval verdict (`002-ADJUDICATE-FIRSTAPPROVAL-92ece28.md`) lists the probes of
LLR-298, LLR-299, TC-313 and TC-314.

## Rulings

- [MEANING] LLR-010 detail -> before: writes the mapped kit files so the generated harness runs green -> after: the same, plus, for a non-Python profile, file_stack_placeholder "creates a pending-toolchain placeholder and queued citer; both id-watermark marks cover the allocation" -> not the same: a new filing obligation. The obligation is right and pinned (B1, B2 caught), but the sentence misstates it. file_stack_placeholder files one thing, the queued row; append_stack_checklist files the open item and raises its mark. "Placeholder" and "queued citer" are two names for one row in the vocabulary the rest of this change uses ("the queued citer is the item's placeholder"). A reader implementing this text would put the open item's filing in the wrong function. RETURN, Fix A1.
- [MEANING] TC-010 method -> before: the bootstrap suite; a fresh scaffold runs green -> after: plus a node scaffold whose "pending-toolchain placeholder has a queued citer" passes check_trajectory --strict -> not the same: a new case. Accurate in substance and pinned (B1, B2 caught), but it repeats LLR-010's misnaming. It states only the strict pass, while its test also pins the blocked reading, the two marks and the single filing on a re-run, which are the clauses LLR-010 states. RETURN, Fix A2.
- [MEANING] LLR-118 detail -> before: every pending open-items row rendered as a brief; every Draft or Modified SR chain with per-cell before/after; a baseline stamp, a check-the-baseline empty state and a masked machine-local region; no second opinion (trace.reattest_model and pending_block imported, so a disagreement makes this view the defect); legibility not claimed; verdict_reattest_block's audit list newest first, or None recorded -> after: only pending items a queued row cites, beside their citers; an uncited item as an integrity notice; Decisions to review last; approval and re-attestation rows with before/after; "the verdict re-attestation audit"; "a projection, not a second decision reader" -> not the same: the card population narrowed, and a notice and a section were added. The narrowing and the notice are what the owner ruled (OI-102 Q2) and what the code does (G1, G2 caught). Dropping the stamp, the mask and Modified is right: those retired before this lane, and the text was stale. But the rewrite also drops obligations the code keeps and no other row states: the audit list's order and its empty state, the empty section that never reads as nothing changed, the empty-queue claim made only with neither card nor notice, which modules the view imports rather than re-derives, and the disclaimer on legibility. "Decisions to review is last" is verified by nothing (G3 survives). The CodeSymbol still names mask_local, which no longer exists. RETURN, Fix A3, with the test in Fix A4.
- [MEANING] TC-123 method -> before: an enumerated method (briefs versus ruled rows; Drafted and drifted rows surface; the empty section's wording; --check bites on drift; vacuity; escaping; the word diff and its percentage; the theme-token guard; the audit list newest first, None recorded, carried on the page) -> after: a cited pending row as a brief and a ruled one not; an uncited item as a notice; the projection agreeing with the status snapshot; "the existing approval, re-attestation, escaping, diff, and verdict-audit cases hold" -> not the same: new cases, and the enumeration replaced by a pointer to "the existing ... cases". A reader with no history cannot resolve that pointer, and it silently drops --check, vacuity, the theme-token guard and the empty section's wording. That is a receipt, not a method (§3, "a cell is not a receipt"). RETURN, Fix A4.
- [MEANING] LLR-058 detail -> before: the frontier derived from the WI registry and reservations, never prose; exclusions with reason codes; the CLI; the ready set is the WIs whose hard predecessors are done; a stopped lane leaves through partial -> after: the same, plus OI-### edges must name ruled items and "a pending or unknown OI blocks the row and names the item"; "never prose" dropped -> not the same: the ready set gained a condition. Correct to the code (R1, R2 caught). Not blessable as written, for three reasons. The derivation's stated inputs omit the open-item states the ready set now depends on. "Never from prose", which decomposes SR-148's no-prose clause here, is gone. And the blocked disposition that names the item is LLR-288's decision restated here, so two rows decide one thing (§3, one decision per row). RETURN, Fix A5.
- [MEANING] LLR-288 detail -> before: load the registry's wi_refs gates; the shared predicate refuses a gated queued row, mutex candidacy included; evaluate reports it blocked with every gating id and title; a ruling releases it unedited -> after: read open-item states for the OI tokens on needs edges; the predicate "blocks a row for every pending or unknown item", keeping its work-item waiting reasons; ruled items release it unedited -> not the same: the edge reversed direction. Correct to the code (R1 to R6 caught). Not blessable as written. "For every pending or unknown item" reads as every such item in the registry, not every one the row cites. Mutex candidacy, which TC-301 verifies, is no longer stated, and neither are the record's item ids and titles that every consumer projects. The blocked disposition is now stated twice (see LLR-058). RETURN, Fix A5.
- [MEANING] TC-301 method -> before: a queued row held through a pending item's wi_refs; the frontier and the simulation omit it without stealing a mutex; a ruling releases it with the spec unchanged; ready and blocked rows projected apart with ids, titles and anchors; multiple gates, absent and example registries, the worker brief -> after: the same through a needs edge, plus mixed edges -> not the same: the edge it drives changed. Accurate except two claimed cases. "Absent and example registries" are driven by no test in its evidence: R7a (an absent registry releases every open-item edge) and R8 (a `-000` example counts as a real item) pass all fifteen tests. "Verify the frontier ... name it as blocked" also misdescribes the frontier, which omits the row. RETURN, Fix A6.
- [MEANING] LLR-153 detail -> before: the anchor's design (the mint invariant and the watermark refusal; triggers (a) to (c); drafts-not-mints; tier signals; context_block's ordered joins; the flip arms; adjudication_action's three arms; idempotence) -> after: identity from the watermark and complete history; an open-item handback writes the id into the successor's needs and supplies the registry SpecRef when the draft has none, leaving the successor blocked; context_block renders pending OIs its kin cite and ignores wi_refs; "The remaining mint, amendment, gap, dial, and idempotence behavior stays as the existing intake contract" -> not the same. The two new behaviours are correct to the code (I1, I2, I3b caught). But the rewrite deletes the row's design (the watermark-refusal rule, the three triggers, drafts-not-mints, the routed traced cells, the tier signals, the join order, the flip arms, adjudication_action's arms and idempotence) and points at it with a sentence naming text the row no longer holds. This is the defect WI-791's sitting returned in this same row (its Fix 1). LLR-167 cites adjudication_action's arms from here, and no other LLR carries drafts-not-mints or the watermark rule. RETURN, Fix A7.
- [MEANING] TC-147 method -> before: the anchor's enumeration -> after: an approved amendment mints one row; a handback mints its disposition; an open-item handback mints a queued blocked successor citing the item, with the registry SpecRef when the draft has none; the context block renders kin-cited OIs and ignores wi_refs; "disposition drafts, gap rows, dial arms, and re-runs obey the existing mint and idempotence contract" -> not the same: new cases, and the enumeration replaced by the same receipt. That drops the report-path dedup key, the SR-Refs routing, the refusals of a malformed block, the dial arms' outcomes and adjudication_action's arms. RETURN, Fix A8.
- [MEANING] SR-225 acceptance_criteria -> before: the closing-lane judgement and the format findings -> after: plus "a reviewed value outside the declared vocabulary" reported, and "an owner-facing surface lists entries not marked reviewed" -> not the same: a new finding and a new obligation. The intent is the owner's 2026-10-04 direction, and the code does it (D1 to D6 caught). Not blessable as written, for four reasons. (1) The listing is an obligation the Requirement's one shall does not state: the Requirement states judging a closing lane and reporting malformed entries, so the cell carries an obligation its requirement lacks. (2) The cell now judges the reviewed key while still saying "keys beyond the required ones are not judged", and reviewed is not a required key, so the cell contradicts itself. (3) "With the dial off ... no record is read" conflicts with an owner surface that reads every record whatever the dial. (4) The rationale argues neither the listing nor why one key, not the review note, marks an entry. RETURN, Fix A9 (Requirement, AcceptanceCriteria and Rationale).
- [MEANING] LLR-283 detail -> before: a module importing nothing and reading no file, git or environment; record_path's mapping; each finding record_findings returns; -000 skipped; extra keys not judged; never raises; owed's every-close rule; session_note's content -> after: the module "defines record paths, required record fields, optional reviewed vocabulary, format findings, reviewed_state, review_queue, close obligation, and session note"; reviewed_state "accepts the declared true and false values or returns no state"; review_queue returns the unreviewed entries; malformed reviewed values are reported "alongside the existing record-shape findings" -> not the same. The new behaviour is correct (D1 to D6 caught). But the rewrite deletes the design the code still implements (the path mapping, each finding, owed's rule, the note's content, the module's purity) and refers to it as "the existing" findings: the receipt again. The Module now spans gen_open_items.py and pending.py, and the CodeSymbol claims decisions_block, _decision_card and decisions_to_review, which the detail never describes. decisions_to_review is also claimed by LLR-198's CodeSymbol, so one method has two homes. RETURN, Fix A10.
- [MEANING] TC-293 method -> before: clauses (a) to (i) -> after: required fields, hoists, reviewed values, malformed values and the review queue "have the declared findings and projection; existing path, obligation, and session-note cases hold" -> not the same: new cases, and (a) to (i) replaced by a pointer to "existing" cases. Every clause is in fact pinned by its evidence (D1 to D6 caught), so the method can say so. The Expected cell, unchanged, does not cover the reviewed-value finding or the listing. RETURN, Fix A11.

VERDICT: MEANING rows=12

## The retirements carried in: LLR-289 and TC-302

No mint routes a removal, so the coordinator carried these two in. Each is judged against its
successor and against design 3 and amendment A3, as WI-782's sitting judged WI-771's
retirements.

- [BLESS] LLR-289 (successor LLR-299) -> it designed check_trajectory.open_item_wi_ref_findings, which resolved each open item's wi_refs pointer against the work registry. Design 3 and A3 remove that pointer as a relationship and delete the resolver with no second path. The code agrees: the function is gone, and test_a_historical_wi_refs_pointer_holds_nothing pins both its absence and that a historical pointer holds nothing. The reversed edge's integrity is LLR-299's (an uncited pending item; the placeholder's SpecRef). A needs token naming no open item stays the existing dangling-edge error (test_a_needs_token_naming_no_open_item_is_reported). The record at `docs/log.d/retired/LLR-289.md` names its successor and its reason. The successor exists as a Drafted row; it is returned this round for its own text, and that does not bear on whether LLR-289's subject is gone. Blessed.
- [BLESS] TC-302 (successor TC-314) -> it verified LLR-289 and IF-073's wi_refs resolution, and both subjects are gone with the function. TC-314 verifies the integrity that replaces it, and also verifies IF-073 and IF-054. The record at `docs/log.d/retired/TC-302.md` names its successor and reason. Blessed.

Both are named in the act's `--reattests` when the act is taken, so the copy accepts the
removals.

## Aftermath: nothing re-anchored this round

Every amended row is returned, so under the owner's in-lane direction no act is taken this round.
The act could not anchor the copies yet in any case: the low-level-requirements and test-cases
copies are refused while returned rows carry drifted approved text. The retirements wait with
them. The first-approval verdict returns its four rows too, so the lane's single act waits for
the re-judge. The act is described there.

Fix A10 also amends LLR-198's `code_symbol`, a traced pointer cell that routes no adjudication.

## Required fixes (to be applied in this lane, then re-judged)

Each replacement is the WHOLE cell value, byte-exact, between the fences (one line, no trailing
newline). Every other cell of every row stays byte-exact. The replacements were applied together
to a scratch copy of 92ece287 with the tests below. Against the unfixed tree they add no trace.py
or check_trajectory.py finding, and they clear three absolute-term advisories that the lane's
texts carried. The smoke tier on that copy: 2038 passed, 2 skipped.

### Fix A1: LLR-010 `detail` and `code_symbol`

`LLR-010` `detail` (`docs/requirements/low-level-requirements.toml`):

```
Writes the mapped kit files into --dest so the generated harness runs green out of the box. For a non-Python profile, append_stack_checklist files the pending toolchain open item, and file_stack_placeholder files the queued work item whose needs cite that item, its placeholder on the queue; both raise their id-watermark marks over the ids they allocate.
```

`LLR-010` `code_symbol` (`docs/requirements/low-level-requirements.toml`):

```
MAPPING/main/append_stack_checklist/file_stack_placeholder
```

### Fix A2: TC-010 `method`

`TC-010` `method` (`docs/test/test-cases.toml`):

```
Run the bootstrap suite; a fresh scaffold's harness runs green, including a node scaffold whose pending toolchain open item is cited by its queued placeholder row: the row reads blocked naming the item, both id-watermark marks cover the ids allocated, check_trajectory --strict passes, and a re-run files neither twice.
```

### Fix A3: LLR-118 `detail` and `code_symbol`

The detail keeps the lane's narrowing and notice. It restores the obligations the code keeps, and
it drops the retired stamp and mask. The CodeSymbol drops `mask_local`, which no longer exists.

`LLR-118` `detail` (`docs/requirements/low-level-requirements.toml`):

```
The rendered half of the attestation regime under SR-049. The page renders, in this order: the pending open items that queued work items cite in their needs, as decision briefs beside the queued rows citing them, preceded by an integrity notice naming and linking the pending items that no queued row cites, the page claiming an empty queue only when there is neither; every SR whose chain holds a row owing a first approval or drifted from the approved snapshot, with the chain's per-cell before/after, a section with no changed cell stating that no cell differs from the approved snapshot and never reading as nothing changed; the audit list of every act-ledger entry naming a verdict, newest first, or None recorded; the pending owner actions; and, last, the Decisions to review section. It owns no second opinion: the queue is pending.open_item_queue, the attestation model trace.reattest_model, the pointers pending.pending_block and the decisions pending.decisions_to_review, imported rather than re-derived, so where this view and the trace.py --approve brief disagree, this view is the defect. NOT claimed: that the rendered page is legible or well-composed.
```

`LLR-118` `code_symbol` (`docs/requirements/low-level-requirements.toml`):

```
render/_brief_cards/_brief_card/_uncited_notice/_attestation_cards/verdict_reattest_block/word_diff
```

### Fix A4: TC-123 `method`, and one test

The anchor's enumeration, with the lane's new cases and the section order added. "Modified"
becomes the drifted state the tests drive (`test_draft_and_DRIFTED_rows_both_surface`), and the
retired-mask aside is dropped. `evidence` stays as the lane wrote it.

`TC-123` `method` (`docs/test/test-cases.toml`):

```
Drive gen_open_items over temp repos: assert a pending registry row a queued work item cites renders as a brief beside the rows citing it and a RULED row does not; that a pending row no queued work item cites is not a card but is named in an integrity notice linking its registry record, and that the page claims an empty queue only when neither a card nor a notice remains; that the status snapshot's open-items and Blocked lists name the same cited and uncited items as the page; that Drafted spine rows and approved rows drifted from the approved snapshot both surface (approval owed vs re-attest owed) while an undrifted Approved row does not; that a section with no changed cells says what is true — no cell differs from the approved snapshot, the row's own Status asking for a human — and never CHECK THE BASELINE nor nothing-changed; that --check bites on drift as a plain regenerate-and-compare, with no baseline stamp left in the view to re-read; that the whole thing is vacuous with neither registry nor view; that registry prose is HTML-escaped; that the word diff marks only what moved and the percentage counts words not whitespace; that the theme tokens equal the dashboard's emitted values (a drift guard, not an extraction); and that Decisions to review is the page's last section. It also drives verdict_reattest_block: every act-ledger entry naming a verdict is listed newest first with its re-attested rows and its verdict file, an entry naming none is left out, a ledger with no such entry reads None recorded, and the rendered page carries the list.
```

In `tests/test_open_item_queue.py`, add `import re` above `from conftest import load_script`,
followed by a blank line, and append this test. It passes at 92ece287 and kills G3:

```python
def test_decisions_to_review_is_the_pages_last_section(tmp_path):
    # LLR-118: the owner surface's sections run in a fixed order, and
    # Decisions to review is the last of them.
    page = gen.render(tmp_path)
    eyebrows = re.findall(
        r'<section class="band"[^>]*><p class="eyebrow">([^<]+)</p>', page
    )
    assert [e.split(" · ", 1)[0] for e in eyebrows] == ["1", "2", "3", "4"]
    assert eyebrows[-1] == "4 · Decisions to review"
```

### Fix A5: LLR-058 and LLR-288 `detail`

LLR-058 owns the ready set; LLR-288 owns the blocked disposition and what its record carries.

`LLR-058` `detail` (`docs/requirements/low-level-requirements.toml`):

```
Derives the dependency-ready frontier from the WI registry, the states of the open items its rows cite and the dispatcher reservations, never from prose; excludes terminally closed, deferred, reserved, protected and exclusive-conflicting work with reason codes; and exposes ready --explain, --format json and simulate --jobs N. The ready set contains exactly the work items whose hard work-item predecessors are done and whose OI-### edges name only items present in the open-items registry and not pending. A lane stopped early leaves the frontier through its terminal partial move.
```

`LLR-288` `detail` (`docs/requirements/low-level-requirements.toml`):

```
Attach to each work row the id and title of every open item its needs cite. The shared readiness predicate, which mutex candidacy also reads, is unmet while a cited item is pending or absent from the open-items registry; such a row reads blocked, with one reason code per holding item naming it pending or unknown, followed by the row's work-item waiting reasons when those edges are unmet too, and its record lists exactly the holding items with their titles. Ruling the holding items releases the row with no edit to it.
```

### Fix A6: TC-301 `method`, and two tests

`evidence` stays `tests/test_open_item_readiness.py`.

`TC-301` `method` (`docs/test/test-cases.toml`):

```
On a temporary work registry, hold a queued row through a needs open-item edge while the item is pending: the frontier and the simulation omit it without stealing a mutex from a row sharing its key, its readiness record reads blocked naming the item and its title, the worker brief refuses it naming the item, and the status snapshot's Blocked list and the Next-work card name the item; then rule the item and verify readiness with the spec unchanged. Also drive several items on one row released one at a time, an item absent from the registry (blocked as unknown and reported as a dangling edge), mixed work-item and open-item edges keeping the waiting reason, a historical wi_refs pointer that holds nothing, no open-items registry (every open-item edge unmet) and a -000 example item (never a real item).
```

Append these two tests to `tests/test_open_item_readiness.py`. They pass at 92ece287 and kill R7a
and R8 respectively:

```python
def test_no_registry_leaves_every_open_item_edge_unmet(tmp_path):
    # TC-301: with no open-items registry an open-item edge fails closed, the
    # item reported unknown, and the row steals no mutex.
    _spec(tmp_path, "WI-684", needs=["OI-98"], exclusive=["shared"])
    _spec(tmp_path, "WI-688", exclusive=["shared"])
    assert sched.load_oi_status(tmp_path) == {}
    held = _records(tmp_path)["WI-684"]
    assert held["disposition"] == "blocked"
    assert held["reasons"] == ["blocked:open-item-unknown:OI-98"]
    assert _frontier(tmp_path) == ["WI-688"]
```

```python
def test_an_example_open_item_is_never_a_real_one(tmp_path):
    # TC-301: a `-000` example row is not an open item, so a row citing it is
    # held as citing an unknown item, never released by the example's state.
    _items(tmp_path, ("OI-000", "ruled"), ("OI-98", "ruled"))
    _spec(tmp_path, "WI-684", needs=["OI-000"])
    held = _records(tmp_path)["WI-684"]
    assert held["disposition"] == "blocked"
    assert held["reasons"] == ["blocked:open-item-unknown:OI-000"]
```

### Fix A7: LLR-153 `detail`

The anchor text, byte for byte, with two edits. The drafts-not-mints clause gains the
open-item draft (its id into `needs`, the placeholder blocked until the ruling, and the registry
record as SpecRef when the draft has none). The context join names `needs` citations and states
that `wi_refs` joins nothing.

`LLR-153` `detail` (`docs/requirements/low-level-requirements.toml`):

```
The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id counts from max(the docs/id-watermark mark, the sweep of every spec FILENAME under docs/work/ and docs/archive/work/, active/<branch>/ included) + 1 - never max(live) alone, so an id freed by a deleted spec is never re-issued - and trace.read_watermark's refusal on an absent or malformed mark is deliberately NOT caught: a mint with no record of what has been allocated must not proceed on a guess (TC-158, IF-101). Three triggers, serial by construction: (a) the approved/routed-cell diff on the merged commit via check_trajectory.staged_spine_amendments, whose walk covers the SR, LLR, TC, SN, DA and SUR tiers -> one adjudication row listing each changed row/cell/before-after (routed traced cells: SR SN-Refs and Boundary-Refs, LLR SR-Refs and TC Verifies per the declared cell split); (b) a merged spec carrying ## Handback -> the disposition row (outcomes cancel / defer / re-queue with drafted follow-up / surface an open item; NEVER minted for an adjudication row - no recursion, and handback.hand_back refuses the act itself); (c) the dispatcher's gap census -> concrete gap-closure rows, deduped against every existing row. Drafts-not-mints: a merged adjudication row's ## Dispositions fenced-toml drafts mint at ITS merge, validated loudly; a draft carrying an [open_item] table also mints a pending open item from it, with no work-item pointer, and writes the item's id into that draft's needs, so the minted row is the item's queued placeholder and reads blocked until the ruling, and a draft with no SpecRef gets the item's own registry record as its SpecRef. Tier signals are measurable (rows touched, gate delta, handback reason class). context_block renders the pure registry joins (cancelled precedent WITH REASONS first, the pending OIs cited in needs by the row, its predecessors or its siblings, the LLR/TC code map, CMP knowledge packs, IF seams, precedent reviews) - advisory-never-gating, three consumers; an open item's wi_refs joins nothing. flip_verified resolves the hold from the approval dial: held prints a recommendation and writes nothing; released requests the flip, but _apply_flips skips an already Approved row and refuses every other Status by name, so it writes nothing; an unreadable dial or stage reads as held. adjudication_action(human_held, verdict) returns flip when released, reattest when held with a CLARITY verdict, and recommend otherwise. The mint commit mirrors the claim's bookkeeping shape; every derived title is deterministic, so the sweep CLI re-run is idempotent.
```

### Fix A8: TC-147 `method`

The anchor text, byte for byte, with two clauses inserted: the open-item draft, and the context
join's kin citations and `wi_refs`. Each is pinned by
`test_the_close_mints_a_pending_oi_that_gates_the_successor` and
`test_the_context_block_renders_from_real_joins_in_failure_cost_order`; I1, I2 and I3b are caught.

`TC-147` `method` (`docs/test/test-cases.toml`):

```
Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPORT PATH, so a re-sweep dedupes exactly and a genuinely second close is a second row): an approved SR amendment mints ONE adjudication row (id max+1, the before/after listing in ## Context) and an LLR SR-Refs re-point mints while a Module-only move stays silent (the ruled routing); a merged handback mints the disposition row (NEEDS-HUMAN reason routes strong; a handed-back adjudication row mints NOTHING and its own handback attempt is refused structurally); a merged adjudication row's ## Dispositions drafts mint at its merge with planmode=dual passing through kind-derived, and a malformed block, an unknown key, a second adjudication kind or a bad bar value refuse with nothing minted; a draft carrying an [open_item] table mints a pending open item with no work-item pointer and a queued successor whose needs cite it and which reads blocked, the successor keeping its own SpecRef and a draft with none getting the item's registry record; the census mints gap rows once and dedupes on re-run; every re-run is idempotent by exact-title dedup; the context block renders every join in failure-cost order, a pending open item the row's kin cite in needs among them while one named only by a historical wi_refs is left out, and answers the empty string on a bare repo; a held dial recommends and leaves the registries byte-identical; a released dial writes nothing, refusing by name a row not already Approved and skipping one that is; an unreadable dial or stage reads as held; adjudication_action returns flip released, reattest held with a CLARITY verdict, recommend otherwise; and an amended approved need, assumption or surrogate mints one amendment row.
```

### Fix A9: SR-225 `requirement`, `acceptance_criteria` and `rationale`

The Requirement states the listing in its one shall. The AcceptanceCriteria scopes "reads no
record" to the close, names the reviewed key among the judged keys, and states what the listing
shows. The Rationale gains one sentence after "...a reporting defect." that argues the listing
and the single key. Nothing else in the cell moves.

`SR-225` `requirement` (`docs/requirements/system-requirements.toml`):

```
Where the declared decision-recording dial asks for a record, the delivered loop content shall hold a delegated run to a decisions record that reaches its owner: refusing to integrate a closing lane whose record is absent, naming where it belongs, reporting without refusing each entry of a present record that omits a required disclosure field or leaves one blank, and listing for the owner each entry not marked reviewed.
```

`SR-225` `acceptance_criteria` (`docs/requirements/system-requirements.toml`):

```
With the dial off or undeclared, a closing lane is judged by nothing here and the close reads no record; with the dial at record or escalate-first, a lane whose work closed complete, cancelled or partial without its record at its run's path is refused, the refusal naming that path, and one carrying its record passes this check; in a present record, an entry that is not a table, an entry lacking what was decided, the alternative passed over, the reversal cost, why it was not escalated or the review cell, or carrying one that is not text, or leaving one of the first four blank, an entry whose optional reviewed value is neither a declared reviewed value nor a declared not-reviewed value, a hoist that is absent or not a list of entry ids, and a hoist naming an entry the record lacks, are each reported naming the entry, none refuses, and keys beyond the required ones and the reviewed key are not judged; the owner's surface lists the present records' entries that are not marked reviewed, the hoisted entries first, an entry with an absent or unrecognized reviewed value among them and the review cell's text marking nothing, and states how many entries are marked reviewed when none is left; an entry numbered -000 is never judged or listed; a value of the dial outside its three, compared trimmed and case-folded, is refused where the policy file is checked, and at the close it is refused as configuration before the record is read; a session handed a lane to build or to adjudicate under a recording dial is told the path its record belongs at, and a review session is not.
```

`SR-225` `rationale` (`docs/requirements/system-requirements.toml`):

```
A DERIVED requirement, and labelled so. SN-029 asks that a run released to automation get as far as it honestly can, and that an approval it makes on a released tier leave a record naming who made it; it does not name the other calls a delegated run makes on the owner's behalf, the ones too settled to hold the run for and not settled enough to be history, so this obligation arrives through the unattended-operations lens rather than through the need's text. A call nobody is told about is the failure that lens listens for: it pages nobody, and a run that looks green is green partly because nothing looked at what it chose. A prose instruction to list such calls was tried and measurably degraded within one session, the fields left out as soon as nothing read them, so the record carries required fields and the close that owes it refuses silence. The obligation is keyed to a dial because how much of the owner's reading a run may claim is the owner's to set; it ships off, so a repository owes nothing until its owner asks. Every close owes the record, a partial close included, because every delegated run closes with one; a lane the machinery closed with no session present is refused too, and that refusal is a hold for a person to write the record rather than a strand. A malformed entry is reported rather than refused, because the record is there and readable and a refusal would hold finished work for a reporting defect. The record reaches its owner as a list of the entries the owner has not marked reviewed, because a record nobody is shown degrades the way the prose instruction did; one key with a closed vocabulary marks an entry reviewed, since a free-text note gives no reader a closed answer to whether the entry was read, and a value outside that vocabulary is listed rather than hidden, so a typo never hides a call. A value of the dial outside its alphabet is judged before the record is read, since the reader keeps the obligation for such a value and would otherwise report a missing record in place of the real fault. The record is never a route for work: a call that is the owner's to make, or an act that cannot be undone, still reaches the owner through the process's exits, at every dial setting. Fed back to the need: SN-029's acceptance could name a record of the delegated calls a run made beside the record of its approvals; until it does, this row is derived and says so.
```

### Fix A10: LLR-283 `detail`, and LLR-198 `code_symbol`

The anchor's design of the pure module, restored, with the reviewed key, review_queue and the two
render-side symbols the row's CodeSymbol claims. `module` and `code_symbol` stay as the lane wrote
them. LLR-198 stops claiming `decisions_to_review`, whose `Implements:` line names LLR-283.

`LLR-283` `detail` (`docs/requirements/low-level-requirements.toml`):

```
kitlib/decisions.py imports nothing and reads no file, git or environment. record_path(run) is DECISIONS_DIR/<run>.toml under docs/decisions, a / in the run's name becoming -. record_findings(text) parses the text as TOML, returning one finding when it does not parse, and otherwise one finding per defect: a decision key that is not a table, an entry of that table whose id is not D-<digits>, an entry that is not a table, a key of REQUIRED_KEYS (decided, alternative, reversal_cost, why_not_escalated, review) absent or not a string, one of the first four blank after trimming, a reviewed value that reviewed_state does not recognize, a top-level high_risk that is absent or not a list of strings, and each hoisted id the decision table lacks; an id ending -000 is skipped wherever it appears, and keys beyond REQUIRED_KEYS and REVIEWED_KEY are not judged. It does not raise. reviewed_state(value) reads the optional reviewed key: absent, false, 0 or a word of REVIEWED_FALSE (false, no, n, 0, the empty string) is not reviewed; true, a non-zero number or a word of REVIEWED_TRUE (true, yes, y, 1, reviewed, done) is reviewed; words are compared trimmed and case-folded, and a value outside both is unrecognized and read as not reviewed. The review cell's text marks nothing. review_queue(text) returns the entries not marked reviewed, hoisted entries first and then by id, with no -000 entry, together with the count marked reviewed; it lists nothing for a text that does not parse and does not raise on a malformed hoist. owed(mode, outcomes) is true for mode record or escalate-first with at least one outcome, whatever the outcome, a partial close included. session_note(mode, run) returns the empty string for off and otherwise the instruction naming record_path(run), the required keys, reviewed left false for the owner, the hoist and the rule that the record is not an exit, with one further sentence under escalate-first preferring the exits over deciding. pending.decisions_to_review applies review_queue to the records under docs/decisions/, hoisted entries ahead of the rest, prefixes a record's findings with its file, and answers no records where the directory is absent; gen_open_items.decisions_block renders the result as the owner surface's Decisions to review section, each entry with its file, id and disclosure fields and a link to its record, the findings after the entries, the count marked reviewed when none is left, and a statement that no record exists when the directory is absent.
```

`LLR-198` `code_symbol` (`docs/requirements/low-level-requirements.toml`):

```
PendingItem/pending_items/open_item_queue/owner_cards/spine_pending/pause_pending/pending_block
```

### Fix A11: TC-293 `method` and `expected`

Clauses (a) to (i) restored, with (g) extended, and (j) and (k) added. Every clause is pinned by
`tests/test_decision_record.py` and `tests/test_decisions_to_review.py`, which the evidence already
names. `evidence` stays as the lane wrote it.

`TC-293` `method` (`docs/test/test-cases.toml`):

```
The kitlib.decisions call surface over record texts planted in memory, clause by clause, and the owner surface over records planted on disk. (a) SOUND: a record with two complete entries, one hoisted, and a record with no entries and an empty hoist, yield no finding. (b) EACH REQUIRED KEY: its absence yields one finding per entry naming the entry and the key; a number, a boolean, a list and a table in it each yield exactly the not-text finding; an empty, a spaces-only and a whitespace-only value yield exactly the blank finding for the first four keys and nothing for review. (c) SHAPE: an entry that is not a table, a decision key that is not a table, an entry id outside D-<digits> and an unparseable text each yield one finding. (d) THE HOIST: a hoist that is a string, a list holding a number, a mixed list or a table, a missing hoist, and a hoisted id the record lacks each yield one finding. (e) EXTRA KEYS on an entry yield none. (f) NEVER RAISES: nine hostile texts each return a list of strings. (g) INERT: a half-filled -000 entry, hoisted, yields none, and the shipped template yields none, lists nothing for review and carries the -000 example with every required key, an empty review and reviewed = false. (h) THE PATH AND THE OBLIGATION: a run's path is one file under the records directory with a / becoming -, and owed holds under record and escalate-first for a complete, a cancelled, a partial and a mixed close, and not under off or for no outcomes. (i) THE NOTE: session_note is empty under off, names the path, every required key and the hoist under record, and adds a sentence under escalate-first; session_body appends it to a build session's body and to an adjudication session's body under record and to neither under off, and reviewer_prompt's brief does not carry it under record. (j) THE REVIEWED KEY: each reviewed form (a TOML true, a non-zero number, and true, yes, y, 1, reviewed and done in any case and padding) hides an entry from the owner surface and yields no finding; each not-reviewed form (false, 0, the empty string, no, n and false) and an absent key shows it and yields no finding; an unrecognized value, a list among them, shows it and yields one finding naming the entry; a review note alone marks nothing. (k) THE QUEUE: the owner surface lists the entries not marked reviewed with their file, id and disclosure fields, the hoisted entries of every record first and never a -000 entry; a malformed hoist is shown as a finding beside the entries rather than raising; when every entry is reviewed the section says so with the count, the status snapshot carries the count left to review, and with no records directory the section says no record exists.
```

`TC-293` `expected` (`docs/test/test-cases.toml`):

```
Satisfies SR-225 AcceptanceCriteria: each shape, required-key, reviewed-value and hoist defect is reported by entry, extra keys are not judged, the findings never raise, a -000 entry is never judged or listed, every close owes a record under a recording dial, a build or adjudication session is told its record's path while a review session is not, and the owner surface lists exactly the entries not marked reviewed
```

## Findings outside the judged rows (owed, not ruled here)

- **LLR-198** now claims `open_item_queue` (pending.py) in its CodeSymbol, and pending.py's
  `Implements:` line names it, but its approved detail does not describe the queue projection.
  This is a traced-only move, so no adjudication routed it. One sentence in the detail would
  close it; that amendment would join the round-2 scope.

## Observations (no fix required by this verdict)

1. **IF-073** (Drafted, off-spine). Its consumers drop `scripts/schedule`, yet `schedule._load`
   still reads the registry for titles and `load_oi_status` reads its states. The notes say a
   citing row's "SpecRef names a real specification after the item is ruled", but a row citing
   several items may keep the registry reference until none is pending (LLR-299). The other
   changed IF rows (IF-054, IF-074, IF-164, IF-255, IF-256, IF-264 and IF-265) match the code,
   and every Data cell is within 160 characters.
2. **Parentage.** LLR-298 and LLR-299 hang under SR-148, as LLR-288 and the retired LLR-289 did.
   SR-148 holds work behind a human-held stop and derives it from tracked registries, which is
   the readiness half. No SR states the owner-decision coupling as such: an uncited decision is
   an error, and a ruling updates its citers. A labelled derived SR would give the open-item
   machinery its own home. It is a follow-up, not a defect of these rows.
3. **A refresh merge can be refused for good.** The merge slot judges each lane commit against
   its first parent, a refresh merge included. Suppose trunk rules an item that only a lane-side
   row cites. The lane's refresh merge then takes the item out of pending against a first parent
   whose citer it does not update, and the slot refuses it. A later commit cannot repair that,
   so the refresh merge itself must carry the citer's update. The rule is as ruled (OI-102 Q3);
   the lane workflow should say so.
4. A **registry SpecRef with no `#OI` anchor** passes while a cited item is pending. A6 calls
   the reference row-specific, and the writers (intake, bootstrap) write it that way, but no
   check requires it. LLR-160's shared-spec overlap would read such a reference as shared with
   every placeholder.
5. `kitlib.spine._held_rows` compares the queued status case-sensitively (`.strip()`), while
   `_pending_items` and the scheduler lower-case it. The folder carrier writes the status
   lower-case, so this has no effect today.
6. I3, a narrower variant of the retired `wi_refs` join (a pointer naming a predecessor or a
   sibling, never the row itself), survives. The faithful variant, I3b, is caught. A fixture in
   which a sibling's id appears in an item's wi_refs would pin it.
